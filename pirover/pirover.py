# Raspberry Pi Rover
#  motor -- using WiringPi2 (GPIO-connected).
#  camera -- using takeshot script.
#import time
import commands
from rsserver import RemoteSensorServer
from rcontroller import RobotController
import wiringpi as wp

MOTOR_IN1A=3
MOTOR_IN1B=2
MOTOR_IN2A=4
MOTOR_IN2B=0

class PiRover(object):
    def __init__(self, server=None):
        self.controller = RobotController(motorCallback=lambda x y:self.motorCallback(x,y))
        self.setup()

    def setup(self):
        wp.wiringPiSetup()
        wp.softPwmCreate(MOTOR_IN1A,0,100)
        wp.softPwmCreate(MOTOR_IN1B,0,100)
        wp.softPwmCreate(MOTOR_IN2A,0,100)
        wp.softPwmCreate(MOTOR_IN2B,0,100)

    def powerMotorA(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
#        print "1A=%d, 1B=%d" % (v1, v2)
        wp.softPwmWrite(MOTOR_IN1A, v1)
        wp.softPwmWrite(MOTOR_IN1B, v2)

    def powerMotorB(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
        print "2A=%d, 2B=%d" % (v1, v2)
        wp.softPwmWrite(MOTOR_IN2A, v1)
        wp.softPwmWrite(MOTOR_IN2B, v2)

    def motorCallback(left, right):
        powerMotorA(left)
        powerMotorB(right)

    def takeShot(self):
        print "take shot"
        (status,output) = commands.getstatusoutput('./takeshot '+self.cameraFormat)
        print output
        filename = "takeshot."+self.cameraFormat
        if status > 0:
            print "Error: "+output
            return
        try:
            f = open(filename, "rb")
            data = f.read()
        except:
            print "Error in reading output:"+filename
        finally:
            f.close()
            server.camera(data)

    def broadcast(self, m):
        message = m.encode('utf-8').lower().replace(' ','')
        if message == 'takeshot':
            self.takeShot()
        else:
            super(PiRover, self).broadcast(m)

    def setupSensors(self, lis):
        for x in lis:
            self.sensors[x] = None

    def updateSensor(self, key, val):
        self.sensors[key] = val

    def sendSensors(self):
        if self.server is None:
            return
        dic = {}
        for x in self.sensors:
            v = self.sensors[x]
            if v is not None:
                dic[x] = v
        self.server.sensorUpdate(dic)

    def sensorUpdate(self, dic):
        for k in dic:
            key = k.encode('utf-8').lower()
            if type(dic[k]) is unicode:
                val = dic[k].encode('utf-8')
            else:
                val = str(dic[k])
            self.setVariable(key, val)

    def broadcastCallback(self, server, m):
        message = m.encode('utf-8').replace(' ','').lower()
        if message == 'forward':
            self.updateMove('forward')
            self.forward()
        elif message == 'back':
            self.updateMove('back')
            self.back()
        elif message == 'left':
            self.updateMove('left')
            self.left()
        elif message == 'right':
            self.updateMove('right')
            self.right()
        elif message == 'stop':
            self.updateMove('stop')
        elif message == 'quit':
            self.stop()
            quit()
        else:
            print "broadcast(unknown):"+message
      
if __name__ == '__main__':

