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

    plot_vehicle_gantt(excel_data, log_data)

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


if __name__ == "__main__":
    plot_log_data("./VOSimu-InputInformation.xlsx","./all-logs/logger_all.log")
