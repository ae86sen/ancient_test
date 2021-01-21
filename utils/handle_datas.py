import json


# 第一种:
# 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
# 转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],

# 第二种:
# 将[{'age': 18}, {'name': '马仔'}]
# 转化为 [{key: 'age', value: 18, param_type: 'int'}]

# 第三种:
# 将 [{'token': 'content.token'}]
# 转化为 [{key: 'token', value: 'content.token'}]

# 第四种:
# 将 {'User-Agent': 'Mozilla/5.0 KeYou'}
# 转化为 [{key: 'User-Agent', value: 'cMozilla/5.0 KeYou'}, {...}]

# 第五种:
# 将 ['${setup_hook_prepare_kwargs($request)}', '${setup_hook_httpntlmauth($request)}']
# 转化为 [{key: '${setup_hook_prepare_kwargs($request)}'}, {key: '${setup_hook_httpntlmauth($request)}'}]

# 第六种:
# 将 {'username': 'keyou', 'age': 18, 'gender': True}
# 转化为 [{key: 'username', value: 'keyou', param_type: 'string'}, {key: 'age', value: 18, param_type: 'int'}]
def handle_param_type(data):
    if isinstance(data, int):
        param_type = 'int'
    elif isinstance(data, bool):
        param_type = 'boolean'
    elif isinstance(data, float):
        param_type = 'float'
    else:
        param_type = 'string'
    return param_type


def handle_data1(data):
    """
    处理validate数据
    将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
    转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        for item in data:
            key = item.get('check')
            value = item.get('expected')
            comparator = item.get('comparator')
            param_type = handle_param_type(value)
            data_dict = {
                'key': key,
                'value': value,
                'comparator': comparator,
                'param_type': param_type
            }
            data_list.append(data_dict)
    return data_list


def handle_data2(data):
    """
    处理variables数据（变量）
    将[{'age': 18}, {'name': '马仔'}]
    转化为 [{key: 'age', value: 18, param_type: 'int'}]
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        for item in data:
            key = list(item)[0]
            value = item.get(key)
            param_type = handle_param_type(value)
            data_dict = {
                'key': key,
                'value': value,
                'param_type': param_type
            }
            data_list.append(data_dict)
    return data_list


def handle_data3(data):
    """
    处理extract和parameters（参数化）数据
    将 [{'token': 'content.token'}]
    转化为 [{key: 'token', value: 'content.token'}]
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        for item in data:
            key = list(item)[0]
            value = item.get(key)
            data_dict = {
                'key': key,
                'value': value
            }
            data_list.append(data_dict)
    return data_list


def handle_data4(data):
    """
    处理headers和params（查询参数）数据
    将 {'User-Agent': 'Mozilla/5.0 KeYou'}
    转化为 [{key: 'User-Agent', value: 'cMozilla/5.0 KeYou'}, {...}]
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        for k, v in data.items():
            key = k
            value = v
            data_list.append({
                'key': key,
                'value': value
            })
    return data_list


def handle_data5(data):
    """
    处理setup和teardown的hook
    将 ['${setup_hook_prepare_kwargs($request)}', '${setup_hook_httpntlmauth($request)}']
    转化为 [{key: '${setup_hook_prepare_kwargs($request)}'}, {key: '${setup_hook_httpntlmauth($request)}'}]
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        data_list = [{'key': item} for item in data]
    return data_list


def handle_data6(data):
    """
    处理form表单数据
    将 {'username': 'keyou', 'age': 18, 'gender': True}
    转化为 [{key: 'username', value: 'keyou', param_type: 'string'}, {key: 'age', value: 18, param_type: 'int'}]
    :param data:
    :return:
    """
    data_list = []
    if data is not None:
        data_list = [{'key': k, 'value': v, 'param_type': handle_param_type(v)} for k, v in data.items()]
    return data_list