# Databricks notebook source
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

databricks_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

response = requests.request(method='POST', \
                            headers={'Authorization': f'Bearer {databricks_token}'}, \
                            url="<paste generated endpoint here>", \
                            data="A faded photograph of a sheep sipping a Pepsi in a Tokyo dive bar")

image = Image.open(BytesIO(response.content), formats=["JPEG"])
plt.imshow(image)
