# Databricks notebook source
# Create Catalog

# se necesita primero crear un storage credential: https://docs.databricks.com/en/connect/unity-catalog/storage-credentials.html

# el storage credential tiene asociado un IAM role: arn:aws:iam::738012852934:role/databricks-s3-ingest-f26cb-db_s3_iam, a este rol debe agregarse permisos para el bucket que se quiere usar como external location


# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW STORAGE CREDENTIALS;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION  `factored-hackaton-2024-external-location`
# MAGIC URL 's3://factored-hackaton-2024-unlock-medallion-bucket'
# MAGIC WITH (STORAGE CREDENTIAL `db_s3_credentials_databricks-s3-ingest-f26cb`)
# MAGIC COMMENT 'External location for Factored Hackaton 2024';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG factored_hackaton_2024 MANAGED LOCATION 's3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024';

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG factored_hackaton_2024;
# MAGIC CREATE SCHEMA bronze MANAGED LOCATION 's3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=bronze';
# MAGIC CREATE SCHEMA silver MANAGED LOCATION 's3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=silver';
# MAGIC CREATE SCHEMA gold MANAGED LOCATION 's3://factored-hackaton-2024-unlock-medallion-bucket/catalog=factored_hackaton_2024/schema=gold';
