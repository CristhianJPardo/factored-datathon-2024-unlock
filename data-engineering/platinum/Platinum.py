# Databricks notebook source
from pyspark.sql.functions import *

# COMMAND ----------

events = spark.table("factored_hackaton_2024.bronze.events")

# COMMAND ----------

events.display()

# COMMAND ----------

(
    events
    .withColumn("date", regexp_extract(col("input_file_name"), r"/events/(\d{8})\.export\.CSV", 1))
    .withColumn("date", to_date(col("date"), "yyyyMMdd"))
    .groupBy("date")
    .agg(
        count("*").alias("news_per_day")
    )
    .orderBy(col("date").desc())
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("factored_hackaton_2024.platinum.news_per_day")
)

# COMMAND ----------

m1 = spark.table("factored_hackaton_2024.platinum.news_per_day")

# COMMAND ----------

m1.display()

# COMMAND ----------



# COMMAND ----------

(
    events
    .groupBy()
    .agg(count("*").alias("total_database_size"))
    .write
    .format("delta")
    .saveAsTable("factored_hackaton_2024.platinum.total_database_size")
)

# COMMAND ----------


