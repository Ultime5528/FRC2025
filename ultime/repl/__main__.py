import argparse
import ipaddress
import time
import socket

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

def start():
    parser = argparse.ArgumentParser(description='REPL client')
    parser.add_argument('target', nargs='?', default='5528',
                        help='Team number, IP address, or "localhost" (default: 5528)')
    args = parser.parse_args()

    nt_inst = NetworkTableInstance.getDefault()
    nt_inst.stopLocal()

    if is_valid_ip(args.target):
        print(f"Connecting to server at {args.target}")
        nt_inst.setServer(args.target)
    elif is_valid_team(args.target):
        team = int(args.target)
        print(f"Connecting to team {team}")
        nt_inst.setServerTeam(team)
    else:
        print("Invalid target. Must be team number, IP address, or 'localhost'")
        return

    nt_inst.startClient4("repl-py")

    while not nt_inst.isConnected():
        time.sleep(3)
        print("Waiting for connection...")

    connections = nt_inst.getConnections()
    print(connections)
    server_ip = connections[0].remote_ip

    if server_ip == '127.0.0.1':
        print("Connected to simulation")
    else:
        print("Connected to robot")

    print(server_ip)

    print("You are now in a pseudo python shell within the robot.")
    print("Your robot is located at 'robot' or at 'r'.")
    print("Ex. 'r.hardware' is the HardwareModule instance of your robot.")

    stdin_entry = nt_inst.getEntry("RemoteREPL/stdin")

    def r():
        user_input = input(">>> ")
        if user_input == "exit()":
            exit()
        user_input += f" T{time.time_ns():<20}"
        stdin_entry.setString(user_input)

    def pr(event):
        # print(entry.value.getRaw()[:-22])
        print("Event")
        print(event)
        r()

    nt_inst.addListener(nt_inst.getRawTopic("RemoteREPL/stdout"), EventFlags.kImmediate, pr)

    r()

    while True: pass


if __name__ == "__main__":
    start()
