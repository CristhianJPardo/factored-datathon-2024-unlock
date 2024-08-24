# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType

# COMMAND ----------

unzipped_bucket = "s3://factored-hackaton-2024-unlock-unzipped-bucket"
medallion_bucket = "s3://factored-hackaton-2024-unlock-medallion-bucket"
type_ = "events"

# COMMAND ----------

events_bronze_base_schema = StructType(
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

(
    events_bronze_base_schema
    .add(StructField('_rescued_data', StringType(), True)) 
    .add(StructField('input_file_name', StringType(), True))
)    

# COMMAND ----------

empty_events_df = spark.createDataFrame([], events_bronze_base_schema)

# COMMAND ----------

(
    empty_events_df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "factored_hackaton_2024.bronze.events",
        path = f"{medallion_bucket}/catalog=factored_hackaton_2024/schema=bronze/table=events"
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- DROP TABLE `factored-hackaton`.bronze.events
