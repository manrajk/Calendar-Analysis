import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='darkgrid')

tips = sns.load_dataset("tips")
sns.relplot(x='total_bill', y='tip', size='size', sizes=(15,200),data=tips, hue='smoker', style='smoker');
plt.show()

fmri = sns.load_dataset("fmri")
sns.relplot(x='timepoint', y='signal', kind='line', data=fmri)
plt.show()