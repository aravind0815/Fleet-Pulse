# import findspark
# findspark.init()

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, from_json, udf
# from pyspark.sql.types import StructType, IntegerType, DoubleType, StringType
# import joblib
# import pandas as pd
# from collections import defaultdict, deque

# # 🔁 Load pre-trained model
# model = joblib.load("rolling_breakdown_predictor.pkl")

# # 🧠 Singleton-style rolling store per truck
# class TruckWindowStore:
#     store = defaultdict(lambda: {"speed": deque(maxlen=5), "temp": deque(maxlen=5)})

# # 🧠 UDF to predict breakdown risk using rolling window
# def predict_breakdown(truck_id, speed, temp):
#     window = TruckWindowStore.store[truck_id]
#     window["speed"].append(speed)
#     window["temp"].append(temp)

#     # 🔍 Print window for debug
#     print(f"[DEBUG] Truck {truck_id} | Speed: {list(window['speed'])} | Temp: {list(window['temp'])}")

#     if len(window["speed"]) < 5:
#         return 0.0  # Not enough data yet

#     # 🧮 Compute rolling features
#     features = pd.DataFrame([{
#         "temp_avg_5": sum(window["temp"]) / 5,
#         "speed_avg_5": sum(window["speed"]) / 5,
#         "temp_std_5": pd.Series(window["temp"]).std(),
#         "speed_std_5": pd.Series(window["speed"]).std()
#     }])

#     # 🔮 Predict risk score (probability)
#     risk_score = model.predict_proba(features)[0][1]

#     print(f"[PREDICT] Truck {truck_id} → Risk Score: {risk_score:.4f} | Features: {features.to_dict(orient='records')[0]}")
#     return float(risk_score)

# # 🧠 Register UDF with Spark
# from pyspark.sql.functions import udf
# from pyspark.sql.types import DoubleType

# @udf(returnType=DoubleType())
# def predict_udf(truck_id, speed, temp):
#     return predict_breakdown(truck_id, speed, temp)

# # 🚀 Spark session
# spark = SparkSession.builder \
#     .appName("FleetPulseStreamingWithML") \
#     .getOrCreate()
# spark.sparkContext.setLogLevel("WARN")

# # 📜 Kafka JSON schema
# schema = StructType() \
#     .add("truck_id", IntegerType()) \
#     .add("timestamp", StringType()) \
#     .add("speed", IntegerType()) \
#     .add("temperature", DoubleType())

# # 📦 Read from Kafka topic
# df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "truck_stream") \
#     .load()

# # 🔄 Parse and select JSON fields
# json_df = df.selectExpr("CAST(value AS STRING)") \
#     .select(from_json(col("value"), schema).alias("data")) \
#     .select("data.*")

# # 🧠 Apply ML prediction UDF
# predicted_df = json_df.withColumn(
#     "breakdown_risk",
#     predict_udf(col("truck_id"), col("speed"), col("temperature"))
# )

# def write_to_postgres(batch_df, epoch_id):
#     batch_df.write \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://localhost:5432/fleetpulse_db") \
#         .option("dbtable", "truck_breakdown_logs") \
#         .option("user", "postgres") \
#         .option("password", "Aravind@123") \
#         .option("driver", "org.postgresql.Driver") \
#         .mode("append") \
#         .save()

# # Write predictions to PostgreSQL
# query = predicted_df.writeStream \
#     .foreachBatch(write_to_postgres) \
#     .outputMode("append") \
#     .start()

# query.awaitTermination()


# import findspark
# findspark.init()

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, from_json, udf
# from pyspark.sql.types import StructType, IntegerType, DoubleType, StringType
# import joblib
# import pandas as pd
# from collections import defaultdict, deque

# # 🔁 Load pre-trained model
# model = joblib.load("rolling_breakdown_predictor.pkl")

# # 🧠 Singleton-style rolling store per truck
# class TruckWindowStore:
#     store = defaultdict(lambda: {"speed": deque(maxlen=5), "temp": deque(maxlen=5)})

# # 🧠 UDF to predict breakdown risk using rolling window
# def predict_breakdown(truck_id, speed, temp):
#     window = TruckWindowStore.store[truck_id]
#     window["speed"].append(speed)
#     window["temp"].append(temp)

#     if len(window["speed"]) < 5:
#         return 0.0

#     features = pd.DataFrame([{
#         "temp_avg_5": sum(window["temp"]) / 5,
#         "speed_avg_5": sum(window["speed"]) / 5,
#         "temp_std_5": pd.Series(window["temp"]).std(),
#         "speed_std_5": pd.Series(window["speed"]).std()
#     }])

#     risk_score = model.predict_proba(features)[0][1]
#     return float(risk_score)

# # Register prediction UDF
# from pyspark.sql.types import DoubleType
# @udf(returnType=DoubleType())
# def predict_udf(truck_id, speed, temp):
#     return predict_breakdown(truck_id, speed, temp)

# # 🚀 Spark session
# spark = SparkSession.builder \
#     .appName("FleetPulseStreamingWithML") \
#     .getOrCreate()
# spark.sparkContext.setLogLevel("WARN")

# # 📜 Kafka JSON schema including GPS
# schema = StructType() \
#     .add("truck_id", IntegerType()) \
#     .add("timestamp", StringType()) \
#     .add("speed", IntegerType()) \
#     .add("temperature", DoubleType()) \
#     .add("latitude", DoubleType()) \
#     .add("longitude", DoubleType())

# # 📦 Read from Kafka
# df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "truck_stream") \
#     .load()

# # 🔄 Parse JSON
# json_df = df.selectExpr("CAST(value AS STRING)") \
#     .select(from_json(col("value"), schema).alias("data")) \
#     .select("data.*")

# # 🧠 Predict breakdown risk
# predicted_df = json_df.withColumn(
#     "breakdown_risk",
#     predict_udf(col("truck_id"), col("speed"), col("temperature"))
# )

# # Write to PostgreSQL
# def write_to_postgres(batch_df, epoch_id):
#     batch_df.write \
#         .format("jdbc") \
#         .option("url", "jdbc:postgresql://localhost:5432/fleetpulse_db") \
#         .option("dbtable", "truck_breakdown_logs") \
#         .option("user", "postgres") \
#         .option("password", "Aravind@123") \
#         .option("driver", "org.postgresql.Driver") \
#         .mode("append") \
#         .save()

# query = predicted_df.writeStream \
#     .foreachBatch(write_to_postgres) \
#     .outputMode("append") \
#     .start()

# query.awaitTermination()


import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StructType, DoubleType, StringType, IntegerType
import joblib
import pandas as pd
from collections import defaultdict, deque

# Load model
model = joblib.load("rolling_breakdown_predictor.pkl")

# Rolling window store
class TruckWindowStore:
    store = defaultdict(lambda: {"speed": deque(maxlen=5), "temp": deque(maxlen=5)})

def predict_breakdown(truck_id, speed, temp):
    if truck_id is None:
        return 0.0

    window = TruckWindowStore.store[truck_id]
    window["speed"].append(speed)
    window["temp"].append(temp)

    if len(window["speed"]) < 5:
        return 0.0

    features = pd.DataFrame([{
        "temp_avg_5": sum(window["temp"]) / 5,
        "speed_avg_5": sum(window["speed"]) / 5,
        "temp_std_5": pd.Series(window["temp"]).std(),
        "speed_std_5": pd.Series(window["speed"]).std()
    }])

    risk_score = model.predict_proba(features)[0][1]
    print(f"[PREDICT] Truck {truck_id} → Risk: {risk_score:.4f}")
    return float(risk_score)

# UDF registration
@udf(returnType=DoubleType())
def predict_udf(truck_id, speed, temp):
    return predict_breakdown(truck_id, speed, temp)

# Spark session
spark = SparkSession.builder \
    .appName("FleetPulseStreamingWithML") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schema (truck_id as string because producer sends string)
schema = StructType() \
    .add("truck_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("speed", IntegerType()) \
    .add("temperature", DoubleType()) \
    .add("latitude", DoubleType()) \
    .add("longitude", DoubleType())

# Read Kafka stream
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "truck_stream") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON from value
json_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Add prediction column
predicted_df = json_df.withColumn(
    "breakdown_risk", predict_udf(col("truck_id"), col("speed"), col("temperature"))
)

# 🚀 CAST truck_id to INT for PostgreSQL
predicted_df = predicted_df.select(
    col("truck_id").cast("int").alias("truck_id"),
    "timestamp", "speed", "temperature",
    "latitude", "longitude", "breakdown_risk"
)

# Write to PostgreSQL
def write_to_postgres(batch_df, epoch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/fleetpulse_db") \
        .option("dbtable", "truck_breakdown_logs") \
        .option("user", "postgres") \
        .option("password", "Aravind@123") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

query = predicted_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()
