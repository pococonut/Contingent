
def make_limit_dict(data, skip=0, limit=10):
    """
    Функция для пагинации по объектам словаря
    :param data: Словарь словарей
    :param skip: Пропускает заданное количество элементов
    :param limit: Ограничивает количество возвращаемых элементов
    :return:
    """
    keys = list(data.keys())
    paginated_keys = keys[skip:skip + limit]
    paginated_dict = {key: data[key] for key in paginated_keys}
    return paginated_dict


def make_limit_list(lst, skip=0, limit=10):
    """
    Функция для пагинации по объектам списка
    :param lst: Список словарей
    :param skip:  Пропускает заданное количество элементов
    :param limit: Ограничивает количество возвращаемых элементов
    :return:
    """
    return lst[skip:skip + limit]

