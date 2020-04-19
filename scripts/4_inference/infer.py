import os
import sys
curr_path = os.getcwd() 
package_path = (os.path.abspath(os.path.join(curr_path, os.pardir))).replace('\\', '/')+'/'
sys.path.insert(1, package_path)
from config.config import *
from processing_scripts.model_preprocessing import *







model , binarizer , encoder = load_estimators(model_path,binarizer_path , encoder_path)

def get_input_data():
    name="Hamsterdam"
    goal= 6000
    rewards = str(['US$ 5', 'US$ 10', 'US$ 18', 'US$ 20', 'US$ 35', 'US$ 50', 'US$ 100', 'US$ 250', 'US$ 500', 'US$ 500', 'US$ 1,000', 'US$ 8', 'US$ 15'])
    blurb="The Best Dam Game Ever (for 2 to 4 Players"
    category = "games"
    sub_category = "tabletop games"
    currency = "USD"
    country = "the United States"
    launched_at = "2019-10-22"
    deadline = "2019-11-21"
    delivery = "2019-03-01"

    return launched_at , deadline , goal , sub_category , category ,country ,currency , blurb  , rewards


def transform_helmert(df , cols , encoder):
    df_temp = encoder.transform(df[cols])
    df = pd.concat([df , df_temp] , axis=1)
    df_resp = df.copy()
    df_resp.drop(cols , axis=1 , inplace=True)
    return df_resp





launched_at , deadline , goal , sub_category , category ,country, currency , blurb  , rewards = get_input_data()


reward_mean  = getMean(rewards)
reward_median = getMedian(rewards)
reward_sd = getSD(rewards)
reward_variance = getVariance(rewards)
reward_max = getMAX(rewards)
reward_min = getMIN(rewards)
reward_num = getNUM(rewards)
blurb_length =get_blurb_length(blurb)
launched_at = pd.to_datetime(launched_at)
deadline	= pd.to_datetime(deadline)
deadline_year= pd.to_datetime(deadline).year
deadline_month = pd.to_datetime(deadline).month
launched_year = pd.to_datetime(launched_at).year
launch_month = pd.to_datetime(launched_at).month
days_to_deadline = (deadline - launched_at).days


pred_df = {
    "days_to_deadline":[days_to_deadline], 
    "goal":[goal], 
    "blurb_length":[blurb_length],
    "rewards_mean":[reward_mean], 
    "rewards_median":[reward_median], 
    "rewards_variance":[reward_variance], 
    "rewards_SD":[reward_sd], 
    "rewards_MIN":[reward_min], 
    "rewards_MAX":[reward_max], 
    "rewards_NUM":[reward_num], 
    "launch_month":[launch_month],  
    "deadline_month":[deadline_month],     
     "location_country":[country],
     "currency":[currency], 
    "category":[category], 
    "sub_category":[sub_category],    
}


df_pred = pd.DataFrame.from_dict(pred_df )
df_pred_hel = transform_helmert(df_pred , categ_cols , encoder)

print(model.predict(df_pred_hel))