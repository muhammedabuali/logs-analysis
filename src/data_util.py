from read_logs import parse_log_file
from plot_excel_data import parse_exceldata

from datetime import datetime, timedelta
import pandas as pd

a_order_id = "order_id"
a_vehicle_id = "vehicle_id"
loc_cap = 'Capacity limitation (# SC)'
loc_name = "Location Name"
a_loc_id = "loc_id"
a_seconds = "seconds"
a_timestamp = "timestamp"
a_distance = "distance"
a_id = "ID"


# from date time to seconds in a day
def to_seconds(timestamp):
    in_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return in_datetime.hour * 3600 + in_datetime.minute * 60 + in_datetime.second

# from seconds in a day to date time
def to_time(seconds):
    return str(timedelta(seconds=seconds))

class DataManager(object):
    def __init__(self, excel_data, log_data):
        self.excel_data = excel_data
        self.log_data = log_data

    # get pairs of orders and corresponding assigned vehicle
    def get_order_assigments(self):
        df_assignments = self.log_data.starting_events[[a_order_id, a_vehicle_id]].drop_duplicates()
        return df_assignments

    # get list of location names having a limited capacity
    def get_locations_with_limited_cap(self):
        df = self.excel_data.df_locations
        locations = df[df[loc_cap].notnull()]
        locations = locations[loc_name].to_list()
        return locations


    # check limited capacity at [location] is respected
    # found issue with pickup events not reliable
    def check_overcapacity(self, location, max_capacity=2):
        df = self.log_data.pickup_events
        df = df[df[a_loc_id] == location]

        # collect the events at the location
        events = []
        for _, row in df.iterrows():
            start, duration, vehicle = to_seconds(row[a_timestamp]), int(row[a_seconds]), row[a_vehicle_id]
            end = start + duration
            events.append((start, 1, vehicle))
            events.append((end, -1, vehicle))

        # check the events
        events.sort()
        active_intervals = 0

        # Sweep through events
        for s, change, vehicle in events:
            active_intervals += change
            # print(("enterig" if change > 0 else "leaving "), f"vehicle {vehicle} at time {to_time(s)}")
            if active_intervals > max_capacity:
                print("max_capacity at time", to_time(s))
                return False  # Overlapping exceeds capacity
        return True  # Valid schedule


    # check limited capacity at [location] is respected
    def check_overcapacity_lanes(self, location, max_capacity=2):
        df1 = self.log_data.using_lane_events
        df1 = df1[df1[a_loc_id] == location]

        # collect the events at the location
        events = []
        for _, row in df1.iterrows():
            event_time, order_id = to_seconds(row[a_timestamp]), row[a_order_id]
            events.append((event_time, 1, order_id))

        df2 = self.log_data.free_lane_events
        df2 = df2[df2[a_loc_id] == location]
        for _, row in df2.iterrows():
            event_time, order_id = to_seconds(row[a_timestamp]), row[a_order_id]
            events.append((event_time, -1, order_id))

        # check the events
        events.sort()
        active_intervals = 0

        # Sweep through events
        for s, change, order in events:
            active_intervals += change
            # print(("entering" if change > 0 else "leaving "), f" for order {order} at time {to_time(s)}")
            if active_intervals > max_capacity:
                print("max_capacity at time", to_time(s))
                return False  # Overlapping exceeds capacity
        return True  # Valid schedule

    # check limited capacity at all locations is respected
    def check_all_capacities(self, max_capacity=2):
        locations = self.get_locations_with_limited_cap()
        failure = False
        for loc in locations:
            success = self.check_overcapacity_lanes(loc, max_capacity)
            if success:
                print(f"success!: no  overcapacity at {loc}")
            else:
                print(f"*****failure!: overcapacity at {loc}*****")
                failure = True
        return not failure

    # get total distance traveled by vehicle [vehicle_id]
    def get_distance_traveled(self, vehicle_id):
        df = self.log_data.driving_events
        df = df[df[a_vehicle_id]== vehicle_id]
        distance = df[a_distance].map(lambda x: int(x)).sum()
        return distance

    # get count of assigned orders to  vehicle [vehicle_id]
    def get_assigned_orders_count(self, vehicle_id):
        df = self.log_data.starting_events
        df = df[df[a_vehicle_id]== vehicle_id]
        order_count = df[a_order_id].drop_duplicates().shape[0]
        return order_count

    def get_all_vehicle_stats(self):
        stats = []
        for _,row in self.excel_data.df_vehicles.iterrows():
            dist = self.get_distance_traveled(row[a_id])
            order_count = self.get_assigned_orders_count(row[a_id])
            print(f"vehicle {row[a_id]}, traveled distance {dist} to fullfil {order_count} orders")
            stats.append([dist, order_count])



if __name__ == "__main__":
    excel_data_path = "./VOSimu-InputInformation.xlsx"
    log_data_path = "./all-logs/logger_all.log"

    print("parsing exceldata started!")
    excel_data = parse_exceldata(excel_data_path)
    print("parsing exceldata completed!")

    print("parsing log files started!")
    log_data = parse_log_file(log_data_path)
    print("parsing log files completed!")

    data_manager = DataManager(excel_data, log_data)
    # data_manager.get_locations_with_limited_cap()
    # success = data_manager.check_overcapacity_lanes("QC003")
    # if success:
    #     print("success, no overcapacity at QC003")
    # data_manager.check_all_capacities(2)
    # dist = data_manager.get_distance_traveled("SC002")
    # print(f"distance = {dist} mm by SC002")
    # order_count = data_manager.get_assigned_orders_count("SC002")
    # print(f"order count = {order_count} orders assigned to SC002")
    data_manager.get_all_vehicle_stats()

