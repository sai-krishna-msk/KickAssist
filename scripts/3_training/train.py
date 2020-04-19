import os
import sys
curr_path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(curr_path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.model_preprocessing import *






df_full= pd.read_csv(Train_path_final)

df_full.drop(['Unnamed: 0'] , axis=1 , inplace=True)
df_train= get_model_data(df_full , train_years)
df_valid = get_model_data(df_full , valid_years)





X_full , y_full = df_full.drop(["status","launch_year","deadline"], axis=1) , df_full['status']
X_train , y_train = df_train.drop(["status","launch_year","deadline"] , axis=1) , df_train['status']
X_valid , y_valid = df_valid.drop(["status","launch_year","deadline"] , axis=1) , df_valid['status']


print("Training.....")
scores  = XG_score(X_train ,y_train ,X_valid , y_valid)
print("Accuracy of the model on validation set-2019")
print(scores)

print("Final Training Model.....")
model = XG_train(X_full , y_full)

try:
    os.remove(model_path)
    print("removed the model file")

except:
    pass
    
print("saving the model")
joblib.dump(model, model_path)

