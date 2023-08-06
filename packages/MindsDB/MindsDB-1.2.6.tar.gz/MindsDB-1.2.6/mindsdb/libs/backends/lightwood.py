from mindsdb.libs.constants.mindsdb import *

import lightwood


class LightwoodBackend():

    def __init__(self, transaction):
        self.transaction = transaction
        self.predictor = None

    def _create_lightwood_config(self):
        config = {}

        #config['name'] = 'lightwood_predictor_' + self.transaction.lmd['name']

        config['input_features'] = []
        config['output_features'] = []

        for col_name in self.transaction.input_data.columns:
            if col_name in self.transaction.lmd['malformed_columns']['names']:
                continue

            col_stats = self.transaction.lmd['column_stats'][col_name]
            data_subtype = col_stats['data_subtype']
            data_type = col_stats['data_type']

            lightwood_data_type = None

            if data_type in (DATA_TYPES.NUMERIC):
                lightwood_data_type = 'numeric'
                try:
                    self.transaction.input_data.data_frame[col_name] = self.transaction.input_data.train_df[col_name].apply(int)
                except:
                    self.transaction.input_data.data_frame[col_name].apply(lambda x: float(x.replace(',','.')))

            elif data_type in (DATA_TYPES.CATEGORICAL):
                lightwood_data_type = 'categorical'

            elif data_type in (DATA_TYPES.DATE):
                lightwood_data_type = 'datetime'

            elif data_subtype in (DATA_SUBTYPES.IMAGE):
                lightwood_data_type = 'image'

            elif data_subtype in (DATA_SUBTYPES.TEXT):
                lightwood_data_type = 'text'

            # @TODO Handle lightwood's time_series data type

            else:
                self.transaction.log.error(f'The lightwood model backend is unable to handle data of type {data_type} and subtype {data_subtype} !')
                raise Exception('Failed to build data definition for Lightwood model backend')

            if col_name not in self.transaction.lmd['predict_columns']:
                config['input_features'].append({
                    'name': col_name,
                    'type': lightwood_data_type
                })
            else:
                config['output_features'].append({
                    'name': col_name,
                    'type': lightwood_data_type
                })

        return config

    def train(self):
        lightwood_config = self._create_lightwood_config()
        self.predictor = lightwood.Predictor(lightwood_config)
        self.predictor.learn(from_data=self.transaction.input_data.train_df, test_data=self.transaction.input_data.test_df)
        print(self.predictor.train_accuracy)

    def predict(self, mode='predict', ignore_columns=[]):
        if mode == 'predict':
            # Doing it here since currently data cleanup is included in this, in the future separate data cleanup
            lightwood_config = self._create_lightwood_config()
            df = self.transaction.input_data.data_frame
        if mode == 'validation':
            df = self.transaction.input_data.validation_df

        # not the most efficient but least prone to bug and should be fast enough
        if len(ignore_columns > 0):
            run_df = df.copy(deep=True)
            for col_name in ignore_columns:
                run_df[col_name] = [None] * len(run_df[col_name])
        else:
            run_df = df

        self.predictor.predict(from_data=run_df)
        pass
