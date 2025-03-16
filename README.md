# WiFi Location Comparator

This Python script uses the [Wigle API](https://api.wigle.net/swagger) to retrieve the geographical coordinates of WiFi access points based on their SSIDs and then compares them to find common location matches. When matching coordinates are found (within a defined threshold), the script provides Google Maps links for the common locations.

## Features

- Retrieves latitude and longitude for specified WiFi SSIDs via the Wigle API.
- Compares coordinates from different access points using a configurable threshold.
- Outputs Google Maps search links for any common location matches detected.

## Requirements

- Python 3.x  
- Requests library  
  Install with:
  ```bash
  pip install requests
  ```
- Valid Wigle API credentials

## Installation

1. Clone or download the repository containing the `locator.py` script.
2. Open `locator.py` and update the API credentials:
   ```python
   API_USERNAME = "YOUR_API_KEY"
   API_PASSWORD = "YOUR_API_PASSWORD"
   ```
3. (Optional) Make the script executable:
   ```bash
   chmod +x locator.py
   ```

## Usage

Run the script in an interactive terminal:

```bash
python3 locator.py
```

or, if executable:

```bash
./locator.py
```

When prompted, enter the number of access points and their SSIDs. The script will query the Wigle API, print out the coordinates for each SSID, and if any common matching coordinates are found, display the corresponding Google Maps links.

## Troubleshooting

- **No output or prompts:**  
  Ensure you are running the script in an interactive terminal and that the file has been updated with the latest code.

- **No common matches found:**  
  If the coordinates for individual SSIDs are returned but no common matches appear, try adjusting the threshold value in the script.

- **API errors (e.g., 401 Unauthorized):**  
  Verify your API credentials and that your Wigle API account is active.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/). You are free to use, modify, and distribute this work for non-commercial purposes, provided that you give appropriate credit.

---
