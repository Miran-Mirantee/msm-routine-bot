import random
import pyautogui
import time
import cv2
import numpy as np
from models import MousePos

def random_position(minX, minY, maxX, maxY):
    x = random.randint(minX, maxX)  # Random x within range
    y = random.randint(minY, maxY)  # Random y within range
    return x, y  # Return as an array

def click(): 
    rand = random.uniform(0.1, 0.25)
    pyautogui.mouseDown()
    time.sleep(rand)
    pyautogui.mouseUp()
    return

def human_pause(): 
    rand = random.uniform(0.584, 1.282)
    time.sleep(rand)
    return

def locate(imgUrl: str, confidence: float = 0.75):
    try:
        pos = pyautogui.locateOnScreen(imgUrl, confidence=confidence)
        x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
        # pyautogui.moveTo(x, y)
        return True
    except pyautogui.ImageNotFoundException:
        return False
    
def wait(image_path: str, timeout: float = 300.0, interval: float = 1, confidence: float = 0.85, sleep: float = 0.0) -> bool:
    start_time = time.time()
    time.sleep(sleep)

    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)  # Adjust confidence if needed
            # x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            # pyautogui.moveTo(x, y)
            # human_pause()
            # time.sleep(wait)
            # click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        # pyautogui.moveRel(100, 100)
        time.sleep(interval)  # Wait before checking again
    
def wait_n_click(image_path: str, timeout: float = 300.0, interval: float = 1, confidence: float = 0.85, wait: float = 0.5, sleep: float = 0.0) -> bool:
    start_time = time.time()
    time.sleep(sleep)

    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            human_pause()
            time.sleep(wait)
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        # pyautogui.moveRel(100, 100)
        time.sleep(interval)  # Wait before checking again
        
def wait_n_match_n_click(image_path: str, confidence: float = 0.85, timeout: float = 5, interval: float = 2.5, wait: float = 0.0, sleep: float = 0.0) -> bool:
    start_time = time.time()
    time.sleep(sleep)
    
    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        
        # screenshot first
        pyautogui.screenshot('./imgs/temp/temp.png')
        
        # read game image
        img = cv2.imread('./imgs/temp/temp.png')

        # read unique weapon image template
        template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        hh, ww = template.shape[:2]
        
        # extract bananas base image and alpha channel and make alpha 3 channels
        base = template[:,:,0:3]
        alpha = template[:,:,3]
        alpha = cv2.merge([alpha,alpha,alpha])

        # do masked template matching and save correlation image
        correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)
        
        # set threshold and get all matches
        loc = np.where(correlation >= confidence)
        # print(len(loc[0]), len(loc[1]))
        
        if len(loc[0]) == 0 or len(loc[1]) == 0:
            put_cursor_away(1895, 1910, 266, 900, 0)
            pyautogui.scroll(-1)
            time.sleep(interval)  # Wait before checking again
            continue
        
        # get first match
        x, y = random_position(loc[1][0], loc[0][0], loc[1][0] + ww, loc[0][0] + hh)
        pyautogui.moveTo(x, y)
        human_pause()
        time.sleep(wait)
        click()
        return True  # Image found, exit loop
    
    # draw matches 
    # result = img.copy()
    # print(loc)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(result, pt, (pt[0]+ww, pt[1]+hh), (0,0,255), 1)
    #     print(pt, (pt[0]+ww, pt[1]+hh))
        
def search_char(image_path: str, timeout: float = 300.0, interval: float = 0.25) -> bool:
    start_time = time.time()
    width, height = pyautogui.size()
    pyautogui.moveTo(width / 2 - 40, height / 2)
    time.sleep(2)
    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=0.95)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            human_pause()
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        pyautogui.scroll(1)
        time.sleep(interval)  # Wait before checking again
    
def put_cursor_away(minX: int = 499, maxX: int = 1416, minY: int = 3, maxY: int = 93, duration: int = 2):
    pyautogui.moveTo(random.randint(minX, maxX),random.randint(minY, maxY), duration=duration)
    return

def search_n_scroll_n_click(image_path: str, mouse_pos: MousePos, direction: int = 1, timeout: float = 300.0, interval: float = 0.25, sleep: float = 0.5, stop_image_path: str | None = None) -> bool:
    start_time = time.time()
    pyautogui.moveTo(mouse_pos.x, mouse_pos.y)
    time.sleep(0.5)
    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=0.95)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            time.sleep(sleep)
            human_pause()
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        if stop_image_path:
            res = locate(stop_image_path)
            if res:
                return False
        pyautogui.scroll(1 * direction)
        time.sleep(interval)  # Wait before checking again