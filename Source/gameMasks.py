from typing import Match
import boxSelectChatbox as bsc
import cv2
import numpy as np
import mss
import pytesseract
import time
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def getGames():
    return ['Dota 2', 'League Of Legends','Default']

class maskClass:
    color1 = np.asarray([235])
    color2 = np.asarray([237])
    color3 = np.asarray([255])
    color4 = np.asarray([255])
    template = cv2.imread('ColonTemplate.png',0)
    templateWidth = template.shape[1]
    templateHeight = template.shape[0]
    threshold = 0.8
    sct = mss.mss()
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    def __init__(self,ChatCoord):
        self.x,self.y,self.w,self.h = self.getXYWH(ChatCoord)
        self.monitor = {"top": self.y, "left": self.x, "width": self.w, "height": self.h}
        # pass



    def getXYWH(self,ChatCoord):
        x = ChatCoord[0]
        y = ChatCoord[1]
        w= ChatCoord[2]
        h= ChatCoord[3]
        return x,y,w,h

    # def mask(self,gameName):
    #     gName = gameName
    #     match gName:
    #         case 'Dota 2':
    #             pass
    #     # match gName:
    #     #     case 'Dota 2':
    #     #         image = np.asarray(self.sct.grab(self.monitor))
    #     #         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     #         mask = cv2.inRange(image, self.color1, self.color2)
    #     #         mask2 = cv2.inRange(image, self.color3, self.color4)
    #     #         mask =  cv2.addWeighted(mask, 1, mask2, 0.7, 0.0);
    #     #         results = cv2.matchTemplate(mask,self.template,cv2.TM_CCOEFF_NORMED)
    #     #         loc = np.where( results >= self.threshold)
    #     #         for pt in zip(*loc[::-1]):
    #     #             cv2.rectangle(mask, pt, (pt[0] + self.templateWidth, pt[1] + self.templateHeight), (0,0,0),cv2.FILLED)
    #     #         return mask
    #     #     case 'League Of Legends':
    #     #         image = np.asarray(self.sct.grab(self.monitor))
    #     #         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     #         _, maskedImg = cv2.threshold(image, thresh=200, maxval=200, type=cv2.THRESH_BINARY)
    #     #         return maskedImg

    def getMask(self,gameName):
        mask = np.asarray(self.sct.grab(self.monitor))
        if gameName == 'Dota 2':
            # mask = np.asarray(self.sct.grab(self.monitor))
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask2 = cv2.inRange(mask, self.color3, self.color4)
            mask = cv2.inRange(mask, self.color1, self.color2)
            # mask2 = cv2.inRange(image, self.color3, self.color4)
            mask =  cv2.addWeighted(mask, 1, mask2, 0.7, 0.0);
            results = cv2.matchTemplate(mask,self.template,cv2.TM_CCOEFF_NORMED)
            loc = np.where( results >= self.threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(mask, pt, (pt[0] + self.templateWidth, pt[1] + self.templateHeight), (0,0,0),cv2.FILLED)
            mask = ~mask

        if gameName == 'League Of Legends':
            # mask = np.asarray(self.sct.grab(self.monitor))
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(mask, thresh=200, maxval=200, type=cv2.THRESH_BINARY)
            mask = ~mask

        return mask


    def leagueOfLegendsPreprocessing(self):

        # x,y,w,h = self.getXYWH(ChatCoord)
        # sct = mss.mss()
        # monitor = {"top": self.y, "left": self.x, "width": self.w, "height": self.h}
        image = np.asarray(self.sct.grab(self.monitor))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, maskedImg = cv2.threshold(image, thresh=200, maxval=200, type=cv2.THRESH_BINARY)
        return maskedImg

    def leagueOfLegendsPostprocessing(text):
        pass

    def dota2Preprocessing(self):
        # x,y,w,h = self.getXYWH(ChatCoord)
        # sct = mss.mss()
        # -1 i think gets primary monitor? 0 is all and then increments to the number they identify as. for example my primary is 2
        # monitor = {"top": self.y, "left": self.x, "width": self.w, "height": self.h}
        image = np.asarray(self.sct.grab(self.monitor))

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(image, self.color1, self.color2)
        mask2 = cv2.inRange(image, self.color3, self.color4)
        mask =  cv2.addWeighted(mask, 1, mask2, 0.7, 0.0);
        # cv2.imshow('mask',mask)
        results = cv2.matchTemplate(mask,self.template,cv2.TM_CCOEFF_NORMED)
        # cv2.imshow('results',results)
        # cv2.waitKey(40)
        loc = np.where( results >= self.threshold)
        for pt in zip(*loc[::-1]):
            # pass
            cv2.rectangle(mask, pt, (pt[0] + self.templateWidth, pt[1] + self.templateHeight), (0,0,0),cv2.FILLED)
            # cv2.rectangle(imgcv,(_x1,_y1),(_x2,_y2),(0,255,0),cv2.FILLED
        # pass

    def dota2Postprocessing(text):
        pass

def main():
    # print(bsc.getCoords())
    lolTest = maskClass((664, 577, 523, 195))
    while 1:
        # leagueOfLegendsPreprocessing((664, 577, 523, 195))
        # lolTest.leagueOfLegendsPreprocessing()
        lolTest.getMask('Dota 2')
    pass

if __name__ == '__main__':
    main()
