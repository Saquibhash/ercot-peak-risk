import pandas as pd
from ingestion.ercot_client import get

out = get("np6-345-cd/act_sys_load_by_wzn",      # path: copy from the API Explorer
          operatingDayFrom="2025-08-01", operatingDayTo="2025-08-01", size=100)
print(out.keys())                                  # see what came back
df = pd.DataFrame(out["data"], columns=[f["name"] for f in out["fields"]])
print(df.head())