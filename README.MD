## Это автотест на проверку получения заказа по его track-номеру
- Для запуска автотеста должны быть установлены библиотеки requests и pytest
- Запуск всех тестов выполянется командой pytest
- в файле config должен быть акутализирован URL_HOST тестового стенда

## Вопрос к ревьюеру:
Пишу вопрос здесь, т.к. ответа от наставников пока не получил.
#### Несмотря на то, что автотест проходит удачно, есть проблема, которую я пытался решить 2 дня, но так и не нашел решения. Возможно подскажете хотя бы направление...
Первое, что я заметил, это то, что на get-запрос получения информации о заказе по его трэк-номеру приходит ответ без JSON-файла с параметрами заказа (метод json(), применяемый к response выдает ошибку JSONDecodeError). Вместо него почему-то приходит HTML.
Дальше больше: при выполнении указанного выше get-запроса с ЛЮБЫМ произвольным трэк-номером заказа бэкенд возвращает ответ 200.
Я бы подумал, что поймал баг, но все те же самые действия, выполняемые через POSTMAN приводят к ожидаемым результатам в соответствии с документацией APi.
И только при применении инструментов requests происходят вот такие вещи.
Я добавлял и убирал разные заголовки, как пишут в сети, искал ошибки в коде, но результат не изменился.
Вот ошибка, вызываемая при попытке получить JSON из ответа сервера:

============================= test session starts ==============================
collecting ... collected 1 item

check_order_test.py::test_get_order_info FAILED                          [100%]
check_order_test.py:3 (test_get_order_info)
self = <Response [200]>, kwargs = {}

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.
    
        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises requests.exceptions.JSONDecodeError: If the response body does not
            contain valid json.
        """
    
        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using charset_normalizer to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return complexjson.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
                except JSONDecodeError as e:
                    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
    
        try:
>           return complexjson.loads(self.text, **kwargs)

venv/lib/python3.11/site-packages/requests/models.py:971: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/__init__.py:346: in loads
    return _default_decoder.decode(s)
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/decoder.py:337: in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <json.decoder.JSONDecoder object at 0x104343910>
s = '<!doctype html><html lang="en"><head><meta charset="utf-8"/><link rel="icon" href="/favicon.ico"/><meta name="viewpor... src="/static/js/2.5c4bd0d5.chunk.js"></script><script src="/static/js/main.71221168.chunk.js"></script></body></html>'
idx = 0

    def raw_decode(self, s, idx=0):
        """Decode a JSON document from ``s`` (a ``str`` beginning with
        a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
    
        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.
    
        """
        try:
            obj, end = self.scan_once(s, idx)
        except StopIteration as err:
>           raise JSONDecodeError("Expecting value", s, err.value) from None
E           json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/decoder.py:355: JSONDecodeError

During handling of the above exception, another exception occurred:

    def test_get_order_info():
        current_body = api_requests.get_current_body("Павел", "Старшинов", "Ленина 2",
                                      5, "89212334455", 1, "2023-09-11",
                                      "тест", ["BLACK"])
    
        create_order_response = api_requests.create_order(current_body)
        track = create_order_response.json()["track"]
    
        get_order_response = api_requests.get_order_info(track)
    
        assert get_order_response.status_code == 200
>       assert get_order_response.json()["order"]["track"] == track

check_order_test.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <Response [200]>, kwargs = {}

    def json(self, **kwargs):
        r"""Returns the json-encoded content of a response, if any.
    
        :param \*\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises requests.exceptions.JSONDecodeError: If the response body does not
            contain valid json.
        """
    
        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using charset_normalizer to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return complexjson.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
                except JSONDecodeError as e:
                    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
    
        try:
            return complexjson.loads(self.text, **kwargs)
        except JSONDecodeError as e:
            # Catch JSON-related errors and raise as requests.JSONDecodeError
            # This aliases json.JSONDecodeError and simplejson.JSONDecodeError
>           raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
E           requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

venv/lib/python3.11/site-packages/requests/models.py:975: JSONDecodeError