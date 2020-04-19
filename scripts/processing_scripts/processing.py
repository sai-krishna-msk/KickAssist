
import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *


##############################################Scrape-1###################################################
def contains(text , subtext):
    if subtext in text:
        return True
    return False


def get_scrape_url(url):
    encoding = "html.parser"
    resp = requests.get(url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, from_encoding=encoding)

    for link in soup.find_all('a', href=True):
        scrape_url = str(link['href'])
        if(contains(scrape_url , "s3.amazonaws.com") and contains(scrape_url , ".zip")):
            break
    file_name = scrape_url.split("/Kickstarter/")[1]
    return scrape_url, file_name

def download(scrape_url , output_directory):
    try:
        wget.download(scrape_url, out=output_directory)
    except:
        raise Exception("Failed in downloading the data file")
    return output_directory


def unzip_data(input_file_path , output_directory):
    try:
        with zipfile.ZipFile(input_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_directory)
    except Exception as e:
        raise Exception("Failed to unzip the data folder !+....{}",format(e))
    os.remove(input_file_path)
    return True

###################################scrape-1ends############################################################


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
df['launched_at'] = df['launched_at'].apply(get_launched_at_int)
df.sort_values(by='launched_at' , inplace=True)
df.reset_index(drop=True, inplace=True)


# Get Proper Date Format
def get_date_format(x):
    ts = int(x)
    return (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

###################################processing-1 ends############################################################











###################################scrape-2############################################################
def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content , 'lxml')
#     return soup
    
    return {'https': choice(list(map(lambda x: x[0]+':'+x[1] ,  
                                     
                                     list(zip(map( lambda x: x.text , soup.findAll('td')[::8]) , map( lambda x: x.text , soup.findAll('td')[1::8])))
                                     
                                    )))}
def proxy_request(request_type , url, **kwargs):
    while 1:
        try:
            proxy = get_proxy()
            r = requests.request(request_type , url , proxies = proxy , timeout=5 , **kwargs)
            break
        except Exception as e:
            pass
    return r



def scarpe_data(url):
    cont = proxy_request('get' , url)
    
    return cont.content

def getRewardRaw(df , i):
    url_string = df["rewards_url"][i]
    html = scarpe_data(url_string)
    return html


def getMoney(html , i):
    rewards = []
    html_cont = BeautifulSoup(html, 'html.parser')
    try:
        for each in html_cont.findAll("span", {"class":"money"}):
            rewards.append(each.text)
    except:
        log.append("There is an error while getting date of delivery in {}".format(i))
        return 'null'
  
  
    return rewards


def get_date_of_delivery(html , i):
    date = ''
    html_cont = BeautifulSoup(html, 'html.parser')
    try:
        for each in html_cont.find("span", {"class":"pledge__detail-info"}):
            date = each["datetime"]
    except:
        log.append("There is an error while getting date of delivery in {}".format(i))
    
    return date



def get_CreatorCount(df , i):
    url = df["creator_url"][i]
    resp = {"created":"null" , "backed":"null" }
    cont = re.get(url)
    content = BeautifulSoup(cont.content, "html.parser")
    try:
        s = content.find("span", {"class":"backed"})
        result = re.search('d (.*) p', s.text)
        resp["backed"] = result.group(1)
    except:
        pass
    try:
        for each in content.find("a", {"class":"nav--subnav__item__link nav--subnav__item__link--gray js-created-link"}):
            if("Created" in str(each)):
                pass
            else:
                sk = BeautifulSoup(str(each) ,  features="lxml")
                for c,e in enumerate(sk.find("span")):
                    
                    if(c==0):
                      resp["created"]= str(e).strip()
    except:
        pass
    return resp
def save_as_csv(path, df):
    df_pandas = pd.DataFrame(df)
    df_pandas.to_csv(path)
    return None 

def save_log(path, log):
    with open(path , 'w') as f:
        for item in log:
            f.write("%s\n" % item)

    return None



def send_to_dropbox(src ,dest):
    access_token="GsAneWDNftAAAAAAAAAAlb1E8KDJp1WmjMHtd3QK8oTSDGT2M5MdP4-cY6hMdPVq"
    dbx = dropbox.Dropbox(access_token)
    f = open(src, 'rb')
    dbx.files_upload(f.read(), dest)


###################################scraping-2-ends############################################################

###################################processing-2############################################################


def getMean(x):
  

  if(x=='[]'):
    return np.nan
  else:
    
    lis=[]
    res = x.strip('][').split(', ') 
    
    for each in res:
        lis.append(int(re.sub('[^0-9]+', '', each)))

    return np.array(lis).mean()

def getMedian(x):
    if(x=='[]'):
        return np.nan
    else:
        lis=[]
        res = x.strip('][').split(', ') 
        for each in res:
            lis.append(int(re.sub('[^0-9]+', '', each)))
            
    return np.median(lis)

def getVariance(x):
    if(x=='[]'):
        return np.nan
    
    else:
        lis=[]
        res = x.strip('][').split(', ') 
        for each in res:
            lis.append(int(re.sub('[^0-9]+', '', each)))
    return np.array(lis).var()


def getSD(x):
    if(x=='[]'):
        return np.nan
    
    else:
        lis=[]
        res = x.strip('][').split(', ') 
        for each in res:
            lis.append(int(re.sub('[^0-9]+', '', each)))
    return np.std(lis)

def getMIN(x):
    if(x=='[]'):
        return np.nan
    
    else:
        lis=[]
        res = x.strip('][').split(', ') 
        for each in res:
            lis.append(int(re.sub('[^0-9]+', '', each)))
    return min(lis)


def getMAX(x):
    if(x=='[]'):
        return np.nan
    
    else:
        lis=[]
        res = x.strip('][').split(', ') 
        for each in res:
            lis.append(int(re.sub('[^0-9]+', '', each)))
    return max(lis)




def getNUM(x):
    if(x=='[]'):
        return np.nan
    
    else:
        lis=[]
        res = x.strip('][').split(', ') 
   
    return len(res)

def get_blurb_length(x):
	try:
		return len(x)
	except:
		return np.nan

def get_delivery_binary(x):
    
    if(pd.isna(x)):
        return -1
    elif(x<0):
        return 0
    else:
        return x
############################2-preprocessing-ends##########################################################


###################################inference############################################################


# test_dic ={
#     "days_to_delivery":[], 
#     "goal":[], 
#     "blurb_length":[], 
#     "rewards_mean":[], 
#     "rewards_median":[], 
#     "rewards_variance":[], 
#     "rewards_SD":[], 
#     "rewards_MIN":[], 
#     "rewards_MAX":[], 
#     "rewards_NUM":[], 
#     "launch_month":[], 
#     "launched_year":[], 
#     "days_to_deadline":[]

    
# }

test_dic ={
    "days_to_delivery":None, 
    "goal":None, 
    "blurb_length":None, 
    "rewards_mean":None, 
    "rewards_median":None, 
    "rewards_variance":None, 
    "rewards_SD":None, 
    "rewards_MIN":None, 
    "rewards_MAX":None, 
    "rewards_NUM":None, 
    "launch_month":None, 
    "launched_year":None, 
    "days_to_deadline":None
    
}


def get_one_hot(category , sub_category , currency , location_country , encoder):
  cat = [1 if i==category else 0 for i in encoder.categories_[0]]

  sub = [1 if i==sub_category else 0 for i in encoder.categories_[1]]

  curr = [1 if i==currency else 0 for i in encoder.categories_[2]]

  loc = [1 if i==location_country else 0 for i in encoder.categories_[3]]


  return cat + sub + curr + loc
###################################inference-ends############################################################
