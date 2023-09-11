import api_requests


# Старшинов Павел, 8-я когорта — Финальный проект. Инженер по тестированию плюс
def test_get_order_info():
    """
    Автотест, проверяющий, что по трэк-номеру заказа приходит ответ 200 на get-запрос
    :return:
    """
    # получаем текущее тело запроса
    current_body = api_requests.get_current_body("Павел", "Старшинов", "Ленина 2",
                                  5, "89212334455", 1, "2023-09-11",
                                  "тест", ["BLACK"])
    # сохраняем результат запроса на созание заказа
    create_order_response = api_requests.create_order(current_body)
    # сохраняем трэк номер заказа из предыдущего ответа
    track = create_order_response.json()["track"]
    # сохраняем результат запроса на полчение информации по созданному заказу
    get_order_response = api_requests.get_order_info(track)
    # проверяем, что статус код ответа 200
    assert get_order_response.status_code == 200
    # проверяем, что в ответе содержится информация именно по запрошенному заказу
    assert get_order_response.json()["order"]["track"] == track

    # поторопился и запушил корректровки сразу в ветку master (название коммита "1st review corrections"),
    # поэтому ввожу этот коммент для новой ветки, как указано в задании




