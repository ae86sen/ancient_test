
from testcases.models import Testcases


# def get_testcases_by_interface_ids(ids_list):
#     """
#     通过接口id获取用例
#     :param ids_list:
#     :return:
#     """
#     one_list = []
#     for interface_id in ids_list:
#         # 返回一个查询集, 查询集中的每一个元素为用例id值
#         # [1, 2, 3]
#         testcases_qs = Testcases.objects.values_list('id', flat=True).\
#             filter(interface_id=interface_id)
#         one_list.extend(list(testcases_qs))
#     return one_list


def get_testcases_by_interface_ids(ids_list):
    # ids_list:接口列表
    runnable_testcases = []
    for interface_id in ids_list:
        testcase_qs = Testcases.objects.filter(interface_id=interface_id)
        if testcase_qs.exists():
            runnable_testcases.extend(list(testcase_qs))
    return runnable_testcases