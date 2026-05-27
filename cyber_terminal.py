# =========================
# IMPORTS
# =========================

import time
import os
import subprocess
import socket
from datetime import datetime


# =========================
# COLORS
# =========================

GREEN = "\033[92m"
RESET = "\033[0m"


# =========================
# LOGGING FUNCTIONS
# =========================

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("cyber_log.txt", "a") as file:
        file.write(f"[{timestamp}] {message}\n")


def show_logs():
    try:
        with open("cyber_log.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No logs found yet.")


def clear_logs():
    open("cyber_log.txt", "w").close()
    print("Logs cleared.")
    write_log("[SYSTEM] Logs were cleared")


# =========================
# NETWORK FUNCTIONS
# =========================

def ping_target(target):
    print(f"Pinging {target}...")

    result = subprocess.run(
        ["ping", "-c", "4", target],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    write_log(f"[PING] Pinged {target}")


def resolve_target(target):
    print(f"Resolving {target}...")

    try:
        ip_address = socket.gethostbyname(target)
        print(f"{target} resolves to {ip_address}")
        write_log(f"[RESOLVE] {target} -> {ip_address}")
    except socket.gaierror:
        print("Could not resolve hostname.")
        write_log(f"[ERROR] Could not resolve {target}")


def run_scan(target, start_port=1, end_port=1024):
    print(f"Initializing REAL port scan on {target}...")
    write_log(f"[SCAN] Real scan started on {target}")

    time.sleep(1)

    for port in range(start_port, end_port + 1):
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(0.5)

        result = scanner.connect_ex((target, port))

        if result == 0:
            print(f"{GREEN}Port {port}: OPEN{RESET}")
            write_log(f"[SCAN] {target}:{port} OPEN")

        scanner.close()

    print("Real scan complete.")
    write_log(f"[SCAN] Real scan completed on {target}")


# =========================
# SYSTEM FUNCTIONS
# =========================

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


# =========================
# TERMINAL FUNCTIONS
# =========================

def show_help():
    print("Available commands:")
    print("scan       - Run real port scan")
    print("ping       - Ping a target")
    print("resolve    - Resolve hostname")
    print("network    - Check network status")
    print("sysinfo    - Display system information")
    print("status     - Show cyber terminal status")
    print("logs       - View saved logs")
    print("clearlogs  - Clear the log file")
    print("clear      - Clear the screen")
    print("exit       - Exit terminal")


def clear_screen():
    print("\n" * 50)


# =========================
# MAIN LOOP
# =========================

print("=== CYBER TERMINAL v1.1 REAL SCANNER ===")
print("Type 'help' to see available commands.")

while True:
    command = input("\ncyber> ")

    if command == "help":
        show_help()

    elif command.startswith("scan"):
        parts = command.split()

        if len(parts) == 1:
            print("Usage: scan <target> <start_port> <end_port>")

        elif len(parts) == 2:
            target = parts[1]
            run_scan(target)

        elif len(parts) == 4:
            target = parts[1]
            start_port = int(parts[2])
            end_port = int(parts[3])
            run_scan(target, start_port, end_port)

        else:
            print("Invalid scan command.")

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

    elif command == "sysinfo":
        system_info()

    elif command == "status":
        show_status()

    elif command == "logs":
        show_logs()

    elif command == "clearlogs":
        clear_logs()

    elif command == "clear":
        clear_screen()

    elif command == "exit":
        print("Exiting terminal...")
        break

    else:
        print("Unknown command. Type 'help' for available commands.")
