import pyautogui
import time
import json
from datetime import datetime
from util import wait_n_click, search_n_scroll_n_click, search_char, put_cursor_away, locate, click, wait, keyPress
from sf import do_sf
from models import MousePos

# TODO:
# - do elite dungeon the entire account (is this a good idea?)

# BUG:

# Load data
with open("./json/alt.json", "r") as f:
    alt_data = json.load(f)
with open("./json/main.json", "r") as f:
    main_data = json.load(f)
with open("./json/farm.json", "r") as f:
    farm_data = json.load(f)
with open("./json/nett.json", "r") as f:
    nett_data = json.load(f)

def main():
    print('Starting...')
    pyautogui.FAILSAFE = True
    time.sleep(3)
        
    start_time = time.time()  # Start timer
    
    # open_farm(farm_data['farmImgUrl'], farm_data['searchStopImgUrl'])
    
    open_menu()
    
    # mass_farm_red_meso()
    
    for char in main_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_main(char['gemColor'])
    
    # 47.35 mins
    for char in alt_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        do_daily_alt(char['doElite'], char['eliteLvl'], char['doCdd'])
    
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    
    do_overnight_farming()
    
    # open_menu()
    # do_sf()
    
    quit_this_damn_game()
    turn_pc_off()
    
def mass_farm_red_meso():
    print('Farming red meso...')
    start_time = time.time()  # Start timer
    
    for char in nett_data:
        # search_char(char['imgUrl'])
        print(char['imgUrl'])
        open_change_character(char['imgUrl'])
        farm_red_meso()
    
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    
    
def open_menu(): 
    wait_n_click('./imgs/buttons/menu.png')
    return

def open_dungeons(): 
    wait_n_click('./imgs/buttons/dungeons.png')
    return

def open_elite_dungeon(elite_lvl: int | None):
    wait_n_click('./imgs/buttons/elite-dungeon.png')
    if (elite_lvl == 200):
        wait_n_click('./imgs/buttons/elite-dungeon-200.png', confidence=0.9)
    elif (elite_lvl == 190):
        wait_n_click('./imgs/buttons/elite-dungeon-190.png', confidence=0.9)
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
    wait_n_click('./imgs/buttons/mail-receive.png', timeout=2)
    wait_n_click('./imgs/buttons/confirm.png', timeout=2)
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
    wait_n_click('./imgs/buttons/guild.png', wait=1.5)
    res = True
    if do_elite:
        res = wait_n_click('./imgs/buttons/guild-claim.png', timeout=2)
    else:
        time.sleep(1)
        
    wait_n_click('./imgs/buttons/close.png')
    
    if do_elite:
        keyPress('esc')
    return not res

def do_daily_alt(do_elite: bool, elite_lvl: int | None, do_cdd: bool):
    open_menu()
    open_guild(do_elite)
    if do_elite:
        open_mail()
        open_menu()
    open_dungeons() 
    if do_elite:
        open_elite_dungeon(elite_lvl)     
    if do_cdd:
        open_daily_dungeon()
    else: 
        wait_n_click('./imgs/buttons/close.png')
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
    wait_n_click('./imgs/buttons/elite-dungeon-200.png', wait=1, confidence=0.9)
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
    put_cursor_away()
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=3)
    wait_n_click('./imgs/buttons/mini-dungeon-auto-select.png')
    wait_n_click('./imgs/buttons/enter.png')
    wait_n_click('./imgs/buttons/enter.png')
    put_cursor_away()
    wait_n_click('./imgs/buttons/mini-dungeon-final-result-exit.png', timeout=900, wait=5)
    wait_n_click('./imgs/buttons/ab-confirm.png', wait=2)
    # locate_n_click('./imgs/buttons/elite-dungeon-go-to-menu.png') # this works too, just in case
    return

def open_tasks_main(): 
    wait_n_click('./imgs/buttons/tasks.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/tasks-get-all.png', timeout=2)
    wait_n_click('./imgs/buttons/confirm.png', timeout=2)
    wait_n_click('./imgs/buttons/tasks-daily-hunt.png')
    wait_n_click('./imgs/buttons/tasks-daily-hunt-get-all.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/close.png')
    return

def open_daily_quest():
    wait_n_click('./imgs/buttons/daily-quest.png')
    wait_n_click('./imgs/buttons/daily-quest-progress.png')
    # wait_n_click('./imgs/buttons/daily-quest-1.png', confidence=0.95, timeout=1)
    # wait_n_click('./imgs/buttons/daily-quest-2.png', confidence=0.95, timeout=1)
    # wait_n_click('./imgs/buttons/daily-quest-3.png', confidence=0.95, timeout=1)
    # wait_n_click('./imgs/buttons/daily-quest-4.png', confidence=0.95, timeout=1)
    # wait_n_click('./imgs/buttons/daily-quest-5.png', confidence=0.95, timeout=1)
    # wait_n_click('./imgs/buttons/daily-quest-6.png', confidence=0.95, timeout=1)
    wait_n_click('./imgs/buttons/daily-quest-sweep.png', wait=1)
    wait_n_click('./imgs/buttons/daily-quest-sweep-confirm.png', wait=1)
    wait_n_click('./imgs/buttons/confirm.png', timeout=1200, wait=4)
    wait_n_click('./imgs/buttons/close.png', wait=1)
    wait_n_click('./imgs/buttons/close-menu.png',)
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

def open_farm(farm_image_path: str, farm_image_stop_path: str):
    if "buttons/af-" in farm_image_path:
        wait_n_click('./imgs/buttons/arcane-power-field.png')
    elif "buttons/sf-" in farm_image_path:
        wait_n_click('./imgs/buttons/star-force-field.png')
    else:
        print("Unknown type")
        return

    search_n_scroll_n_click(farm_image_path, MousePos(1585, 600))
    
    time.sleep(0.5)
    found_no_party = locate('./imgs/buttons/af-no-party.png')

    if found_no_party:  # same as "if found_no_party == True"
        wait_n_click('./imgs/buttons/create.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/create-orange.png')
        wait_n_click('./imgs/buttons/auto-battle.png')
        put_cursor_away()
        wait_n_click('./imgs/buttons/auto-battle.png')
        wait_n_click('./imgs/buttons/start.png')
        return
    
    default_stop_image_path = './imgs/buttons/view-more-party.png'
    
    party_paths = [
        ('./imgs/buttons/af-party-5.png', -1, default_stop_image_path),
        ('./imgs/buttons/af-party-4.png', 1, farm_image_stop_path),
        ('./imgs/buttons/af-party-3.png', -1, default_stop_image_path),
        ('./imgs/buttons/af-party-2.png', 1, farm_image_stop_path),
        ('./imgs/buttons/af-party-1.png', -1, default_stop_image_path),
    ]

    for path, direction, stop_path in party_paths:
        if search_n_scroll_n_click(path, MousePos(1585, 600), direction, stop_image_path=stop_path):
            break
        
    wait_n_click('./imgs/buttons/apply.png')
    wait_n_click('./imgs/buttons/confirm.png')
    # wait_n_click('./imgs/buttons/auto-battle.png')
    # put_cursor_away()
    wait('./imgs/buttons/forged.png', confidence=0.85, sleep=1)
    wait_n_click('./imgs/buttons/close-menu.png', wait=3)
    wait_n_click('./imgs/buttons/auto-battle.png')
    wait_n_click('./imgs/buttons/start.png')
    return

def quit_this_damn_game():
    time.sleep(5)
    keyPress('esc')
    put_cursor_away()
    wait_n_click('./imgs/buttons/yes.png')
    return

def turn_pc_off():
    wait_n_click('./imgs/desktop-buttons/window.png', sleep=1)
    wait_n_click('./imgs/desktop-buttons/power.png')
    time.sleep(1)
    # wait_n_click('./imgs/desktop-buttons/sleep.png')
    wait_n_click('./imgs/desktop-buttons/power.png')
    # wait_n_click('./imgs/desktop-buttons/sleep.png')
    click()
    return

def do_overnight_farming():
    # open_change_character(alt_data[len(alt_data) - 2]['imgUrl']) # literally any character you don't plan on farming with
    # open_menu()
    open_change_character(farm_data['imgUrl']) 
    open_menu()
    open_dungeons()
    open_farm(farm_data['farmImgUrl'], farm_data['searchStopImgUrl'])
    return
   
def farm_red_meso():
    open_menu()
    is_claim = open_guild(True)
    if (not is_claim):
        open_mail()
    else:
        put_cursor_away(duration=0.5)
    open_menu()
    open_dungeons()
    open_nett()
    time.sleep(1.5)
    open_menu()
    return
    
def open_nett():
    wait_n_click('./imgs/buttons/nett.png')
    wait_n_click('./imgs/buttons/quick-party-search.png')
    wait_n_click('./imgs/buttons/confirm.png')
    wait_n_click('./imgs/buttons/nett-exit.png')
    return
 
if __name__ == "__main__":
    main()
