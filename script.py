import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage  
import seaborn as sns
import pandas as pd

iris = sns.load_dataset("iris")
species = iris.pop("species")

dfs = pd.read_excel("MM_SS_IMZ Studie_Liste 210319_excluded_050719 wo patient names.xlsx", sheet_name="IMZ Studie 0-2")
#print(dfs[['Interne-Nr','Major genetic subtype',each for each in dfs.columns if 'CD' in each]])
names= ['Major genetic subtype']
for each in dfs.columns:
     if 'CD' in each:
        names.append(each)
print(dfs[names])
dfs = dfs[names]
dfs = dfs.dropna(axis = 0, thresh = 30)
dfs = dfs.set_index('Major genetic subtype')

labels = names #dfs.index.array
lut = dict(zip(set(labels), sns.hls_palette(len(set(labels)), l=0.5, s=0.8)))
row_colors = pd.DataFrame(labels)[0].map(lut)
del dfs.index.name
dfs = dfs.dropna(axis = 1, how = 'any')

row_colors = pd.DataFrame(labels)[0].map(lut)

#g=sns.clustermap(dfs, col_cluster=False, linewidths=0.1, cmap='coolwarm', row_colors=row_colors)
#plt.show()

#plt.figure(figsize=(10, 7))  
sns.clustermap(dfs)
plt.show()
