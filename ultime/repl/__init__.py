import code
import io
import time
from contextlib import redirect_stdout, redirect_stderr

import ntcore
from ntcore import EventFlags

from typing import Any


class RemoteREPL:
    def __init__(self, variables: dict[str, Any], objects_to_expose: list = None):
        inst = ntcore.NetworkTableInstance.getDefault()
        self.stdout_entry = inst.getEntry("RemoteREPL/stdout")
        self.stdin_entry = inst.getEntry("RemoteREPL/stdin")
        self.variables_entry = inst.getEntry("RemoteREPL/variables")

        exposed_variables = dict(variables)
        for obj in objects_to_expose:
            exposed_variables.update(obj.__dict__)

        print("Exposing: ", exposed_variables.keys())

        self.interpreter = code.InteractiveInterpreter(locals=exposed_variables)

        self.stdin_entry.setString("")
        self.stdout_entry.setString("")

        exposed_variable_names = list(exposed_variables.keys())
        exposed_variable_names.sort()
        self.variables_entry.setStringArray(exposed_variable_names)

        inst.addListener(self.stdin_entry.getTopic(), EventFlags.kValueAll, self.on_new_stdin)

    def on_new_stdin(self, event):
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                value = event.data.value.getString()
                if value:
                    source = value[:-22]
                    self.interpreter.runsource(source)

        out = stdout.getvalue()

        if not out.strip():
            out = "\n"

        out += stderr.getvalue()

        out += f" T{time.time_ns():<20}"

        self.stdout_entry.setString(out)
