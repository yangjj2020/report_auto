__coding__ = "utf-8"

from app import db_pool
from tools.utils.DBOperator import query_table


class IOTestDataInDB(object):
    # 查询test_area下test_scenario,需要得信号量
    def get_io_test_data(self, test_area: str = None, test_area_dataLabel: str = None) -> dict:
        query = '''
                    SELECT pin_no,hw_pin,short_name,io_comment,long_name,information_hints,device_encapsulation,
                        level1,checked_values,preparation_1,stimulation_1,tester,measurements_1,
                        level2,checked_errors,preparation_2,stimulation_2,measurements_2,
                        level3,debouncing_healing,preparation_3,stimulation_3,measurements_3,
                        level4,error_substitute,preparation_4,stimulation_4,measurements_4,
                        '' as level5
                    FROM io_test_checklist
                    WHERE pin_no =  %s and hw_pin= %s
            '''
        params = (test_area_dataLabel,test_area)
        result_dicts: dict = query_table(db_pool, query=query, params=params)
        return result_dicts

    def csv_needed_columns(self, result_dicts: dict) -> list[str]:
        columns_set: set[str] = set()

        keys = [
            "measurements_1", "preparation_2", "measurements_2",
            "preparation_3", "measurements_3", "preparation_4", "measurements_4"
        ]

        obj: dict = result_dicts[0]
        # 使用列表推导式获取所有非空内容
        contents = [obj.get(key) for key in keys if obj.get(key)]

        # 将所有内容按行分割并添加到集合中
        for content in contents:
            columns_set.update(content.splitlines())

        columns_list = list(columns_set)
        return columns_list