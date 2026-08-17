import time
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from logger import write_log

GREEN = "\033[92m"
RESET = "\033[0m"

last_scan_results = []

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}

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

def scan_port(target, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(0.5)

    result = scanner.connect_ex((target, port))

    scanner.close()

    if result == 0:
        return port

    return None

def ping_host(ip_address):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip_address],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return ip_address

    return None

def discover_hosts(network_prefix):
    print(f"Discovering hosts on {network_prefix}.0/24...")

    live_hosts = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        addresses = [
            f"{network_prefix}.{host}"
            for host in range(1, 255)
        ]

        results = executor.map(ping_host, addresses)

        for result in results:
            if result is not None:
                print(f"{GREEN}{result} ONLINE{RESET}")
                live_hosts.append(result)

    print(f"\nHosts found: {len(live_hosts)}")

def run_scan(target, start_port=1, end_port=1024):
    print(f"Initializing REAL port scan on {target}...")
    write_log(f"[SCAN] Real scan started on {target}")

    start_time = time.time()

    open_ports = []
    last_scan_results.clear()



    time.sleep(1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(
            lambda port: scan_port(target, port),
            range(start_port, end_port + 1)
        )

        for port in results:
            if port is not None:
                service = COMMON_SERVICES.get(port, "Unknown")

                print(f"{GREEN}Port {port}: OPEN ({service}){RESET}")
                write_log(f"[SCAN] {target}:{port} OPEN ({service})")

                open_ports.append(port)
                last_scan_results.append((target, port))

    print("Real scan complete.")

    print("\n=== SCAN SUMMARY ===")

    if open_ports:
        print(f"Open ports found: {len(open_ports)}")

        for port in open_ports:
            service = COMMON_SERVICES.get(port, "Unknown")
            print(f"- {port} ({service})")
    else:
        print("No open ports found.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Scan completed in {elapsed_time:.2f} seconds.")

    write_log(f"[SCAN] Real scan completed on {target}")

def export_results():
    if not last_scan_results:
        print("No scan results available to export.")
        return

    with open("scan_results.txt", "w") as file:
        for target, port in last_scan_results:
            file.write(f"{target}:{port} OPEN\n")

    print("Scan results exported to scan_results.txt")
