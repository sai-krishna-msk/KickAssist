import numpy as np
import pandas as pd
import eli5
import joblib


class KickModel:

    def __init__(self, model_oh, model_hel, encoder_oh, encoder_hel, encoder_label):
        self.model_oh = model_oh
        self.model_hel = model_hel
        self.encoder_oh = encoder_oh
        self.encoder_hel = encoder_hel
        self.encoder_label = encoder_label

        self.target_encoding_cols = ['location_country',
                                     'currency', 'category', 'sub_category']
        self.interpret_cols = ['blurb_length', 'goal', 'rewards_variance', 'rewards_median', 'rewards_SD',
                               'rewards_MIN', 'rewards_MAX', 'rewards_NUM', 'days_to_deadline', 'launch_month', 'deadline_month']

        self.df_pred_oh = None
        self.df_pred_hel = None
        self.hel_pred = None
        self.oh_pred = None

    def _getMean(self, lis):
        return np.mean(lis)

    def _getMedian(self, lis):
        return np.median(lis)

    def _getVariance(self, lis):
        return np.var(lis)

    def _getSD(self, lis):
        return np.std(lis)

    def _getMIN(self, lis):
        return np.min(lis)

    def _getMAX(self, lis):
        return np.max(lis)

    def _getNUM(self, lis):
        return len(lis)

    def _get_blurb_length(self, blurb):
        return len(blurb)

    def _transform_onehot(self):
        try:
            df_temp = pd.DataFrame(self.encoder_oh.transform(self.df_pred[self.target_encoding_cols]), columns=[
                                   x for sublist in self.encoder_oh.categories_ for x in sublist])
            self.df_pred_oh = pd.concat([self.df_pred, df_temp], axis=1)
            self.df_pred_oh.drop(self.target_encoding_cols,
                                 axis=1, inplace=True)

        except Exception as e:
            raise Exception(f"Following error during One Hot Encoding: {e}")

    def _transform_helmert(self):

        try:
            df_temp = pd.DataFrame(self.encoder_hel.transform(
                self.df_pred[self.target_encoding_cols]))
            self.df_pred_hel = pd.concat([self.df_pred, df_temp], axis=1)
            self.df_pred_hel.drop(
                self.target_encoding_cols, axis=1, inplace=True)

        except Exception as e:
            raise Exception(f"Following error during Helmert Encoding: {e}")

    def load_data(self, pred_dict):

        pred_df = {
            "days_to_deadline": [],
            "goal": [],
            "blurb_length": [],
            "rewards_mean": [],
            "rewards_median": [],
            "rewards_variance": [],
            "rewards_SD": [],
            "rewards_MIN": [],
            "rewards_MAX": [],
            "rewards_NUM": [],
            "launch_year": [],
            "launch_month": [],
            "deadline_year": [],
            "deadline_month": [],
            "location_country": [],
            "currency": [],
            "category": [],
            "sub_category": []}

        pred_df["rewards_mean"].append(self._getMean(pred_dict['rewards']))
        pred_df["rewards_median"].append(self._getMedian(pred_dict['rewards']))
        pred_df["rewards_variance"].append(
            self._getVariance(pred_dict['rewards']))
        pred_df["rewards_SD"].append(self._getSD(pred_dict['rewards']))
        pred_df["rewards_MIN"].append(self._getMIN(pred_dict['rewards']))
        pred_df["rewards_MAX"].append(self._getMAX(pred_dict['rewards']))
        pred_df["rewards_NUM"].append(self._getNUM(pred_dict['rewards']))
        pred_df['launch_year'].append(
            pd.to_datetime(pred_dict['launched_at']).year)
        pred_df['launch_month'].append(
            pd.to_datetime(pred_dict['launched_at']).month)
        pred_df['deadline_year'].append(
            pd.to_datetime(pred_dict['deadline']).year)

        pred_df['deadline_month'].append(
            pd.to_datetime(pred_dict['deadline']).month)
        pred_df['days_to_deadline'].append((pd.to_datetime(
            pred_dict['deadline']) - pd.to_datetime(pred_dict['launched_at'])).days)
        pred_df['blurb_length'].append(
            self._get_blurb_length(pred_dict['blurb']))
        pred_df['goal'].append(pred_dict['goal'])
        pred_df['category'].append(pred_dict['category'])
        pred_df['sub_category'].append(pred_dict['sub_category'])
        pred_df['currency'].append(pred_dict['currency'])
        pred_df['location_country'].append(pred_dict['location_country'])
        self.df_pred = pd.DataFrame.from_dict(pred_df)

    def _prepData(self):
        self._transform_onehot()
        self._transform_helmert()

    def _filter_func(self, x, s):
        return x in self.interpret_cols

    def pred(self):
        self._prepData()
        self.pred_oh_intr = eli5.format_as_dataframe(eli5.explain_prediction_xgboost(
            self.model_oh.get_booster(), self.df_pred_oh.iloc[0], feature_filter=self._filter_func))
        self.pred_hel_intr = eli5.format_as_dataframe(eli5.explain_prediction_xgboost(
            self.model_hel.get_booster(), self.df_pred_hel.iloc[0], feature_filter=self._filter_func))

        self.pred_oh = self.model_oh.predict_proba(self.df_pred_oh)
        self.pred_hel = self.model_hel.predict_proba(self.df_pred_hel)
