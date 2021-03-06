#   Todo -
#       main menu, Choose langages : this can control masking color, translation language target and easyocr language reader
#       implement boxSelectChatbox Location to the main menu when user doesnt want to use default location
#       front end with node/electron

# https://python-mss.readthedocs.io/examples.html
# https://www.codegrepper.com/code-examples/python/mss+grab+part+of+screen

# from easyocr import Reader
# import numpy as np
# import cv2 as cv2
# from PIL import ImageGrab
# https://realpython.com/pysimplegui-python/
import PySimpleGUI as sg
# import time
# import torch.multiprocessing as mp
import multiprocessing as mp
# from deep_translator import GoogleTranslator
# import mss
# gui_queue = None
# ocr_queue = None


class GameOverlayInterface: #rename to gameoverlayinterface
    global overlayQueue
    global ocr_queue
    global closeOverlayQueue
    def __init__(self,oQueue,ocrQueue,closeQueue):
        self.overlayQueue = oQueue
        self.ocr_queue = ocrQueue
        self.closeOverlayQueue = closeQueue
        # global gui_queue
        # global ocr_queue
        sg.theme('DarkBlack') # give our window a spiffy set of colors

        layout = [
                [sg.Text(size=(50,10),font=('Helvetica', '8','bold'), text_color = 'White', key = '_OUTPUT_',background_color= 'grey')],
                # [sg.Output(size=(50, 10), font=('Helvetica', '8','bold'), text_color = 'White', key = '_OUTPUT_',background_color= 'grey')],
                [sg.Image('./118639_move_icon.png', size=(32, 30),background_color='lightgrey'),sg.Button('Exit')]
                ]
        # frame = [sg.Frame('Chat Output', [sg.Text(size=(50,10),font=('Helvetica', '8','bold'), text_color = 'White', key = '_OUTPUT_',background_color= 'grey')],),]

        col1 = sg.Column([[sg.Frame('Chat Output:', [
            [sg.Column([
                [sg.Text(size=(40,10),font=('Helvetica', '8','bold'), text_color = 'White', key = '_OUTPUT_',background_color= 'grey'),]
            ],background_color='grey')]#,size=(200,315)
        ],background_color='grey')]],background_color='grey',pad=(0,0))

        layout = [[col1,sg.Image('./118639_move_icon.png', size=(32, 30),background_color='lightgrey')],
                [sg.Image('./118639_move_icon.png', size=(32, 30),background_color='lightgrey'),sg.Button('Exit')]]

        self.window = sg.Window('Chat window', layout, font=('Helvetica', ' 13','bold'),background_color='grey', default_button_element_size=(1,1), use_default_focus=False,
                    transparent_color='grey',alpha_channel=1,titlebar_background_color='black', no_titlebar=True,grab_anywhere=True,keep_on_top=True,enable_close_attempted_event=True, location=sg.user_settings_get_entry('-location-', (None, None)))

        while True:  # Event Loop
            event, values = self.window.read(timeout=100, timeout_key='timeout')#,timeout_key='timeout'timeout=500
            # self.window.KeepOnTop = True
            self.window.bring_to_front()
            # print(event, values)
            # print("test take over")
            # self.window['_OUTPUT_'].Update('')
            if event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'):
                self.overlayQueue.put('Stop')

                sg.user_settings_set_entry('-location-', self.window.current_location())  # The line of code to save the position before exiting
                break
            # if event == 'Start':
            #     # Update the "output" text element to be the value of "input" element
            #     self.window['_OUTPUT_'].update("started")
            #     begin(gui_queue, ocr_queue)
            self.printOutput()

            if self.checkForStop():
                break
            # print('realtest')
            # self.window.refresh()
            # self.window.TKroot.after(1000, self.printOutput)
        self.window.close()

    def printOutput(self):
        # self.window['_OUTPUT_'].Update('')
        # print(ocr_queue.get())
        outText = []
        try:
            for msg in self.ocr_queue.get(0):
                if msg[0] == r'[':
                    continue
        # https://medium.com/analytics-vidhya/how-to-translate-text-with-python-9d203139dcf5
                # print(msg)
                outText.append(msg)#+'\n'
            self.window['_OUTPUT_'].Update(''.join(outText))
        except:
            pass
        # self.window.refresh()
        # self.window.TKroot.after(1000, self.printOutput)

    def checkForStop(self):
        stop = False
        try:
            message = self.closeOverlayQueue.get_nowait()    # see if something has been posted to Queue
        except Exception as e:                     # get_nowait() will get exception when Queue is empty
            message = None                      # nothing in queue so do nothing
        if message:
            print(f'Got a queue message {message}!!!')
            # break
            stop = True
        return stop




def main():
    global overlayQueue
    global ocr_queue
    ocr_queue = mp.Queue()
    overlay_Queue = mp.Queue()
    global closeOverlayQueue
    closeOverlayQueue = mp.Queue()
    gui = GameOverlayInterface(overlay_Queue,ocr_queue,closeOverlayQueue)
    # startOcr(gui_queue,ocr_queue,(560,595,500,300))

if __name__ == '__main__':
    main()

# # https://github.com/PySimpleGUI/PySimpleGUI/issues/1077
# # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Notification_Window_Multiprocessing.py
# # https://stackoverflow.com/questions/60213167/pysimplegui-how-to-make-transparent-click-through-window
# # https://github.com/PySimpleGUI/PySimpleGUI/issues/2525
# # https://docs.python.org/3/library/multiprocessing.html