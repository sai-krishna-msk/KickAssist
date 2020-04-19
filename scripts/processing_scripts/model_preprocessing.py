import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
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

def pre_proc(df):
    df= df.dropna(axis=0, subset=["rewards_MIN"])
    df= df.dropna(axis=0, subset=["blurb_length"])
    df.sort_values("launched_at" , inplace=True)
    df = df.reset_index(drop=True)

    df["launch_year"]  = pd.to_datetime(df["launched_at"]).dt.year
    df['launch_month'] = pd.to_datetime(df['launched_at']).dt.month
    df['deadline_month'] = pd.to_datetime(df['deadline']).dt.month
    df.sort_values("launched_at" , inplace=True)
    df.drop(['launched_at'] ,axis=1 , inplace=True)
    df.reset_index(inplace=True)
    df.drop('index', inplace=True , axis=1)
    
    binarizer= LabelBinarizer()
    df["status"] = binarizer.fit_transform(df["status"])
    
    
    return df , binarizer

def helmert_categ(df_train, onehot_cols):
    encoder = ce.HelmertEncoder(cols = onehot_cols , drop_invariant=True )
    dfh = encoder.fit_transform(df_train[onehot_cols])
    df_train = pd.concat([df_train , dfh], axis=1)
    df_train.drop(onehot_cols , axis=1 , inplace=True)
    
    return df_train , encoder

def get_model_data(df , train_years ):
    
    df_train = df[df['launch_year'].apply(lambda x: True if x in train_years else False)]
    
    return df_train


##############################Train################################################################
def XG_train(X_train,  y_train):
    
    XG= XGBClassifier(n_estimators=150, random_state=9)
    XG.fit(X_train, y_train)
   
    return XG

def XG_score(X_train , y_train , X_valid , y_valid):
    XG =XGBClassifier(n_estimators=150 , random_state=9)
    XG.fit(X_train , y_train)
    return XG.score(X_valid , y_valid)



###################################inference############################################################
def load_estimators(model_path,binarizer_path , encoder_path):
    model =joblib.load(model_path)
    binarizer = joblib.load(binarizer_path)
    encoder = joblib.load(encoder_path)

    return model , binarizer, encoder

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
