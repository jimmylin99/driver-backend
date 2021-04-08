if __name__ == "__main__":
    import sys
    sys.path.append('../..')
from .safesjtu_algo.detection import Detection

def getFastTurnIndicator(acc_list, gyr_list, speed_list):
    '''
    Wrapper of Detection.getFastTurnPeriods.
    It returns a list with the same length of input lists,
    each entry has either 0 (negative) or 1 (positive)
    '''
    d = Detection(acc_list, gyr_list, speed_list)
    p = d.getFastTurnPeriods()
    ll = []
    n = len(acc_list)
    lenP = len(p)
    curP = 0
    for i in range(n):
        while curP < lenP:
            pair = p[curP]
            end = pair[0]+pair[1]
            if i < end:
                break
            curP += 1
        if curP >= lenP or i < p[curP][0]:
            ll.append(0)
        else: # p[curP][0] <= i < p[curP][0]+p[curP][1]
            ll.append(1)
    return ll

if __name__ == "__main__":
    import sys
    sys.path.append('../..')
    acc = [0] * 30
    gyr = [0]*10 + [2]*4 + [0.5]*2 + [2]*9 + [2]*5
    speed = [50] * 30
    print(getFastTurnIndicator(acc, gyr, speed))
