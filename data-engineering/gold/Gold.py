# Databricks notebook source
from pyspark.sql.functions import md5, col, lit, concat

# COMMAND ----------

events = spark.table("factored_hackaton_2024.bronze.events")

# COMMAND ----------

unique_urls = spark.table("factored_hackaton_2024.silver.unique_urls")

# COMMAND ----------

join_ = (
    events
    .select("sourceurl")
    .withColumnRenamed("sourceurl", "sourceurl_")
    .distinct()
    .withColumn("md5_id", md5(col("sourceurl_")))
    .join(unique_urls, on="md5_id", how="inner")
    .withColumn("content", col("md5_id"))
    .withColumn("title", col("md5_id"))
    .drop("sourceurl_")
)

# COMMAND ----------

(
    join_
    # .coalesce(1)
    .write
    # .partitionBy("md5_id")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .format("delta")
    # .save("s3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=gold/json/")
    .saveAsTable("factored_hackaton_2024.gold.events")
)

# COMMAND ----------


