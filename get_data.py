import requests
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import matplotlib.dates as mdates

def color_code(key):
    dict = {-1 : "lawngreen", 1 : "g", 3 : "orange", 4 : "red"}
    color = dict[key]
    return color

def text_code(key):
    dict = {-1 : "Strom bevorzugt nutzen", 
            1 : "Strom wie gewoghnt nutzen", 
            3 : "Stromverbrauch reduzieren um Kotsen und CO2 zu sparen", 
            4 : "Stromverbrauch reduzieren um Strommangel zu verhindern"}
    text = dict[key]
    return text

def current_carbon_intensity(plz):

    stromgedachtURL = "https://api.stromgedacht.de/v1/now?zip=" + str(plz)
    response = requests.get(stromgedachtURL, headers = {"accept":"application/json"})
    content = json.loads(response.text)
    state = content["state"]
    return state

def forecast_carbon_intensity(plz):
    stromgedachtURL = "https://api.stromgedacht.de/v1/statesRelative?zip=" + str(plz) + "&hoursInFuture=48&hoursInPast=96"
    response = requests.get(stromgedachtURL, headers = {"accept":"application/json"})
    content = json.loads(response.text)
    return content

def forecast_all(plz):
    stromgedachtURL = "https://api.stromgedacht.de/v1/forecast?zip=" + str(plz)
    response = requests.get(stromgedachtURL, headers = {"accept":"application/json"})
    content = json.loads(response.text)
    return content

def show_current_carbon_intensity(plz):
    state = current_carbon_intensity(plz)
    color = color_code(state)
    text = text_code(state)

    # Create a figure without axes
    fig, ax = plt.subplots(frameon=False)

    # Create a green square using the Rectangle class from patches module
    green_square = patches.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='none', facecolor=color)

    # Add the green square to the figure
    ax.add_patch(green_square)

    # Set the aspect ratio to be equal
    ax.set_aspect('equal', adjustable='box')

    # Add text at the top of the suqare:
    text_in_square1 = "Dein aktueller Strommix für: " + str(plz)
    ax.text(0.5, 0.9, text_in_square1, color='white', fontsize=12, ha='center', va='center')

    # Add text in the middle of the square
    text_in_square2 = "Jetzt solltest du " + text
    ax.text(0.5, 0.5, text_in_square2, color='white', fontsize=10, ha='center', va='center')


    # Remove axes and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Display the plot without axes
    plt.show()

def show_forecast_carbon_intensity(plz):
    api_response = forecast_carbon_intensity(plz)
    
    # Extract data
    states_data = api_response["states"]

    # Convert date strings to datetime objects
    from_dates = [datetime.fromisoformat(entry["from"][:-6]) for entry in states_data]
    to_dates = [datetime.fromisoformat(entry["to"][:-6]) for entry in states_data]
    state_values = [entry["state"] for entry in states_data]

    # Plotting
    fig, ax = plt.subplots(figsize=(15, 3))

    # Iterate over time steps and plot bars with corresponding colors
    for from_date, to_date, state in zip(from_dates, to_dates, state_values):
        ax.barh(0, to_date - from_date, left=from_date, color=color_code(state), edgecolor='black')

    # Set x-axis date formatting
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))  # Set the interval as needed
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Set labels and title
    plt.xlabel('Time')

    # Remove y-axis labels
    ax.set_yticklabels([])

    # Display the plot
    plt.show()

def show_forecast_all(plz):
    api_response = forecast_all(plz)

    # Extract data
    load_data = api_response["load"]
    renewable_energy_data = api_response["renewableEnergy"]
    residual_load_data = api_response["residualLoad"]
    super_green_threshold_data = api_response["superGreenThreshold"]

    # Convert date strings to datetime objects
    load_dates = [datetime.strptime(entry["dateTime"], "%Y-%m-%dT%H:%M:%SZ") for entry in load_data]
    renewable_energy_dates = [datetime.strptime(entry["dateTime"], "%Y-%m-%dT%H:%M:%SZ") for entry in renewable_energy_data]
    residual_load_dates = [datetime.strptime(entry["dateTime"], "%Y-%m-%dT%H:%M:%SZ") for entry in residual_load_data]
    super_green_threshold_dates = [datetime.strptime(entry["dateTime"], "%Y-%m-%dT%H:%M:%SZ") for entry in super_green_threshold_data]


    # Extract values
    load_values = [entry["value"] for entry in load_data]
    renewable_energy_values = [entry["value"] for entry in renewable_energy_data]
    residual_load_values = [entry["value"] for entry in residual_load_data]
    super_green_threshold_values = [entry["value"] for entry in super_green_threshold_data]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines without markers
    ax.plot(load_dates, load_values, label='Load', linestyle='-', linewidth=2)
    ax.plot(renewable_energy_dates, renewable_energy_values, label='Renewable Energy', linestyle='-', linewidth=2)
    ax.plot(residual_load_dates, residual_load_values, label='Residual Load', linestyle='-', linewidth=2)
    ax.plot(super_green_threshold_dates, super_green_threshold_values, label='Super Green Threshold', linestyle='-', linewidth=2)

    # Set ticks every 8 values on the time axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))

    # Beautify the x-labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Rotate and format the x-axis labels for better readability
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Set labels and title
    ax.set_xlabel('Time')

    # Display legend
    ax.legend()

    # Display the plot
    plt.show()