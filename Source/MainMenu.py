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


gui_queue = None
ocr_queue = None
overlayQueue = None

class MainUserInterface:
    #this overlayOpen is used to swap printing from main window to game overlay.
    overlayOpen = False
    additionalLangs = ''
    targetLanguage = 'english'
    startedOcr = False

    ocrProcess = None
    gameOverlayProc = None

    def __init__(self):
        global gui_queue
        global ocr_queue
        global overlayQueue

        self.chatLocation = None
        col2 = sg.Column([[sg.Frame('Output:',
        [[sg.Column([[sg.Output(font=('Helvetica', '8','bold'), text_color = 'Black', key = '-OUTPUT-',background_color= 'White',size=(27,21)),]],size=(200,315))]])]],pad=(0,0))

        # https://github.com/tesseract-ocr/tessdoc/blob/main/Data-Files-in-different-versions.md
        language_Rkeys = ['rus']#,'kor'
        col1 = sg.Column([
            [sg.Frame('Settings:', [[sg.Text(), sg.Column([[sg.Text('Additional Character Set:')],
                                    [sg.Checkbox(text = name, default = False, enable_events=True,key=name ,size=(5,1)) for name in language_Rkeys],
                                    # [ sg.Radio('S. Chinese', 'radio1',enable_events=True, default=True, key='-SCHINESE-', size=(10,1)),
                                    # sg.Radio('Russian', 'radio1',enable_events=True, key='-RUSSIAN-',  size=(10,1))],
                                    [sg.Text('Target Language:')],
                                    [sg.Input(key='-LANG-IN-', default_text='english', size=(27,1), disabled=False)],
                                    [sg.Text('Game Profiles:')],
                                    [sg.Listbox(values=['Dota 2', 'Extra Cushions', 'Organic Diet','Blanket', 'Neck Rest'],highlight_background_color='#0083cb', select_mode='single', key='game', size=(25, 5))],
                                    # [sg.Listbox()]
                                    # [sg.Multiline(key='-PROFILE-', default_text='Dota 2', size=(25,5),disabled=True)],
                                    [sg.Button('Load',disabled=True), sg.Button('Delete',disabled=True)],
                                    ], size=(220,321), pad=(0,0))]])], ], pad=(0,0))

        col3 = sg.Column([[sg.Frame('Actions:',
                                    [[sg.Column([[sg.Button('Start'), sg.Button('Stop'), sg.Button('Custom Chat Location'),sg.Button('Launch Game Overlay'), ]],
                                                size=(460,45), pad=(0,0))]])]], pad=(0,0))

        # The final layout, 2 columns with one column below.
        self.layout = [sg.vtop([col1, col2]),
                [col3]]

        self.window = sg.Window('Game Chat Translator', self.layout)

        while True:
            event, values = self.window.read(timeout=10, timeout_key='timeout')

            if event in language_Rkeys:
                self.additionalLangs = ''
                for key in language_Rkeys:
                    if values.get(key):
                        self.additionalLangs += ('+' + key)

                if self.startedOcr == True:
                    with gui_queue.mutex:
                        gui_queue.queue.clear()
                    gui_queue.put('Stop')
                    self.ocrProcess.join()
                    self.ocrProcess.close()
                    ot.begin(gui_queue, ocr_queue,self.chatLocation,self.additionalLangs)

            if event == sg.WIN_CLOSED:
                gui_queue.put('Stop')
                break

            if event == 'Custom Chat Location':
                newCoords = bsc.getCoords()
                self.chatLocation = newCoords

            if event == 'Start':
                self.window['-OUTPUT-'].update("started")
                #  testing launching with defaults
                if self.chatLocation == None:
                    self.chatLocation = (570, 610, 800, 150) #(377, 405, 530, 103)
                ot.begin(gui_queue, ocr_queue,self.chatLocation,self.additionalLangs)
                self.window['Start'].update(disabled=True)
                self.startedOcr = True

            if event == 'Stop':
                gui_queue.put('Stop')
                self.window['Start'].update(disabled=False)



            if event == 'Launch Game Overlay':
                self.window['-OUTPUT-'].update("Switched output to GameOverlay")
                self.overlayOpen = True
                self.window['Launch Game Overlay'].update(disabled=True)
                self.gameOverlayProc = mp.Process(target=go.GameOverlayInterface, args=(overlayQueue,ocr_queue))
                self.gameOverlayProc.start()

            self.checkIfOverlayClosed()

            self.mainPrintOutput()

        self.window.close()

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

    ocr_queue = mp.Queue()
    gui_queue = mp.Queue()
    overlayQueue = mp.Queue()
    mainGui = MainUserInterface()

if __name__ == '__main__':
    main()
