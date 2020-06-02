<img src="images/kickassist.jpg">


# **Contents**

1. **Introduction/Context**
2. **Objective**
3. **Domain Knowledge**
4. **Data Source**
5. **Framing into ML Problem**
6. **Methodology and results**
7. **Limitations**

<hr>

# Introduction/Context

KickStarter is a crowd funding platform for ideas and projects of diverse categories such as films, games, and music to art, design, and technology.

Individuals/Entrepreneurs  with ideas or products start a campaign by creating a project on the platform explaining what the idea is about

- Creator must specify a date and goal(amount) when creating a project which are not flexible

- Creators are allowed to give rewards to Backers(AKA people who donated for the project) of the project based on the amount these rewards can be anything depending on the project mostly it's the product itself which is being donated for(if it's a course then early access to a course or if it's some tech product them limited edition of the product etc.)

- If the project for some reason is not able to reach the goal amount by the given date then the money collected up until that point is returned back to the backers and the project gets nothing( **all-or-nothing funding model**)

- So it is more like people bringing the project to life which makes it interesting

<hr>

# Objective

As discussed above there are a few decisions which creator needs to make when starting the campaign, Which include the following

- Deciding when to start the campaign(Launch Date)

- When to set the deadline

- Goal Amount

- Deciding the right amount for the rewards

Since it is **all-or-nothing funding model** decisions creator takes with the above variables play a key role in deciding the success of the project

**Therefore our objective is to Assist the creator of the campaign in deciding what would be the optimal values for the above 4 features which would maximize the probability of a successful campaign based on certain characteristics of the product**

<hr>

# Domain Knowledge

Condensing most of the content about what goes into a successful campaign can be summarized by the following 

1. Having a well polished landing page with videos and images
2. Interaction with donors(through comment section and others)
3. Marketing and networking as a whole
4. Well planned rewards
5. Feasible duration for the given goal
6. Delivering the rewards without delay

<hr>

# Data Source

A Web Crawler Platform named [Web Robots](https://webrobots.io/) has a few free data projects one of them happens to be kickstarter data, which is scrapped every month of the platform.

It provides a bunch of csv files with data loaded as dictionaries(JSON), Following are the features which can be extracted from the source

- Status(Success or failed)
- Category and Sub Category of the project
- lunch and deadline date
- Author and creator information
- Country of origin and currency to be used for transaction

and a few other

<hr>

# Framing into ML Problem

- Based on our objective and our data source, there are two kinds of features(variables)

-  Variables Which are related to our product itself and are fixed, can not be changed for the purpose of increasing the chances of success, variables like category, sub category etc. These variables can not be changed after we decide what our campaign is going to be because they are about the product of the campaign itself, For naming reasons lets call them fixed variables.

-  One's which are to be decided strategically  and which can(should) be altered if doing so increases our probability of being successfully funded, this type of variables include rewards, goal, deadline , launch date etc., Let's call them flexible variables

- As the target feature(success or failed) is a categorical feature, it will be a classification problem

- **Since our objective is not to make predictions about the campaign's success based on the features rather suggesting the optimal features for maximum chances for success, this slight variation in our problem statement demands our Model to be interpretable**

- **Requirement for Interpretability does not only effect our choice of ML model but it essentially drives our Machine Learning pipeline from preprocessing to model deployment, It mainly effects our feature engineering process, where in we are bound not to make any transformations(like dimensionality reduction) to our variables, Therefore accuracy/performance is the price to pay for interpretability **

- Model would be served to the end user as an **Interactive dashboard**, Where the creators can tune/adjust both their fixed, flexible variables and visualize not only the probability of success but also, How has each of the flexible variables effected the probability this way creators can adjust those variable's values to the closest plausible value to increase the chances for a successful campaign.

- A model with 80% accuracy(given balanced dataset) seems to be an acceptable , as it e will be using the model for interpretation not the predictions themselves

<hr>

# Methodology and results

*All the code and a clear procedure is provided* [*here*](https://github.com/sai-krishna-msk/KickAssist/tree/master/notebooks)

- Extracting the data  from the source mentioned above

- Exploring the variables and getting the feel of the data.
 
- Performed basic cleaning like removed null values(beyond a threshold) and duplicate values.

- Performed  basic preprocessing(Label Encoding, OneHot Encoding) and modeling

-   As identified in the Introduction,  features present in the data source are not suffice to full fill our objective because  as identified in the  domain knowledge section,  rewards is an important feature and  there is no feature indicating any measure of rewards in the dataset and section also suggest marketing and networking increases the chances of success,  since we do not have any direct way of extracting that information for each campaign, therefore Scraping is performed on the kickstarter website and following are the features being scrapped from each campaign(200000 total)

   - Rewards

   - Number of Campaigns the Creator already had

   - Number of Campaigns the creator has already funded

   - When would the rewards be delivered

- Scrapped data and source data are merged

- EDA along with Statical tests(t-test, ANOVA) are performed to validate various assumptions and questions,One of the important findings in this process  is data prior to 3-4 years to the current date can be considered  stale as it does not have similar patterns, It not only  helps us reduce our training size by a large factor but also when updating the model each year it need not be trained on aggregated data of all the previous years.
 
- As discussed previously due to the interpretability  constraints, Transformations such as dimensionality reduction(PCA) and polynomial interactions can not  be performed,  but clear distinction has been made between our features as fixed and flexible,   Fixed variables are not required to be  interpretable according to our business objective therefore, Feature encoding is used on categorical variables of flexible type, Helmert is used as 
 our categorical vairbale have a natural sense of order to them which is ideal case for helmert encoding
![img](https://github.com/sai-krishna-msk/KickAssist/blob/master/images//model.PNG?raw=true)


- At this stage modeling is performed, as the relationships are clearly not linear as observed in EDA, Random Forest and XGBoost are trained  and XGBoost is chosen as it produces highest accuracy of 86% and is compatible with the tool being used for interpretation


-   ELI5 package is used for interpreting the XGBoost Model, Which makes use of LIME algorithm, This implementation suits our objective as it generates feature contribution for each instance predicted, Allowing creators/users to experiment with various values of 
variables 
![img](https://github.com/sai-krishna-msk/KickAssist/blob/master/images/eli5.png?raw=true)


- Model(XGBoost) and ELI5 tool are  wrapped into an api so that it can serve dashboard built using plotly, App is  hosted on heroku for creators to validate and tune their decisions to maximize the probability of success, Dashboard can we accessed [here](https://kick-assist.herokuapp.com/)

![img](https://github.com/sai-krishna-msk/KickAssist/blob/master/images/dashboard.png?raw=true)

<hr>

# Limitations

-  Content such as videos and images used to present the project compel the donors to some degree and it's signal is not being taken into consideration
-  Experience of the person hosting the project (how many backed and how many pledged) is not being taken into consideration which gives us an insight into, how well the creator can market is product 
-  Utility and relevance of the overall product is not being quantified 

<hr>

# Reproducing the results

*I will be walking through each of the sub repository's*

**Note**

**Data is not present in the repository as it exceeds the limit of 100mb for each file on Github, it can be downloaded** [**here**](https://bit.ly/2XHwxAx) **and placed in the outermost directory of the project(along with API, Dashboard etc.)**

**Before running any code install all required packages present in requirements.txt**

```
pip install -r requirements.txt
```

## Notebook

It contains all the code required to reproduce the process from data extraction to model interpretation divided into different notebooks in the order listed in the methodology section

## Scripts

- As already mentioned data source updates the data every month so to keep our model from getting stale we need to retrain it every month, which is not efficient to carry out in Jupiter notebooks as the pipeline and procedure is determined and is no more experimental

- This sub repo consists of code to carry out the entire procedure from downloading the source data(through scraping), scraping our key features directly and train our model  and further save it

**Note** If the project is intended to run in future then variables in config file have to be altered accordingly

## Scraping

- As scraping our new features takes a lot of time, the code is written to run on heroku and files would be saved to dropboox.

- We would be having two types files saved in dropbox

- - CSV for dataset
  - Log.txt for viewing the rows which for some reason could not be scraped

- Before running DropBox api key has to updated in config file

Models and encoders are saved in estimators folder

## API

A simple Flask-API to serve the predictions and feature importance's for the corresponding prediction

## Dashboard

Contains code for Dash(plotly) dashboard which is the final product

Dashboard itself can be accessed [here](https://kick-assist.herokuapp.com/)
