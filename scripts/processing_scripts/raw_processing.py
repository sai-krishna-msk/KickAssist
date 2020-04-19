import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
###################################processing-1############################################################


# Filter only the rows which are either Sucessfull or have failed
def getValidState(x):
    try:
        if(x=='successful' or x=='failed'):
            return True
        else:
            return False
    except:
        return False

#Getting Category and Sub Category

def get_cat(x):
    dic = eval(x)
    cat = dic['slug'].split("/")
    return cat[0]

def get_subcat(x):
    try:
        dic = eval(x)
        cat = dic['slug'].split("/")
        return cat[1]
    except:
        return "sub_"+str(cat[0])


#Get Reward URL
def get_reward_url(x):
    urls = eval(x)
    return urls['web']['rewards']

# Get project url
def get_project_url(x):
    urls = eval(x)
    return urls['web']['project']

#Get creator name
def get_creator_name(x):
    import re
    result = re.search('"id":(.*),"name"', x)
    pro_id = result.group(1)
    base_url = "https://www.kickstarter.com/profile/"
    return base_url+str(pro_id)


#Sort df based on launched date 

def get_launched_at_int(x):
    ts = int(x)
    return ts



# Get Proper Date Format
def get_date_format(x):
    ts = int(x)
    return (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

###################################processing-1 ends############################################################
