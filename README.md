# GameChatTranslator

Hey everyone. In an attempt to try and bridge the gap between languages and reduce toxicity, I've created a tool to read the in-game chat, translate it, and display it in an overlay that has the ability to be clicked through. This isn't interacting with Dota or any game in any way. It's just taking screenshots of the desktop and reading an area of it. The overlay is a python-created window that is click-through enabled and the overlay can still be moved while playing the game, but the window grabbing area is currently very small.


Select if you want to run with cryillic (rus) char set.

Then select a target language.

Then create a game profile. This contains the game name, and stores the coords for the chat box.

Hit the "New" button and a games list will show. Select Dota 2.

Start a bot match and fill the chat with text to get the bounds of the chat box.

Head back to the translator app and hit Custom Chat Location and click and drag a box around the chat box in dota.

Save and hit start!


This will start translating text within the area selected on your main monitor and show it in the out put.
You then can launch the in game overlay by hitting the button "Launch Game Overlay".
To move the box try and click and drag the window by the text that says "Chat Output" as this box is mostly click through.

Demo video. Sorry for the length.
https://www.youtube.com/watch?v=Gk9X52-XJ8c

Reddit post contains gifs.
https://www.reddit.com/r/DotA2/comments/s6ygu6/ive_created_a_ingame_chat_translator_tool/















------------

#Features

Real-time translation: The tool instantly translates in-game chat messages into the user's preferred language.
Overlay display: Translated messages are displayed in an overlay that can be clicked through, allowing seamless integration with the gameplay experience.
Compatibility: The tool works with games of any resolution, thanks to its adaptable chat reading mechanism.
Wide language support: It can translate chat messages into any language supported by Google Translator.
Future development: The project aims to improve the user interface, scalability, and compatibility with different platforms, as well as expanding language support.

-----------
#Installation
##Prerequisites

pip install deep-translator

pip install opencv-python

pip install numpy

pip install Pillow

pip install mss

pip install PySimpleGUI

pip install pytesseract

https://github.com/tesseract-ocr/tesseract/releases

https://github.com/UB-Mannheim/tesseract/wiki

Install additional language and script models

https://github.com/UB-Mannheim/tesseract/wiki/Install-additional-language-and-script-models

the newest tesseract 5.0 exe from this place was having issues getting additional languages.
looks like we need to manually get them.
I'll grab the ones we will support first i guess.
English will handle most of the work for video games, this is just for new characters.

https://tesseract-ocr.github.io/tessdoc/Data-Files

https://github.com/tesseract-ocr/tessdata_fast
