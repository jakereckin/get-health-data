from config.service import get_config
from py.garmin_stats import data_source, log, garmin
import datetime as dt
import pandas as pd


def main() -> None:
    #date = dt.datetime.today() - dt.timedelta(days=1)
    get_config()
    my_mongo = data_source.MongoDatabase()
    garmin_api = garmin.GarminStats()
    try:
        log.start_log()
        my_mongo.get_client()
        my_mongo.get_my_db()
        max_date = pd.to_datetime(my_mongo.max_date)
        all_dates = pd.date_range(
            start=max_date + dt.timedelta(days=1), 
            end=dt.datetime.today() - dt.timedelta(days=1)
        )
        garmin_api.get_api()
        for date in all_dates:
            date = date.strftime(format='%Y-%m-%d')
            log.log_info(msg=f'Processing date: {date}')
            garmin_api.call_api(date=date)
            garmin_api.get_garmin_data(date=date)
            garmin_api.get_garmin_df()
            my_mongo.update_db(my_df=garmin_api.my_df)
    except Exception as e:
        log.log_exception(exception=e)
    finally:
        log.end_log()
    return None


if __name__ == '__main__':
    main()
