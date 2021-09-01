from time import sleep
from pyautogui import position, click, rightClick, middleClick, doubleClick, write, FailSafeException


def execute_action(list, running, action):
    for time in range(0, list[4]):
        sleep(list[3])
        if running:
            try:
                action(list[1], list[2])
            except FailSafeException:
                break
            finally:
                if len(list) == 6:
                    write(list[5])
