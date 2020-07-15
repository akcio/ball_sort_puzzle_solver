from state import *
import json

name = {
    'Голубой' : 1,
    'ТЗеленый' : 2,
    'Бирюзовый' : 3,
    'Серый' : 4,
    'Коричневый' : 5,
    'Зеленый' : 6,
    'Желтый' : 7,
    'Фиолетовый' : 8,
    'Синий' : 9,
    'Оранжевый' : 10,
    'Розовый' : 11,
    'Красный' : 12,
}

jsonParse = json.dumps({
    'flasks_count': 14,
    'flask_size': 4,
    'flasks': [
        [name[x] for x in ['Красный','Розовый', 'Синий', 'ТЗеленый']],
        [name[x] for x in ['Бирюзовый','Зеленый', 'Оранжевый', 'Зеленый']],
        [name[x] for x in ['Розовый','Коричневый', 'Бирюзовый', 'Серый']],
        [name[x] for x in ['Коричневый','ТЗеленый', 'Синий', 'Фиолетовый']],
        [name[x] for x in ['Бирюзовый','Красный', 'ТЗеленый', 'Коричневый']],
        [name[x] for x in ['Оранжевый','Серый', 'Желтый', 'Голубой']],
        [name[x] for x in ['Желтый','Желтый', 'Красный', 'Фиолетовый']],
        [name[x] for x in ['Бирюзовый','Фиолетовый', 'Синий', 'ТЗеленый']],
        [name[x] for x in ['Синий','Зеленый', 'Зеленый', 'Фиолетовый']],
        [name[x] for x in ['Серый','Голубой', 'Голубой', 'Оранжевый']],
        [name[x] for x in ['Серый','Красный', 'Розовый', 'Коричневый']],
        [name[x] for x in ['Оранжевый','Желтый', 'Голубой', 'Розовый']],
        [],
        []
    ]
})


if __name__ == '__main__':
    from collections import deque
    parsed = json.loads(jsonParse)
    initState = State(
        min(int(parsed['flasks_count']), 12),
        min(int(parsed['flask_size']), 4)
    )
    flasks = []
    flaskCount = min(len(parsed['flasks']), initState.flaskCount)
    for i in range(flaskCount):
        if i >= len(parsed['flasks']):
            flasks.append(Flask(initState.flaskSize))
            continue
        userFlask = parsed['flasks'][i]
        flask = Flask(initState.flaskSize)
        if len(userFlask) <= initState.flaskSize:
            flask.setStack([int(x) for x in userFlask])
        flasks.append(flask)
    flasks.append(Flask(initState.flaskSize))
    flasks.append(Flask(initState.flaskSize))

    initState.setFlasks(flasks)

    queueState = deque()
    queueState.append(initState)
    visited = []

    solvedState = None

    while len(queueState) != 0:
        currentState = queueState.pop()
        if not isinstance(currentState, State):
            continue
        if currentState in visited:
            continue
        visited.append(currentState)
        if currentState.isWinState:
            solvedState = currentState
            break
        flasks = currentState.getFlasks()
        for flaskNum in range(len(flasks)):
            if flasks[flaskNum].isEmpty or flasks[flaskNum].isOneColor or flasks[flaskNum].isNeedOneMore:
                #print('Continue')
                continue
            lastItem = flasks[flaskNum].getLastItem()
            for otherFlaskNum in range(len(flasks)):
                if otherFlaskNum == flaskNum or flasks[otherFlaskNum].isFull:
                    continue
                if flasks[otherFlaskNum].isEmpty or (not flasks[otherFlaskNum].isFull and flasks[otherFlaskNum].isLastValueEqual(lastItem)):
                    #print('Empty flask')
                    newFlasks = copy.deepcopy(flasks)
                    newFlasks[otherFlaskNum].addItem(newFlasks[flaskNum].getLastItemAndPop())
                    newState = State(currentState.flaskCount, currentState.flaskSize, currentState)
                    newState.setFlasks(newFlasks)
                    if newState not in queueState:
                        queueState.append(newState)

    if solvedState == None:
        print("Can't solve")

    while solvedState != None:
        #print(solvedState)
        #print(solvedState.compare(solvedState.parentState))
        comPared = solvedState.compare(solvedState.parentState)
        if comPared is None:
            print(solvedState)
            solvedState = solvedState.parentState
            continue
        print([",".join([y for y in name if name[y] == x]) + "Колба:" + str(comPared+1) for x in solvedState.getFlasks()[comPared].getStack()])
        solvedState = solvedState.parentState
