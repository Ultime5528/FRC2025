import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import queue
import wpilib

from ultime.module import Module


class RemoteDebugService(rpyc.Service):
    """RPyC service that allows executing code on the robot."""

    def __init__(self, robot_context, command_queue):
        self.robot_context = robot_context
        self.command_queue = command_queue
        self.results = {}
        self.next_id = 0

    def on_connect(self, conn):
        print(f"Remote debugging client connected from {conn._config['endpoints'][1][0]}")

    def on_disconnect(self, conn):
        print(f"Remote debugging client disconnected from {conn._config['endpoints'][1][0]}")

    def exposed_get_context(self):
        """Returns the current robot context (available objects and modules)."""
        return self.robot_context

    def exposed_execute(self, code_str):
        """Queue code to be executed synchronously in robotPeriodic."""
        cmd_id = self.next_id
        self.next_id += 1
        self.results[cmd_id] = None
        self.command_queue.put((cmd_id, code_str))
        return cmd_id

    def exposed_get_result(self, cmd_id):
        """Get the result of a previously executed command."""
        result = self.results.get(cmd_id)
        if result:
            del self.results[cmd_id]
        return result

    def set_result(self, cmd_id, result):
        """Set the result of a command execution."""
        self.results[cmd_id] = result


class RemoteDebugModule(Module):
    """Module for remote debugging of the robot code.

    This module starts an RPyC server that allows remote clients to execute
    code on the robot, synchronously within the robotPeriodic method.

    Usage:
    1. Add this module to your robot
    2. Connect to it from a client using the rpyc library
    3. Execute code remotely and get results
    """

    def __init__(self, robot, port=18861):
        super().__init__()
        self.robot = robot
        self.port = port
        self.command_queue = queue.Queue()

        # Create a context dictionary with all robot modules and objects
        self.context = self._build_context()

        # Create the RPyC service
        self.service = RemoteDebugService(self.context, self.command_queue)

        # Start the server in a separate thread
        self.server = None
        self.server_thread = None

    def _build_context(self):
        """Build a context dictionary with all robot modules and objects."""
        context = {
            'robot': self.robot,
            'wpilib': wpilib,
        }

        # Add all robot modules
        for module_name in dir(self.robot):
            module = getattr(self.robot, module_name)
            if isinstance(module, Module) and not module_name.startswith('_'):
                context[module_name] = module

        return context

    def robotInit(self):
        """Start the RPyC server when the robot initializes."""
        self.server = ThreadedServer(
            self.service,
            port=self.port,
            protocol_config={
                'allow_public_attrs': True,
                'allow_pickle': True,
                'sync_request_timeout': None
            }
        )

        self.server_thread = threading.Thread(
            target=self.server.start,
            daemon=True
        )
        self.server_thread.start()
        print(f"Remote debug server started on port {self.port}")

    def robotPeriodic(self):
        """Check for and execute any pending commands."""
        try:
            while not self.command_queue.empty():
                cmd_id, code_str = self.command_queue.get_nowait()
                try:
                    # Execute code in the context of the robot
                    # Using exec for statements and eval for expressions
                    local_context = dict(self.context)  # Copy to allow local modifications

                    try:
                        # Try to evaluate as an expression first
                        result = eval(code_str, globals(), local_context)
                        self.service.set_result(cmd_id, {
                            'success': True,
                            'result': result,
                            'is_expression': True
                        })
                    except SyntaxError:
                        # If it's not an expression, execute as a statement
                        exec(code_str, globals(), local_context)

                        # Update context with any new locals
                        for key, value in local_context.items():
                            if key not in self.context:
                                self.context[key] = value

                        self.service.set_result(cmd_id, {
                            'success': True,
                            'result': None,
                            'is_expression': False
                        })
                except Exception as e:
                    # Capture any exceptions
                    self.service.set_result(cmd_id, {
                        'success': False,
                        'error': str(e),
                        'error_type': type(e).__name__
                    })
        except Exception as e:
            print(f"Error in RemoteDebugModule.robotPeriodic: {e}")

    def disabledExit(self):
        """Update the context when exiting disabled mode."""
        # This is a good time to refresh the context, as it's likely modules have been updated
        self.context = self._build_context()

    def close(self):
        """Shut down the server when the robot is done."""
        if self.server:
            self.server.close()
