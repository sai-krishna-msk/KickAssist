from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import wget
import zipfile

import os
import re
import numpy as np
import pandas as pd
from datetime import datetime
import joblib
from xgboost import XGBClassifier
import  category_encoders as ce
import operator
from sklearn.preprocessing import LabelBinarizer



import json
import requests 
import time
import dropbox
from random import choice


import warnings
warnings.simplefilter("ignore")



#Pass on the Drop Box API key below
ACCESS_TOKEN = ""

train_years =[2016, 2017, 2018]

valid_years = [2019]

Initial_cols=['backers_count', 'blurb', 'converted_pledged_amount', 'country_displayable_name', 'created_at', 'launched_at',
     'currency', 'deadline', 'disable_communication', 'fx_rate', 'goal',  'is_starrable', 
     'name', 'pledged', 'slug', 'spotlight', 'staff_pick', 'state', 'state_changed_at', 'static_usd_rate', 'usd_pledged' ,
      'cat','sub_cat', 'project_url', 'rewards_url', 'creator_url' ]

model_cols = ['launched_at', 'status', 'days_to_deadline', 'goal',
       'sub_category', 'category', 'blurb_length', 'location_country',  'rewards_mean', 'rewards_median',
       'rewards_variance', 'rewards_SD', 'rewards_MIN', 'rewards_MAX' , 'rewards_NUM', 'currency','deadline']


categ_cols = ['location_country' , 'currency' , 'category', 'sub_category']

initial_scraped_files = "../../data/scripts/1_IntialScrape-source_data/"

intial_scraped_preprocessed_file = "../../data/scripts/1_InitialScrape-final_data/intialScrape_final.csv"



raw_scrapped_path= "../../data/scripts/2_AdditionalScrape_source_data/"

raw_scrapped_preprocessed_path = "../../data/scripts/2_AdditionalScrape_final_data/Final_data_model.csv"

alt = "../../data/scripts/2_AdditionalScrape_final_data/alt.csv"

Train_path_final = "../../data/scripts/3_training_data/train.csv"

model_path = "../estimators/model.sav"

binarizer_path ="../estimators/binarizer.sav"

encoder_path = "../estimators/encoder.sav"
