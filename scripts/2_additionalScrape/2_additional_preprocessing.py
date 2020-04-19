import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.model_preprocessing import *




intial_csv=str()
for file in os.listdir(raw_scrapped_path):
	print(file)
	intial_csv= file
	break

df_original = pd.read_csv(intial_scraped_preprocessed_file )
final_df = pd.read_csv(raw_scrapped_path+intial_csv)

for file in os.listdir(raw_scrapped_path):

	if(file.endswith("csv") and file!=intial_csv):
		print(file)
		df  = pd.read_csv(raw_scrapped_path+file)
		final_df = pd.concat([df , final_df], ignore_index=True)

print(final_df.shape)

df = final_df.copy()



df_original['deadline']  = pd.to_datetime(df_original['deadline'])
df_original['launched_at'] = pd.to_datetime(df_original['launched_at'])

df_original['days_to_deadline'] = (df_original['deadline'] - df_original['launched_at']).dt.days

if((df_original['days_to_deadline']<0).any()):
	raise Exception("Some rows have negetive days to deadline, Please verify !")


df_original['blurb_length'] = df_original['blurb'].apply(get_blurb_length)


df["rewards_mean"] = df["rewards"].apply(getMean)
df["rewards_median"] = df["rewards"].apply(getMedian)
df["rewards_variance"] = df["rewards"].apply(getVariance)
df["rewards_SD"] = df["rewards"].apply(getSD)
df["rewards_MIN"] = df["rewards"].apply(getMIN)
df["rewards_MAX"] = df["rewards"].apply(getMAX)
df["rewards_NUM"] = df["rewards"].apply(getNUM)

df.drop("rewards", axis=1 , inplace=True)
df = df[~df['name'].duplicated()]
print("Importing the prior dataset")

df_final= pd.merge(df_original,df,on='name')



print("shape of the dataframe")
print(df.shape)
print("Number of null values")
print(df.isnull().mean())

try:
    os.remove(raw_scrapped_preprocessed_path)
    print("removed the alredy present file")
except:
    pass
    
print("saving the file to {}".format(raw_scrapped_preprocessed_path))
df_final.to_csv(raw_scrapped_preprocessed_path)

