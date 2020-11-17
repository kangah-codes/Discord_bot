"""
DISCORD GAMES BOT
Author: CHR-onicles
Date: 17-11-2020 20:00GMT

A bot to automatically play discord bot games.
"""

import pyautogui, time, random, os
from os import path
from datetime import datetime

# PATHS FOR SCREENSHOTS
DC_PATH = '.\\dc'
DANK_PATH = '.\\dank'
POKE_PATH = '.\\poke'
EVENTS_PATH = '.\\all_events'

# GLOBAL VARIABLES
DISPLAY_REGION = ()  # (left,top,width,height)
MT = 1.2  # mouse pointer movement duration
T = 0.1  # general typing interval


def getRandNum(i, j):
    """
    Function to return a random number from a range passed in.
    :param i: lower boundary
    :param j: upper boundary inclusive
    :return: random number from given range
    """
    return random.randint(i, j)


def getDiscordRegion():
    """
    Function to grab discord window region.
    Modifies global variable DISPLAY REGION with the new found display region
    :return: returns modified DISPLAY_REGION as a tuple.
    """
    global DISPLAY_REGION
    # Values below will have to be changed if discord window is resized.
    # More vertical screen space needed to catch events on time and process them.
    x = 1174  # This is the minimum width for a discord window.
    y = 1045
    # TODO: Use pics of extreme window edges to determine size of window and possible
    #   resizing itself. Currently this is manual.
    region = pyautogui.locateOnScreen(path.join(DC_PATH, 'discord_logo.png'), confidence=0.9)
    if region is None:
        raise Exception('Could not find Discord on Screen! Make sure discord is visible.')
    else:
        pyautogui.moveTo(region.left, region.top, T)
        print('Found discord logo.')
        # TODO: Return value if successful for openDiscord() function to use for processing.

    DISPLAY_REGION = (region.left, region.top, region.left + x, region.top + y)

    # Test to move mouse pointer around display region
    #   to let you know what the bot assumes is the DISPLAY REGION
    pyautogui.moveTo(DISPLAY_REGION[0], DISPLAY_REGION[1], .5)
    pyautogui.moveTo(DISPLAY_REGION[0] + x, DISPLAY_REGION[1], .5)
    pyautogui.moveTo(DISPLAY_REGION[0] + x, DISPLAY_REGION[1] + y, .5)
    pyautogui.moveTo(DISPLAY_REGION[0], DISPLAY_REGION[1] + y, .5)
    pyautogui.moveTo(DISPLAY_REGION[0], DISPLAY_REGION[1], .5)
    print('Mouse movement showed display region available to bot.')


def checkForSpamChannel():
    """
    Function to check display region if bot is in spam channel.
    :return: returns 'n' if spam channel is not found or 'p' if it is.
    """
    spam = pyautogui.locateOnScreen(path.join(DC_PATH, 'spam_channel.png'),
                                    region=(DISPLAY_REGION[0] + 380, DISPLAY_REGION[1] + 20, 270, 60),
                                    confidence=0.9)
    if spam is None:
        print("Couldn't find spam channel.")
        return 'n'
    else:
        print('Spam channel found.')
        return 'p'
        # print(spam)  # For debugging


def changeToSpamChannel():
    """
    Function to change spam channel after verifying that bot isn't in it.
    """
    status = checkForSpamChannel()
    while True:
        if status == 'n':
            pass
        elif status == 'p':
            break
        pyautogui.hotkey('alt', 'down')  # shortcut to move to next channel
        print('Channel changed: ' + datetime.now().strftime("%H:%M:%S"))
        time.sleep(3)
        status = checkForSpamChannel()


def openDiscord():
    """
    Function to open discord and go to appropriate server and channel for further use.
    """

    pyautogui.press('win')
    pyautogui.write('discord', T)
    pyautogui.press('enter')
    time.sleep(5)
    # TODO: factor in first-time load time later(extend time -> ~40s)
    #   Let bot sleep for some time if it couldn't find discord window as it may take long to
    #   load for the first time.

    getDiscordRegion()

    # make sure we are in my server (always the first server)
    pyautogui.hotkey('ctrl', '2')  # shortcut to move to first server
    print('Personal server selected.')

    # set to not show channel member list for maximum display size
    if pyautogui.locateOnScreen(path.join(DC_PATH, 'channel_member_list.png'), region=DISPLAY_REGION,
                                confidence=0.9):
        pyautogui.hotkey('ctrl', 'u')  # shortcut to remove channel member list
        print('Channel member list was found and deactivated.')
    else:
        print('There was no channel member list.')

    changeToSpamChannel()

    # set mouse cursor in message box
    loc = pyautogui.locateCenterOnScreen(path.join(DC_PATH, 'message_box.png'), region=DISPLAY_REGION,
                                         confidence=0.9)
    if loc is not None:
        pyautogui.moveTo(loc.x - 200, loc.y, MT)  # move a little to the left in message box
        pyautogui.click()
        print('Message box was made active with cursor.')
    else:
        print("Message box wasn't found.")

    print('Discord ready.\n')


def checkForEvents():
    """
    Function to check for dank memer or pokeverse events and process them accordingly.
    """
    time.sleep(1)
    for item in os.listdir(EVENTS_PATH):
        # removed DISPLAY_REGION to slow it down and search everywhere on screen
        p_loc = pyautogui.locateOnScreen(path.join(EVENTS_PATH, item), confidence=0.8)
        # If-block below has no current use.
        # if item == os.listdir(EVENTS_PATH)[-1] and p_loc is None:
        #     # print('No event found.\n')
        #     pass
        if p_loc is None:
            continue
        else:
            # No else statement to prevent unforeseen occurrences.
            if item in ['break-raider.png', 'raider.png', 'rare-raider.png', 'mega-boss.png']:
                print('Raider/Boss event found: ' + datetime.now().strftime("%H:%M:%S"))
                pyautogui.hotkey('alt', 'down')
                print('Channel changed.')
                time.sleep(3)
                changeToSpamChannel()
            elif item == 'glitch-poke.png':
                print('Glitch event found: ' + datetime.now().strftime("%H:%M:%S"))
                Pokeverse.glitch_event()
            elif item in ['super_rare_event.png', 'uncommon_event.png', 'rare_event.png']:
                print('Dank event found: ' + datetime.now().strftime("%H:%M:%S"))
                DankMemer.dank_event()
            elif item == 'easter-egg.png':
                Pokeverse.easter_egg_event()
                print('Easter egg event found: ' + datetime.now().strftime("%H:%M:%S"))
            elif item == 'candy-event.png':
                Pokeverse.candy_event()


class Pokeverse:
    """
    Pokeverse class to do pokeverse commands and handle its events.
    """

    def __init__(self):
        pass

    @staticmethod
    def glitch_event():
        """
        Static method to catch glitch pokemon.
        """
        catch = ['catch_failed.png', 'catch_success.png']
        pyautogui.write('!c 5', T)
        pyautogui.press('enter')
        time.sleep(3)
        while True:
            g_loc = pyautogui.locateOnScreen(path.join(POKE_PATH, catch[0]), confidence=0.8)
            if g_loc is None:
                g_loc = pyautogui.locateOnScreen(path.join(POKE_PATH, catch[1]), confidence=0.8)
                if g_loc is None:
                    print(
                        "Couldn't tell whether I caught glitch pokemon or not: " + datetime.now().strftime("%H:%M:%S"))
                    break
                else:
                    print('Glitch pokemon caught!: ' + datetime.now().strftime("%H:%M:%S"))
                    time.sleep(2)
                    break
            else:
                pyautogui.write('!c 5', T)
                pyautogui.press('enter')
                time.sleep(3)

    @staticmethod
    def easter_egg_event():
        """
        Static method to get literal easter eggs from easter egg events.
        """
        pyautogui.write('!te', T)
        pyautogui.press('enter')
        print('Got easter egg: ' + datetime.now().strftime("%H:%M:%S"))

    @staticmethod
    def candy_event():
        """
        Static method to get candies from candy events.
        """
        pyautogui.write('!treat', T)
        pyautogui.press('enter')
        checkForEvents()

    @staticmethod
    def fish_comm():
        """
        Static method to run fish command every 4 minutes.
        """
        pyautogui.write('!fs', T)
        pyautogui.press('enter')
        checkForEvents()


class DankMemer:
    """
    Dank Memer class which takes care of dank memer commands, checks for its events,
    and handles them.
    """
    PLS_PM_LIST = ['n', 'e', 'r', 'd']
    TRIVIA_LIST = ['A', 'B', 'C', 'D']
    rand_num = getRandNum(0, 3)

    # Dictionaries of what to type when events occur:
    # PS: Weird names found were intentional for REASONS you saw during testing.
    PLS_SCOUT_DICT = {'air_option.png': 'air', 'attic_option.png': 'attic',
                      'bank_option.png': 'bank', 'bus_option.png': 'bus',
                      'coat_option.png': 'coat', 'discord_option.png': 'discord',
                      'grass_option.png': 'grass', 'mailbox_option.png': 'mailbox',
                      'pocket_option.png': 'pocket', 'tree_option.png': 'tree',
                      'uber_option.png': 'uber', 'bushes_option.png': 'bushes',
                      'dresser_option.png': 'dresser', 'pumpkin_option.png': 'pumpkin',
                      'car_option.png': 'car', 'sewer_option.png': 'sewer', 'sink.png': 'sink',
                      'glovebox_option.png': 'glovebox', 'dumpster_option.png': 'dumpster'
                      }
    FISH_EVENT_DICT = {'big_bait.png': 'Big bait catches big fish',
                       'big_fishies.png': 'Big bait catches big fishies',
                       'big_fishy.png': 'big fishy', 'big_one.png': 'woah a big one',
                       'fishy.png': 'fish fish fish fishy', 'get_camera.png': 'get the camera ready',
                       'hook_line.png': 'hook line sinker', 'massive_one.png': 'woah a massive one',
                       'very_fishy.png': 'this is very fishy', 'glub_x3.png': 'glub glub glub'
                       }
    DRAGON_EVENT_DICT = {'frick_dragon.png': 'oh frick a dragon', 'no_eat_me.png': 'pls no eating my face',
                         'drag_moma.png': 'dragon these nuts on your momma',
                         'dragon_repellent.png': 'I forgot dragon repellent again',
                         'eat_lead.png': 'eat lead dragon', 'look_dragon.png': 'oh look a dragon',
                         'just_go_fish.png': "why didn't I just go fishing",
                         'toothers.png': 'woah those are some toothers'
                         }
    DANK_EVENT_DICT = {'2021_when_event.png': '2021 when', 'apple_event.png': 'awh not another apple',
                       'banned_idiot_event.png': 'banned idiot', 'banned_scrub_event.png': 'banned scrub',
                       'bitch_event.png': 'bitch', 'boo_ew_event.png': 'boo more like ew',
                       'bored_event.png': 'bored in the house and I\'m in the house bored',
                       'cheddar_event.png': 'cheddar', 'chug_event.png': 'chug', 'disinfect_event.png': 'disinfect',
                       'dislike_event.png': 'dislike', 'downdoot_event.png': 'downdoot',
                       'epic_gamer_event.png': 'epic gamer moment', 'fko_2020_event.png': 'fuck off 2020',
                       'fko_karen_event.png': 'fuck off karen', 'gaming_event.png': 'we\'re gaming now',
                       'mask_up_event.png': 'mask up', 'masks_save_lives_event.png': 'masks save lives idiot',
                       'pno_event.png': 'no', 'pls_rich_event.png': 'why my pls rich no work?',
                       'provolone_event.png': 'provolone', 'skype_event.png': 'lol imagine using skype in 2020',
                       'unoriginal_content_event.png': 'unoriginal content', 'what_gamer_event.png': 'what a gamer',
                       'renegade_event.png': 'renegade', 'downvote_event.png': 'downvote',
                       'bbanned_event.png': 'banned', 'mask_mask_event.png': 'mask mask mask',
                       '2020_lost_event.png': '2020 get lost', 'big_f_event.png': 'big f',
                       'aTrivia_event.png': TRIVIA_LIST[rand_num], 'wear_mask_event.png': 'wear a mask',
                       'vine_ripoff_event.png': 'vine ripoff', 'mobile_best_event.png': 'mobile is best!',
                       'xbox_best_event.png': 'xbox is best!', 'dance_event.png': 'dance',
                       'swiss_event.png': 'swiss'
                       }

    # Paths for Dank Memer specific stuff
    SCOUT_PATH = path.join(DANK_PATH, 'scout')
    ANIMALS_PATH = path.join(DANK_PATH, 'animals')
    FISH_PATH = path.join(ANIMALS_PATH, 'fish_event')
    FISH_TYPE_PATH = path.join(FISH_PATH, 'fish_type')
    DRAGON_PATH = path.join(ANIMALS_PATH, 'drag_event')
    DRAGON_TYPE_PATH = path.join(DRAGON_PATH, 'drag_type')
    DANK_EVENT_PATH = path.join(DANK_PATH, 'event')

    def __init__(self):
        pass

    def basic_comms(self):
        """
        Method to do basic commands like pls beg, pls postmeme, pls scout etc.
        """
        pyautogui.write('pls beg', T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls pm', T)
        pyautogui.press('enter')
        checkForEvents()
        pyautogui.write(self.PLS_PM_LIST[self.rand_num], T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls scout', T)
        pyautogui.press('enter')
        checkForEvents()
        for item in os.listdir(self.SCOUT_PATH):
            pp = pyautogui.locateOnScreen(path.join(self.SCOUT_PATH, item), region=DISPLAY_REGION,
                                          confidence=0.8)
            if pp is None:
                continue
            # Elif block below never seems to run.
            # elif item == os.listdir(self.SCOUT_PATH)[-1] and pp is None:
            #     print("Didn't recognize any scout option given: " + datetime.now().strftime("%H:%M:%S"))
            else:
                pyautogui.write(self.PLS_SCOUT_DICT[item], T)
                pyautogui.press('enter')
                break
        checkForEvents()

        pyautogui.write('pls bal', T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls profile', T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls multi', T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls shop', T)
        pyautogui.press('enter')
        checkForEvents()

        for a in range(1, 8):
            pyautogui.write('pls inv ' + str(a), T)
            pyautogui.press('enter')
            time.sleep(1)
            checkForEvents()

    def extra_comms(self):
        """
        Method to do 'extra' commands like pls profile --help, pls profile --gamble, etc. and pls pet.
        They show the stats of the commands passed in.
        Devs said they were resource-intensive so might wanna keep away from these but idk.
        """
        comms = ['help', 'cd', 'gamble', 'share', 'gift', 'cmds', 'rob']
        for command in comms:
            pyautogui.write('pls profile --' + command, T)
            pyautogui.press('enter')
            checkForEvents()

        pyautogui.write('pls pet', T)
        pyautogui.press('enter')
        checkForEvents()

    def gamble_comms(self):
        """
        Method to do pls bet (amount) and pls slots (amount) commands.
        """
        pyautogui.write('pls bet ' + str(getRandNum(420, 700)), T)
        pyautogui.press('enter')
        checkForEvents()

        pyautogui.write('pls slots ' + str(getRandNum(500, 1000)), T)
        pyautogui.press('enter')
        checkForEvents()

    def animal_comms(self):
        """
        Method to use pls fish and pls hunt commands while checking for their
        respective events and handling them.
        """

        pyautogui.write('pls fish', T)
        pyautogui.press('enter')
        time.sleep(2)  # to give it enough time to load in and check for event.
        checkForEvents()
        f_loc = pyautogui.locateOnScreen(path.join(self.FISH_PATH, 'rare_fish_event.png'),
                                         confidence=0.8)
        if f_loc is None:
            pass
            print('No fish event found.')
        else:
            for item in os.listdir(self.FISH_TYPE_PATH):
                pr = pyautogui.locateOnScreen(path.join(self.FISH_TYPE_PATH, item),
                                              confidence=0.9)
                if pr is None:
                    continue
                elif item == os.listdir(self.FISH_TYPE_PATH)[-1] and pr is None:
                    print("Couldn't recognize what to type for fish rare event.")
                else:
                    pyautogui.write(self.FISH_EVENT_DICT[item])
                    pyautogui.press('enter')
                    print('Got rare fish!: ' + datetime.now().strftime("%H:%M:%S"))
                    break
        checkForEvents()

        pyautogui.write('pls hunt', T)
        pyautogui.press('enter')
        time.sleep(2)
        checkForEvents()
        d_loc = pyautogui.locateOnScreen(path.join(self.DRAGON_PATH, 'dragon_event.png'), confidence=0.8)
        if d_loc is None:
            pass
            print('No dragon event found.')
        else:
            for item in os.listdir(path.join(self.DRAGON_PATH, 'drag_type')):
                doj = pyautogui.locateOnScreen(path.join(self.DRAGON_TYPE_PATH, item), confidence=0.8)
                if doj is None:
                    continue
                elif item == os.listdir(self.DRAGON_TYPE_PATH)[-1] and doj is None:
                    print("Couldn't recognize what to type for dragon event: " + datetime.now().strftime("%H:%M:%S"))
                else:
                    pyautogui.write(self.DRAGON_EVENT_DICT[item])
                    pyautogui.press('enter')
                    print('Got a dragon!: ' + datetime.now().strftime("%H:%M:%S"))
                    break
        time.sleep(1)

    @staticmethod
    def dank_event():
        """
        Static method to deal with dank memer uncommon, super rare, and rare events,
        or let user handle it if bot doesn't recognize it.
        """
        for item in os.listdir(DankMemer.DANK_EVENT_PATH):
            p_loc = pyautogui.locateOnScreen(path.join(DankMemer.DANK_EVENT_PATH, item), confidence=0.9)
            if item == os.listdir(DankMemer.DANK_EVENT_PATH)[-1] and p_loc is None:
                inp = pyautogui.confirm('Couldn\'t recognize event...Proceed?', title='NEW EVENT ALERT',
                                        buttons=['Yes', 'No'])
                if inp == 'No':
                    time.sleep(60)
                else:
                    print('Couldn\'t recognize this event: ' + datetime.now().strftime("%H:%M:%S"))
                    break
            elif p_loc is None:
                continue
            else:
                pyautogui.write(DankMemer.DANK_EVENT_DICT[item])  # no interval time for faster typing with events
                #                                                    which require multiple inputs.
                pyautogui.press('enter')
                break
        time.sleep(2)


# TODO: Save print statements to a log file
#   including time stamps
if __name__ == '__main__':
    print('Started at: ' + datetime.now().strftime("%H:%M:%S"))
    openDiscord()
    checkForEvents()
    d = DankMemer()
    p = Pokeverse()
    for x in range(1, 101):
        print(f'************* {x} *************')
        print(datetime.now().strftime("%H:%M:%S"))
        if x % 2 != 0:  # 1 loop lasts for ~2mins
            p.fish_comm()
        d.basic_comms()
        d.extra_comms()
        d.gamble_comms()
        d.animal_comms()

    print('Poggers.')
