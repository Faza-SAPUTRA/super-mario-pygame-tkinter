# Super Mario Implementation in Python

This is inspired by Meth-Meth-Method's [super mario game](https://github.com/meth-meth-method/super-mario/)

## Running

* $ pip install -r requirements.txt
* $ python main.py

The game starts with a Tkinter launcher. Use it to select a level, configure
audio volume, enable fullscreen mode, or read the controls guide before
starting the pygame window. Reach the flag at the end of the map to finish.
The adventure contains three ordered levels. Completing a flag automatically
continues to the next level, and the third flag finishes the campaign.

While playing, press `B` to open the Tkinter helper shop. Coins collected in
the level can be spent on power-ups and emergency assistance. Purchased items
are stored in an inventory until activated. The companion window also contains
optional quests and a one-use checkpoint pipe.

## Standalone windows build

* $ pip install py2exe
* $ python compile.py py2exe

## Controls

* Left: Move left  
* Right: Move right  
* Space: Jump  
* Shift: Boost   
* B: Open helper shop
* Down: Enter a configured green warp pipe while standing on top of it
* Left/Right Mouseclick: secret   

## Current state:
![Alt text](img/pics.png "current state")

## Dependencies	
* pygame	
* scipy	
* tkinter (included with most Python installations)
* customtkinter
* pillow

## Team Progress

Project ini dibagi menjadi beberapa area kerja agar progress tim mudah
dijelaskan saat presentasi:

| Nama | Fokus |
| --- | --- |
| Fatir Zaidan | Gameplay utama, campaign, shop, inventory, quest, checkpoint, dan integrasi akhir |
| Ghazi | Launcher Tkinter, setting audio, pilihan level, dan testing fitur setting |
| Kala | Level design, balancing koin/enemy, dan testing manual setiap level |
| Rafa Rabbani | Dokumentasi, aset UI, panduan kontrol, dan bahan presentasi |

File progress per anggota tersedia di folder `team_progress/`.

## Contribution

If you have any Improvements/Ideas/Refactors feel free to contact me or make a Pull Request.
The code needs still alot of refactoring as it is right now, so I appreciate any kind of Contribution.
