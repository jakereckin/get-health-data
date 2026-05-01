import pandas as pd
from garminconnect import Garmin
import logging
import os
from config.service import get_config

from .log import  log_time

LOG = logging.getLogger()
CONFIG = get_config()


# ============================================================================
class GarminStats:

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------------
    @log_time
    def get_api(self) -> 'GarminStats':
        self.api = Garmin(
            email=os.getenv('GARMIN_EMAIL'), 
            password=os.getenv('GARMIN_PASSWORD')
        )
        self.api.login()
        return self
    
    # ------------------------------------------------------------------------
    @log_time
    def call_api(self, date) -> 'GarminStats':
        LOG.info(msg=f'Getting data for {date}')

        self.user_summary = self.api.get_user_summary(cdate=date)
        self.hr_data = self.api.get_heart_rates(cdate=date)
        self.stats = self.api.get_stats(cdate=date)
        self.water = self.api.get_hydration_data(cdate=date)
        self.runs = self.api.get_activities_by_date(
            startdate=date, enddate=date, activitytype='running'
        )
        return self
    
    # ------------------------------------------------------------------------
    @log_time
    def get_garmin_data(self, date) -> 'GarminStats':
        data_to_frame = []

        if self.water.get('valueInML') is None:
            water_val = 0
        else:
            water_val = self.water.get('valueInML')
        
        data_to_frame.append(
            [date, 'CALORIES', self.user_summary.get('totalKilocalories')]
        )
        data_to_frame.append(
            [date, 'RESTING_HR', self.hr_data.get('restingHeartRate')]
        )
        data_to_frame.append(
            [date, 'LAST_7_DAYS_RESTING_HR', 
             self.hr_data.get('lastSevenDaysAvgRestingHeartRate')]
        )
        data_to_frame.append(
            [date, 'MIN_HR', self.hr_data.get('minHeartRate')]
        )
        data_to_frame.append(
            [date, 'MAX_HR', self.hr_data.get('maxHeartRate')]
        )
        data_to_frame.append(
            [date, 'TOTAL_STEPS', self.stats.get('totalSteps')]
        )
        data_to_frame.append(
            [date, 'ACTIVE_MIN', self.stats.get('activeSeconds')/60]
        )
        data_to_frame.append(
            [date, 'VIGOROUS_INTENSITY_MIN', 
             self.stats.get('vigorousIntensityMinutes')]
        )
        data_to_frame.append(
            [date, 'MODERATED_INTENSITY_MIN', 
             self.stats.get('moderateIntensityMinutes')]
        )
        data_to_frame.append(
            [date, 'AVG_STRESS', self.stats.get('averageStressLevel')]
        )
        data_to_frame.append(
            [date, 'MAX_STRESS', self.stats.get('maxStressLevel')]
        )
        data_to_frame.append(
            [date, 'LOW_STRESS_PERCENT', 
             self.stats.get('lowStressPercentage')]
        )
        data_to_frame.append(
            [date, 'MEDIUM_STRESS_PERCENT', 
             self.stats.get('mediumStressPercentage')]
        )
        data_to_frame.append(
            [date, 'HIGH_STRESS_PERCENT', 
             self.stats.get('highStressPercentage')]
        )
        data_to_frame.append(
            [date, 'STRESS_DESCRIPTION', self.stats.get('stressQualifier')]
        )
        data_to_frame.append(
            [date, 'BODY_BATTERY_DURING_SLEEP', 
             self.stats.get('bodyBatteryDuringSleep')]
        )
        data_to_frame.append([date, 'WATER_DRANK_OZ', water_val/29.5735])
        data_to_frame.append(
            [date, 'SLEEP_HRS', 
             self.user_summary.get('sleepingSeconds')/60/60]
        )
        if len(self.runs) > 0:
            data_to_frame.append(
                [date,'MILES_RAN', self.runs[0].get('distance')/1609.34]
            )
            data_to_frame.append(
                [date, 'RUN_PACE', 
                 (self.runs[0].get('duration')
                  / 60
                  / (self.runs[0].get('distance')/1609.34))]
            )

        self.data_to_frame = data_to_frame
        return self 
    
    # ------------------------------------------------------------------------
    @log_time
    def get_garmin_df(self) -> 'GarminStats':
        my_df = pd.DataFrame(
            data=self.data_to_frame,
            columns=['DATE', 'DATA_LABEL', 'VALUE']
        )
        my_df['DATE'] = pd.to_datetime(arg=my_df['DATE'])
        my_df['DATE'] = my_df['DATE'].dt.strftime(date_format='%m/%d/%Y')
        my_df['_id'] = (
            my_df['DATE'] + '_' + my_df['DATA_LABEL']
        )
        self.my_df = my_df.copy()
        return self
