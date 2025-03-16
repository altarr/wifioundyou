import requests

# Set your Wigle API credentials here.
# Wigle uses HTTP Basic Auth: your API token (or username) and your API password.
API_USERNAME = "your_api_username"  # Replace with your API username/token
API_PASSWORD = "your_api_password"  # Replace with your API password/secret

# Wigle network search endpoint
WIGLE_URL = "https://api.wigle.net/api/v2/network/search"

def query_access_point(ssid):
    """
    Query the Wigle API for a given SSID and return the first result's coordinates.
    """
    params = {"ssid": ssid}
    try:
        response = requests.get(WIGLE_URL, auth=(API_USERNAME, API_PASSWORD), params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving data for {ssid}: {e}")
        return None

    data = response.json()
    # Check if there are results; Wigle returns a 'results' key.
    if data.get("results"):
        first_result = data["results"][0]
        lat = first_result.get("trilat")
        lon = first_result.get("trilong")
        if lat is not None and lon is not None:
            print(f"Found '{ssid}' at latitude: {lat}, longitude: {lon}")
            return (ssid, lat, lon)
        else:
            print(f"No coordinate data found for {ssid}.")
    else:
        print(f"No results found for {ssid}.")
    return None

def main():
    try:
        num_points = int(input("Enter the number of access points to compare: "))
    except ValueError:
        print("Invalid number entered. Exiting.")
        return

    access_points = []
    for i in range(num_points):
        ssid = input(f"Enter SSID for access point {i + 1}: ").strip()
        if ssid:
            access_points.append(ssid)
        else:
            print("Empty SSID provided; skipping.")

    if not access_points:
        print("No access points provided. Exiting.")
        return

    results = []
    for ssid in access_points:
        result = query_access_point(ssid)
        if result:
            results.append(result)

    if not results:
        print("No valid results were found for the given access points.")
        return

    # Compare the locations: here we compute the average latitude and longitude.
    total_lat = sum(res[1] for res in results)
    total_lon = sum(res[2] for res in results)
    count = len(results)
    avg_lat = total_lat / count
    avg_lon = total_lon / count

    print("\n----- Comparison Results -----")
    for ssid, lat, lon in results:
        print(f"{ssid}: (lat: {lat}, lon: {lon})")
    print(f"\nProbable common location (average coordinates): (lat: {avg_lat}, lon: {avg_lon})")

if __name__ == "__main__":
    main()
