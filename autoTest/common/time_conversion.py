"""
时间转化：时间戳转化为type为datetime.datetime的时间
"""
import time
import datetime


class TimeConversion:
    @staticmethod
    def time_stamp(timestamp):
        """
        时间戳转换
        :param timestamp: 时间戳
        :return:
        """
        if not len(str(timestamp)) == 13:
            print("时间戳输入不正确！")
            return False
        else:
            time_tuple = time.localtime(timestamp / 1000)

            current_time_beijing = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

            date_list = current_time_beijing.split(' ')[0].split('-')
            time_list = current_time_beijing.split(' ')[1].split(':')

            date_time = datetime.datetime(int(date_list[0]),
                                          int(date_list[1]),
                                          int(date_list[2]),
                                          int(time_list[0]),
                                          int(time_list[1]),
                                          int(time_list[2]))
            return date_time
