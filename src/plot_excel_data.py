import pandas as pd
import matplotlib.pyplot as plt

sheet_names = ['Locations', 'Vehicles', 'ContainerOrders']

loc_x = 'X-Coordinate [mm]'
loc_y = 'Y-Coordinate [mm]'
loc_name = 'Location Name'
loc_cap = 'Capacity limitation (# SC)'

order_cols = [ "TractorOrderId","ContainerOrderId","ContainerName","Length","OriginLocation","DestinationLocation","Time first known" ]
order_org = "OriginLocation"
order_dst = "DestinationLocation"

org_x= "Origin X-Coordinate"
org_y= "Origin Y-Coordinate"
dst_x= "Destination X-Coordinate"
dst_y= "Destination Y-Coordinate"

class ExcelDataManger(object):
    def __init__(self):
        self.df_locations = pd.DataFrame()
        self.df_vehicles = pd.DataFrame()
        self.df_orders = pd.DataFrame()

def parse_exceldata(path: str):
    data = ExcelDataManger()
    data.df_locations = pd.read_excel(path, sheet_names[0])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    data.df_vehicles = pd.read_excel(path, sheet_names[1])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    data.df_orders = pd.read_excel(path, sheet_names[2])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return data

def plot_exceldata(path: str):
    df_locations = pd.read_excel(path, sheet_names[0])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    df_vehicles = pd.read_excel(path, sheet_names[1])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    df_orders = pd.read_excel(path, sheet_names[2])\
        .apply(lambda x: x.str.strip() if x.dtype == "object" else x)


    # plot_locations(df_locations)
    # plot_order_locations(df_orders)
    plot_order_paths(df_orders,df_locations)

def plot_locations(df_locations):
    color_map = {"WS": "red", "YARD": "blue", "RAIL": "green", "QC": "yellow"}
    df_locations["color"] = df_locations[loc_name].str[0].map(color_map)  # Extract first letter and map to color
    # plot the locations
    for prefix in color_map:
        subset = df_locations[df_locations[loc_name].str.startswith(prefix)]
        plt.scatter(subset[loc_x],subset[loc_y],color=color_map[prefix],label=prefix)
    plt.xlabel(loc_x)
    plt.ylabel(loc_y)
    plt.title("Locations Plot")
    plt.legend()
    plt.grid()
    plt.show()

def plot_order_locations(df_orders):
    plt.scatter(df_orders[order_org], df_orders[order_dst])
    plt.xlabel(order_org)
    plt.ylabel(order_dst)
    plt.title("Order Locations matrix Plot")
    plt.legend()
    plt.grid()
    plt.show()

def plot_order_paths(df_orders, df_locations):
    # get origin and destiation locations and merge them with the orders
    df_paths = df_orders[[order_org,order_dst]]\
        .merge(df_locations[[loc_x,loc_y,loc_name]], left_on=order_org,right_on=loc_name)\
        .rename(columns={loc_x: org_x, loc_y: org_y})\
        .merge(df_locations[[loc_x,loc_y,loc_name]], left_on=order_dst,right_on=loc_name)\
        .rename(columns={loc_x: dst_x, loc_y: dst_y})
    df_paths.to_csv("paths.csv")

    # plot locations
    color_map = {"WS": "red", "YARD": "blue", "RAIL": "green", "QC": "yellow"}
    for prefix in color_map:
        subset = df_locations[df_locations[loc_name].str.startswith(prefix)]
        plt.scatter(subset[loc_x],subset[loc_y],color=color_map[prefix],label=prefix)
    plt.legend()

    # plot order paths
    path_color_map = {"WS": "brown", "YARD": "black", "RAIL": "purple", "QC": "brown"}
    df_paths["color"] = df_paths[order_dst].str[0].map(path_color_map)  # Extract first letter and map to color
    for prefix in path_color_map:
        subset = df_paths[df_paths[order_org].str.startswith(prefix)]
        for _, row in subset.iterrows():
            plt.plot([row[org_x], row[dst_x]], [row[org_y], row[dst_y]])
            # Add an arrow annotation
            plt.annotate("",
                         xy=(row[dst_x], row[dst_y]),  # Arrow end (x2, y2)
                         xytext=(row[org_x], row[org_y]),  # Arrow start (x1, y1)
                         arrowprops=dict(arrowstyle="->", color=path_color_map[prefix], linewidth=2))


    plt.grid()
    plt.xlabel(loc_x)
    plt.ylabel(loc_y)
    plt.title("Order dsitances Plot")
    plt.show()

if __name__ == "__main__":
    plot_exceldata("./VOSimu-InputInformation.xlsx")
