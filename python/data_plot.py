import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

directory = "data"
file ="rate_collection_006_01_1hz_160deg.csv"

data = pd.read_csv(directory+"/"+file).to_numpy()
plt.plot(data,'.-',markersize=0.7,linewidth=0.5)
plt.show()
