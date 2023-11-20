import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium

import requests
import pandas as pd
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

resp = requests.get(URL)
data = resp.text
df = pd.read_csv(io.StringIO(data))
print('Data downloaded and read into a dataframe!')

# Create dataframes for recession period
rec_data = df[df['Recession'] == 1]

# Scatter plot
plt.scatter(rec_data['Price'], rec_data['Automobile_Sales'])

# Customize plot
plt.xlabel('Price')
plt.ylabel('Automobile Sales Volume')
plt.title('Correlation between Price and Sales Volume during Recessions')

plt.show()
