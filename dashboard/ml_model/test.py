from model import *


pred_dic = {
    
 "launched_at":'2019-11-06', 
    "deadline":"2019-12-06", 
    "goal":1000, 
    "sub_category":"comic books", 
    "category":"comics",
    "currency":"GBP", 
    "location_country":"the United Kingdom",
    "blurb":"A multimedia journalistic trip to a culture different than my own in order to explore & document a radically different way of life.",
    "rewards":[10,20, 50, 250, 500 , 1000 ] 
    
}

model_oh = joblib.load('estimators/model_oh.sav')
model_hel = joblib.load('estimators/model_hel.sav')
encoder_oh = joblib.load('estimators/encoder_oh.sav')
encoder_hel = joblib.load('estimators/encoder_hel.sav')
encoder_label = joblib.load('estimators/encoder_label.sav')


obj  = KickModel(model_oh , model_hel , encoder_oh , encoder_hel , encoder_label)

obj.load_data(pred_dic)
obj.pred()
print(obj.pred_hel_intr)

