from collections import defaultdict, Counter


def get_raw_calculations(cards):
    """
    Функция для первичного расчета, без группировки групп и подгрупп
    :param cards: Список Студенческих карт
    :return: Словарь с расчетами
    """
    directions = defaultdict(lambda: defaultdict(Counter))

    for card in cards.values():
        direction = card.get("direction")
        course = card.get("course")

        lst = [card.get("degree_payment"),
               f'group_{card.get("group")}',
               f'sub_{card.get("subgroup")}',
               "total"]

        directions[direction][course] += Counter(lst)
    return directions


def get_calculations(data):
    """
    Функция для расчета численного списка
    :param data: Словарь с расчетами без группировки групп и подгрупп
    :return: Словарь с расчетами
    """
    total_groups = len({v for k, v in data.items() if "group" in k})
    total_subgroups = len({v for k, v in data.items() if "sub" in k})

    return {"бюджет": data.get("бюджет"),
            "договор": data.get("договор"),
            "total": data.get("total"),
            "groups": total_groups,
            "subgroups": total_subgroups}


def format_cards_for_calculations(cards):
    """
    Функция формирования словаря из студенческих карт для расчетов
    :param cards: Студенческие карты
    :return:Форматированные студенческие карты
    """
    students_cards = defaultdict(dict)
    for person_id, person_data in cards.items():
        for table_data in person_data.values():
            data = table_data.__dict__
            students_cards[person_id].update(data)
    return students_cards


def get_students_number_contingent(cards):
    """
    Функция для формирования численного списка студентов
    :param cards: Словарь карт студентов
    :return: Численный список, содержащий данные о количестве студентов в группах,
    подгруппах, количестве форм обучения в подгруппах и общее количество на курсе
    """

    formatted_cards = format_cards_for_calculations(cards)
    directions = get_raw_calculations(formatted_cards)
    number_contingent = defaultdict(defaultdict)

    for direction, courses in directions.items():
        for course, data in courses.items():
            number_contingent[direction][course] = get_calculations(data)

    return number_contingent
