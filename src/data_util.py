from read_logs import parse_log_file
from plot_excel_data import parse_exceldata

a_order_id = "order_id"
a_vehicle_id = "vehicle_id"

class DataManager(object):
    def __init__(self, excel_data, log_data):
        self.excel_data = excel_data
        self.log_data = log_data

    # get pairs of orders and corresponding assigned vehicle
    def get_order_assigments(self):
        df_assignments = self.log_data.starting_events[[a_order_id, a_vehicle_id]].drop_duplicates()
        df_assignments.to_csv("assigments.csv")
        return df_assignments


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
    data_manager.get_order_assigments()
