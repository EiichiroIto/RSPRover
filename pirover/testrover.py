# Raspberry Pi Rover
#  motor -- nothing
#  camera -- using takephoto script.
from rsserver import RemoteSensorServer
from twowheels import RobotController
import commands

class GenericDevice(object):
    def __init__(self):
        pass

    def powerMotorA(self, power):
        print "motorA=", power

    def powerMotorB(self, power):
        print "motorB=", power

class PiRover(object):
    def __init__(self, host):
        self.device = GenericDevice()
        self.controller = RobotController(motorCallback=lambda x,y:self.mtCallback(x,y))
        self.server = RemoteSensorServer(host=host, sensorCallback=lambda x,y:self.seCallback(x,y), broadcastCallback=lambda x,y:self.bcCallback(x,y), timeoutCallback=lambda x:self.toCallback(x))

    def mtCallback(self, left, right):
        print "motor:", left, right
        self.device.powerMotorA(left)
        self.device.powerMotorB(right)

    def seCallback(self, server, list):
        print "sensor:", list
        self.options(list)
        self.controller.doOneCycle()

    def bcCallback(self, server, msg):
        print "broacast:", msg
        self.command(msg)
        self.controller.doOneCycle()

    def toCallback(self, server):
        self.controller.doOneCycle()

    def takePhoto(self):
        print "take a photo"
        (status,output) = commands.getstatusoutput('./takephoto.sh '+self.controller.cameraFormat)
        print output
        filename = "takephoto."+self.controller.cameraFormat
        if status > 0:
            print "Error: "+output
            return
        f = None
        try:
            f = open(filename, "rb")
            data = f.read()
        except:
            print "Error in reading output:"+filename
        finally:
            if f is not None:
                f.close()
                self.server.camera(self.controller.cameraFormat, data)

    def command(self, _cmd):
        cmd = _cmd.encode('utf-8').lower().replace(' ','')
        if cmd == 'forward':
            self.controller.forward()
        elif cmd == 'left':
            self.controller.left()
        elif cmd == 'right':
            self.controller.right()
        elif cmd == 'back':
            self.controller.back()
        elif cmd == 'stop':
            self.controller.stop()
        elif cmd == 'quit':
            self.server.stop()
        elif cmd == 'takeaphoto' or cmd == 'takephoto':
            self.takePhoto()
        else:
            print "Unknown Command=", _cmd

    def options(self, list):
        for k in list:
            self.controller.setOption(k, list[k])

if __name__ == '__main__':
    pi = PiRover(host='')
    pi.server.start()
