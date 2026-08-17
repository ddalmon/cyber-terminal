# =========================
# IMPORTS
# =========================

from network_tools import grab_banner, ping_target, resolve_target, run_scan, export_results
from logger import show_logs, clear_logs 
from system_tools import network_status, system_info, show_status

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
    print("banner     - Attempt banner grab on a target port")


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

    elif command.startswith("banner"):
        parts = command.split()

        if len(parts) == 3:
            target = parts[1]
            port = int(parts[2])
            grab_banner(target, port)
        else:
            print("Usage: banner <target> <port>")

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

    elif command == "export":
        export_results()

    elif command == "clear":
        clear_screen()

    elif command == "exit":
        print("Exiting terminal...")
        break

    else:
        print("Unknown command. Type 'help' for available commands.")
