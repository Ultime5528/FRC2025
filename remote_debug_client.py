#!/usr/bin/env python3
"""
Remote debugging client for FRC robots.
This script connects to a robot running the RemoteDebugModule
and provides a Python REPL for executing code on the robot.
Cross-platform implementation using prompt_toolkit for REPL with PyCharm-like styling.
"""

import rpyc
import sys
import argparse
import code
import threading
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

try:
    from pygments.lexers.python import PythonLexer
    from pygments.styles import get_style_by_name

    pygments_available = True
except ImportError:
    pygments_available = False


class RobotCompleter(Completer):
    """Custom completer for robot context objects."""

    def __init__(self, context):
        self.context = context

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        # Simple completion for attributes and methods
        if '.' in text:
            parts = text.split('.')
            attr_prefix = parts[-1]  # The part we're currently typing

            # Try to get the object by traversing the chain
            obj = None
            try:
                # Start with the first object
                if parts[0] in self.context:
                    obj = self.context[parts[0]]

                    # Traverse the object chain for each part except the last one
                    for part in parts[1:-1]:
                        if part:  # Skip empty parts (happens if there's a trailing dot)
                            obj = getattr(obj, part)

                    # Now obj is the object whose attributes we want to complete
                    if obj is not None:
                        # Get attributes from the remote object
                        obj_attrs = dir(obj)

                        # Split attributes into three categories
                        regular_attrs = [attr for attr in obj_attrs if not attr.startswith('_')]
                        private_attrs = [attr for attr in obj_attrs if
                                         attr.startswith('_') and not (attr.startswith('__') and attr.endswith('__'))]
                        dunder_attrs = [attr for attr in obj_attrs if attr.startswith('__') and attr.endswith('__')]

                        # Sort each group alphabetically
                        regular_attrs.sort()
                        private_attrs.sort()
                        dunder_attrs.sort()

                        # Yield completions in order of priority
                        # 1. Regular attributes (no underscore)
                        for attr in regular_attrs:
                            if attr.startswith(attr_prefix):
                                yield Completion(attr, start_position=-len(attr_prefix))

                        # 2. Private attributes (single underscore)
                        for attr in private_attrs:
                            if attr.startswith(attr_prefix):
                                yield Completion(attr, start_position=-len(attr_prefix))

                        # 3. Dunder methods
                        for attr in dunder_attrs:
                            if attr.startswith(attr_prefix):
                                yield Completion(attr, start_position=-len(attr_prefix))
            except Exception as e:
                # Handle any errors silently - they're common when traversing incomplete paths
                pass
        else:
            # Complete for top-level objects
            word = text.split()[-1] if text.split() else ''
            context_keys = sorted(self.context.keys())
            for key in context_keys:
                if key.startswith(word):
                    yield Completion(key, start_position=-len(word))


class RemoteDebugREPL:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None
        self.robot_context = {}
        self.connected = False
        self.results_thread = None
        self.pending_results = {}
        self.cmd_count = 0

    def connect(self):
        """Connect to the robot."""
        try:
            print(f"Connecting to robot at {self.host}:{self.port}...")
            self.conn = rpyc.connect(
                self.host,
                self.port,
                config={
                    'allow_public_attrs': True,
                    'allow_pickle': True,
                    'sync_request_timeout': None
                }
            )
            self.connected = True
            self.robot_context = self.conn.root.get_context()

            # Start thread to periodically check for results
            self.results_thread = threading.Thread(target=self._check_results, daemon=True)
            self.results_thread.start()

            print("Connected to robot!")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def _check_results(self):
        """Periodically check for results of async operations."""
        while self.connected:
            try:
                for cmd_id in list(self.pending_results.keys()):
                    result = self.conn.root.get_result(cmd_id)
                    if result:
                        callback = self.pending_results.pop(cmd_id)
                        callback(result)
            except Exception as e:
                # Silently handle errors to prevent thread crashes
                pass
            time.sleep(0.1)

    def execute(self, code_str, callback=None):
        """Execute code on the robot."""
        if not self.connected:
            print("Not connected to robot")
            return

        try:
            cmd_id = self.conn.root.execute(code_str)
            if callback:
                self.pending_results[cmd_id] = callback
            return cmd_id
        except Exception as e:
            print(f"Failed to execute: {e}")
            return None

    def start_prompt_repl(self):
        """Start an interactive REPL using prompt_toolkit."""
        if not self.connected:
            print("Not connected to robot")
            return

        # Banner message
        banner = f"""
Remote Python Debug Console
Connected to robot at {self.host}:{self.port}
Type Python code to execute on the robot.
Available robot objects: {', '.join(sorted(self.robot_context.keys()))}
Type 'exit()' or press Ctrl+D to exit.
"""
        print(banner)

        # Set up prompt session with history and custom completer
        history = InMemoryHistory()
        robot_completer = RobotCompleter(self.robot_context)

        # Configure lexer if pygments is available
        lexer = PygmentsLexer(PythonLexer) if pygments_available else None

        # Configure PyCharm-like style for dark terminals
        style = Style.from_dict({
            # Prompt styling with PyCharm-like colors
            'prompt': '#8AADF4',

            # Syntax highlighting (PyCharm Darcula-inspired)
            'pygments.comment': '#808080',  # Grey for comments
            'pygments.keyword': '#CC7832',  # Orange-ish for keywords
            'pygments.function': '#FFC66D',  # Yellow for functions
            'pygments.string': '#6A8759',  # Green for strings
            'pygments.number': '#6897BB',  # Blue for numbers
            'pygments.operator': '#A9B7C6',  # Light grey for operators
            'pygments.builtin': '#8AADF4',  # Light blue for builtins
            'pygments.class': '#A9B7C6',  # Light grey for classes
            'pygments.variable': '#A9B7C6',  # Light grey for variables
            'pygments.constant': '#9876AA',  # Purple for constants

            # Completion menu styling
            'completion-menu': 'bg:#2B2B2B #A9B7C6',
            'completion-menu.completion': 'bg:#2B2B2B #A9B7C6',
            'completion-menu.completion.current': 'bg:#0D293E #FFFFFF',
            'scrollbar.background': 'bg:#323232',
            'scrollbar.button': 'bg:#585858',
        })

        # Create custom prompts with PyCharm-like colors
        message = [('class:prompt', '>>> ')]
        continuation_message = [('class:prompt', '... ')]

        session = PromptSession(
            message=message,
            history=history,
            completer=robot_completer,
            lexer=lexer,
            style=style,
            complete_while_typing=True,
            complete_in_thread=True  # Perform completion in a background thread
        )

        # Main REPL loop
        multiline_buffer = []
        while True:
            try:
                if not multiline_buffer:
                    # Regular prompt for new input
                    user_input = session.prompt(message)

                    # Handle exit commands
                    if user_input.strip() in ('exit()', 'quit()'):
                        break
                else:
                    # Continuation prompt for multiline input
                    user_input = session.prompt(continuation_message)

                # Check for empty lines
                if not user_input.strip():
                    if multiline_buffer:
                        # Empty line in multiline mode - execute the buffer
                        code_to_execute = '\n'.join(multiline_buffer)
                        multiline_buffer = []
                        self._execute_code(code_to_execute)
                    continue

                # Check for indentation which indicates multiline input
                if user_input.endswith(':') or user_input.startswith(' ') or user_input.startswith('\t'):
                    multiline_buffer.append(user_input)
                    continue

                # Add to buffer if we're already in multiline mode
                if multiline_buffer:
                    multiline_buffer.append(user_input)
                    continue

                # Otherwise execute single line
                self._execute_code(user_input)

            except KeyboardInterrupt:
                # Clear the current input buffer
                multiline_buffer = []
                print("\nKeyboardInterrupt")
            except EOFError:
                print("\nExiting...")
                break

    def _execute_code(self, code_str):
        """Execute code and handle the result."""

        def handle_result(result):
            if result['success']:
                if result['is_expression'] and result['result'] is not None:
                    # Format different result types with appropriate colors
                    value = result['result']
                    if isinstance(value, str):
                        # Use string color (green)
                        formatted = f"\033[32m{repr(value)}\033[0m"
                    elif isinstance(value, (int, float)):
                        # Use number color (light blue)
                        formatted = f"\033[36m{repr(value)}\033[0m"
                    elif value is None:
                        # Use keyword color (orange)
                        formatted = f"\033[33mNone\033[0m"
                    elif isinstance(value, bool):
                        # Use keyword color (orange)
                        formatted = f"\033[33m{repr(value)}\033[0m"
                    else:
                        # Default color (light grey)
                        formatted = repr(value)
                    print(formatted)
            else:
                # Print errors in red
                print(f"\033[31m{result['error_type']}: {result['error']}\033[0m")

        # Generate a unique event for waiting
        self.cmd_count += 1
        event = threading.Event()

        def callback_with_event(result):
            handle_result(result)
            event.set()

        self.execute(code_str, callback_with_event)

        # Wait for result with timeout
        event.wait(timeout=5.0)
        if not event.is_set():
            print("(Still running...)")

    def close(self):
        """Close the connection to the robot."""
        self.connected = False
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='Remote robot debugging client')
    parser.add_argument('host', help='Robot IP address or hostname')
    parser.add_argument('--port', type=int, default=18861, help='Port number (default: 18861)')
    args = parser.parse_args()

    repl = RemoteDebugREPL(args.host, args.port)
    if repl.connect():
        try:
            repl.start_prompt_repl()
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            repl.close()


if __name__ == '__main__':
    main()