import re
import pandas as pd


class LogEventManager(object):
    def __init__(self):
        self.added_containers = pd.DataFrame(columns=["timestamp", "order_id"])
        self.added_schedule = pd.DataFrame(columns=["timestamp", "vehicle_id", "schedule"])
        self.starting_events = pd.DataFrame(columns=["timestamp", "vehicle_id", "order_id"])
        self.driving_events = pd.DataFrame(columns=["timestamp", "vehicle_id", "body", "loc_id", "seconds", "distance"])
        self.pickup_events = pd.DataFrame(columns=["timestamp", "vehicle_id", "body", "loc_id", "seconds"])
        self.using_lane_events = pd.DataFrame(columns=["timestamp", "loc_id", "lane_num", "order_id"])
        self.free_lane_events = pd.DataFrame(columns=["timestamp", "loc_id", "lane_num", "order_id"])
        self.pickup_done_events = pd.DataFrame(columns=["timestamp", "vehicle_id", "body", "loc_id"])
        self.schedule_done_events = pd.DataFrame(columns=["timestamp", "schedule"])

def parse_log_file(filepath):
    manager = LogEventManager()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            process_line(manager, line)  # Custom function to process individual lines
    return manager

def append(df, new_row):
    df.loc[len(df)] = new_row


# Extract timestamp and log level using regex
# TODO: write assert that all methods have non empty matches
# TODO: use .+ instead of \w+ and test
def process_line(manager, line):
    if process_added_container_message(manager.added_containers, line):
        return
    if process_schedule_message(manager.added_schedule, line):
        return
    if process_starting_event_message(manager.starting_events, line):
        return
    if process_driving_event_message(manager.driving_events, line):
        return
    if process_pickup_event_message(manager.pickup_events, line):
        return
    if process_using_lane_event_message(manager.using_lane_events, line):
        return
    if process_free_lane_event_message(manager.free_lane_events, line):
        return
    if process_pickup_done_event_message(manager.pickup_done_events, line):
        return
    if process_schedule_done_message(manager.schedule_done_events, line):
        return

def process_added_container_message(added_containers, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO adding TO (TO_CO_\w+), .+'
    matching = re.match(pattern, line)
    if matching:
        timestamp, order_id = matching.groups()
        append(added_containers,[timestamp, order_id])
        return True
    return False

def process_schedule_message(added_schedule, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) schedule (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, schedule = matching.groups()
        append(added_schedule,[timestamp, vehicle_id, schedule])
        if output:
            print(f"timestamp {timestamp} added for vehicle {vehicle_id} schedule {schedule}")
        return True
    return False

def process_starting_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (SC\w+) starting .+#(.+)#.+'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, order_id = matching.groups()
        append(recorded_events,[timestamp, vehicle_id, order_id])
        if output:
            print(f"timestamp {timestamp} event for vehicle {vehicle_id} : {event}")
        return True
    return False

def process_driving_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) (\(.+\)) driving to (.+); (.+) s; (.+) mm'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, body, loc_id, seconds, distance = matching.groups()
        append(recorded_events,[timestamp, vehicle_id, body, loc_id, seconds, distance])
        if output:
            print(f"timestamp {timestamp} driving vehicle {vehicle_id} to location {loc_id} for time {seconds} s")
        return True
    return False

def process_pickup_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (\w+) (\(.+\)) working at (.+); (.+) s'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, body, loc_id, seconds = matching.groups()
        append(recorded_events,[timestamp, vehicle_id, body, loc_id, seconds])
        if output:
            print(f"timestamp {timestamp} vehicle {vehicle_id} working at location {loc_id} for time {seconds} s")
        return True
    return False

def process_using_lane_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) DEBUG location (.+): using lane (\d+) for CO (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, loc_id, lane_num, order_id = matching.groups()
        append(recorded_events,([timestamp, loc_id, lane_num, order_id]))
        if output:
            print(f"timestamp {timestamp} location {loc_id} using lane {lane_num} for order {order_id}")
        return True
    return False

def process_free_lane_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) DEBUG location (.+): freeing lane (\d+) for CO (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, loc_id, lane_num, order_id = matching.groups()
        append(recorded_events,[timestamp, loc_id, lane_num, order_id])
        if output:
            print(f"timestamp {timestamp} location {loc_id} freeing lane {lane_num} for order {order_id}")
        return True
    return False

def process_pickup_done_event_message(recorded_events, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (.+) (\(.+\)) finished at (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, vehicle_id, body, loc_id = matching.groups()
        append(recorded_events,[timestamp, vehicle_id, body, loc_id])
        if output:
            print(f"timestamp {timestamp} vehicle {vehicle_id} finished working at location {loc_id}")
        return True
    return False

def process_schedule_done_message(added_schedule, line, output=False):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) DEBUG finished expected schedule_element (.+)'
    matching = re.match(pattern, line)
    if matching:
        timestamp, schedule = matching.groups()
        append(added_schedule,[timestamp, schedule])
        if output:
            print(f"timestamp {timestamp} finished schedule element {schedule}")
        return True
    return False

if __name__ == "__main__":
    manager = parse_log_file("./all-logs/logger_all.log")
    manager.starting_events.to_csv("assigments.csv")
