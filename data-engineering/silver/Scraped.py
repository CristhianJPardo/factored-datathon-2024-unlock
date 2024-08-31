# Databricks notebook source
raw = "s3://factored-hackaton-2024-unlock-scraping-bucket/scraped/"

# COMMAND ----------

scraped = spark.read.format("json").option("multiLine", "true").load(raw)

# COMMAND ----------

scraped.display()

# COMMAND ----------

scraped.count()

# COMMAND ----------

(
    scraped
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("factored_hackaton_2024.silver.scraped")
)

# COMMAND ----------

(
    scraped
    .coalesce(1)
    .write
    .partitionBy("md5_id")
    .format("json")
    .mode("overwrite")
    .save("s3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=silver/scraped_json")
)
