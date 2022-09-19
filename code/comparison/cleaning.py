import pandas as pd

def clean_datasets(df1, df2, column1, column2, df1_label, df2_label):
	df1 = df1[(df1[column1] != "-") & (df1[column2] != "-")]
	df2 = df2[(df2[column1] != "-") & (df2[column2] != "-")]

	df1 = df1.drop_duplicates()
	df2 = df2.drop_duplicates()

	df1["GA"] = "{} GA".format(df1_label)
	df2["GA"] = "{} GA".format(df2_label)

	df = pd.concat([df1, df2], axis = 0)
	df = df.reset_index(drop = True)
	df[column1] = df[column1].astype(float)
	df[column2] = df[column2].astype(float)

	return df