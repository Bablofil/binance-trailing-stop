"""
    Подробная информация о боте на сайте bablofil.ru/bot-dlya-binance
"""
import sqlite3
import logging
import time
import os
import math

from datetime import datetime

from binance_api import Binance

bot = Binance(
    API_KEY='',
    API_SECRET=''
)

settings = dict(
    symbol='EOSBTC',            # Пара для отслеживания
    strategy="Short",           # Стратегия - Long (повышение), Short (понижение)           
    stop_loss_perc = 0.5,       # % оставания от цены
    stop_loss_fixed = 0,        # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
                                # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount = 0.0015             # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
                                # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
                                # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
)

multiplier = -1 if settings['strategy'] == "Long" else 1

print("Получаем настройки пар с биржи")
symbols = bot.exchangeInfo()['symbols']
step_sizes = {symbol['symbol']:symbol for symbol in symbols}
for symbol in symbols:
    for f in symbol['filters']:
        if f['filterType'] == 'LOT_SIZE':
            step_sizes[symbol['symbol']] = float(f['stepSize'])


while True:
    try:
        print('Проверяю пару {pair}, стратегия {strategy}'.format(pair=settings['symbol'], strategy=settings['strategy']))
        # Получаем текущие курсы по паре
        current_rates = bot.depth(symbol=settings['symbol'], limit=5)

        bid=float(current_rates['bids'][0][0])
        ask=float(current_rates['asks'][0][0])

        # Если играем на повышение, то ориентируемся на цены, по которым продают, иначе на цены, по которым покупают
        curr_rate = bid if settings['strategy'] == "Long" else ask
        
        if settings['stop_loss_fixed'] == 0:
           settings['stop_loss_fixed'] = (curr_rate/100) * (settings['stop_loss_perc']*multiplier+100)
 
        print("Текущие курсы bid {bid:0.8f}, ask {ask:0.8f}, выбрана {cr:0.8f} stop_loss {sl:0.8f}".format(
            bid=bid, ask=ask, cr=curr_rate, sl=settings['stop_loss_fixed']
        ))

        # Считаем, каким был бы stop-loss, если применить к нему %
        curr_rate_applied = (curr_rate/100) * (settings['stop_loss_perc']*multiplier+100)

        if settings['strategy'] == "Long":
            # Выбрана стратегия Long, пытаемся продать монеты как можно выгоднее
            if curr_rate > settings['stop_loss_fixed']:
                print("Текущая цена выше цены Stop-Loss")
                if curr_rate_applied > settings['stop_loss_fixed']:
                    print("Пора изменять stop-loss, новое значение {sl:0.8f}".format(sl=curr_rate_applied))                    
                    settings['stop_loss_fixed'] = curr_rate_applied
            else:
                # Текущая цена ниже или равна stop loss, продажа по рынку
                res = bot.createOrder(
                    symbol=settings['symbol'],
                    recvWindow=15000,
                    side='SELL',
                    type='MARKET',
                    quantity=settings['amount']
                )
                print('Результат создания ордера', res)
                if 'orderId' in res:
                    # Создание ордера прошло успешно, выход
                    break
        else:
            # Выбрана стратегия Short, пытаемся купить монеты как можно выгоднее
            if curr_rate < settings['stop_loss_fixed']:
                print("Текущая цена ниже stop-loss")
                if curr_rate_applied < settings['stop_loss_fixed']:
                    print("Пора изменять stop-loss, новое значение {sl:0.8f}".format(sl=curr_rate_applied))                    
                    settings['stop_loss_fixed'] = curr_rate_applied
            else:
                # Цена поднялась выше Stop-Loss, Покупка по рынку
                quantity = math.floor((settings['amount']/curr_rate)*(1/step_sizes[settings['symbol']]))/(1/step_sizes[settings['symbol']])
                print("Цена поднялась выше Stop-Loss, Покупка по рынку, кол-во монет {quantity:0.8f}".format(quantity=quantity))
                # math.Floor(coins*(1/stepSize)) / (1 / stepSize)
                res = bot.createOrder(
                    symbol=settings['symbol'],
                    recvWindow=15000,
                    side='BUY',
                    type='MARKET',
                    quantity=quantity
                )
                print('Результат создания ордера', res)
                if 'orderId' in res:
                    # Создание ордера прошло успешно, выход
                    break

    except Exception as e:
        print(e)
    time.sleep(1)
#print(bot.myTrades(symbol='PPTETH'))
