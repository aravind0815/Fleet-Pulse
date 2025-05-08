# import json
# import time
# import random
# import logging
# from kafka import KafkaProducer

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# # Kafka setup
# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# # Simulate truck behavior
# def generate_truck_data(truck_id, risky=False):
#     speed = random.randint(50, 80)
#     temp = random.uniform(75, 85)

#     if risky:
#         speed += random.randint(-10, 15)
#         temp += random.uniform(10, 25)
#         temp = min(temp, 130)
#         speed = min(speed, 120)

#     return {
#         "truck_id": truck_id,
#         "speed": speed,
#         "temperature": round(temp, 2),
#         "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#     }

# # Main loop to send data continuously
# truck_ids = list(range(101, 111))  # 10 trucks

# try:
#     while True:
#         for truck_id in truck_ids:
#             risky = random.random() < 0.3  # 30% chance of risky
#             for _ in range(6):  # 🚨 Send 6 readings per truck to populate rolling window
#                 message = generate_truck_data(truck_id, risky=risky)
#                 producer.send("truck_stream", value=message)
#                 logging.info(f"🚚Sent: {message}")
#         producer.flush()
#         time.sleep(2)  # Send batch every 2 seconds
# except KeyboardInterrupt:
#     logging.info("Stopped truck data simulation.")


import json
import time
import random
import logging
from kafka import KafkaProducer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Base GPS locations
base_locations = {
    '101': (40.7128, -74.0060),  # New York
    '102': (34.0522, -118.2437),
    '103': (41.8781, -87.6298),
    '104': (29.7604, -95.3698),
    '105': (33.4484, -112.0740),
    '106': (39.7392, -104.9903),
    '107': (47.6062, -122.3321),
    '108': (32.7157, -117.1611),
    '109': (25.7617, -80.1918),
    '110': (38.9072, -77.0369)
}

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Generate data with optional risk
def generate_truck_data(truck_id, risky=False):
    speed = random.randint(50, 80)
    temp = random.uniform(75, 85)

    if risky:
        speed += random.randint(-10, 15)
        temp += random.uniform(10, 25)
        temp = min(temp, 130)
        speed = min(speed, 120)

    # Add GPS jitter
    base_lat, base_lon = base_locations[str(truck_id)]
    latitude = base_lat + random.uniform(-0.01, 0.01)
    longitude = base_lon + random.uniform(-0.01, 0.01)

    return {
        "truck_id": str(truck_id),
        "speed": speed,
        "temperature": round(temp, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6)
    }

# Main loop
truck_ids = list(range(101, 111))

try:
    while True:
        for truck_id in truck_ids:
            risky = random.random() < 0.3
            for _ in range(6):  # Fill rolling window
                message = generate_truck_data(truck_id, risky=risky)
                producer.send("truck_stream", value=message)
                logging.info(f"🚚 Sent: {message}")
        producer.flush()
        time.sleep(2)
except KeyboardInterrupt:
    logging.info("Stopped simulation.")
