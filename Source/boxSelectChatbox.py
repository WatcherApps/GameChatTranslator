import numpy as np
import cv2 as cv2
from PIL import ImageGrab
import mss

# Soloution to the hard coding problem is to just hardcode a ratio in which to resize display and then resize back to full!
#
# sct = mss.mss()
# image = np.asarray(sct.grab(sct.monitors[-1]))
# (origH, origW) = image.shape[:2]
# ratioW = 1.5#origW / newW
# ratioH = 1.5#origH / newH
# newW = origH/ratioW
# newH = origW/ratioH
# image = cv2.resize(image, (int(newH), int(newW)))
# cv2.imshow("image",image)
# cv2.waitKey(0)
def getCoords():

    # Taking screenshot from primary monitor, this can be changed later check mss documentation
    # with mss.mss() as sct:
    # # The screen part to capture
    #     monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
    #     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    #     # Grab the data
    #     sct_img = sct.grab(monitor)

    # with mss.mss() as sct:
    sct = mss.mss()
    # -1 i think gets primary monitor? 0 is all and then increments to the number they identify as. for example my primary is 2
    image = np.asarray(sct.grab(sct.monitors[-1]))
    # cv2.imshow("filename",img)
    # cv2.waitKey(0)

    # deskimage = ImageGrab.grab()
    # image = np.array(deskimage)
    (origH, origW) = image.shape[:2]
    # set the new width and height and then determine the ratio in change
    # for both the width and height
    # (newW, newH) = (1366,768)
    ratio = 1.5#origW / newW
    # ratioH = 1.5#origH / newH
    newW = origH/ratio
    newH = origW/ratio
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (int(newH), int(newW)))
    # (H, W) = image.shape[:2]

    def areaOfInterest(x,y,w,h):
        return(x, y, x+w, y+h)

    def cropAreaOfInterest(x,y,x2,y2,image):
        return image[y:y2, x:x2]

    bbox = cv2.selectROI("Drag Box Around Chat",image,False)
    print(bbox)
    # bbox returns x,y,w,h
    # use area of interest function to get starting and ending x,y coords for image
    x,y,x2,y2 = areaOfInterest(bbox[0],bbox[1],bbox[2],bbox[3])

    # deskimage = ImageGrab.grab()
    # image2 = np.array(deskimage)
    # cropImg2 = cropAreaOfInterest(int(x*ratioW),int(y*ratioH),int(x2*ratioW),int(y2*ratioH),image2)
    # cv2.imshow('cropImg2', cropImg2)
    # cv2.waitKey(1)
    cv2.destroyWindow("Drag Box Around Chat")
    # return (int(x*ratioW),int(y*ratioH),int(x2*ratioW),int(y2*ratioH))
    # using mss as our new screenshot tool i think i can just return the bbox coords after making them 1.5x bigger
    return (int(bbox[0]*ratio),int(bbox[1]*ratio),int(bbox[2]*ratio),int(bbox[3]*ratio))


def main():
    ChatCoord = getCoords()
    x = ChatCoord[0]
    y = ChatCoord[1]
    w= ChatCoord[2]
    h= ChatCoord[3]
    sct = mss.mss()
    # -1 i think gets primary monitor? 0 is all and then increments to the number they identify as. for example my primary is 2
    monitor = {"top": y, "left": x, "width": w, "height": h}
    image = np.asarray(sct.grab(monitor))
    cv2.imshow("image",image)
    cv2.waitKey(0)
    # global gui_queue
    # global ocr_queue
    # ocr_queue = mp.Queue()
    # gui_queue = mp.Queue()
    # # gui = GraphicalUserInterface()
    # startOcr(gui_queue,ocr_queue,(560,595,500,300))
if __name__ == '__main__':
    main()
