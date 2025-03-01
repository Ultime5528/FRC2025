import code
import io
import time
from contextlib import redirect_stdout, redirect_stderr

import ntcore
from ntcore import EventFlags


class RemoteREPL:
    def __init__(self, robot):
        inst = ntcore.NetworkTableInstance.getDefault()
        self.stdout_entry = inst.getEntry("RemoteREPL/stdout")
        self.stdin_entry = inst.getEntry("RemoteREPL/stdin")
        self.interpreter = code.InteractiveInterpreter(locals={"robot": robot, "r": robot})

        self.stdin_entry.setString("")
        self.stdout_entry.setString("")

        inst.addListener(self.stdin_entry.getTopic(), EventFlags.kValueAll, self.on_new_stdin)

    def on_new_stdin(self, event):
        print("Event")
        print(event)

        stdout = io.StringIO()

        with redirect_stdout(stdout):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                value = self.stdin_entry.getRaw(None)
                if value:
                    self.interpreter.runsource(value[:-22])
                else:
                    print("(received empty stdin)")

        out = stdout.getvalue()

        if not out.strip():
            out = "\n"

        out += stderr.getvalue()

        out += f" T{time.time_ns():<20}"

        self.stdout_entry.setString(out)
