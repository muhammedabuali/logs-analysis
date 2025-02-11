import pandas as pd
import matplotlib.pyplot as plt


sheet_names = ['Locations', 'Vehicles', 'ContainerOrders']

loc_x = 'X-Coordinate [mm]'
loc_y = 'Y-Coordinate [mm]'
loc_name = 'Location Name'
loc_cap = 'Capacity limitation (# SC)'

def plot_exceldata(path: str):
    df_locations = pd.read_excel(path, sheet_names[0])
    plot_locations(df_locations)

    df_vehicles = pd.read_excel(path, sheet_names[1])
    process_vehicles(df_vehicles)

    df_orders = pd.read_excel(path, sheet_names[2])
    plot_order_locations(df_orders)

def plot_locations(df_locations):
    color_map = {"WS": "red", "YARD": "blue", "RAIL": "green", "QC": "yellow"}
    df_locations["color"] = df_locations[loc_name].str[0].map(color_map)  # Extract first letter and map to color
    # plot the locations
    for prefix in color_map:
        subset = df_locations[df_locations[loc_name].str.startswith(prefix)]
        plt.scatter(subset[loc_x],subset[loc_y],color=color_map[prefix],label=prefix)
    plt.xlabel(loc_x)
    plt.ylabel(loc_y)
    plt.title("Locations DataFrame")
    plt.legend()
    plt.grid()
    plt.show()

def process_vehicles(df_vehicles):
    pass

order_cols = [ "TractorOrderId","ContainerOrderId","ContainerName","Length","OriginLocation","DestinationLocation","Time first known" ]
order_org = "OriginLocation"
order_dst = "DestinationLocation"

def plot_order_locations(df_orders):
    plt.scatter(df_orders[order_org], df_orders[order_dst])
    plt.xlabel(order_org)
    plt.ylabel(order_dst)
    plt.title("Order Locations Plot")
    plt.legend()
    plt.grid()
    plt.show()

def process_orders(df_orders):
    plot_order_locations(df_orders)

if __name__ == "__main__":
    process_exceldata("./VOSimu-InputInformation.xlsx")
