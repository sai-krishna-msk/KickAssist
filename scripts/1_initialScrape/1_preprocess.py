import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.raw_processing import * 


																
intial_csv=str()
for file in os.listdir(initial_scraped_files):
	print(file)
	intial_csv= file
	break


final_df = pd.read_csv(initial_scraped_files+intial_csv)

for file in os.listdir(initial_scraped_files):

	if(file.endswith("csv") and file!=intial_csv):
		print(file)
		df  = pd.read_csv(initial_scraped_files+file)
		final_df = pd.concat([df , final_df], ignore_index=True)

df =final_df.copy()


df = df[df['state'].apply(getValidState)]




df['cat'] = df['category'].apply(get_cat)
df['sub_cat'] = df['category'].apply(get_subcat)
    



df['rewards_url'] = df['urls'].apply(get_reward_url)



df['project_url'] = df['urls'].apply(get_project_url)




df['creator_url'] = df['creator'].apply(get_creator_name)


df = df[Initial_cols]


df.rename(columns = {"country_displayable_name":"location_country", "state":"status", "cat":"category", "sub_cat":"sub_category"}, inplace=True)
df = df[~df['name'].duplicated()]

df['launched_at'] = df['launched_at'].apply(get_launched_at_int)
df.sort_values(by='launched_at' , inplace=True)
df.reset_index(drop=True, inplace=True)


df['launched_at'] = pd.to_datetime(df['launched_at'].apply(get_date_format))
df['created_at'] = pd.to_datetime(df['created_at'].apply(get_date_format))
df['deadline'] = pd.to_datetime(df['deadline'].apply(get_date_format))
df['state_changed_at'] = pd.to_datetime(df['state_changed_at'].apply(get_date_format))

print("Shape of the scrapped dataset")
print(df.shape)
print("Distribution of the dataset")
print(df.groupby(df['launched_at'].map(lambda x: int(str(x).split("-")[0]))).count())
print("Null values ")
print(df.isnull().mean())

print("Saving the csv file into {}".format(intial_scraped_preprocessed_file))
try:
    os.remove(intial_scraped_preprocessed_file)
    print("removing already present csv file")
except:
    pass
    

df.to_csv(intial_scraped_preprocessed_file)