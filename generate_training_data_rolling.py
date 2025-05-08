import pandas as pd
import random

records = []

# Generate time-series data per truck
for truck_id in range(100, 110):
    temp = 80.0
    speed = 60
    for t in range(300):
        # Introduce occasional spikes to simulate breakdown risk
        if random.random() < 0.1:
            temp += random.uniform(10, 20)
            speed += random.randint(-20, 20)
        else:
            temp += random.uniform(-1.5, 1.5)
            speed += random.randint(-2, 2)

        temp = max(70, min(130, temp))
        speed = max(20, min(100, speed))
        records.append([truck_id, t, speed, temp])

df = pd.DataFrame(records, columns=["truck_id", "time", "speed", "temperature"])

# Rolling features
df['temp_avg_5'] = df.groupby("truck_id")["temperature"].rolling(5).mean().reset_index(0, drop=True)
df['speed_avg_5'] = df.groupby("truck_id")["speed"].rolling(5).mean().reset_index(0, drop=True)
df['temp_std_5'] = df.groupby("truck_id")["temperature"].rolling(5).std().reset_index(0, drop=True)
df['speed_std_5'] = df.groupby("truck_id")["speed"].rolling(5).std().reset_index(0, drop=True)

# Define breakdown condition (more aggressive)
df["breakdown"] = (
    (df["temp_avg_5"] > 100) &
    (df["temp_std_5"] > 4) &
    (df["speed_std_5"] > 5)
).astype(int)

df = df.dropna()
df.to_csv("training_rolling_data.csv", index=False)
print("✅ Regenerated 'training_rolling_data.csv' with breakdown cases")
