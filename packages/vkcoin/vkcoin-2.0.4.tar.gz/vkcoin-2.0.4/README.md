# vkcoin
Билиотека для платёжного API VK Coin. Оффициальная документация: https://vk.com/@hs-marchant-api

После обновления **2.0** множество функций и классов изменило свой прежний вид. [Миграция](https://github.com/crinny/vkcoin/blob/master/MIGRATION.md). [Старая документация](https://github.com/crinny/vkcoin/blob/master/OLDREADME.md).

[![PyPI version](https://badge.fury.io/py/vkcoin.svg)](https://badge.fury.io/py/vkcoin)
[![Month downloads](https://img.shields.io/pypi/dm/vkcoin.svg)](https://pypi.org/project/vkcoin)
[![Чат ВКонтакте](https://img.shields.io/badge/%D0%A7%D0%B0%D1%82-%D0%92%D0%9A%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5-informational.svg)](https://vk.me/join/AJQ1d25EgA8/Mv0/xkMvc0i1)
# Установка
* Скачайте и установите [Python](https://www.python.org/downloads/) версии 3.6 и выше, если он не установлен
* Введите следующую команду в [командную строку](https://beginpc.ru/windows/komandnaya-stroka):
```bash
pip install vkcoin
```
Если вы любите приключения, можно установить библиотеку с GitHub. В таком случае она может работать нестабильно:
```bash
pip install git+git://github.com/crinny/vkcoin.git
```
* Вы прекрасны!
# Начало работы
Для начала разработки, необходимо создать исполняемый файл с расширением .py, например test.py. **Вы не можете назвать файл vkcoin.py**, так как это приведёт к конфликту. Теперь файл нужно открыть и импортировать библиотеку:
```python
import vkcoin

merchant = vkcoin.VKCoin(user_id=123456789, key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
```
|Параметр|Тип|Описание|
|-|-|-|
|user_id|Integer|ID аккаунта ВКонтакте|
|key|String|Ключ для взаимодействия с API|
|token|String|Токен ВКонтакте для WebSocket|
# Методы
Необязательные параметры при вызове функций выделены _курсивом_.

[`get_payment_url`](https://vk.com/@hs-marchant-api?anchor=ssylka-na-oplatu) - получет ссылку на оплату VK Coin
```python
merchant.get_payment_url(amount=10, payload=78922, free_amount=False)
>>> https://vk.com/coin#m1625cf67_1_-298c0d20
```
|Параметр|Тип|Описание|
|-|-|-|
|amount|Float|Количество VK Coin для перевода|
|_payload_|Integer|Число от -2000000000 до 2000000000, вернется в списке транзаций|
|_free_amount_|Boolean|True, чтобы разрешить пользователю изменять сумму перевода|
#
[`get_transactions`](https://vk.com/@hs-marchant-api?anchor=poluchenie-spiska-tranzaktsy) - получает список ваших транзакций
```python
merchant.get_transactions(tx=[2])
>>> [{'id': 1000000, 'from_id': 371576679, 'to_id': 1, 'amount': '1', 'type': 2, 'payload': 0, 'external_id': 0, 'created_at': 1557241950}]
```
|Параметр|Тип|Описание|
|-|-|-|
|tx|List|Массив ID переводов для получения или [1] - 1000 последних транзакций со ссылок на оплату, [2] — 100 последних транзакций на текущий аккаунт|
|_last_tx_|Integer|Если указать номер последней транзакции, то будут возвращены только транзакции после указанной|
#
[`send_payment`](https://vk.com/@hs-marchant-api?anchor=perevod) - делает перевод другому пользователю
```python
result = merchant.send_payment(to_id, amount)
>>> {'id': 1000000, 'amount': 1, 'current': 1430}
```
|Параметр|Тип|Описание|
|-|-|-|
|amount|Float|Сумма перевода|
|to_id|Integer|ID аккаунта, на который будет совершён перевод|
#
[`get_balance`](https://vk.com/@hs-marchant-api?anchor=poluchenie-balansa) - возвращает баланс аккаунта
```python
merchant.get_balance(123456789, 987654321)
>>> {'371576679': 1430}
```
|Тип|Описание|
|-|-|
Integer|ID аккаунтов, баланс которых нужно получить (если не указывать ничего, то возвратится баланс текущего аккаунта)|
#
[`set_shop_name`](https://vk.com/@hs-marchant-api?anchor=nazvanie-magazina) - устанавливает название магазина

Обратите внимание что название может быть закешированно на срок до 5 часов. Сбросить кеш никак нельзя.
```python
merchant.set_shop_name(name='Best Shop Ever')
>>> 1
```
|Параметр|Тип|Описание|
|-|-|-|
|name|String|Новое название магазина|
#
`run_longpoll` - запускает LongPoll
```python
merchant.run_longpoll(tx=[1], interval=0.05)
```
|Параметр|Тип|Описание|
|-|-|-|
|tx|List|Массив ID переводов для получения или [1] - 1000 последних транзакций со ссылок на оплату, [2] — 100 последних транзакций на текущий аккаунт|
|interval|Float|Частота опроса серверов на новые платежи в секундах|

# Callback
Оффициальный Callback. Поднимает сервер и принимает входящие запросы от VK Coin.

`set_callback_endpoint` - устанавливает Endpoint
```python
merchant.set_callback_endpoint('0.0.0.0', 80)
```
|Параметр|Тип|Описание|
|-|-|-|
|address|String|Адрес, на который будет поступать информация|
|port|Integer|Порт|
#
`remove_callback_endpoint` - удаляет Endpoint
```python
merchant.remove_callback_endpoint()
```
#
[`run_callback`](https://vk.com/@hs-marchant-api?anchor=callback-api) - запускает сервер для Callback
```python
merchant.run_callback()
```

[Пример использования](https://github.com/crinny/vkcoin/blob/master/examples/callback.py)

# WebSocket
**VKCoin** для взаимодействия между клиентом и сервером использует протокол WebSocket.
Данный класс реализован для получения обратных вызовов при входящих транзакциях на аккаунт, доступ к которому должен быть предоставлен токеном в классе VKCoin:

Для получения токена - перейдите по [ссылке](https://vk.cc/9f4IXA), нажмите "Разрешить" и скопируйте часть адресной строки после `access_token=` и до `&expires_in` (85 символов)

Если при использовании способа выше вы получаете ошибку, перейдите по ссылке: `https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=LOGIN&password=PASSWORD`, перед этим заменив login и password на ваш логин и пароль. После перехода по этой ссылке вам будет выдан расширенный токен.

После инициализации объекта необходимо зарегистрировать функцию, которая будет обрабатывать входящие платежи. Для этого используется декоратор `payment_handler`
```python
@merchant.payment_handler(handler_type='websocket')
def your_func(data):
	pass
```
При получении обратного вызова - входящей транзакции - в зарегестрированную функцию возвращается словарь, который является абстракцией входящего перевода и содержит следующие параметры:
```python
data['to_id']  # ваш ID
data['from_id']  # ID отправителя (инициатор входящей транзакции)
data['amount']  # количество полученных коинов
data['payload']  # Payload
```

[Пример использования](https://github.com/crinny/vkcoin/blob/master/examples/websocket.py)

# Longpoll

Постоянно опрашивает сервер на наличие новых платежей и при поступлении таковых, оповещает об этом через декоратор.

После инициализации объекта необходимо зарегистрировать функцию, которая будет обрабатывать входящие платежи. Для этого используется декоратор `payment_handler`
```python
@merchant.payment_handler(handler_type='longpoll')
def your_func(data):
	pass
```
При получении обратного вызова - входящей транзакции - в зарегестрированную функцию возвращается словарь, который является абстракцией входящего перевода и содержит следующие параметры:
```python
data['to_id']  # ваш ID
data['id']  # ID платежа
data['balance']  # баланс вашего аккаунта 
data['from_id']  # ID отправителя (инициатор входящей транзакции)
data['amount']  # количество полученных коинов
data['created_at']  # Unix Timestamp, когда был совершён перевод
```

[Пример использования](https://github.com/crinny/vkcoin/blob/master/examples/longpoll.py)

# Примеры
Примеры расположены в отдельной [папке](https://github.com/crinny/vkcoin/tree/master/examples) репозитория.

# Где меня можно найти
Я готов ответить на ваши вопросы, связанные с библиотекой.
* [ВКонтакте Crinny](https://vk.com/crinny)  or [ВКонтакте Spooti](https://vk.com/edgar_gorobchuk)
* [Telegram Crinny](https://t.me/truecrinny) or [Telegram Spooti](https://t.me/spooti)
* [Чат ВКонтакте по VK Coin API](https://vk.me/join/AJQ1d5eSUQ81wnwgfHSRktCi)
