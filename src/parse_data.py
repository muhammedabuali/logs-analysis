import pandas as pd
import matplotlib.pyplot as plt


sheet_names = ['Locations', 'Vehicles', 'ContainerOrders']

loc_x = 'X-Coordinate [mm]'
loc_y = 'Y-Coordinate [mm]'
loc_name = 'Location Name'
loc_cap = 'Capacity limitation (# SC)'

def process_exceldata(path: str):
    df_locations = pd.read_excel(path, sheet_names[0])
    plot_locations(df_locations)
    
    df_vehicles = pd.read_excel(path, sheet_names[1])
    process_vehicles(df_vehicles)
    
    df_orders = pd.read_excel(path, sheet_names[2])
    process_orders(df_orders)

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

def process_orders(df_orders):
    pass

if __name__ == "__main__":
    process_exceldata("./VOSimu-InputInformation.xlsx")