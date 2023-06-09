# Databricks notebook source
import requests

databricks_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

response = requests.request(method='POST', \
                            headers={'Authorization': f'Bearer {databricks_token}'}, \
                            url="<paste generated endpoint here>", \
                            data="In `samples.nyctaxi`, find the maximum fare by pickup ZIP")
sql = response.content.decode("unicode_escape").strip('"')
print(sql)

# COMMAND ----------

spark.sql("USE samples.nyctaxi")
display(spark.sql(sql))

# COMMAND ----------


