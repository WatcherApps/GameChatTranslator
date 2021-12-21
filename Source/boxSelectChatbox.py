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

    sct = mss.mss()
    # https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    primary = next((index for (index, d) in enumerate(sct.monitors) if d["left"] == 0), -1)
    image = np.asarray(sct.grab(sct.monitors[primary]))

    (origH, origW) = image.shape[:2]
    ratio = 1.5

    newW = origH/ratio
    newH = origW/ratio
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (int(newH), int(newW)))
    # (H, W) = image.shape[:2]

    def areaOfInterest(x,y,w,h):
        return(x, y, x+w, y+h)

    def cropAreaOfInterest(x,y,x2,y2,image):
        return image[y:y2, x:x2]

    bbox = cv2.selectROI("Drag Box Around Chat and press enter or c to cancel",image,False)
    print(bbox)
    # bbox returns x,y,w,h
    # use area of interest function to get starting and ending x,y coords for image
    x,y,x2,y2 = areaOfInterest(bbox[0],bbox[1],bbox[2],bbox[3])

    cv2.destroyWindow("Drag Box Around Chat and press enter or c to cancel")
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

    monitor = {"top": y, "left": x, "width": w, "height": h}
    image = np.asarray(sct.grab(monitor))
    cv2.imshow("image",image)
    cv2.waitKey(0)
if __name__ == '__main__':
    main()
