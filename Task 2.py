# -*- coding: utf-8 -*-
"""Task 2
## Import libraries; load data
"""

from google.colab import drive
drive.mount("/content/drive/")

import pandas as pd
import numpy as np

from datetime import datetime

df = pd.read_csv("/content/drive/MyDrive/JP Morgan Chase/Nat_Gas.csv")
df.head()

"""## Define Function"""

# Function calculates value of storage contract; calculates gross profit and
# then deducts total costs (deductions); returns net value of contract.
def gas_storage_contract(
    df,
    inject_dates,     # list of injection dates
    wthdrl_dates,     # list of withdrawal dates
    volumes,          # list of injection/withdrawal volumes
    max_storage,      # maximum storage capacity
    str_cost_mnth,    # monthly storage fees
    inject_cost_rate, # injection rate(USD) per MMBtu
    wthdrl_cost_rate  # withdrawal rate(USD) per MMBtu
):
    # Parse dates to datetime
    df["Dates"] = pd.to_datetime(df["Dates"])
    # Create a lookup table for easier data retrieval
    price_lookup = df.set_index("Dates")["Prices"]

    # Instantiate initial value and storage
    total_value = 0
    current_storage = 0

    # loop to calc net value for an injection-withdrawal cycle
    for inj_date, wdr_date, vol in zip(inject_dates,
                                       wthdrl_dates,
                                       volumes):

        inj = pd.to_datetime(inj_date)
        wdr = pd.to_datetime(wdr_date)

        if wdr <= inj:
            raise ValueError("Withdrawal must occur after injection.")

        if current_storage + vol > max_storage:
            raise ValueError("Storage capacity exceeded.")

        current_storage += vol

        # Retrieve prices
        buy = price_lookup.loc[inj]
        sell = price_lookup.loc[wdr]

        # Storage duration
        months = (wdr - inj).days / 30

        # Profit
        gross_profit = (sell - buy) * vol

        # Costs: storage, injection, & withdrawal
        storage_cost = months * str_cost_mnth
        inject_cost = inject_cost_rate * vol
        wthdrl_cost = wthdrl_cost_rate * vol

        net_value = (
            gross_profit
            - storage_cost
            - inject_cost
            - wthdrl_cost
        )

        total_value += net_value

        current_storage -= vol

    return total_value

# Run the function
value = gas_storage_contract(
    df,
    inject_dates=["2021/05/31", "2022/04/30"],
    wthdrl_dates=["2022/02/28", "2023/01/31"],
    volumes=[500000, 600000],
    max_storage=2000000,
    str_cost_mnth=50000,
    inject_cost_rate=0.01,
    wthdrl_cost_rate=0.015
)

print(f"Contract Value: ${value:,.2f}")
