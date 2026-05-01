from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging
import os
import pandas as pd

from .log import log_time, setup_log
from config import service

setup_log()
CONFIG = service.get_config()
LOG = logging.getLogger()


# ============================================================================
class MongoDatabase:

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------------
    @log_time
    def get_client(self):
        uri = (
            os.getenv('MONGO_PATH') 
            + ':' 
            + os.getenv('DB_PASSWORD') 
            + os.getenv('MONGO_CLUSTER')
        )
        # Create a new client and connect to the server
        self.client = MongoClient(host=uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command(command='ping')
            return self.client
        except Exception as e:
            raise Exception
    
    # ------------------------------------------------------------------------
    @log_time   
    def get_my_db(self) -> 'MongoDatabase':
        my_db = self.client['HEALTH']
        self.garmin = my_db['GARMIN_DATA']
        self.current_data = pd.DataFrame(data=list(self.garmin.find()))
        self.max_date  = pd.to_datetime(self.current_data['DATE']).max()
        LOG.info(msg=f'Max date in DB: {self.max_date}')
        return self
    
    # ------------------------------------------------------------------------
    @log_time
    def update_db(self, my_df) -> None:
        my_df_test = pd.merge(
            left=self.current_data.drop(columns=['VALUE']),
            right=my_df,
            on=['_id', 'DATE', 'DATA_LABEL'],
            how='outer',
            indicator='exists'
        )
        my_df = (
            my_df_test[my_df_test['exists'] == 'right_only']
                      .drop(columns=['exists'])
        )
        if len(my_df) > 0:
            data_list = my_df.to_dict(orient='records')
            self.garmin.insert_many(
                documents=data_list, bypass_document_validation=True
            )
            LOG.info(msg=f'Add {len(my_df)} to DB')
        else:
            LOG.info(msg=f'Data not updated, nothing added to DB')
        return None
