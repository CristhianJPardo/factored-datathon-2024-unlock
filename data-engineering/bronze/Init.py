# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType

# COMMAND ----------

# MAGIC %sql
# MAGIC -- based on documentation http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf, using ChatGpt we create the comments metadata for every column
# MAGIC USE CATALOG factored_hackaton_2024;
# MAGIC CREATE TABLE bronze.events (
# MAGIC     globaleventid STRING COMMENT 'Globally unique identifier assigned to each event record.',
# MAGIC     sqldate STRING COMMENT 'Date the event took place in YYYYMMDD format.',
# MAGIC     monthyear STRING COMMENT 'Alternative formatting of the event date, in YYYYMM format.',
# MAGIC     year STRING COMMENT 'Alternative formatting of the event date, in YYYY format.',
# MAGIC     fractiondate STRING COMMENT 'Alternative formatting of the event date as a fraction of the year.',
# MAGIC     actor1code STRING COMMENT 'Complete raw CAMEO code for Actor1, including geographic, class, ethnic, religious, and type classes.',
# MAGIC     actor1name STRING COMMENT 'The actual name of Actor1, such as a leader’s name or an organization.',
# MAGIC     actor1countrycode STRING COMMENT '3-character CAMEO code for the country affiliation of Actor1.',
# MAGIC     actor1knowngroupcode STRING COMMENT 'CAMEO code for a known IGO/NGO/rebel organization associated with Actor1.',
# MAGIC     actor1ethniccode STRING COMMENT 'CAMEO code representing the ethnic affiliation of Actor1.',
# MAGIC     actor1religion1code STRING COMMENT 'Primary CAMEO code for the religious affiliation of Actor1.',
# MAGIC     actor1religion2code STRING COMMENT 'Secondary CAMEO code for the religious affiliation of Actor1, if multiple religions are specified.',
# MAGIC     actor1type1code STRING COMMENT 'CAMEO code of the type or role of Actor1, such as Police Forces or Government.',
# MAGIC     actor1type2code STRING COMMENT 'Second type/role code for Actor1.',
# MAGIC     actor1type3code STRING COMMENT 'Third type/role code for Actor1.',
# MAGIC     actor2code STRING COMMENT 'Complete raw CAMEO code for Actor2, including geographic, class, ethnic, religious, and type classes.',
# MAGIC     actor2name STRING COMMENT 'The actual name of Actor2, such as a leader’s name or an organization.',
# MAGIC     actor2countrycode STRING COMMENT '3-character CAMEO code for the country affiliation of Actor2.',
# MAGIC     actor2knowngroupcode STRING COMMENT 'CAMEO code for a known IGO/NGO/rebel organization associated with Actor2.',
# MAGIC     actor2ethniccode STRING COMMENT 'CAMEO code representing the ethnic affiliation of Actor2.',
# MAGIC     actor2religion1code STRING COMMENT 'Primary CAMEO code for the religious affiliation of Actor2.',
# MAGIC     actor2religion2code STRING COMMENT 'Secondary CAMEO code for the religious affiliation of Actor2, if multiple religions are specified.',
# MAGIC     actor2type1code STRING COMMENT 'CAMEO code of the type or role of Actor2, such as Police Forces or Government.',
# MAGIC     actor2type2code STRING COMMENT 'Second type/role code for Actor2.',
# MAGIC     actor2type3code STRING COMMENT 'Third type/role code for Actor2.',
# MAGIC     isrootevent STRING COMMENT 'Flag indicating if the event is considered a root event, often representing the main event in a document.',
# MAGIC     eventcode STRING COMMENT 'Raw CAMEO action code describing the action performed by Actor1 on Actor2.',
# MAGIC     eventbasecode STRING COMMENT 'The level two leaf root node of the CAMEO event code.',
# MAGIC     eventrootcode STRING COMMENT 'Root-level category of the CAMEO event code.',
# MAGIC     quadclass STRING COMMENT 'Primary classification of the event type, such as Verbal Cooperation or Material Conflict.',
# MAGIC     goldsteinscale STRING COMMENT 'Goldstein Scale score for the event type, ranging from -10 to +10.',
# MAGIC     nummentions STRING COMMENT 'Total number of mentions of the event across all source documents.',
# MAGIC     numsources STRING COMMENT 'Total number of information sources containing one or more mentions of the event.',
# MAGIC     numarticles STRING COMMENT 'Total number of source documents containing one or more mentions of the event.',
# MAGIC     avgtone STRING COMMENT 'Average tone of all documents mentioning the event, ranging from -100 to +100.',
# MAGIC     actor1geo_type STRING COMMENT 'Geographic resolution of Actor1’s location, such as country or city.',
# MAGIC     actor1geo_fullname STRING COMMENT 'Full human-readable name of the location for Actor1.',
# MAGIC     actor1geo_countrycode STRING COMMENT '2-character FIPS10-4 country code for Actor1’s location.',
# MAGIC     actor1geo_adm1code STRING COMMENT 'FIPS10-4 administrative division 1 code for Actor1’s location.',
# MAGIC     actor1geo_lat STRING COMMENT 'Centroid latitude of Actor1’s location for mapping.',
# MAGIC     actor1geo_long STRING COMMENT 'Centroid longitude of Actor1’s location for mapping.',
# MAGIC     actor1geo_featureid STRING COMMENT 'GNS or GNIS FeatureID for Actor1’s location.',
# MAGIC     actor2geo_type STRING COMMENT 'Geographic resolution of Actor2’s location, such as country or city.',
# MAGIC     actor2geo_fullname STRING COMMENT 'Full human-readable name of the location for Actor2.',
# MAGIC     actor2geo_countrycode STRING COMMENT '2-character FIPS10-4 country code for Actor2’s location.',
# MAGIC     actor2geo_adm1code STRING COMMENT 'FIPS10-4 administrative division 1 code for Actor2’s location.',
# MAGIC     actor2geo_lat STRING COMMENT 'Centroid latitude of Actor2’s location for mapping.',
# MAGIC     actor2geo_long STRING COMMENT 'Centroid longitude of Actor2’s location for mapping.',
# MAGIC     actor2geo_featureid STRING COMMENT 'GNS or GNIS FeatureID for Actor2’s location.',
# MAGIC     actiongeo_type STRING COMMENT 'Geographic resolution of the action location, such as country or city.',
# MAGIC     actiongeo_fullname STRING COMMENT 'Full human-readable name of the location where the action took place.',
# MAGIC     actiongeo_countrycode STRING COMMENT '2-character FIPS10-4 country code for the action location.',
# MAGIC     actiongeo_adm1code STRING COMMENT 'FIPS10-4 administrative division 1 code for the action location.',
# MAGIC     actiongeo_lat STRING COMMENT 'Centroid latitude of the action location for mapping.',
# MAGIC     actiongeo_long STRING COMMENT 'Centroid longitude of the action location for mapping.',
# MAGIC     actiongeo_featureid STRING COMMENT 'GNS or GNIS FeatureID for the action location.',
# MAGIC     dateadded STRING COMMENT 'Date the event was added to the master database.',
# MAGIC     sourceurl STRING COMMENT 'URL of the news article where the event was found.',
# MAGIC     _rescued_data STRING COMMENT 'Data that was rescued during processing and could not be parsed into specific columns.',
# MAGIC     input_file_name STRING COMMENT 'Name of the input file from which the data was extracted.'
# MAGIC )
# MAGIC USING DELTA
# MAGIC LOCATION 's3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=bronze/table=events/'
# MAGIC ;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED factored_hackaton_2024.bronze.events;
