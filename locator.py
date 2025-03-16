#!/usr/bin/env python3
import requests
from itertools import product

# Wigle API credentials
API_USERNAME = "YOUR_API_KEY"       # Replace with your actual API key
API_PASSWORD = "YOUR_API_PASSWORD"  # Replace with your actual API password

# Wigle network search endpoint
WIGLE_URL = "https://api.wigle.net/api/v2/network/search"

def query_access_point(ssid):
    """
    Query the Wigle API for a given SSID and return a list of coordinate matches.
    Each element in the list is a tuple: (ssid, latitude, longitude)
    """
    params = {"ssid": ssid}
    coords = []
    try:
        response = requests.get(WIGLE_URL, auth=(API_USERNAME, API_PASSWORD), params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving data for {ssid}: {e}", flush=True)
        return coords

    data = response.json()
    if data.get("results"):
        for result in data["results"]:
            lat = result.get("trilat")
            lon = result.get("trilong")
            if lat is not None and lon is not None:
                coords.append((ssid, lat, lon))
                print(f"Found '{ssid}' at latitude: {lat}, longitude: {lon}", flush=True)
        if not coords:
            print(f"No coordinate data found for {ssid}.", flush=True)
    else:
        print(f"No results found for {ssid}.", flush=True)
    return coords

def find_common_matches(results_by_ssid, threshold):
    """
    Check all combinations (one coordinate per SSID) to find common matches within the threshold.
    Returns a list of average (lat, lon) for each matching combination.
    """
    common_matches = []
    ssids = list(results_by_ssid.keys())
    for combo in product(*(results_by_ssid[ssid] for ssid in ssids)):
        lats = [item[1] for item in combo]
        lons = [item[2] for item in combo]
        if max(lats) - min(lats) < threshold and max(lons) - min(lons) < threshold:
            avg_lat = sum(lats) / len(lats)
            avg_lon = sum(lons) / len(lons)
            common_matches.append((round(avg_lat, 6), round(avg_lon, 6)))
    return list(set(common_matches))

def main():
    print("Starting script...")
    try:
        num_points = int(input("Enter the number of access points to compare: "))
    except ValueError:
        print("Invalid number entered. Exiting.", flush=True)
        return

    access_points = []
    for i in range(num_points):
        ssid = input(f"Enter SSID for access point {i+1}: ").strip()
        if ssid:
            access_points.append(ssid)
        else:
            print("Empty SSID provided; skipping.", flush=True)

    if not access_points:
        print("No access points provided. Exiting.", flush=True)
        return

    results_by_ssid = {}
    for ssid in access_points:
        results = query_access_point(ssid)
        if results:
            results_by_ssid[ssid] = results

    print("\nResults by SSID:", results_by_ssid, flush=True)

    if len(results_by_ssid) < 2:
        print("Need at least two access points with results for comparison.", flush=True)
        return

    # First attempt with threshold 0.01 degrees
    threshold = 0.01
    common_matches = find_common_matches(results_by_ssid, threshold)
    if not common_matches:
        print("\nNo common matches found with threshold 0.01 degrees.", flush=True)
        # Widen search threshold to approximately 1 mile (~0.0145 degrees)
        threshold = 0.0145
        print("Widening search threshold to 0.0145 degrees (approximately 1 mile)...", flush=True)
        common_matches = find_common_matches(results_by_ssid, threshold)

    if common_matches:
        print("\n----- Common Location Matches Found -----", flush=True)
        for lat, lon in common_matches:
            maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            print(f"Common Coordinates: (lat: {lat}, lon: {lon}) -> {maps_link}", flush=True)
    else:
        print("\nNo common matches found between the compared access points within the widened threshold.", flush=True)

if __name__ == "__main__":
    main()
