from collections import defaultdict, Counter


async def get_dict_of_lists(students_cards, params):
    """
    Функция для формирования словаря списков
    :param students_cards:
    :param params: Параметры для формирования словаря нужного формата
    :return: Словарь списков
    """
    key_param, value_param = params
    dict_of_lists = defaultdict(list)

    for v in students_cards.values():
        dict_of_lists[v.get(key_param)].append(v.get(value_param))

    return dict_of_lists


async def get_subgroups_lists(students_cards):
    """
    Функция возвращает словарь, где ключами являются группы,
    значениями - списки соответствующих подгрупп
    :param students_cards: Словарь карт студентов
    :return: Словарь списков подгрупп
    """
    params = ["group", "subgroup"]
    subgroups_lists = await get_dict_of_lists(students_cards, params)

    return subgroups_lists


async def get_degree_lists(students_cards):
    """
    Функция возвращает словарь, где ключами являются группы,
    значениями - списки форм обучения (бюджет/договор)
    :param students_cards: Словарь карт студентов
    :return: Словарь списков форм обучения
    """
    params = ["group", "degree_payment"]
    degree_payment_lists = await get_dict_of_lists(students_cards, params)

    return degree_payment_lists


async def get_group_students_amount(students_cards):
    """
    Функция для подсчета количества студентов в подгруппах
    :param students_cards: Словарь карт студентов
    :return: Словарь, где ключами являются номера групп,
    значениями словари подгрупп с количеством студентов
    """
    subgroups_lists = await get_subgroups_lists(students_cards)

    group_students_amount = defaultdict()
    for k, v in subgroups_lists.items():
        group_students_amount[k] = Counter(v)

    return group_students_amount


async def get_degree_students_amount(students_cards):
    """
    Функция для подсчета форм обучения студентов в группе
    :param students_cards: Словарь карт студентов
    :return: Словарь, где ключами являются номера групп,
    значениями словари с количеством форм обучения студентов
    """
    degree_payment_lists = await get_degree_lists(students_cards)

    degree_students_amount = defaultdict()
    for k, v in degree_payment_lists.items():
        degree_students_amount[k] = Counter(v)

    return degree_students_amount


async def get_total_students_amount(students_cards):
    """
    Функция для подсчета количества студентов в группе
    :param students_cards: Словарь карт студентов
    :return: Словарь где ключом является номер группы,
    значением количество студентов
    """
    subgroups_lists = await get_subgroups_lists(students_cards)
    total_students_amount = defaultdict()

    for k, v in subgroups_lists.items():
        total_students_amount[k] = {"total": len(v)}

    return total_students_amount


async def get_students_number_contingent(students_cards):
    """
    Функция для формирования численного списка студентов
    :param students_cards: Словарь карт студентов
    :return: Численный список, содержащий данные о количестве студентов по
    подгруппам, количестве форм обучения в подгруппах и общее количество в группе
    """
    group_students_amount = await get_group_students_amount(students_cards)
    degree_students_amount = await get_degree_students_amount(students_cards)
    total_students_amount = await get_total_students_amount(students_cards)
    number_contingent = defaultdict()

    for k in group_students_amount:
        number_contingent[k] = group_students_amount[k].copy()
    for k in number_contingent:
        number_contingent[k].update(degree_students_amount[k])
        number_contingent[k].update(total_students_amount[k])

    return number_contingent
