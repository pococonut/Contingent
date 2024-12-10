from collections import defaultdict, Counter

from fastapi.encoders import jsonable_encoder


def add_ids(data):
    """
    Функция для добавления параметра идентификатора в словарь
    :param data: Список словарей
    :return: Список словарей с идентификатором
    """
    data_with_ids = []
    for i, d in enumerate(data):
        d["id"] = i
        data_with_ids.append(d)
    return data_with_ids


def get_rid_of_ids(data):
    """
    Функция для удаления параметра идентификатора в словаре
    :param data: Список словарей
    :return: Список словарей без идентификаторов
    """
    data_new = []
    for item in data:
        js_item = jsonable_encoder(item)
        del js_item["id"]
        data_new.append(js_item)
    return data_new


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

        degree_payment = card.get("degree_payment")
        group = f'group_{card.get("group")}'
        subgroup = f'sub_{card.get("subgroup")}'
        lst = [degree_payment, group, subgroup, "total"]

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

    return {"budget": data.get("бюджет", 0),
            "contract": data.get("договор", 0),
            "total": data.get("total", 0),
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
    number_contingent = list()

    for direction, courses in directions.items():
        for course, data in courses.items():
            calculations = get_calculations(data)
            data = {"direction": direction,
                    "course": int(course),
                    "budget": calculations.get("budget"),
                    "contract": calculations.get("contract"),
                    "groups": calculations.get("groups"),
                    "subgroups": calculations.get("subgroups"),
                    "total": calculations.get("total")}
            number_contingent.append(data)

    number_contingent = add_ids(number_contingent)
    return number_contingent
