#  todo-
#       update and restart reader with it's new settings when ever settings are changed on the main menu via event calls
#       save new game profiles (coords from custom chatbox)
#       save and load profiles
#       save the profile as a key value pair. We can display the key as Aoe4 value :x y x2y2 or something
#       I could use the custom box tool to also have the user select the colour of the text so we can run custom threshholding mask for anything but that colour.
#       option to use custom mask or default mask?
#       ***fix box select not matching primary monitor***
#       https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Combo_Filechooser_With_History_And_Clear.py

import PySimpleGUI as sg
# import MaskedMpGood as mmg
import boxSelectChatbox as bsc
import multiprocessing as mp
# import TesseractRead as tr
import gameOverlay as go
import ocrTranslator as ot
import profileHandler as ph
import gameMasks as gm
from queue import Empty
from deep_translator import GoogleTranslator
# import threading
# import json


# gui_queue = None
# ocr_queue = None
# overlayQueue = None

class MainUserInterface:
    # #this overlayOpen is used to swap printing from main window to game overlay.
    # overlayOpen = False
    # additionalLangs = ''
    # targetLanguage = 'english'
    # startedOcr = False

    # ocrProcess = None
    # gameOverlayProc = None


    def __init__(self):
        global gui_queue
        global ocr_queue
        global overlayQueue
        global closeOverlayQueue

        #this overlayOpen is used to swap printing from main window to game overlay.
        self.overlayOpen = False
        self.additionalLangs = ''
        self.langsList = GoogleTranslator.get_supported_languages()
        self.targetLanguage = ''
        self.selectedGame = ''
        self.profiles = ph.getProfiles()
        self.startedOcr = False

        self.ocrProcess = None
        self.gameOverlayProc = None


        self.chatLocation = None
        col2 = sg.Column([[sg.Frame('Output:',
        [[sg.Column([[sg.Output(font=('Helvetica', '8','bold'), text_color = 'Black', key = '-OUTPUT-',background_color= 'White',size=(27,21)),]],size=(200,315))]])]],pad=(0,0))

        # https://github.com/tesseract-ocr/tessdoc/blob/main/Data-Files-in-different-versions.md
        language_Rkeys = ['rus']#,'kor'
        col1 = sg.Column([
            [sg.Frame('Settings:', [[sg.Text(), sg.Column([[sg.Text('Additional Character Set:')],
                                    [sg.Checkbox(text = name, default = sg.user_settings_get_entry(name, False), enable_events=True,key=name ,size=(5,1)) for name in language_Rkeys],
                                    [sg.Text('Target Language:')],
                                    [sg.Combo(key='targetLang', values=self.langsList, default_value = sg.user_settings_get_entry('trgtLang', ''),enable_events=True, size=(27,1), disabled=False,readonly=True)],
                                    [sg.Text('Game Profiles:')],

                                    [sg.Listbox(values=[gameName.get('Profile') for gameName in self.profiles], default_values = [sg.user_settings_get_entry('defaultProfile', ''),],highlight_background_color='#0083cb',enable_events = True, select_mode='single', key='selectedGame', size=(25, 5))],
                                    [sg.Button('New',disabled=False), sg.Button('Delete',disabled=False)],
                                    ], size=(220,321), pad=(0,0))]])], ], pad=(0,0))

        col3 = sg.Column([[sg.Frame('Actions:',
                                    [[sg.Column([[sg.Button('Start'), sg.Button('Stop'),sg.Button('Launch Game Overlay'), ]],
                                                size=(460,45), pad=(0,0))]])]], pad=(0,0))

        # The final layout, 2 columns with one column below.
        self.layout = [sg.vtop([col1, col2]),
                [col3]]

        self.window = sg.Window('Game Chat Translator', self.layout)
        self.window.read(timeout=10)
        self.window.write_event_value('loadAdditionalLangs', None)
        # self.window.write_event_value('GameName', None)
        while True:
            event, values = self.window.read(timeout=10, timeout_key='timeout')

            if event in language_Rkeys or event == 'loadAdditionalLangs':
                self.additionalLangs = ''
                for key in language_Rkeys:
                    sg.user_settings_set_entry(key, values[key])
                    if values.get(key):
                        self.additionalLangs += ('+' + key)

                if self.startedOcr == True:

                    self.clear(gui_queue)
                    gui_queue.put('Stop')
                    self.ocrProcess.join()
                    self.ocrProcess.close()
                    self.ocrProcess = ot.begin(gui_queue, ocr_queue,self.chatLocation,self.additionalLangs,self.targetLanguage,self.selectedGame)

            if event == 'targetLang':
                sg.user_settings_set_entry('trgtLang', values['targetLang'])

            if event == 'New':
                self.newProfilePopup(self.window)

            if event == 'selectedGame':
                try:
                    sg.user_settings_set_entry('defaultProfile', values['selectedGame'])
                    profile=ph.getProfile(values['selectedGame'][0],self.profiles)
                    self.chatLocation = profile.get('ChatLoc')
                    self.selectedGame = profile.get('Game')
                except:
                    pass
                # self.game




            if event == sg.WIN_CLOSED:
                gui_queue.put('Stop')
                if self.startedOcr:
                    # this needs to be in the function for stopOcr() as this section of code is written a few times
                    self.startedOcr = False
                    gui_queue.put('Stop')
                    self.ocrProcess.join()
                    self.ocrProcess.close()

                if self.overlayOpen:
                    # Make this a function for closeGameOverlay()
                    self.overlayOpen = False
                    closeOverlayQueue.put('Stop')
                    self.gameOverlayProc.join()
                    self.gameOverlayProc.close()
                    self.window['Launch Game Overlay'].update(disabled=False)
                break

            if event == 'Start':
                self.start(values)
                #  testing launching with defaults
                # self.targetLanguage = values.get('targetLang')
                # if (self.targetLanguage.lower() in self.langsDict or self.targetLanguage.lower() in self.langsDict.values()):
                #     self.window['-OUTPUT-'].update("started")
                #     if self.chatLocation == None:
                #         self.chatLocation = (570, 610, 800, 150) #(377, 405, 530, 103)
                #     self.ocrProcess = ot.begin(gui_queue, ocr_queue,self.chatLocation,self.additionalLangs,self.targetLanguage.lower())
                #     self.window['Start'].update(disabled=True)
                #     self.startedOcr = True
                # else:
                #     sg.popup('Invalid Target Language', '"' + self.targetLanguage +'" is not a valid language, please correct spelling of language.' )

            if event == 'Stop':
                if self.startedOcr:
                    # Make this a function for stopOcr()
                    self.startedOcr = False
                    gui_queue.put('Stop')
                    self.ocrProcess.join()
                    self.ocrProcess.close()
                    self.window['Start'].update(disabled=False)

                if self.overlayOpen:
                    self.closeGameOverlay()
                    # # Make this a function for closeGameOverlay()
                    # self.overlayOpen = False
                    # closeOverlayQueue.put('Stop')
                    # self.gameOverlayProc.join()
                    # self.gameOverlayProc.close()
                    # self.window['Launch Game Overlay'].update(disabled=False)

            if event == 'Launch Game Overlay':
                self.window['-OUTPUT-'].update("Switched output to GameOverlay")
                self.overlayOpen = True
                self.window['Launch Game Overlay'].update(disabled=True)
                self.gameOverlayProc = mp.Process(target=go.GameOverlayInterface, args=(overlayQueue,ocr_queue,closeOverlayQueue))
                self.gameOverlayProc.start()

            if event == 'UpdateProfiles':
                self.profiles = ph.getProfiles()
                self.window['selectedGame'].update([gameName.get('Profile') for gameName in self.profiles])
                # print('test')

            if event == 'Delete':
                # self.profiles[:] = [profile for profile in self.profiles if profile.get('Profile') != values['GameName']]
                if values.get('selectedGame'):
                    confirm = sg.popup_ok_cancel('Confirm Delete','Are you sure you want to delete the ' +str(values.get('selectedGame')[0])+' profile?')
                    if confirm == 'OK':
                        self.profiles[:] = [p for p in self.profiles if p.get('Profile') != values.get('selectedGame')[0]]
                        ph.saveProfiles(self.profiles)
                        self.window['selectedGame'].update([gameName.get('Profile') for gameName in self.profiles])


            self.checkIfOverlayClosed()

            self.mainPrintOutput()

        self.window.close()

    def closeGameOverlay(self):
        self.overlayOpen = False
        closeOverlayQueue.put('Stop')
        self.gameOverlayProc.join()
        self.gameOverlayProc.close()
        self.window['Launch Game Overlay'].update(disabled=False)

    def newProfilePopup(self,window):
        title = "Create A New Game Profile"
        layout = [
            [sg.Text('Profile Name:')],
            [sg.Input(key='ProfileName')],
            [sg.Text('Select Game:')],
            [sg.Combo(values = gm.getGames(),readonly=True,key='GameName')],
            [sg.Button('Custom Chat Location')],
            [sg.Button('Save'),sg.Button('Cancel')]
        ]
        win = sg.Window(title, layout, modal=True, grab_anywhere=True, enable_close_attempted_event=False,no_titlebar=False)
        while True:
            event, values = win.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break

            if event == 'Custom Chat Location':
                newCoords = bsc.getCoords()
                self.chatLocation = newCoords

            if event == 'Save':
                if not any(p.get('Profile', None) == values['ProfileName'] for p in self.profiles):
                # if values['ProfileName'] not in self.profiles.values():
                    self.profiles.append({
                        "Profile": values['ProfileName'],
                        "Game": values['GameName'],
                        "ChatLoc": self.chatLocation
                    })
                    ph.saveProfiles(self.profiles)
                    break
                else:
                    sg.popup('Invalid Profile Name', 'Profile name exists, Please enter something unique.' )

        win.close()
        window.write_event_value('UpdateProfiles', None)

    def start(self,values):
        self.targetLanguage = values.get('targetLang')
        if (self.targetLanguage.lower() in self.langsList):
            self.window['-OUTPUT-'].update("started")
            if self.chatLocation == None:
                # self.chatLocation = (570, 610, 800, 150) #(377, 405, 530, 103)

                sg.popup('Profile Not Selected', 'Please create a profile or select one to start.' )
            else:
                self.window['-OUTPUT-'].update("started")
                self.ocrProcess = ot.begin(gui_queue, ocr_queue,self.chatLocation,self.additionalLangs,self.targetLanguage.lower(),self.selectedGame)
                self.window['Start'].update(disabled=True)
                self.startedOcr = True
        else:
            sg.popup('Invalid Target Language', 'Please reselect a target Language. It will be saved for future use.' )

    def clear(self,q):
        try:
            while True:
                q.get_nowait()
        except Empty:
            pass

    def checkIfOverlayClosed(self):
        overlayStoppedFlag = ''
        try:
            overlayStoppedFlag = overlayQueue.get_nowait()    # see if something has been posted to Queue
        except Exception as e:                     # get_nowait() will get exception when Queue is empty
            overlayStoppedFlag = None                      # nothing in queue so do nothing
        if overlayStoppedFlag:
            print(f'Got a queue message {overlayStoppedFlag}!!!')
            self.window['Launch Game Overlay'].update(disabled=False)
            self.overlayOpen = False
            # break

    def mainPrintOutput(self):
        if not self.overlayOpen:
            outText = []
            try:
                for msg in ocr_queue.get(0):
                    if msg[0] == r'[':
                        continue
                    outText.append(msg)#+'\n'
                self.window['-OUTPUT-'].Update(''.join(outText))
                self.window.Refresh()
            except:
                pass


def main():
    global gui_queue
    global ocr_queue
    global overlayQueue
    global closeOverlayQueue

    ocr_queue = mp.Queue()
    gui_queue = mp.Queue()
    overlayQueue = mp.Queue()
    closeOverlayQueue = mp.Queue()
    mainGui = MainUserInterface()

if __name__ == '__main__':
    # pyinstallerTest
    mp.freeze_support()
    main()
