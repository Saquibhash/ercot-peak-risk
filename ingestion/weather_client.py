import os
import requests, pandas as pd

def fetch_weather(lat, lon, start, end):
    r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
        "latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
        "daily": "temperature_2m_max,temperature_2m_mean",
        "hourly": "dew_point_2m",
        "temperature_unit": "fahrenheit", "timezone": "America/Chicago"}, timeout=60)
    r.raise_for_status()
    j = r.json()
    daily = pd.DataFrame(j["daily"]).rename(columns={
        "time": "day", "temperature_2m_max": "tmax_f", "temperature_2m_mean": "tmean_f"})
    hourly = pd.DataFrame(j["hourly"])
    hourly["day"] = hourly["time"].str[:10]
    dew = hourly.groupby("day").dew_point_2m.max().rename("dewpoint_max_f")
    return daily.merge(dew, on="day")

if __name__ == "__main__":
    w = fetch_weather(32.78, -96.80, "2025-06-01", "2025-09-30")   # Dallas
    os.makedirs("data/raw/weather", exist_ok=True)
    w.to_csv("data/raw/weather/dallas_2025.csv", index=False)
    print(w.head())