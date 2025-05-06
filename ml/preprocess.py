def preview_csv(filepath):
    df = pd.read_csv(filepath)
    print(df.head())

# sample csv file print
#   site_id         timestamp  flow  latitude  longitude
# 0      101  2025-04-01 00:00    35  -37.8136   144.9631
# 1      101  2025-04-01 00:15    42  -37.8136   144.9631
# 2      101  2025-04-01 00:30    38  -37.8136   144.9631
# 3      101  2025-04-01 00:45    30  -37.8136   144.9631
# 4      101  2025-04-01 01:00    45  -37.8136   144.9631
