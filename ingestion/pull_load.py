import os, time
import pandas as pd
from ingestion.ercot_client import get

PATH = "np6-345-cd/act_sys_load_by_wzn"

def fetch_load(start, end, size=5000):
    frames, page = [], 1
    while True:
        out = get(PATH, operatingDayFrom=start, operatingDayTo=end, size=size, page=page)
        cols = [f["name"] for f in out["fields"]]
        frames.append(pd.DataFrame(out["data"], columns=cols))
        meta = out["_meta"]
        total_pages = meta.get("totalPages", 1)
        if page >= total_pages:
            break
        page += 1
        time.sleep(2)          # ERCOT limits request rate, so keep this pause
    return pd.concat(frames, ignore_index=True)

if __name__ == "__main__":
    df = fetch_load("2025-06-01", "2025-09-30")
    print(df.shape, df.operatingDay.min(), df.operatingDay.max())
    os.makedirs("data/raw/load", exist_ok=True)
    df.to_csv("data/raw/load/api_2025_summer.csv", index=False)