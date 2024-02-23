import pandas as pd

df = pd.read_csv("csvdump_18k.csv")

df_new_columns = pd.read_csv("csvdump_just_shops_data.csv")
df_new_columns = df_new_columns[["how_many_shops"]]

df = pd.concat([df, df_new_columns], axis=1)

df_new_columns = pd.read_csv("csvdump_just_schools_data.csv")
df_new_columns = df_new_columns[["how_many_schools","closest_school"]]

df = pd.concat([df, df_new_columns], axis=1)

df.to_csv("csvdump_with_shops_and_schools_18_k.csv")