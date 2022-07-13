# BeatCatcher
A rhythm game that lets you use your own songs to play.

## Summary
BeatCatcher is a rhythm game with simple mechanics. In this game, you get to choose a song stored on your computer. As the game starts, notes will begin to fall from above in tune with the rhythm of the song. Using your mouse, try to catch as many notes as possible before the song ends.

## Detailed instructions
### Installation
1. Go to the **Release** section, find the version you want to use and download the `.exe` file from that version. The latest version is `0.1.1`
2. Open the `.exe` file, specify the folder in which you want the game to be saved, then press **Extract**. A folder named `dist` will appear at the specified location.
3. Go to `dist`, then run `launch.bat`, wait until the game window appear, then you're ready to go!<br>

:warning: **NOTE: On the first run, it might take a few seconds before the game starts loading its assets and libraries.**

### How to play
1. Click on the :arrow_forward:	**Play button**, then choose a song from your music library. This game natively supports `.wav` files. Non-WAV files are automatically converted using `ffmpeg` (already bundled with the game)
![helpPage0](https://user-images.githubusercontent.com/91553769/178778702-0804116b-c1f0-43e0-9677-cadbd635d3b5.png)
2. Throughout the game, notes fall from above in tune with the rhythm of the song. Move the pad at the bottom of the window with your mouse to collect the notes. Each **Note** gives you **200 points**, and each **Small Note** gives you **100 points**.
![helpPage1](https://user-images.githubusercontent.com/91553769/178778715-edfbc93c-77f7-4b8d-a1ff-3e5e0cdd9644.png)
![helpPage2](https://user-images.githubusercontent.com/91553769/178778718-7d2913d7-e0c6-4101-b19c-a9383f0e6f23.png)
3. At the end of the game, the number of notes catched and your total score are shown.
![helpPage3](https://user-images.githubusercontent.com/91553769/178778722-a38fb37c-4ff3-4d6f-a600-f6681fbaa05d.png)

### How to make modifications to this game / create your own version of the game
1. [Download Python (this project uses Python 3.10.5)](https://www.python.org/downloads/)
1. Download the source code of the game by clicking **Code -> Download Zip** or running this command via Git CLI: `git clone https://github.com/cykablyat12/BeatCatcher.git`
1. Navigate to the source code folder, then run these commands <br>
`py -m venv .venv` to create a virtual environment <br>
`.venv\Scripts\activate` to activate the virtual environment <br>
`py -m pip install -r requirements.txt` to install the dependencies. This includes `librosa v0.9.2`, `numpy v1.22.4` and `pygame v2.1.2`.<br>
:warning: **NOTE: Problems regarding the library `numba` may arise. Reinstalling `numba` and `librosa` may resolve this issue.**<br>
1. Edit the source code files and the assets as you wish, but making changes to the license file `COPYING` isn't allowed.
1. Build this project using a build tool of your choice. Be sure to put the files `COPYING`, `ffmpeg.exe` and the assets folder into the same folder as the game's executable (`.exe` file)
