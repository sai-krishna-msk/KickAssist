import os
import sys
path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.model_preprocessing import *





df_raw = pd.read_csv(alt)
# df_raw = pd.read_csv(raw_scrapped_preprocessed_path)
df = df_raw.copy()
df = df[model_cols]
df_proc , binarizer  = pre_proc(df)
X_train_raw = get_model_data(df_proc , train_years+valid_years)
X_train_hel ,helmert_encoder  = helmert_categ(X_train_raw, categ_cols)


try:
    os.remove(Train_path_final)
    print("removed training data")
    os.remove(binarizer_path)
    print("removed binarizer")
    os.remove(encoder_path)
    print("removed encoder")

except  FileNotFoundError:
    pass 
except Exception as e:
    (f"Error in saving preprocessing files: {e}")

print("saving the train and test files")
X_train_hel.to_csv(Train_path_final)

print("saving binarizer")
joblib.dump(binarizer, binarizer_path)


print("saving encoder")
joblib.dump(helmert_encoder,  encoder_path)
