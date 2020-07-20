import copy

class Flask:
    def __init__(self, maxCount:int = 4):
        self._maxCount = maxCount
        self._stack = []

    def __str__(self):
        return str(self._stack)

    @property
    def isEmpty(self):
        return len(self._stack) == 0

    @property
    def isFull(self):
        return len(self._stack) >= self._maxCount

    @property
    def isOneColor(self):
        return self.isFull and all([x == self._stack[0] for x in self._stack])

    def getStack(self):
        ret = copy.deepcopy(self._stack)
        return ret

    def setStack(self, stack):
        self._stack = stack

    @property
    def isNeedOneMore(self):
        return len(self._stack) == (self._maxCount - 1) and all(x == self._stack[0] for x in self._stack)

    def isLastValueEqual(self, item):
        return self._stack[-1] == item

    def getLastItemAndPop(self):
        item = self._stack[-1]
        self._stack = self._stack[0:-1]
        return item

    def getLastItem(self):
        return self._stack[-1]

    def addItem(self, item):
        self._stack.append(item)

    def __eq__(self, other):
        if not isinstance(other, Flask):
            return False
        return len(self._stack) == len(other.getStack()) and all([self._stack[x] == other.getStack()[x] for x in range(len(self._stack))])