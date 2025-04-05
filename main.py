import pyautogui
import time
import random
import json
from datetime import datetime

# TODO:
# - refactor code, re-organize (should I even bother?)
# - force the program to click until the image is gone
# - do elite dungeon the entire account (is this a good idea?)

# Load data
with open("./json/alt.json", "r") as f:
    alt_data = json.load(f)
with open("./json/main.json", "r") as f:
    main_data = json.load(f)

last_click_time = None  # Stores the timestamp of the last click

def main():
    print('Starting...')
    pyautogui.FAILSAFE = True
    time.sleep(3)
    
    start_time = time.time()  # Start timer
    
    # locate('./imgs/buttons/elite-dungeon-go-to-menu-chaos.png')
    
    open_menu()
    for char in alt_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_alt(char['doElite'], char['eliteLvl'])
        
    for char in main_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_main(char['gemColor'])
        
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time:.4f} seconds")
    
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

def locate(imgUrl: str):
    pos = pyautogui.locateOnScreen(imgUrl, confidence=0.75)
    x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
    pyautogui.moveTo(x, y)
    return

def wait_n_click(image_path: str, timeout: float = 300.0, interval: float = 1, confidence: float = 0.7) -> bool:
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            return False  # Timeout reached, exit loop
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)  # Adjust confidence if needed
            x, y = random_position(pos.left, pos.top, pos.left + pos.width, pos.top + pos.height)
            pyautogui.moveTo(x, y)
            human_pause()
            click()
            return True  # Image found, exit loop
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(interval)  # Wait before checking again
        
def search_char(image_path: str, timeout: float = 300.0, interval: float = 0.25) -> bool:
    start_time = time.time()
    width, height = pyautogui.size()
    pyautogui.moveTo(width / 2 - 40, height / 2)
    
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
        pyautogui.scroll(-1)
        time.sleep(interval)  # Wait before checking again
        
def open_menu(): 
    wait_n_click('./imgs/buttons/menu.png')
    return

def open_dungeons(): 
    wait_n_click('./imgs/buttons/dungeons.png')
    return

def open_elite_dungeon(elite_lvl: int | None):
    wait_n_click('./imgs/buttons/elite-dungeon.png')
    if (elite_lvl == 200):
        wait_n_click('./imgs/buttons/elite-dungeon-200.png')
    elif (elite_lvl == 190):
        wait_n_click('./imgs/buttons/elite-dungeon-190.png')
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png')
    wait_n_click('./imgs/buttons/back.png')
    return

def open_daily_dungeon():
    wait_n_click('./imgs/buttons/daily-dungeon.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-exit.png')
    return

def open_mail(): 
    wait_n_click('./imgs/buttons/mail.png')
    wait_n_click('./imgs/buttons/mail-personal.png')
    wait_n_click('./imgs/buttons/mail-receive.png', timeout=1)
    wait_n_click('./imgs/buttons/confirm.png', timeout=1)
    wait_n_click('./imgs/buttons/close.png')
    return

def open_tasks(): 
    wait_n_click('./imgs/buttons/tasks.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/close.png')
    return

def open_change_character(img_url: str):
    wait_n_click('./imgs/buttons/change-character.png')
    search_char(img_url)
    wait_n_click('./imgs/buttons/change-character-change.png')
    return

def open_guild(do_elite: bool):
    wait_n_click('./imgs/buttons/guild.png')
    if do_elite:
        wait_n_click('./imgs/buttons/guild-claim.png', timeout=1)
    else:
        time.sleep(1)
        
    wait_n_click('./imgs/buttons/close.png')
    
    if do_elite:
        pyautogui.press('esc')
    return

def do_daily_alt(do_elite: bool, elite_lvl: int | None):
    open_menu()
    open_guild(do_elite)
    if do_elite:
        open_mail()
        open_menu()
    open_dungeons() 
    if do_elite:
        open_elite_dungeon(elite_lvl)     
    open_daily_dungeon()
    open_mail()
    open_menu()
    if do_elite:
        open_tasks()
    return

def open_elite_dungeon_main():
    wait_n_click('./imgs/buttons/elite-dungeon.png')

    # Do chaos first
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu-chaos.png')
    
    # Do 200 later
    wait_n_click('./imgs/buttons/elite-dungeon-200.png')
    wait_n_click('./imgs/buttons/elite-dungeon-create-room.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/elite-dungeon-start.png')
    wait_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png')
    
    wait_n_click('./imgs/buttons/back.png')
    return

def open_daily_dungeon_main(gemColor: str):
    # Get the weekday number
    # 0 = Monday, 6 = Sunday
    weekday_number = datetime.today().weekday()
    wait_n_click('./imgs/buttons/daily-dungeon.png')
    
    # Do chaos first
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-go-to-menu.png')
    
    # Do normal later
    wait_n_click('./imgs/buttons/daily-dungeon-hell.png')
    # Check if it's weekend or not
    if weekday_number in [5, 6]:
        if gemColor == "cyan":
            wait_n_click('./imgs/buttons/daily-dungeon-cyan.png')
        elif gemColor == "yellow":
            wait_n_click('./imgs/buttons/daily-dungeon-yellow.png')
        wait_n_click('./imgs/buttons/daily-dungeon-option-2.png')
        wait_n_click('./imgs/buttons/daily-dungeon-enter-special.png')
    else:
        wait_n_click('./imgs/buttons/daily-dungeon-enter-normal.png')
        wait_n_click('./imgs/buttons/daily-dungeon-minus.png')

    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/daily-dungeon-go-to-menu.png')
    wait_n_click('./imgs/buttons/back.png')
    return

def open_dimension_invasion():
    wait_n_click('./imgs/buttons/dimension-invasion.png')
    wait_n_click('./imgs/buttons/quick-party-search.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/dimension-invasion-go-to-menu.png', 600)
    wait_n_click('./imgs/buttons/back.png')
    return

def open_mini_dungeon():
    wait_n_click('./imgs/buttons/mini-dungeon.png')
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=1)
    wait_n_click('./imgs/buttons/mini-dungeon-auto-select.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=900)
    time.sleep(1)
    wait_n_click('./imgs/buttons/ab-confirm.png')
    # locate_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png') # this works too, just in case
    return

def open_tasks_main(): 
    wait_n_click('./imgs/buttons/tasks.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png', timeout=1)
    wait_n_click('./imgs/buttons/confirm.png', timeout=1)
    wait_n_click('./imgs/buttons/tasks-daily-hunt.png')
    wait_n_click('./imgs/buttons/tasks-daily-hunt-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/close.png')
    return

def open_daily_quest():
    wait_n_click('./imgs/buttons/daily-quest.png')
    wait_n_click('./imgs/buttons/daily-quest-progress.png')
    wait_n_click('./imgs/buttons/daily-quest-1.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-2.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-3.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-4.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-5.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-6.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/confirm.png', timeout=1200)
    return

def do_daily_main(gemColor: str):
    open_menu()
    open_guild(True)
    open_mail()
    open_menu()
    open_dungeons()
    open_elite_dungeon_main()
    open_daily_dungeon_main(gemColor)
    open_dimension_invasion()
    open_mini_dungeon()
    open_menu()
    open_tasks_main()
    open_daily_quest()
    open_mail()
    open_menu()
    return
    
if __name__ == "__main__":
    main()
