import time
import random
import os
import subprocess
import socket
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("cyber_log.txt", "a") as file:
        file.write(f"[{timestamp}] {message}\n")

def ping_target(target):
    print(f"Pinging {target}...")

    result = subprocess.run(
        ["ping", "-c", "4", target],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    write_log(f"[PING] Pinged {target}")

def show_help():
    print("Available commands:")
    print("scan    - Run system scan")
    print("network - Check network status")
    print("sysinfo - Display system information")
    print("clear   - Clear the screen")
    print("exit    - Exit terminal")
    print("ping    - Ping a target")
    print("resolve - Resolve a hostname to an IP address")
    print("logs    - View saved log entries")
    print("status - show cyber terminal status")

def resolve_target(target):
    print(f"Resolving {target}...")

    try:
        ip_address = socket.gethostbyname(target)
        print(f"{target} resolves to {ip_address}")
        write_log(f"[RESOLVE] {target} -> {ip_address}")

    except socket.gaierror:
        print("Could not resolve hostname.")

def run_scan(target):
    print(f"Initializing scan on {target}...")
    write_log(f"[scan] Scan started on {target}")

    time.sleep(1)

    ports = [21, 22, 80, 443, 8080]
    statuses = ["OPEN", "CLOSED", "FILTERED", "VULNERABLE"]

    for port in ports:
        status = random.choice(statuses)

        if status == "OPEN":
            print(f"{GREEN}Port {port}: {status}{RESET}")
        elif status == "VULNERABLE":
            print(f"{RED}Port {port}: {status}{RESET}")
        elif status == "FILTERED":
            print(f"{YELLOW}Port {port}: {status}{RESET}")
        else:
            print(f"Port {port}: {status}")

        time.sleep(1)

    write_log(f"[SCAN] Scan completed on {target}")
    print("Scan complete.")


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


def show_logs():
    try:
        with open("cyber_log.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No logs found yet.")


def clear_screen():
    print("\n" * 50)


print("=== CYBER TERMINAL v1.0 ===")
print("Type 'help' to see available commands.")

while True:
    command = input("\ncyber> ")

    if command == "help":
        show_help()

    elif command.startswith("scan"):
        parts = command.split()

        if len(parts) == 1:
            run_scan("local system")
        else:
            target = parts[1]
            run_scan(target)
    elif command.startswith("ping"):
        parts = command.split()

        if len(parts) == 1:
            print("Usage: ping <target>")
        else:
            target = parts[1]
            ping_target(target)
    elif command.startswith("resolve"):
        parts = command.split()

        if len(parts) == 1:
            print("Usage: resolve <hostname>")
        else:
            target = parts[1]
            resolve_target(target)
    elif command == "network":
        network_status()

    elif command == "logs":
        show_logs()

    elif command == "sysinfo":
        system_info()

    elif command == "status":
        show_status()

    elif command == "clear":
        clear_screen()

    elif command == "exit":
        print("Exiting terminal...")
        break

    else:
        print("Unknown command. Type 'help' for available commands.")
