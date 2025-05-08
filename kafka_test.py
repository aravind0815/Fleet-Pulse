# from kafka import KafkaProducer
# import json
# import time

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# message = {
#     "truck_id": 42,
#     "speed": 77,
#     "temperature": 93,
#     "timestamp": time.time()
# }

# producer.send("truck_stream", value=message)
# producer.flush()

# print("✅ Sent message to Kafka topic: truck_stream")


from kafka import KafkaConsumer
import json

# Create Kafka consumer for the 'truck_stream' topic
consumer = KafkaConsumer(
    "truck_stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("🔍 Listening to topic: truck_stream... Press Ctrl+C to stop.\n")

try:
    for message in consumer:
        print("📦 Received message:")
        print(json.dumps(message.value, indent=2))
except KeyboardInterrupt:
    print("🛑 Stopped consumer.")

