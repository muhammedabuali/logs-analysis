from read_logs import parse_log_file
from plot_excel_data import parse_exceldata

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_log_data(excel_data_path, log_data_path):
    print("parsing exceldata started!")
    excel_data = parse_exceldata(excel_data_path)
    print("parsing exceldata completed!")

    print("parsing log files started!")
    log_data = parse_log_file(log_data_path)
    print("parsing log files completed!")

    # plot_vehicle_gantt(excel_data, log_data)
    # plot_location_gantt(excel_data, log_data)
    plot_lane_gantt(excel_data, log_data)

# attribute names as variables to avoid typos
a_timestamp = "timestamp"
a_vehicle_id = "vehicle_id"
a_seconds = "seconds"
vehicle_id = "ID"

# from date time to seconds in a day
def to_seconds(in_datetime):
    return in_datetime.hour * 3600 + in_datetime.minute * 60 + in_datetime.second

def plot_vehicle_gantt(excel_data, log_data):
    vehicles = excel_data.df_vehicles[vehicle_id].to_list()
    # create a map from vehicle id to index for drawing
    vehicle_map = {v: i for i, v in enumerate(vehicles)}
    fig, ax = plt.subplots(figsize=(20, 10))
    for _, row in log_data.driving_events.iterrows():
        start_date = datetime.strptime(row[a_timestamp], "%Y-%m-%d %H:%M:%S")
        ax.broken_barh([(to_seconds(start_date), int(row[a_seconds]))],
                       (vehicle_map[row[a_vehicle_id]], 0.3), facecolors='tab:blue')

    for _, row in log_data.pickup_events.iterrows():
        start_date = datetime.strptime(row[a_timestamp], "%Y-%m-%d %H:%M:%S")
        ax.broken_barh([(to_seconds(start_date), int(row[a_seconds]))],
                       (vehicle_map[row[a_vehicle_id]], 0.3), facecolors='tab:green')
    # Formatting
    ax.set_yticks(range(len(vehicles)))
    ax.set_yticklabels([v for v in vehicles])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for straddle carriers")
    plt.xticks(rotation=45)
    plt.show()

loc_name = "Location Name"
a_loc_id = "loc_id"
def plot_location_gantt(excel_data, log_data):
    df = excel_data.df_locations
    locations = ["QC003"]
    # locations = df[loc_name].to_list()
    # create a map from location id to index for drawing
    # location_map = {l: i for i, l in enumerate(locations)}
    fig, ax = plt.subplots(figsize=(20, 10))
    i = 0
    for _, row in log_data.pickup_events.iterrows():
        if row[a_loc_id] != "QC003":
            continue
        i += 1
        start_date = datetime.strptime(row[a_timestamp], "%Y-%m-%d %H:%M:%S")
        ax.broken_barh([(to_seconds(start_date), int(row[a_seconds]))],
                       (i, 0.3), facecolors='tab:green', alpha=0.5)
    # Formatting
    # ax.set_yticks(range(len(locations)))
    # ax.set_yticklabels([l for l in locations])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for straddle carriers")
    plt.xticks(rotation=45)
    plt.show()


loc_cap = 'Capacity limitation (# SC)'
a_order_id = "order_id"
a_lane_num = "lane_num"
a_start = "start"
a_end = "end"
def plot_lane_gantt(excel_data, log_data):
    df_l = excel_data.df_locations
    locations = df_l[df_l[loc_cap].isin([2])]
    locations = locations[loc_name].to_list()
    location_map = {l: i for i, l in enumerate(locations)}

    # merge data from using lane data frame and free lane dataframe
    df_using = log_data.using_lane_events
    df_freeing = log_data.free_lane_events
    df_merged = df_using.rename(columns={a_timestamp: a_start, a_lane_num: "same_lane"})\
    .merge(df_freeing.rename(columns={a_timestamp: a_end}), on=[ a_order_id, a_loc_id ])

    print(df_merged.head())

    fig, ax = plt.subplots(figsize=(20, 10))
    for i, row in df_merged.iterrows():
        if row[a_loc_id] not in locations:
            continue
        start_date = datetime.strptime(row[a_start], "%Y-%m-%d %H:%M:%S")
        start_seconds = mdates.date2num(start_date)
        end_date = datetime.strptime(row[a_end], "%Y-%m-%d %H:%M:%S")
        end_seconds = mdates.date2num(end_date)
        loc_idx = location_map[row[a_loc_id]]
        ax.broken_barh([(start_seconds, end_seconds-start_seconds)],
                       (loc_idx*2+int(row[a_lane_num]), 0.5), facecolors='tab:blue', alpha=0.5)
    # Formatting
    ax.set_yticks(range(len(locations*2)))
    ax.set_yticklabels([l+str(i) for l in locations for i in range(1,3)])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for Locations")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    plot_log_data("./VOSimu-InputInformation.xlsx","./all-logs/logger_all.log")
