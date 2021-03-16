# Edited by Yunchi Lu on Mar.5th 2021 
if __name__ == "__main__":
    import sys
    sys.path.append('../..')
from carserver.algo.defaultParameters import defaultParameters

class Detection:
    def __init__(self, accelerations, gyroscopes, speeds, params = defaultParameters):
        self._accelerations = accelerations
        self._gyroscopes = gyroscopes
        self._speeds = speeds
        
        self._params = params
        self._sharpAccPeriods = None
        self._fastTurnPeriods = None
        self._frequency = params['FREQUENCY']
        self._lenth = self._getLength()

        self.setParams()     
    
    
    def setParams(self, modify = {}):
        '''
        Modify stored parameters. 
        '''
        for k, v in modify.items():
            if not k in self._params:
                print('Modify key: {} does not exist'.format(k))
                return
            self._params[k] = v
        self._sharpAccPeriods = self._computeSharpAccPeriods()
        self._fastTurnPeriods = self._computeFastTurnPeriods()


    def getSharpAccPeriods(self, modify = {}):
        '''
        getSharpAccPeriods()
        >>> [(3,4),(12,1)]
        time index [3,7) and [12,13) is over accelerating
        '''
        if not modify:
            return self._sharpAccPeriods
        else:
            modifiedParams = self._getModifiedParams(modify)
            return self._computeSharpAccLocs(modifiedParams)


    def getFastTurnPeriods(self, modify = {}):
        '''
        getFastTurnPeriods()
        >>> [(3,4),(12,1)]
        time index [3,7) and [12,13) is turning too fast
        '''
        if not modify:
            return self._fastTurnPeriods
        else:
            modifiedParams = self._getModifiedParams(modify)
            return self._computeFastTurnPeriods(modifiedParams) 


    def _getLength(self):
        '''
        Get input length.
        '''
        l1, l2, l3 = len(self._accelerations), len(self._gyroscopes), len(self._speeds)
        assert l1 == l2 and l2 == l3
        return l1


    def _getModifiedParams(self, modify):
        '''
        Get a copy of hyper parameters based on stored 'params' and 'modify'.
        '''
        modifiedParams = self._params.copy()
        for k, v in modify.items():
            if not k in self._params:
                print('Modify key: {} does not exist'.format(k))
                return None
            modifiedParams[k] = v
        return modifiedParams


    def _computeSharpAccPeriods(self, params = {}):
        if not params:
            params = self._params
        ACC_THREASHOLD = params['SA_ACC_THREASHOLD']
        DURATION_THREASHOLD = params['SA_DURATION_THREASHOLD']

        ret = []
        duration = 0
        for i in range(0, self._lenth):
            flag = abs(self._accelerations[i] >= ACC_THREASHOLD)
            duration += 1 / self._frequency if flag else 0
            if not flag:
                if duration >= DURATION_THREASHOLD:
                    ret.append((i-duration*self._frequency, duration*self._frequency))
                duration = 0
            elif i == self._lenth-1 and duration >= DURATION_THREASHOLD:
                ret.append((i-duration*self._frequency+1, duration*self._frequency))
        return ret


    def _computeFastTurnPeriods(self, params = {}):
        if not params:
            params = self._params
        SPEED_THREASHOLD = params['FT_SPEED_THREASHOLD']
        GYRO_THREASHOLD = params['FT_GYRO_THREASHOLD']
        DURATION_THREASHOLD = params['FT_DURATION_THREASHOLD']
        CD = params['FT_CD']

        ret = []
        duration = 0
        i = 0
        while i < self._lenth:
            flag = (self._gyroscopes[i] >= GYRO_THREASHOLD and self._speeds[i] >= SPEED_THREASHOLD) 
            duration += 1/self._frequency if flag else 0
            cd = 0
            if not flag:
                if duration >= DURATION_THREASHOLD:
                    ret.append((i-duration*self._frequency, duration*self._frequency))
                    cd = CD
                duration = 0
            elif i == self._lenth - 1 and duration >= DURATION_THREASHOLD:
                ret.append((i-duration*self._frequency+1, duration*self._frequency))
            i += (1 + self._frequency*cd)
        return ret

        


# Testing
if __name__ == "__main__":
    acc = [0] * 30
    gyr = [0]*10 + [2]*4 + [0.5]*2 + [2]*9 + [2]*5
    speed = [50] * 30
    d = Detection(acc,gyr,speed)
    print(d.getFastTurnPeriods())
