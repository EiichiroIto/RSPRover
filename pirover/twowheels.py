import time

def testCallback(left, right):
    print "TW:", left, right

class RobotController(object):
    def __init__(self, motorCallback=None):
        self.movingTime = 500 # parameter (ms)
        self.movingPower = 100 # parameter (-100..100)
        self.balance = 50 # parameter (0..100)
        self.turningTime = 300 # parameter (ms)
        self.turningPower = 50 # parameter (0..100)
        self.interval = 200 # parameter (ms)
        self.cameraFormat = "jpg" # "jpg" or "gif" or "png"
        self.acceleration = 50 # parameter(1..100)
        self.moveTimeout = 0 # private
        self.lastMSec = 0 # private
        self.currentLeft = 0 # private
        self.currentRight = 0 # private
        self.targetLeft = 0 # private
        self.targetRight = 0 # private
        self.motorCallback = motorCallback

    def newCurrent(self, current, target):
        diff = target - current
        iabs = int(abs(diff))
        sign = int(diff) / iabs
        return current + sign * (iabs if iabs < self.acceleration else self.acceleration)

    def updateCurrent(self):
        changed = False
        if self.currentLeft != self.targetLeft:
            changed = True
            self.currentLeft = self.newCurrent(self.currentLeft, self.targetLeft)
        if self.currentRight != self.targetRight:
            changed = True
            self.currentRight = self.newCurrent(self.currentRight, self.targetRight)
        if changed and self.motorCallback is not None:
            self.motorCallback(self.currentLeft, self.currentRight)

    def doOneCycle(self):
        now = int(time.time()*1000)
        if now - self.lastMSec < self.interval:
            return
        self.lastMSec = now
        if self.moveTimeout > 0 and now > self.moveTimeout:
            self.stop()
        self.updateCurrent()

    def setTarget(self, left, right):
        self.targetLeft = int(left)
        self.targetRight = int(right)

    def stop(self):
        self.setTarget(0, 0)
        self.moveTimeout = 0

    def forward(self):
        left = self.movingPower * min(self.balance, 50) / 50.0
        right = self.movingPower * min(100 - self.balance, 50) / 50.0
        self.setTarget(left, right)
        self.moveTimeout = int(time.time()*1000) + self.movingTime

    def left(self):
        left = self.turningPower
        right = - self.turningPower
        self.setTarget(left, right)
        self.moveTimeout = int(time.time()*1000) + self.turningTime

    def right(self):
        left = - self.turningPower
        right = self.turningPower
        self.setTarget(left, right)
        self.moveTimeout = int(time.time()*1000) + self.turningTime

    def back(self):
        left = - (self.movingPower * min(self.balance, 50) / 50.0)
        right = - (self.movingPower * min(100 - self.balance, 50) / 50.0)
        self.setTarget(left, right)
        self.moveTimeout = int(time.time()*1000) + self.movingTime

    def setOption(self, _k, val):
        key = _k.encode('utf-8').replace(' ','').lower()
        if key == 'movingtime' or key == 'mt':
            self.movingTime = int(val)
        elif key == 'movingpower' or key == 'mp':
            self.movingPower = min(max(int(val),-100),100)
        elif key == 'balance' or key == 'bl':
            self.balance = min(max(int(val),0),100)
        elif key == 'turningtime' or key == 'tt':
            self.turningTime = int(val)
        elif key == 'turningpower' or key == 'tp':
            self.turningPower = min(max(int(val),0),100)
        elif key == 'interval' or key == 'it':
            self.interval = min(max(int(val),0),100)
        elif key == 'acceleration' or key == 'ac':
            self.acceleration = min(max(int(val),0),100)
        elif key == 'cameraformat' or key == 'ca':
            if val == 'jpg' or val == 'gif' or val == 'png':
                self.cameraFormat = val
        else:
            print "Unknown option:"+key+"="+val

if __name__ == '__main__':
    rc = RobotController(motorCallback=testCallback)
    rc.forward()
    for i in range(10):
        rc.updateCurrent()
    rc.left()
    for i in range(10):
        rc.updateCurrent()
    for i in range(10):
        rc.doOneCycle()
        time.sleep(0.3)

