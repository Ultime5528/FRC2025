import argparse
import ipaddress
import time
from pprint import pprint, pformat

import colorama
from colorama import Style, Fore, Back
from ntcore import NetworkTableInstance, EventFlags


def is_valid_ip(ip):
    if ip.lower() == 'localhost':
        return True
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_team(value):
    try:
        team = int(value)
        return team >= 1
    except ValueError:
        return False


def highlight(text) -> str:
    return Style.BRIGHT + Fore.BLACK + Back.WHITE + str(text) + Style.RESET_ALL


def faded(text) -> str:
    return Fore.LIGHTBLACK_EX + text + Style.RESET_ALL


def start():
    colorama.init()

    parser = argparse.ArgumentParser(description='REPL client')
    parser.add_argument('target', nargs='?', default='5528',
                        help='Team number, IP address, or "localhost" (default: 5528)')
    args = parser.parse_args()

    inst = NetworkTableInstance.getDefault()
    inst.stopLocal()

    if is_valid_ip(args.target):
        print(f"Connecting to server at {highlight(args.target)}")
        inst.setServer(args.target)
    elif is_valid_team(args.target):
        team = int(args.target)
        print(f"Connecting to team {highlight(team)}")
        inst.setServerTeam(team)
    else:
        print(Fore.RED +"Invalid target. Must be team number, IP address, or 'localhost'")
        exit(1)

    print(Style.RESET_ALL)

    inst.startClient4("repl")

    while not inst.isConnected():
        print(faded("Waiting for connection..."))
        time.sleep(1)

    connections = inst.getConnections()
    server_ip = connections[0].remote_ip

    if server_ip == '127.0.0.1':
        print("Connected to simulation", end="")
    else:
        print("Connected to robot", end="")

    print(f" at {highlight(server_ip)}")
    print()

    variables_entry = inst.getEntry("RemoteREPL/variables")

    while True:
        print(faded("Waiting for robot code..."))
        variables = variables_entry.getStringArray([])
        if variables:
            break
        time.sleep(1)

    print("Robot code started")
    print()

    print("You are now in a pseudo python shell within the robot.")
    print(f"Type {Fore.GREEN}exit(){Fore.RESET} to quit.")
    print()
    print(Fore.RED + "Be careful if you manually activate motors." + Fore.RESET)
    print()
    print("The following variables are accessible:")
    print(*(Fore.GREEN + v.replace(" ", "") + "   " + Style.RESET_ALL for v in pformat(variables, indent=0, compact=True, width=65).replace("'", "")[1:-1].split(",")))

    stdin_entry = inst.getEntry("RemoteREPL/stdin")
    stdout_entry = inst.getEntry("RemoteREPL/stdout")

    def ask_for_input():
        user_input = input(">>> ")
        if user_input == "exit()":
            exit()
        user_input += f" T{time.time_ns():<20}"
        stdin_entry.setString(user_input)

    def on_response(event):
        value = event.data.value.getString()
        if value and len(value) > 22:
            received = value[:-22]
            print(Style.BRIGHT + received + Style.RESET_ALL)
        else:
            print(value)

        ask_for_input()

    inst.addListener(stdout_entry.getTopic() , EventFlags.kValueAll, on_response)

    # ask_for_input()

    while True:
        time.sleep(1)
        # TODO, True ?


if __name__ == "__main__":
    start()
