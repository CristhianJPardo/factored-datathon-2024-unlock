# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import input_file_name
import datetime
import os
import boto3

# COMMAND ----------

unzipped_bucket = "s3://factored-hackaton-2024-unlock-unzipped-bucket"
medallion_bucket = "s3://factored-hackaton-2024-unlock-medallion-bucket"
type_ = "events"
catalog = "catalog=factored_hackaton_2024"

# COMMAND ----------


raw_data_location = f"{unzipped_bucket}/{type_}/"
schema_location = f"{medallion_bucket}/{catalog}/autoloader/schemas/{type_}"
checkpoint_location = f"{medallion_bucket}/{catalog}/autoloader/checkpoints/{type_}"

# COMMAND ----------

events_bronze_schema = StructType(
    [
        StructField('globaleventid', StringType(), True),
        StructField('sqldate', StringType(), True),
        StructField('monthyear', StringType(), True),
        StructField('year', StringType(), True),
        StructField('fractiondate', StringType(), True),
        StructField('actor1code', StringType(), True),
        StructField('actor1name', StringType(), True),
        StructField('actor1countrycode', StringType(), True),
        StructField('actor1knowngroupcode', StringType(), True),
        StructField('actor1ethniccode', StringType(), True),
        StructField('actor1religion1code', StringType(), True),
        StructField('actor1religion2code', StringType(), True),
        StructField('actor1type1code', StringType(), True),
        StructField('actor1type2code', StringType(), True),
        StructField('actor1type3code', StringType(), True),
        StructField('actor2code', StringType(), True), 
        StructField('actor2name', StringType(), True),
        StructField('actor2countrycode', StringType(), True),
        StructField('actor2knowngroupcode', StringType(), True),
        StructField('actor2ethniccode', StringType(), True),
        StructField('actor2religion1code', StringType(), True),
        StructField('actor2religion2code', StringType(), True),
        StructField('actor2type1code', StringType(), True),
        StructField('actor2type2code', StringType(), True),
        StructField('actor2type3code', StringType(), True),
        StructField('isrootevent', StringType(), True),
        StructField('eventcode', StringType(), True),
        StructField('eventbasecode', StringType(), True),
        StructField('eventrootcode', StringType(), True),
        StructField('quadclass', StringType(), True),
        StructField('goldsteinscale', StringType(), True),
        StructField('nummentions', StringType(), True),
        StructField('numsources', StringType(), True),
        StructField('numarticles', StringType(), True),
        StructField('avgtone', StringType(), True),
        StructField('actor1geo_type', StringType(), True),
        StructField('actor1geo_fullname', StringType(), True),
        StructField('actor1geo_countrycode', StringType(), True),
        StructField('actor1geo_adm1code', StringType(), True),
        StructField('actor1geo_lat', StringType(), True),
        StructField('actor1geo_long', StringType(), True),
        StructField('actor1geo_featureid', StringType(), True),
        StructField('actor2geo_type', StringType(), True),
        StructField('actor2geo_fullname', StringType(), True),
        StructField('actor2geo_countrycode', StringType(), True),
        StructField('actor2geo_adm1code', StringType(), True),
        StructField('actor2geo_lat', StringType(), True),
        StructField('actor2geo_long', StringType(), True),
        StructField('actor2geo_featureid', StringType(), True),
        StructField('actiongeo_type', StringType(), True),
        StructField('actiongeo_fullname', StringType(), True),
        StructField('actiongeo_countrycode', StringType(), True),
        StructField('actiongeo_adm1code', StringType(), True),
        StructField('actiongeo_lat', StringType(), True),
        StructField('actiongeo_long', StringType(), True),
        StructField('actiongeo_featureid', StringType(), True),
        StructField('dateadded', StringType(), True),
        StructField('sourceurl', StringType(), True)
    ]
)

# COMMAND ----------

autoloader = (
    spark
    .readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("sep", "\t")
    .option("header", "false")
    .option("lineSep", "\n")
    .schema(events_bronze_schema)
    .option("cloudFiles.schemaLocation", schema_location)
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .option("rescuedDataColumn", "_rescued_data")
    .load(raw_data_location)
    .select("*")
    .withColumn("input_file_name", input_file_name())
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_location)
    .trigger(once=True)
    .toTable("factored_hackaton_2024.bronze.events"   
    )
)

autoloader.awaitTermination()

# COMMAND ----------

events = spark.table("factored_hackaton_2024.bronze.events")

# COMMAND ----------

events.display()

# COMMAND ----------

events.count()
