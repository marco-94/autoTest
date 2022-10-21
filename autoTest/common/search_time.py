"""
时间范围搜索
"""
from autoTest.common.time_conversion import TimeConversion
from autoTest.common.render_response import APIResponse


class SearchTime:
    @staticmethod
    def search_time_conversion(created_start_time, created_end_time, search_dict):
        if len(str(created_start_time)) != 13 or len(str(created_end_time)) != 13:
            return APIResponse(400015, '时间戳输入不正确', success=False)
        else:
            start_date = TimeConversion().time_stamp(created_start_time)
            end_date = TimeConversion().time_stamp(created_end_time)
            search_dict["created_tm__range"] = (start_date, end_date)
        return search_dict
