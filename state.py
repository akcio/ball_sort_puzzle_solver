from flask import Flask
import copy

class State:
    def __init__(self, flaskCount: int = 12, flaskSize: int = 4, parentState = None, movingFlaskNum = None):
        self.flaskCount = flaskCount
        self.flaskSize = flaskSize
        self._flasks = [Flask(flaskSize) for x in range(flaskCount)]
        self.parentState = parentState
        self.movingFlaskNum = movingFlaskNum

    def getFlasks(self):
        ret = copy.deepcopy(self._flasks)
        return ret

    def setFlasks(self, flasks):
        self._flasks = flasks

    def __str__(self):
        return ",".join([str(x) for x in self._flasks])

    @property
    def isWinState(self):
        return all([x.isOneColor or x.isEmpty for x in self._flasks])

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        otherFlasks = other.getFlasks()
        if sum([x.isEmpty for x in otherFlasks]) != sum([x.isEmpty for x in self._flasks]):
            return False

        visited = []
        for flaskNum in range(len(self._flasks)):
            if self._flasks[flaskNum].isEmpty:
                continue
            for otherFlaskNum in range(len(otherFlasks)):
                if otherFlaskNum not in visited and self._flasks[flaskNum] == otherFlasks[otherFlaskNum]:
                    visited.append(otherFlaskNum)

        return len(self._flasks) == (sum([x.isEmpty for x in self._flasks]) + len(visited))
        
    def compare(self, other):
        if (not isinstance(other, State)):
            return None
        otherFlasks = other.getFlasks()
        for flaskNum in range(len(self._flasks)):
            if not (self._flasks[flaskNum] == otherFlasks[flaskNum]):
                return flaskNum
        return None

    def toDict(self):
        res = {
            'flasks': [],
            'movingFlaskNum': self.movingFlaskNum
        }
        for flaskNum in range(len(self._flasks)):
            res['flasks'].append(self._flasks[flaskNum].getStack())

        return res
        

