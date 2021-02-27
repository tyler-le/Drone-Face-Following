import KeyPressModule as kp
from djitellopy import tello
import time


kp.init()

tello = tello.Tello()
tello.connect()
print(tello.get_battery())


def getKeyboardInput():
    leftRight, forwardBackward, upDown, yaw = 0, 0, 0, 0
    speed = 50

    if kp.getKeypress('LEFT'): leftRight = -speed
    elif kp.getKeypress('RIGHT'): leftRight = speed #

    if kp.getKeypress('UP'): forwardBackward = speed
    elif kp.getKeypress('DOWN'): forwardBackward = -speed

    if kp.getKeypress('w'): upDown = speed
    elif kp.getKeypress('s'): upDown = -speed

    if kp.getKeypress('a'): yaw = -speed
    elif kp.getKeypress('d'): yaw = speed

    if kp.getKeypress('1'): tello.flip_forward()
    if kp.getKeypress('2'): tello.flip_right()
    if kp.getKeypress('3'): tello.flip_back()
    if kp.getKeypress('4'): tello.flip_left()

    if kp.getKeypress('q'): tello.land()
    elif kp.getKeypress('SPACE'): tello.takeoff()

    return [leftRight, forwardBackward, upDown, yaw]


while True:
    tello.send_rc_control(0, 0, 0, 0)
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    time.sleep(0.05)

