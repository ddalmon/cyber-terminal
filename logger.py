from datetime import datetime


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("cyber_log.txt", "a") as file:
        file.write(f"[{timestamp}] {message}\n")