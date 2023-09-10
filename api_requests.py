import requests
import config, data


def get_current_body(firstName: str,
                     lastName: str,
                     address: str,
                     metroStation: int,
                     phone: str,
                     rentTime: int,
                     deliveryDate: str,
                     comment: str,
                     color: list[str]) -> dict:
    """
    Функция для получения текущего тела запроса
    :param firstName: имя клиента
    :param lastName: фамилия
    :param address: адрес
    :param metroStation: станция метро в виде числа
    :param phone: номер телефона в виде строки
    :param rentTime: срок аренды в виде числа
    :param deliveryDate: дата доставки в формате:"yyyy-mm-dd"
    :param comment: комментарий
    :param color: цвет в виде списка строк
    :return: словарь с телом запроса
    """
    # получаем копию тела запроса нужного формата
    current_body = data.body_create_order.copy()
    # редактируем тело запроса текущими параметрами
    current_body["firstName"] = firstName
    current_body["lastName"] = lastName
    current_body["address"] = address
    current_body["metroStation"] = metroStation
    current_body["phone"] = phone
    current_body["rentTime"] = rentTime
    current_body["deliveryDate"] = deliveryDate
    current_body["comment"] = comment
    current_body["color"] = color
    return current_body


def create_order(current_body) -> requests.Response:
    """
    Функция для выполнения post-запроса на создание заказа
    :param current_body: тело запроса
    :return: объект Response
    """
    # сохраняем результат запроса
    create_response = requests.post(config.URL_HOST+config.CREATE_ORDER_PATH,
                                    headers=data.headers,
                                    json=current_body)
    return create_response


def get_order_info(track: int) -> requests.Response:
    """
    Функция для выполнения get-запроса на получение информации по заказу по его трэк-номеру
    :param track: трэк-номер заказа в виде числа
    :return: объект Response
    """
    # прописываем в переменную параметр запроса
    param = {"t": str(track)}
    # сохраняем результат запроса
    get_order_response = requests.get(config.URL_HOST+config.GET_ORDER_PATH, params=param)
    return get_order_response

