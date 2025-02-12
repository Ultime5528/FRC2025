import argparse
import json
import subprocess
import time
from datetime import datetime

from ntcore import NetworkTableInstance

from ultime.autoproperty import registry

loop_delay = 30.0
entry_name_check_time = "/CheckSaveLoop/time"
entry_name_check_mirror = "/CheckSaveLoop/mirror"


def getNTInst() -> NetworkTableInstance:
    inst = NetworkTableInstance.getDefault()

    inst.stopLocal()
    inst.startClient4("properties-py")
    inst.setServerTeam(5528)
    inst.startDSClient()
    # inst.setServer("localhost")

    return inst


def clear():
    """
    Clear real robot's NetworkTables of persistent properties that no longer exist.

    It is dangerous to run this in Robot.robotInit(): if another branch's code is ru2n on the robot where
    new autoproperties do not exist yet, they will be deleted and set values will be lost.
    """
    from robot import Robot

    print("Connecting to robot...")

    inst = getNTInst()

    robot = Robot()
    robot.robotInit()

    topics = inst.getTopics()
    registry_keys = list(map(lambda x: x.key, registry))

    print("Found", len(registry_keys), "properties")

    for topic in topics:
        name = topic.getName()
        if name.startswith("/Properties/"):
            print(name)
            if name not in registry_keys:
                entry = inst.getEntry(topic.getName())
                entry.clearPersistent()
                entry.unpublish()
                print("Deleted unused persistent property:", name)


def save_loop():
    inst = getNTInst()

    entry_time = inst.getEntry(entry_name_check_time)
    entry_mirror = inst.getEntry(entry_name_check_mirror)
    last_save_time = time.time()

    try:
        while True:
            save_once()
            current_time = time.time()
            while current_time - last_save_time < loop_delay:
                entry_mirror.setDouble(entry_time.getDouble(current_time))
                time.sleep(1.0)
                current_time = time.time()
            last_save_time = current_time
    except KeyboardInterrupt:
        print("Save loop interrupted")


def save_once():
    print(
        f"[{datetime.now().time().replace(microsecond=0).isoformat()}] Connecting to robot..."
    )
    proc = subprocess.run(
        "scp -o StrictHostKeyChecking=no -o ConnectTimeout=3 lvuser@10.55.28.2:/home/lvuser/networktables.ini robot_networktables.json"
    )

    # Error code
    if proc.returncode != 0:
        return

    print("Saved properties to robot_networktables.json")

    update_files()


def update_files():
    from ast_selector import AstSelector
    from asttokens import ASTTokens

    with open("robot_networktables.json", "r") as f:
        data = json.load(f)

    for entry in data:
        matched_prop = next(
            (prop for prop in registry if prop.key == entry["name"]), None
        )

        if matched_prop:
            print("Updating", entry["name"])

            with open(matched_prop.filename, "r") as f:
                file_content = f.read()

            atok = ASTTokens(file_content, parse=True)

            # ast.Call of every function call to autoproperty
            calls = AstSelector(
                "ClassDef Assign[value is Call].value[func is Name].func[id=autoproperty] $Assign.value",
                atok.tree,
            ).all()

            # Finding the call for the current autoproperty
            matched_calls = [
                call
                for call in calls
                if call.lineno == matched_prop.lineno
                and call.col_offset == matched_prop.col_offset
            ]
            assert (
                len(matched_calls) == 1
            ), f"There should be only be one Call at the specified location"
            call = matched_calls[0]

            # Replace value
            value_expr = call.args[0]
            start = value_expr.first_token.startpos
            end = value_expr.last_token.endpos
            new_file = atok.text[:start] + str(entry["value"]) + atok.text[end:]

            # Rewrite file
            with open(matched_prop.filename, "w") as f:
                f.write(new_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        required=True, help="Enter the command to be executed."
    )

    # Clean
    parser_clear = subparsers.add_parser(
        "clear",
        help="Clear real robot's NetworkTables of persistent properties that no longer exist.",
    )
    parser_clear.set_defaults(func=clear)

    # Save once
    parser_save_once = subparsers.add_parser(
        "saveonce",
        help="Save once real robot's NetworkTables properties to local file.",
    )
    parser_save_once.set_defaults(func=save_once)

    # Save loop
    parser_save_loop = subparsers.add_parser(
        "saveloop",
        help="Save periodically real robot's NetworkTables properties to local file.",
    )
    parser_save_loop.set_defaults(func=save_loop)

    # Update files
    parser_update_files = subparsers.add_parser(
        "updatefiles",
        help="Update files autoproperties values with robot_networktables.json values.",
    )
    parser_update_files.set_defaults(func=update_files)

    args = parser.parse_args()
    args.func()
