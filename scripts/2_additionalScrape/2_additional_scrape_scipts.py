import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.add_scrape_processing import *



if __name__=="__main__":
	intial_scraped_preprocessed_file = "C:/Users/saima/Desktop/kickstarter/Final/data/1_InitialScrape-final_data/intialScrape_final.csv"
	df_new = {"name":[] , "rewards":[], "delivery":[] , "creator_created":[], "creator_backed":[]}
	log = []
	df  = pd.read_csv(intial_scraped_preprocessed_file)
	num = len(df)
	for i in range(num):
		if( (i%==0 or i==num) and (i!=0)):

			print("saving {}th row".format(i))
			csv_path = "C:/Users/saima/Desktop/kickstarter/Final/data/2_AdditionalScrape_source_data/kickscraper"+str(i)+".csv"
			log_path =  "C:/Users/saima/Desktop/kickstarter/Final/data/2_AdditionalScrape_source_data/kickscraper"+str(i)+"_log.txt"
			save_as_csv(csv_path,df_new)
			save_log(log_path, log)
			send_to_dropbox( csv_path, "/dataset/kickscraper"+str(i)+".csv")
			send_to_dropbox(log_path , "/dataset/kickscraper"+str(i)+"_log.txt")
			df_new = {"name":[] , "rewards":[], "delivery":[] , "creator_created":[], "creator_backed":[]}
			log=[]
		print("currently Processing {}".format(str(i)))
		df_new["name"].append(df["name"][i])
		reward_raw = getRewardRaw(df,i)
		df_new["rewards"].append(getMoney(reward_raw, i))
		df_new["delivery"].append(get_date_of_delivery(reward_raw, i))
		sk= get_CreatorCount(df , i)
		df_new["creator_created"].append(sk["created"]) 
		df_new["creator_backed"].append(sk["backed"])



