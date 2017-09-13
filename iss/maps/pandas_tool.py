#coding:utf-8


import pandas as pd
import numpy as np


df1 = pd.read_csv('csv/2017-08-08-unt-krs.csv', sep=';', dtype={'OPERSTATUS':np.str})
df2 = pd.read_csv('csv/2017-09-08-unt-krs.csv', sep=';', dtype={'OPERSTATUS':np.str})

del df1["ADMINSTATUS"]
del df2["ADMINSTATUS"]


df1 = df1.loc[df1["OPERSTATUS"] == "1"]
df2 = df2.loc[df2["OPERSTATUS"] == "1"]
del df1['PORT']
del df2['PORT']
del df1['OPERSTATUS']
del df2['OPERSTATUS']

df1 = df1['IP'].value_counts().to_frame()
df2 = df2['IP'].value_counts().to_frame()

df1 = df1.rename(index=str, columns={"IP":"OLDPORTS"})
df2 = df2.rename(index=str, columns={"IP":"NEWPORTS"})

df1['OLDDATE'] = '08.08.2017'
df2['NEWDATE'] = '08.09.2017'

df3 = df1.merge(df2, how='inner', left_index=True, right_index=True)


df3.to_csv('csv/ports.csv', sep=';')


print df3.head()