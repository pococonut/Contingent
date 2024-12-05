
def make_limit_dict(data, skip=0, limit=None):
    """
    Функция для пагинации по объектам словаря
    :param data: Словарь словарей
    :param skip: Пропускает заданное количество элементов
    :param limit: Ограничивает количество возвращаемых элементов
    :return:
    """
    keys = list(data.keys())
    if limit:
        keys = keys[skip:skip + limit]
    paginated_dict = {key: data[key] for key in keys}
    return paginated_dict


def make_limit_list(lst, skip=0, limit=None):
    """
    Функция для пагинации по объектам списка
    :param lst: Список словарей
    :param skip:  Пропускает заданное количество элементов
    :param limit: Ограничивает количество возвращаемых элементов
    :return:
    """
    if not limit:
        return lst
    return lst[skip:skip + limit]

