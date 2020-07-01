from state import *
import json


jsonParse = json.dumps({
    'flasks_count': 7,
    'flask_size': 4,
    'flasks': [
        [1,2,2,3],
        [2,4,5,5],
        [3,1,3,4],
        [4,2,4,1],
        [5,5,1,3],
        [],
        [],
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
    for i in range(min(len(parsed['flasks']), initState.flaskCount)):
        userFlask = parsed['flasks'][i]
        flask = Flask(initState.flaskSize)
        if len(userFlask) <= initState.flaskSize:
            flask.setStack([int(x) for x in userFlask])
        flasks.append(flask)

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
                continue
            lastItem = flasks[flaskNum].getLastItem()
            for otherFlaskNum in range(len(flasks)):
                if otherFlaskNum == flaskNum or flasks[otherFlaskNum].isFull:
                    continue
                if flasks[otherFlaskNum].isEmpty or (not flasks[otherFlaskNum].isFull and flasks[otherFlaskNum].isLastValueEqual(lastItem)):
                    newFlasks = copy.deepcopy(flasks)
                    newFlasks[otherFlaskNum].addItem(newFlasks[flaskNum].getLastItemAndPop())
                    newState = State(currentState.flaskCount, currentState.flaskSize, currentState)
                    newState.setFlasks(newFlasks)
                    if newState not in queueState:
                        queueState.append(newState)

    if solvedState == None:
        print("Can't solve")

    while solvedState != None:
        print(solvedState)
        solvedState = solvedState.parentState
