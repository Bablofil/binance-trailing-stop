"""
    Подробная информация о боте на сайте bablofil.ru/bot-dlya-binance
"""
import b_api
import time
import os
import math


settings = dict(
    symbol='BTCUSDT',            # Пара для отслеживания
    strategy="Long",           # Стратегия - Long (повышение), Short (понижение)           
    stop_loss_perc = 0.05,       # % оставания от цены
    stop_loss_fixed = 0,        # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
                                # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount = 0.0003,             # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
                                # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
    #amount = 11              # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
    startrate = 0       # Нефиг продавать себе в убыток
)

multiplier = -1 if settings['strategy'] == "Long" else 1
mstart = 1 if settings['strategy'] == "Long" else -1 # startrate множитель
#print("Получаем настройки пар с биржи")

while True:
    try:
        print('ProveriaeM paru {pair}, strata= {strategy}'.format(pair=settings['symbol'], strategy=settings['strategy']))
        # Получаем текущие курсы по паре
        
        bid=b_api.bid() ; bid
        #ask=b_api.ask() ;# ask

        # Если играем на повышение, то ориентируемся на цены, по которым продают, иначе на цены, по которым покупают
        curr_rate = bid # if settings['strategy'] == "Long" #else ask
        
        if settings['startrate'] == 0:
            settings['startrate'] = (curr_rate/100) * (settings['stop_loss_perc']*mstart+100) # авто трейлстоп стартовый
 
        print("tekyshie kypcbi bid {bid:0.8f}, BblbpaHa {cr:0.8f} stop_loss {sl:0.8f}".format(
            bid=bid,  cr=curr_rate, sl=settings['stop_loss_fixed']
        ))

        # Считаем, каким был бы stop-loss, если применить к нему %
        curr_rate_applied = (curr_rate/100) * (settings['stop_loss_perc']*multiplier+100); print('cr_applied = ' , curr_rate_applied); print('startrate = ' , settings['startrate'])

        if settings['strategy'] == "Long":
            # Выбрана стратегия Long, пытаемся продать монеты как можно выгоднее
            if curr_rate > settings['stop_loss_fixed']:
                print("Cena vyshe Stop-Loss")
                if curr_rate_applied > settings['startrate']:
                   if curr_rate_applied > settings['stop_loss_fixed']:
                    print("Pora N3MEHRTb stop-loss, HOBOE 3HA4EHNE {sl:0.8f}".format(sl=curr_rate_applied))                    
                    settings['stop_loss_fixed'] = curr_rate_applied; print('slfixed= ' , settings['stop_loss_fixed'])
            else:
                # Текущая цена ниже или равна stop loss, продажа по рынку
                b_api.sync()

                tmsp = (int(time.time()) + 946684800 -1) * 1000
                tmsp
                API_KEY='2q2q2q2q2q2q2q2q2q2q2q2q2qBWMqn9evA8PeTj3e3eewe' 
                API_SECRET = bytearray(b'xQp2w2w2e33e3e3e3e3e3eJNxvGgj987meB7rmPaSUIKJsxLhUTTalrHqpUz')
                symbol='BTCUSDT'
                amount = 0.0003
                side ='SELL'
                type = 'MARKET'

                ps=('symbol='+symbol+'&recvWindow=25000&side='+side+'&type='+type+'&quantity='+str(amount)+'&timestamp='+str(tmsp)) ; ps
                                                                                                                                            #'&timeInForce=GTC&&price=0.0033
                msg = bytes(ps, "utf-8") ; msg

                import hmac # , hashlib
                from hashlib._sha256 import sha256
                                                   # msg = msg ; msg
                sign = hmac.new(
                                b'2w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2w22aSUIKJsxLhUTTalrHqpUz',
               
                                msg=msg,

                                digestmod=sha256
                                ).hexdigest()
                sign

                payload = (ps+'&signature='+sign) ; payload
                headers = {"X-MBX-APIKEY": API_KEY}
                print("headers = " , headers)
                import gc
                gc.mem_free()
                gc.collect()
                gc.mem_free()
                import urequests
                res = urequests.request(method= 'POST', url="https://api.binance.com/api/v3/order" , data=payload, headers=headers)
                print (res.text)
                print('PE3YJIbTAT CO3DAHNR', res.text)
                if 'orderId' in res.text:
                        # Создание ордера прошло успешно, выход
                    break
       

    except Exception as e:
        print(e)
    time.sleep(0.6)
import gc
gc.mem_free()
gc.collect()
gc.mem_free()
print('KOHELL')
