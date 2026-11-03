import pandas as pd, matplotlib.pyplot as plt

load = pd.read_csv("data/raw/load/api_2025_summer.csv")
daily = (load.groupby("operatingDay").total.max()
             .rename("peak_mw").reset_index().rename(columns={"operatingDay": "day"}))
weather = pd.read_csv("data/raw/weather/dallas_2025.csv")
m = daily.merge(weather, on="day")

plt.scatter(m.tmax_f, m.peak_mw)
plt.xlabel("Dallas max temperature (F)")
plt.ylabel("Daily peak ERCOT load (MW)")
plt.title("Hotter days, higher peak demand")
plt.show()
print(m.sort_values("peak_mw", ascending=False).head(5)[["day", "peak_mw", "tmax_f"]])