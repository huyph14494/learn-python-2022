import time
import traceback
import logging
from pynput.keyboard import Listener, KeyCode, Key, Controller
import pyautogui as pg
import mouseLib
import imageLib
import cv2 as cv
import numpy as np

keyboard = Controller()

timne_upgrade = 1
retry_time = 5
hasUpgrItem = False
hasMaterials = False
firstClick = False

delay=0.2
start_key=KeyCode(char='s')

# images
button_down_image = 'button_down.png'
button_ok_image = 'button_ok.png'
material_image = 'material.png'
weapon_image = 'weapon.png'
materials_image = 'materials.png'
upgr_item_image = 'upgr_item.png'
screen_image = 'screen.png'
action_click = 'action_click.png'

def move_to_target(pos, dir = 'center'):
    global firstClick
    if dir == 'left':
        point = [pos['top'] + 50, pos['left'] + 50]
    else:
        point = [pos['top'] + int(pos['width']/2), pos['left'] + int(pos['height']/2)]
    mouseLib.move(point[0], point[1])

def do_click():
    global firstClick
    if firstClick == False:
        time.sleep(0.2)
        pg.mouseDown(button='left')
        pg.mouseUp(button='left')
        time.sleep(0.2)
        pg.mouseDown(button='left')
        firstClick = True
    else:
        time.sleep(0.2)
        pg.mouseDown(button='left')
        time.sleep(0.2)
        pg.mouseUp(button='left')

def click_target(image_url, condition = True):
    print('click ', image_url)
    clicked = False
    for index in range(retry_time):
        do_click()
        time.sleep(1)
        screenShot()
        haystack_img = cv.imread(screen_image)
        actionClickPos = imageLib.detectImage(haystack_img, image_url, 0.9)
        if (condition and actionClickPos != None) or (condition == False and actionClickPos == None):
            clicked = True
            break

    if clicked == False:
        print('Click Fail')
    return clicked

def press_target(key, image_url):
    pressed = False
    for index in range(retry_time):
        keyboard.press(key)
        time.sleep(1)
        screenShot()
        haystack_img = cv.imread(screen_image)
        needlePos = imageLib.detectImage(haystack_img, image_url, 0.95)
        if needlePos == None:
            pressed = True
            break

    if pressed == False:
        print('Press Fail')
    return pressed

def screenShot():
    # take screenshot using pyautogui
    screenObj = pg.screenshot()
    screenObj = cv.cvtColor(np.array(screenObj), cv.COLOR_RGB2BGR)
    cv.imwrite(screen_image, screenObj)
    time.sleep(0.5)


def play_auto():
    try:
        global hasUpgrItem, hasMaterials
        for index in range(timne_upgrade):
            screenShot()
            haystack_img = cv.imread(screen_image)
            time.sleep(1)

            # click materials
            if hasMaterials == False:
                materialsPos = imageLib.detectImage(haystack_img, materials_image, 0.95)
                if materialsPos == None:
                    print('Materials already')
                    hasMaterials = True
                else:
                    materialPos = imageLib.detectImage(haystack_img, material_image)
                    if materialPos == None:
                        pass
                    else:
                        move_to_target(materialPos)
                        if click_target(action_click) == False:
                            break
                        move_to_target(materialsPos, 'left')
                        if click_target(materials_image, False) == False:
                            break
                        hasMaterials = True

            # click weapon
            if hasUpgrItem == False:
                upgrItemPos = imageLib.detectImage(haystack_img, upgr_item_image, 0.95)
                if upgrItemPos == None:
                    print('UpgrItem already')
                    hasUpgrItem = True
                else:
                    weaponPos = imageLib.detectImage(haystack_img, weapon_image)
                    if weaponPos == None:
                        pass
                    else:
                        move_to_target(weaponPos)
                        if click_target(action_click) == False:
                            break
                        move_to_target(upgrItemPos, 'left')
                        if click_target(upgrItemPos, False) == False:
                            break
                        hasUpgrItem = True

           
            if hasMaterials and hasUpgrItem:
                buttonOkPos = imageLib.detectImage(haystack_img, button_ok_image, 0.5)
                if buttonOkPos == None:
                    print('Can not find button ok!!!')
                else:
                    move_to_target(buttonOkPos)
                    if click_target(materials_image, False) == True:
                        keyboard.press('z')
                hasMaterials = False
                hasUpgrItem = False
            else:
                print('Can not upgrade!!!')
                break

    except Exception as e:
        logging.error(traceback.format_exc())

def on_press(key):
    try:
        print('key {0} pressed'.format(key.char))
        if key == start_key:
            play_auto()
    except AttributeError:
        print('special key {0} pressed'.format(key))
    

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()