import asyncio

data_klines = []
trend_klines = ''
klines_array = []
levels_klines = [0.0, 0.0] #    0 - down, 1 - up
size_klines = []

async def Main_Solves():
    global data_klines
    global trend_klines
    global klines_array
    global levels_klines
    global size_klines

    while True:

        with open('klines.ssb', 'r') as file:
            data_klines = file.readlines()[-7:]
            for i in range(len(data_klines)):
                data_klines[i] = eval(data_klines[i].replace('\n', ''))
                size_klines.append(data_klines[i]['Size'])
            file.close()
        
        if data_klines[-1]['Open'] < data_klines[-2]['Open']  and data_klines[-2]['Open']  < data_klines[-3]['Open'] :
            trend_klines = 'UP'
        else:
            trend_klines = 'DOWN'
        
        for i in range(len(data_klines) - 1):
            klines_array.append(data_klines[i]['Color'])

            if data_klines[i]['Open']  > data_klines[i + 1]['Open'] :
                levels_klines[0] += data_klines[i]['Open'] 
            else:
                levels_klines[1] += data_klines[i]['Open'] 

        result = solves(trend_klines, klines_array, data_klines[0]['High'], levels_klines[0], [0, 0, 0], [0, 0], size_klines, trend_klines)
        
        with open('result.ssb', 'a+') as file:
            file.write(str(result) + '\n')
            file.close()

        await asyncio.sleep(1800)

def solves(trend, candle_array,
                up_level, down_level,
                volumes, shadows, body, 
                potential):
    coeff = 0

    # плюс - открытие вверх, минус - открытие вниз, чем больше модуль, тем увереннее открытие

    # ОПРЕДЕЛЕНИЕ КОЭФФИЦИЕНТОВ ПОД ТИПы СВЕЧИ
    if candle_array[1] == 'green':
        veryGood = 3
        good = 2
        ok = 1
        bad = -2
        veryBad = -3
    elif candle_array[1] == 'red':
        veryGood = -3
        good = -2
        ok = -1
        bad = 2
        veryBad = 3

    # РАЗМЕР ПРЕДПОСЛЕДНЕЙ СВЕЧИ
    if body[1] > body[2]:
        coeff += veryGood
    elif body[1] == body[2]:
        coeff += good

    # РАЗМЕР ТЕНИ ПРЕДПОСЛЕДНЕЙ ТЕНИ
    if shadows[1] < body[1] * .2:
        coeff += veryGood
    elif body[1] * .3 > shadows[1] > body[1] * .2:
        coeff += good
    elif body[1] * .4 > shadows[1] > body[1] * .3:
        coeff += ok
    else:
        coeff += veryBad

    # УЧЕТ ОБЪЕМОВ
    if volumes[1] > volumes[2]:
        coeff += veryGood
    elif volumes[1] == volumes[2]:
        coeff += good
    else:
        coeff -= veryBad

    # УРОВНИ СОПРОТИВЛЕНИЯ/ПОДДЕРЖКИ
    if candle_array == 'green' and up_level:
        coeff -= 3
    elif candle_array =='red' and down_level:
        coeff += 3

    # ТРЕНД
    if trend == 'UP':
        coeff += 1
    elif trend == 'DOWN':
        coeff -= 1
    
    # ПОТЕНЦИАЛ
    if potential == 'UP':
        coeff += 2
    elif potential == 'DOWN':
        coeff -= 2

    # ПОТЕНЦИАЛ И ТРЕНД
    if trend == 'UP' and potential == 'UP':
        coeff += 3
    elif trend == 'DOWN' and potential == 'DOWN':
        coeff -= 3
    
    if coeff > 0:
        return 'UP'
    elif coeff < 0:
        return 'DOWN'
    else:
        return 'ХЗ'

Main_Solves()