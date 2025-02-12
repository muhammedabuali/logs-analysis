import re

def parse_log_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            process_line(line)  # Custom function to process individual lines

# Extract timestamp and log level using regex
# Error: event arrays are local and will be cleared at end of each call
# TODO: write assert that all methods have non empty matches
# TODO: use .+ instead of \w+ and test
def process_line(line):
    added_containers = []
    if process_added_container_message(added_containers, line):
        return
    added_schedule = []
    if process_schedule_message(added_schedule, line):
        return
    starting_events = []
    if process_starting_event_message(starting_events, line):
        return
    driving_events = []
    if process_driving_event_message(driving_events, line):
        return
    pickup_events = []
    if process_pickup_event_message(pickup_events, line):
        return
    using_lane_events = []
    if process_using_lane_event_message(using_lane_events, line):
        return
    free_lane_events = []
    if process_free_lane_event_message(free_lane_events, line, True):
        return

def process_added_container_message(added_containers, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO adding TO (TO_CO_\w+), .+'
    matching = re.match(pattern, line)
    if matching:
        timestamp, order_id = matching.groups()
        added_containers.append([timestamp, order_id])
        return True
    return False

def process_schedule_message(added_schedule, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) schedule (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, schedule = matching.groups()
        added_schedule.append([timestamp, vehicle_id, schedule])
        if output:
            print(f"timestamp {timestamp} added for vehicle {vehicle_id} schedule {schedule}")
        return True
    return False

def process_starting_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (SC\w+) starting (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, event = matching.groups()
        recorded_events.append([timestamp, vehicle_id, event])
        if output:
            print(f"timestamp {timestamp} event for vehicle {vehicle_id} : {event}")
        return True
    return False

def process_driving_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) (\(.+\)) driving to (.+); (.+) s; (.+) mm'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, body, loc_id, seconds, distance = matching.groups()
        recorded_events.append([timestamp, vehicle_id, body, loc_id, seconds, distance])
        if output:
            print(f"timestamp {timestamp} driving vehicle {vehicle_id} to location {loc_id} for time {seconds} s")
        return True
    return False

def process_pickup_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) (\(.+\)) working at (.+); (.+) s'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, body, loc_id, seconds = matching.groups()
        recorded_events.append([timestamp, vehicle_id, body, loc_id, seconds])
        if output:
            print(f"timestamp {timestamp} vehicle {vehicle_id} working at location {loc_id} for time {seconds} s")
        return True
    return False

def process_using_lane_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) DEBUG location (.+): using lane (\d+) for CO (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, loc_id, lane_num, order_id = matching.groups()
        recorded_events.append([timestamp, loc_id, lane_num, order_id])
        if output:
            print(f"timestamp {timestamp} location {loc_id} using lane {lane_num} for order {order_id}")
        return True
    return False

def process_free_lane_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) DEBUG location (.+): freeing lane (\d+) for CO (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, loc_id, lane_num, order_id = matching.groups()
        recorded_events.append([timestamp, loc_id, lane_num, order_id])
        if output:
            print(f"timestamp {timestamp} location {loc_id} freeing lane {lane_num} for order {order_id}")
        return True
    return False

if __name__ == "__main__":
    parse_log_file("./all-logs/logger_all.log")
