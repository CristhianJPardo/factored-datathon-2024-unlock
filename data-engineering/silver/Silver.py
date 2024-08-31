# Databricks notebook source
from pyspark.sql.functions import regexp_extract, col, to_date, md5

# COMMAND ----------

events_bronze = spark.table("factored_hackaton_2024.bronze.events")

# COMMAND ----------

events_bronze.display()

# COMMAND ----------

pattern = r"(\d{8}).export"

# COMMAND ----------

events_silver = (
    events_bronze
    .withColumn("date", regexp_extract(col("input_file_name"), pattern, 1))
    .withColumn("date", to_date(col("date"), "yyyyMMdd"))
    .withColumn("md5_id", md5("sourceurl"))
    # .orderBy(col("date").desc())
)

# COMMAND ----------

events_silver.display()

# COMMAND ----------

(
    events_silver
    .select("sourceurl", "md5_id")
    .distinct()
    .write
    .mode("overwrite")
    .saveAsTable("factored_hackaton_2024.silver.unique_urls")
)

# COMMAND ----------

(
    events_silver    
    .filter("actiongeo_countrycode IN ('AR','BL','BR','CI','CO','EC','GY','PA','PE','NS','UY','VE')")    
    .select("sourceurl", "md5_id")
    .distinct()
    .write
    .mode("overwrite")    
    .saveAsTable("factored_hackaton_2024.silver.unique_urls_filtered")
)

# COMMAND ----------

(
    events_silver    
    .filter("actiongeo_countrycode IN ('AR','BL','BR','CI','CO','EC','GY','PA','PE','NS','UY','VE')")    
    .select("actiongeo_lat", "actiongeo_long")
    .filter("actiongeo_lat IS NOT NULL AND actiongeo_long IS NOT NULL")
    .withColumnRenamed("actiongeo_lat", "lat")
    .withColumnRenamed("actiongeo_long", "lon")
    .write
    .mode("overwrite")    
    .saveAsTable("factored_hackaton_2024.gold.geo_filtered")
)
