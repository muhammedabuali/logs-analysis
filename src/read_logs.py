import re

def parse_log_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            process_line(line)  # Custom function to process individual lines

# Extract timestamp and log level using regex
def process_line(line):
    added_containers = []
    if process_added_container_message(added_containers, line):
        return
    added_schedule = []
    if process_schedule_message(added_schedule, line):
        return

def process_added_container_message(added_containers, line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO adding TO (TO_CO_\w+), .+'
    matching = re.match(pattern, line)
    if matching:
        timestamp, order_id = matching.groups()
        added_containers.append([timestamp, order_id])
        return True
    return False


def process_schedule_message(added_containers, line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) schedule (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, schedule = matching.groups()
        added_containers.append([timestamp, vehicle_id, schedule])
        print(f"timestamp {timestamp} added for vehicle {vehicle_id} schedule {schedule}")
        return True
    return False

if __name__ == "__main__":
    parse_log_file("./all-logs/logger_all.log")
