import logging
import pyautogui
from gbf_bot import trial_mission


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        print('gbf robot is executing...')
        count = 1
        while True:
            print('\nexecution times: ' + str(count))
            trial_mission.activate()
            count += 1
    except KeyboardInterrupt:
        print('gbf robot finished')
    except pyautogui.FailSafeException:
        print('gbf robot finished')
