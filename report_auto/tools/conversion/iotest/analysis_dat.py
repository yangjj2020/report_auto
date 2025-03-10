__coding__ = "utf-8"

import logging
import os
from pathlib import Path

from app.service.iotest.analogue_input_service import simple_electrical_test, analogue_input_level4
from app.service.iotest.levels_analysis_common import level1_simple_electrical_test, level2_error_detection, \
    level3_debouncing_error_healing
from pojo.MSTReqPOJO import ReqPOJO
from tools.conversion.iotest.analysis_tocsv import write_analysis_tocsv
from tools.conversion.iotest.analysis_todb import IOTestDataInDB
from tools.utils.CsvFileCombineUtil import CSVCombiner
from tools.utils.xlsm_utils import find_first_empty_row_after_string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

"""
csvPath: /outputpath/测试团队/测试场景/测试功能
outputPath：/outputpath/测试团队/测试区域
"""


def dat_data_analysis(req_data: ReqPOJO):
    csv_path = req_data.csv_path
    output_path = req_data.output_path

    test_scenario: str = req_data.test_scenario
    test_area = req_data.test_area
    test_area_dataLabel = req_data.test_area_dataLabel

    logging.debug(f"CSV Path: {csv_path}")
    logging.debug(f"Output Path: {output_path}")
    logging.debug(f"Test Scenario: {test_scenario}")
    logging.debug(f"Test Area: {test_area}")
    logging.debug(f"Test Area DataLabel: {test_area_dataLabel}")

    # 1.引脚测试报告输出模板
    ioTestDataInDB = IOTestDataInDB()
    result_dicts: dict = ioTestDataInDB.get_io_test_data(test_project=req_data.test_team,
                                                         test_scenario=req_data.test_scenario,
                                                         test_area_dataLabel=req_data.test_area_dataLabel)
    logging.info(f"result_dicts:{result_dicts}")

    # 2.分析测量文件 1-passed 2-failed 3-na 4-nottested
    level1: set[str] = set()
    level2: set[str] = set()
    level3: set[str] = set()
    level4: set[str] = set()
    return_msg_list: list[str] = []

    target_files = {'level1.csv', 'level2.csv', 'level3.csv', 'level4.csv'}
    for file_path in Path(csv_path).glob('**/*.csv'):
        file_name = file_path.name.lower()
        # 如果文件名不在目标文件集合中，跳过该文件并继续下一个循环
        if file_name not in target_files:
            continue
        logging.info("文件:%s", file_name)

        try:
            if "level1" in file_name:
                logging.info(">>>>>>>>level1")
                # 模拟量输入
                if "analogue_input" == req_data.test_scenario:
                    # 调整相应PIN脚的raw值，检查raw值能否读取且范围在0~5V内
                    op_code, op_msg = simple_electrical_test(file_path, result_dicts)
                    logging.info(f"level1:{op_code},{op_msg}")
                # 数字量输入、数字量输出、pwm输入、pwm输出
                elif "digital_input" == req_data.test_scenario or "digital_output" == req_data.test_scenario \
                        or "PWM_input" == req_data.test_scenario or "PWM_output" == req_data.test_scenario:
                    # xxx_stRaw值是否变化(有跳变)>1
                    op_code, op_msg = level1_simple_electrical_test(file_path, result_dicts)
                    logging.info(f"level1:{op_code},{op_msg}")
                level1.add(op_code)

                if op_code != 1:
                    return_msg_list.append("level1:" + op_msg)

            elif "level2" in file_name:
                logging.info(">>>>>>>>level2")
                op_code, op_msg = level2_error_detection(file_path, result_dicts)
                logging.info(f"level2:{op_code},{op_msg}")
                level2.add(op_code)

                if op_code != 1:
                    return_msg_list.append("level2:" + op_msg)

            elif "level3" in file_name:
                logging.info(">>>>>>>>level3")
                op_code, op_msg = level3_debouncing_error_healing(file_path, result_dicts)
                logging.info(f"level3:{op_code},{op_msg}")
                level3.add(op_code)

                if op_code != 1:
                    return_msg_list.append("level3:" + op_msg)

            elif "level4" in file_name:
                logging.info(">>>>>>>>level4")

                op_code, op_msg = analogue_input_level4(file_path, result_dicts)
                level4.add(op_code)

                if op_code != 1:
                    return_msg_list.append("level4:" + op_msg)

        except Exception as e:
            raise e
            return_msg_list.append(e)
            logging.error(e)

    # 3.输出文件
    output_file = os.path.join(output_path, "xlsm", "IOTest_Main_Tmplt.xlsm")
    logging.info(f"输出文件:{output_file}")

    insert_rownum = 0
    if os.path.exists(output_file):
        test_scenario = test_scenario.replace("_", " ")
        insert_rownum = find_first_empty_row_after_string(output_file, test_scenario)
    logging.info(f"insert_rownum:{insert_rownum}")

    # 4.分析结果、引脚模板、合成输出文件
    levels = {
        "level1": level1,
        "level2": level2,
        "level3": level3,
        "level4": level4,
    }

    if len(return_msg_list) > 0:
        return_msg_str = ",".join(return_msg_list)
    else:
        return_msg_str: str = ''

    o_file: str = write_analysis_tocsv(output_file, insert_rownum, levels, result_dicts)
    if o_file:
        for file_path in Path(csv_path).glob('**/*.csv'):  # 遍历所有匹配的CSV文件并删除
            try:
                if file_path.is_file():  # 确保我们只删除文件，而不是目录
                    file_path.unlink()  # 删除文件
                    logging.info(f"Deleted: {file_path}")
                else:
                    logging.info((f"Skipped directory: {file_path}"))
            except Exception as e:
                raise e
                logging.error(f"Failed to delete {file_path}. Reason: {e}")

    return return_msg_str
