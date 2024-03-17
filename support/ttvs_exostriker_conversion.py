import pandas as pd

# using
# transit_1,336.4158128791701,0.0019768852404810997
# transit_2,428.90741928170985,0.0023101877311829
# transit_3,521.3990157413659,0.00215576782910745
# transit_4,613.8906075509657,0.0037682825852606
# transit_5,798.8737988732507,0.0015629754371861999
# transit_6,1076.3485972557396,0.00113741301184935
# transit_7,1168.8401910245566,0.0008988321194941
# transit_8,1353.8233881245326,0.00088223156574625
# transit_9,1446.3149835840013,0.0045108672117186
# transit_10,1538.8065771936788,0.0019899126272656
# transit_11,1816.281369130129,0.00285265956341605
# transit_12,1908.772975927818,0.0025759658001512
# transit_13,2093.756166039521,0.0014701241215540001
# transit_14,2278.7393530091585,0.00420507140193875


# Given data
data = {
    # Include all original transit IDs
    "transit_id": ["transit_1", "transit_2", ...],
    # Include all midtime days
    "transit_midtime_day": [336.4158128791701, 428.90741928170985, ...],
    # Include all uncertainties
    "uncertainty": [0.0019768852404810997, 0.0023101877311829, ...]
}

# Create DataFrame
df = pd.DataFrame(data)

# Given period
period = 92.42

# Calculate expected transit number and update transit ID
first_transit_midtime = df["transit_midtime_day"].iloc[0]
df["expected_transit_number"] = (
    (df["transit_midtime_day"] - first_transit_midtime) / period).round().astype(int) + 1
df["real_transit_id"] = "transit_" + df["expected_transit_number"].astype(str)

# Create new table
new_table = df[["real_transit_id", "transit_midtime_day", "uncertainty"]]
