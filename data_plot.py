import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

directory = "data"
file ="rate_collection_1.csv"

data = pd.read_csv(directory+"/"+file).to_numpy()
plt.plot(data,'.-')
plt.show()
