import os
import time

def network_status():
    print("Checking network status...")
    time.sleep(1)
    print("Network status: ONLINE")

def system_info():
    print("Retrieving system information...")
    time.sleep(1)

    username = os.getlogin()
    system = os.uname()

    print(f"Current User: {username}")
    print(f"System Name: {system.sysname}")
    print(f"Hostname: {system.nodename}")

def show_status():
    print("=== CYBER TERMINAL STATUS ===")

    username = os.getlogin()
    system = os.uname()

    print(f"User: {username}")
    print(f"Hostname: {system.nodename}")

    if os.path.exists("cyber_log.txt"):
        with open("cyber_log.txt", "r") as file:
            lines = file.readlines()

        print("Log file: Found")
        print(f"Log entries: {len(lines)}")
    else:
        print("Log file: Not found")
        print("Log entries: 0")

