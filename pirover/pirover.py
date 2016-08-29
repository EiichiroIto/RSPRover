# Raspberry Pi Rover
#  motor -- using WiringPi2 (GPIO-connected).
#  camera -- using takeshot script.
from rsserver import RemoteSensorServer
from twowheels import RobotController
import wiringpi2 as wp
import commands

MOTOR_IN1A = 3 # WiringPi2 GPIO pin #
MOTOR_IN1B = 2 # WiringPi2 GPIO pin #
MOTOR_IN2A = 4 # WiringPi2 GPIO pin #
MOTOR_IN2B = 0 # WiringPi2 GPIO pin #

class WiringPiDevice(object):
    def __init__(self):
        wp.wiringPiSetup()
        wp.softPwmCreate(MOTOR_IN1A,0,100)
        wp.softPwmCreate(MOTOR_IN1B,0,100)
        wp.softPwmCreate(MOTOR_IN2A,0,100)
        wp.softPwmCreate(MOTOR_IN2B,0,100)

    def powerMotorA(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
        wp.softPwmWrite(MOTOR_IN1A, v1)
        wp.softPwmWrite(MOTOR_IN1B, v2)

    def powerMotorB(self, power):
        v1 = int(power) if power > 0 else 0
        v2 = 0 if power > 0 else - int(power)
        wp.softPwmWrite(MOTOR_IN2A, v1)
        wp.softPwmWrite(MOTOR_IN2B, v2)

class PiRover(object):
    def __init__(self, host):
        self.device = WiringPiDevice()
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
        else:
            print "Unknown Command=", _cmd

    def options(self, list):
        for k in list:
            self.controller.setOption(k, list[k])

if __name__ == '__main__':
    pi = PiRover(host='')
    pi.server.start()
