import time
import subprocess
import socket
from logger import write_log

GREEN = "\033[92m"
RESET = "\033[0m"


def grab_banner(target, port):
    print(f"Attempting banner grab on {target}:{port}...")

    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(2)

    try:
        scanner.connect((target, port))
        if port in [80, 8080]:
            scanner.send(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")

        banner = scanner.recv(1024)

        response = banner.decode(errors="ignore")

        print("\n=== BANNER RESULTS ===")
        print(f"Target: {target}")
        print(f"Port: {port}\n")
        
        print(response.split("\r\n\r\n")[0])

    except Exception:
        print("No banner received.")

    finally:
        scanner.close()

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

    open_ports = []


    time.sleep(1)

    for port in range(start_port, end_port + 1):
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanner.settimeout(0.5)

        result = scanner.connect_ex((target, port))

        if result == 0:
            print(f"{GREEN}Port {port}: OPEN{RESET}")
            write_log(f"[SCAN] {target}:{port} OPEN")
            open_ports.append(port)

        scanner.close()

    print("Real scan complete.")

    print("\n=== SCAN SUMMARY ===")

    if open_ports:
        print(f"Open ports found: {len(open_ports)}")

        for port in open_ports:
            print(f"- {port}")
    else:
        print("No open ports found.")

    write_log(f"[SCAN] Real scan completed on {target}")
