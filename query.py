# Databricks notebook source
import requests

databricks_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

response = requests.request(method='POST', \
                            headers={'Authorization': f'Bearer {databricks_token}'}, \
                            url="<paste generated endpoint here>", \
                            data="Explain to me the difference between nuclear fission and fusion.")
print(response.content)
