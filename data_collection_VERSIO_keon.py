import requests
import time
import re
import json
import argparse
import sys
import os

# Function to fetch and process the data
def fetch_data(ip):
    url = "http://" + ip + "/devices/AdvanReader-m2-70-76af/jsonMinLocation"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        # Extract data using regex
        results = re.findall(r'<result>(.*?)</result>', data)
        # Convert extracted data to list of dictionaries
        data_list = []
        for result in results:
            # Assuming result is a JSON string that can be parsed to a dictionary
            try:
                data_dict = json.loads(result)
                data_list.append(data_dict)
            except json.JSONDecodeError:
                # If it's not JSON, store it as a plain string
                data_list.append({"result": result})
        return data_list
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return []

# Function to display the data
def display_data(data_list):
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Updated Data:")
    for data in data_list[0]:
        print(data)

# Main loop to continuously fetch and display data
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A script that requires an IP address as an argument.')
    parser.add_argument('--IP', type=str, required=True, help='The IP address to be processed')
    
    args = parser.parse_args()
    
    if not args.IP:
        print("Error: IP address not specified.")
        sys.exit(1)

    while True:
        data_list = fetch_data(args.IP)
        display_data(data_list)
        time.sleep(0.01)  # Wait for 1 second before the next fetch
