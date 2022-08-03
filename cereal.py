# %% [markdown]
# Let's collect data, transform a little and look at the description of it

# %%
import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\darar\Downloads\cereal.xlsx',header=None)
name_brands = {'A':'American Home Food Products', 'G':'General Mills', 'K':'Kelloggs', 'N':'Nabisco', 'P':'Post', 'Q':"Quaker Oats", 'R':'Ralston Purina'}
column_names = {
    0: 'cereal name',
	1: 'manufacturer',
	2: 'type',
	3: 'calories',
	4: 'protein',
	5: 'fat',
	6: 'sodium',
	7: 'dietary fiber',
	8: 'complex carbohydrates',
	9: 'sugars',
	10: 'display shelf',
	11: 'potassium',
	12: 'vitamins and minerals',
	13: 'weight',
	14: 'cups per serving' 
}

df[1] = df[1].fillna('')
df[2] = df[2].fillna('')
df[0] = df[0] + df[1] + df[2] 
df = df[0].str.split(' ', expand=True)
df.rename(columns={x: column_names[x] for x in column_names if x in df.columns}, inplace=True)
df['manufacturer'] = df['manufacturer'].map(name_brands)	
df = df.astype({x: 'float' for x in df.columns[3:]})
df.describe()


# %% [markdown]
# Some MIN values in measures columns are negative. It can not be possible. Firstly change them to Nan 

# %%
col_selected_to_nan = [col for col in df.columns if df.dtypes[col]!= 'object']
df.loc[:,col_selected_to_nan] = df.loc[:,col_selected_to_nan].applymap(lambda x: x if x >= 0 else np.nan)
df.loc[df.isna().values.any(axis=1),df.isna().values.any(axis=0)]

# %% [markdown]
# We have to normalize data because of different weights, and cups per serving. However ['cups per serving'] has more missing values than ['weight']
# For this: 
# - delete ['cups per serving'] column
# - rows with Nan values in ['weight'] (2 products only)  

# %%
df.drop(['cups per serving'], axis=1,inplace=True)
df.dropna(subset=['weight'], inplace=True)
df.loc[df.isna().values.any(axis=1),df.isna().values.any(axis=0)]

# %% [markdown]
# I suppose that it'll be a right way to fill remained NaN with a median across each column, where NaN value exists.  
# 

# %%
df = df.fillna(df.median())

# %% [markdown]
# Now normalize all numeric data, except ['display shelf'], using ['weight] column

# %%
l = list(df[df['weight']!=1].index)
df[df['weight']!=1]

# %%
col_selected_to_normalize = [col for col in df.columns if df.dtypes[col]!= 'object' and col != 'display shelf']
df.loc[:,col_selected_to_normalize] = df.loc[:,col_selected_to_normalize].div(df['weight'],axis=0)
df.drop(['weight'], axis=1,inplace=True)

# %%
df.loc[l,]

# %%


# %%

df


