import re
import requests
import logging
import argparse
from prometheus_client import start_http_server, Gauge

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

URL = "https://www.freibad-arnum.de/"
TEMP_REGEX = r"Aktuelle Wassertemperatur:\s*([\d,]+)\s*°C"

def fetch_temperature():
    logging.info("Fetching temperature from %s", URL)
    resp = requests.get(URL, timeout=10)
    resp.raise_for_status()
    match = re.search(TEMP_REGEX, resp.text)
    if not match:
        raise ValueError("Temperature not found")
    temp_str = match.group(1).replace(",", ".")
    return float(temp_str)

gauge = Gauge(
    "freibad_arnum_water_temperature_celsius",
    "Aktuelle Wassertemperatur im Freibad Arnum"
)

def temperature_callback():
    try:
        return fetch_temperature()
    except Exception as e:
        logging.error("Error fetching temperature: %s", e)
        return float("nan")

gauge.set_function(temperature_callback)

def main():
    parser = argparse.ArgumentParser(description="Freibad Arnum Prometheus metrics exporter")
    parser.add_argument("--host", default="127.0.0.1", help="Host to listen on (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    args = parser.parse_args()

    start_http_server(args.port, addr=args.host)
    logging.info("Prometheus metrics server running on %s:%d", args.host, args.port)
    import time
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()