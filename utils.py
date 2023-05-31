from datetime import datetime, timedelta
from threading import Lock
import logging
import sqlite3
import traceback
import argparse


class BusinessDaysUtil(object):
    DATETIME_FORMAT = '%Y%m%d'

    HOLIDAYS = []

    _unique_instance = None
    _lock = Lock()
    db_connection = None

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def init(cls):
        logging.info('initializing util class....')

        cls.HOLIDAYS = cls.load_data_from_db()

        if not cls._unique_instance:
            with cls._lock:
                if not cls._unique_instance:
                    cls._unique_instance = cls.__internal_new__()
        return cls._unique_instance

    @classmethod
    def load_data_from_db(cls):
        logging.info('loading data from db')
        try:
            cls.db_connection = sqlite3.connect('app.db')
            cur = cls.db_connection.cursor()
            cur.execute("SELECT date FROM holidays")
            rows = cur.fetchall()
            return [row[0].replace('/', '') for row in rows]
        except Exception as e:
            logging.error(traceback.format_exc())

    @classmethod
    def add_n_biz_days(cls, from_date=None, n=None):
        days_to_add = n
        result = datetime.strptime(from_date, cls.DATETIME_FORMAT)
        positive = True if days_to_add > 0 else False
        if positive:
            while days_to_add > 0:
                result += timedelta(days=1)
                if result.weekday() >= 5 or result.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:  # sunday = 6
                    continue
                days_to_add -= 1
        else:
            while days_to_add < 0:
                result -= timedelta(days=1)
                if result.weekday() >= 5 or result.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:  # sunday = 6
                    continue
                days_to_add += 1
        return result.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def get_closest_business_day(cls):
        target = datetime.today()
        while target.weekday() >= 5 or target.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:
            target -= timedelta(days=1)
        return target.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def get_target_two_days(cls, ago, pattern=None):
        t2 = cls.get_closest_business_day()
        t1 = cls.add_n_biz_days(from_date=t2, n=int(ago))
        x2 = datetime.today() - datetime.strptime(t2, cls.DATETIME_FORMAT)
        x1 = datetime.today() - datetime.strptime(t1, cls.DATETIME_FORMAT)
        return t2, t1, x2.days, x1.days

    @staticmethod
    def valid(_from):
        # 20190512
        if len(_from) != 8:
            return False
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments of business days util')
    parser.add_argument('--days_to_add', help='Set how many days to add.')
    parser.add_argument('--from_date', help='From when you want to start. use %Y%m%d format')

    args = parser.parse_args()
    BusinessDaysUtil.init()
    d = BusinessDaysUtil.add_n_biz_days(args.from_date, int(args.days_to_add))
    print(d)