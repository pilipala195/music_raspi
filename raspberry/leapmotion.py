import sys
import Leap
from Leap import *
from time import sleep
import serial

        
class listener(Leap.Listener):
    def __init__(self, pos, v_pos, cws, ctcws):
        super(listener, self).__init__()
        self.pos = pos
        self.v_pos = v_pos
        self.cws = cws
        self.ctcws = ctcws

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def start(self, controller):
        frame = controller.frame()
        flag = 0

        # for gesture in frame.gestures():
        #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
        #         return True
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                if circle.pointable.direction.angle_to(circle.normal) > Leap.PI/2:
                    return True

    def on_frame1(self, controller):
        frame = controller.frame()

        self.pos = 0
        self.v_pos = 0
        self.cws = False
        self.ctcws = False

        for gesture in frame.gestures():
            self.cws = False
            self.ctcws = False
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    self.cws = True
                else:
                    self.ctcws = True

        for hand in frame.hands:
            self.pos = hand.palm_position[0]
            self.v_pos = hand.palm_position[1]

    def on_frame2(self, controller):
        frame = controller.frame()

        if not(self.pos == 0):
            for hand in frame.hands:
                self.pos = hand.palm_position[0] - self.pos
                print self.v_pos
                print hand.palm_position[1]
                self.v_pos = hand.palm_position[1] - self.v_pos


def valid(lis, ctrl):
    flag = False
    if lis.start(ctrl):
        while not flag:
            lis.on_frame1(ctrl)
            sleep(0.5)
            lis.on_frame2(ctrl)
            if lis.pos > 70:
                print "next music!"
                return 'a'
                flag = True
            elif lis.pos < -70:
                print "pre music!"
                return 'b'
                flag = True
            elif lis.v_pos > 50:
                print "get aloud!"
                return 'c'
                flag = True
            elif lis.v_pos < -50:
                print "be quiet!"
                return 'd'
                flag = True
            if lis.cws:
                print "clockwise"
                return 'e'
                flag = True
            # elif lis.ctcws:
            #     print "counterclockwise"
            #     return 'f'
            #     flag = True

    return 'g'


if __name__ == '__main__':
    lis = listener(0, 0, False, False)
    ctrl = Leap.Controller()
    ctrl.add_listener(lis)

    ser = serial.Serial("COM3", 115200)

    while True:
        signal = valid(lis, ctrl)
        ser.write(signal)