import numpy as np
import mss
import cv2
import pytesseract
from deep_translator import GoogleTranslator
import multiprocessing as mp
import time



# ChatCoord = (560, 610, 800, 150)
# x = ChatCoord[0]
# y = ChatCoord[1]
# w= ChatCoord[2]
# h= ChatCoord[3]
# color1 = np.asarray([235])
# color2 = np.asarray([237])
# color3 = np.asarray([255])
# color4 = np.asarray([255])
# template = cv2.imread('ColonTemplate.png',0)
# # template.astype(np.uint8)
# cv2.imshow('template',template)
# cv2.waitKey(40)
# tw = template.shape[1]
# th = template.shape[0]
# threshold = 0.8

# while True:

#     sct = mss.mss()
#     # -1 i think gets primary monitor? 0 is all and then increments to the number they identify as. for example my primary is 2
#     monitor = {"top": y, "left": x, "width": w, "height": h}
#     image = np.asarray(sct.grab(monitor))
#     cv2.imshow('image',image)
#     cv2.waitKey(40)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('image',image)
#     cv2.waitKey(40)
#     # mask = image
#     mask = cv2.inRange(image, color1, color2)

#     results = cv2.matchTemplate(mask,template,cv2.TM_CCOEFF_NORMED)
#     cv2.imshow('results',results)
#     cv2.waitKey(40)
#     loc = np.where( results >= threshold)
#     for pt in zip(*loc[::-1]):
#         pass
#         cv2.rectangle(mask, pt, (pt[0] + tw, pt[1] + th), (0,0,0),cv2.FILLED)
#         # cv2.rectangle(imgcv,(_x1,_y1),(_x2,_y2),(0,255,0),cv2.FILLED


#     cv2.imshow('mask2',mask)

#     pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
#     text = pytesseract.image_to_string(mask, lang=('eng+rus'), config=' -c page_separator='' --psm 6') #--oem 1
#     print(f"Text extracted using image_to_string: \n {text}")

#     try:
#         translated = GoogleTranslator(source='auto', target='en').translate(text)
#     except:
#         translated = text
#     print(f"Translated Text extracted using image_to_string: \n {translated}")


#     cv2.waitKey(500)


def begin(gui_queue, ocr_queue,coords,langs):
    ocrProc = mp.Process(target=startOcr, args=(gui_queue,ocr_queue,coords))
    ocrProc.start()
    return ocrProc

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def startOcr(gui_queue, ocr_queue, ChatCoord):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    x = ChatCoord[0]
    y = ChatCoord[1]
    w= ChatCoord[2]
    h= ChatCoord[3]
    color1 = np.asarray([235])
    color2 = np.asarray([237])
    color3 = np.asarray([255])
    color4 = np.asarray([255])

    while True:

        try:
            message = gui_queue.get_nowait()    # see if something has been posted to Queue
        except Exception as e:                     # get_nowait() will get exception when Queue is empty
            message = None                      # nothing in queue so do nothing
        if message:
            print(f'Got a queue message {message}!!!')
            break

        sct = mss.mss()
        # -1 i think gets primary monitor? 0 is all and then increments to the number they identify as. for example my primary is 2
        monitor = {"top": y, "left": x, "width": w, "height": h}
        image = np.asarray(sct.grab(monitor))

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(image, color1, color2)

        # Extract text
        text = pytesseract.image_to_string(mask, lang='rus', config='--psm 6 -c page_separator=''')
        print(f"Text extracted using image_to_string: \n {text}")

        # results = reader.readtext(mask,decoder='greedy',width_ths = 1.5)#workers=4,
        # results = reader.readtext(image)
        # outputText = []

        # loop over the results
        # for (bbox, text, prob) in results:
        #     text = cleanup_text(text)
        #     # print(text)
        # if text[0] == '♀':
        #     continue
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
        except:
            translated = text
        #     outputText.append(translated)#+'\n'
        ocr_queue.put(translated)
        time.sleep(2)
        # print(outputText)
        # i=0
    # return outputText