import streamlit as st
import pandas as pd
import numpy as np
from models.data import Data

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")

st.title("Input")
d = Data()
# st.write(d.result_dict)
df = pd.DataFrame(data=d.result_dict)
st.write(df.T)

fig = plt.figure(figsize=(10, 20))
sns.lineplot(data=df)
st.pyplot(fig)
# print(d.production_cost_increase)
