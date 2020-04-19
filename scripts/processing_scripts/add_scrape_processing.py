import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *

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
    access_token=ACCESS_TOKEN
    dbx = dropbox.Dropbox(access_token)
    f = open(src, 'rb')
    dbx.files_upload(f.read(), dest)


###################################scraping-2-ends############################################################
