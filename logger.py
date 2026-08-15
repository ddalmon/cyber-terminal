from datetime import datetime


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