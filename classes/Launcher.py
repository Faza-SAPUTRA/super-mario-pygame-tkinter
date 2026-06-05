import json
import tkinter as tk

import customtkinter as ctk

from classes.UiAssets import UiAssets


class Launcher:
    """Mario-themed startup window for level selection and local preferences."""

    def __init__(self, settingsUrl):
        self.settingsUrl = settingsUrl
        self.startGame = False
        self.levelNames = self.loadLevelNames()
        self.levelButtons = {}
        self.assets = UiAssets()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Super Mario Python Launcher")
        self.window.geometry("900x610")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.closeLauncher)

        settings = self.loadSettings()
        self.selectedLevel = tk.StringVar(self.window, value=settings["selectedLevel"])
        self.fullscreen = tk.BooleanVar(self.window, value=settings["fullscreen"])
        self.music = tk.BooleanVar(self.window, value=settings["sound"])
        self.sfx = tk.BooleanVar(self.window, value=settings["sfx"])
        self.musicVolume = tk.IntVar(self.window, value=settings["musicVolume"])
        self.sfxVolume = tk.IntVar(self.window, value=settings["sfxVolume"])

        self.drawLauncher()
        self.selectLevel(self.selectedLevel.get())

    def loadLevelNames(self):
        return [
            "Level1-1",
            "Level1-2",
            "Level1-3",
        ]

    def loadSettings(self):
        defaultLevel = self.levelNames[0]
        defaultSettings = {
            "sound": True,
            "sfx": True,
            "musicVolume": 20,
            "sfxVolume": 20,
            "selectedLevel": defaultLevel,
            "fullscreen": False,
        }

        try:
            with open(self.settingsUrl) as jsonData:
                settings = json.load(jsonData)

            for key in defaultSettings:
                if key not in settings:
                    settings[key] = defaultSettings[key]

            if settings["selectedLevel"] not in self.levelNames:
                settings["selectedLevel"] = defaultLevel

            return settings
        except (IOError, OSError, json.JSONDecodeError):
            return defaultSettings

    def loadLevelInfo(self, levelName):
        with open("./levels/" + levelName + ".json") as jsonData:
            data = json.load(jsonData)

        entities = data["level"].get("entities", {})
        coinCount = len(entities.get("coin", [])) + len(entities.get("CoinBox", []))
        enemyCount = len(entities.get("Goomba", [])) + len(entities.get("Koopa", []))

        return {
            "length": data["length"],
            "coins": coinCount,
            "enemies": enemyCount,
        }

    def getSettings(self):
        return {
            "sound": self.music.get(),
            "sfx": self.sfx.get(),
            "musicVolume": self.musicVolume.get(),
            "sfxVolume": self.sfxVolume.get(),
            "selectedLevel": self.selectedLevel.get(),
            "fullscreen": self.fullscreen.get(),
        }

    def saveSettings(self):
        with open(self.settingsUrl, "w") as outfile:
            json.dump(self.getSettings(), outfile, indent=4)

    def drawLauncher(self):
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(
            self.window,
            width=245,
            corner_radius=0,
            fg_color="#111827",
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        self.drawSidebar(sidebar)

        content = ctk.CTkFrame(
            self.window,
            corner_radius=0,
            fg_color="#1F2937",
        )
        content.grid(row=0, column=1, sticky="nsew")

        tabs = ctk.CTkTabview(
            content,
            width=610,
            height=500,
            fg_color="#111827",
            segmented_button_selected_color="#DC2626",
            segmented_button_selected_hover_color="#B91C1C",
        )
        tabs.pack(fill="both", expand=True, padx=24, pady=22)

        playTab = tabs.add("PLAY")
        audioTab = tabs.add("AUDIO")
        controlsTab = tabs.add("CONTROLS")

        self.drawPlayTab(playTab)
        self.drawAudioTab(audioTab)
        self.drawControlsTab(controlsTab)

    def drawSidebar(self, sidebar):
        ctk.CTkLabel(
            sidebar,
            text="",
            image=self.assets.titleLogo,
        ).pack(anchor="w", padx=0, pady=(22, 0))

        ctk.CTkLabel(
            sidebar,
            text="PYTHON EDITION",
            text_color="#F9FAFB",
            font=("Arial", 14, "bold"),
        ).pack(anchor="w", padx=24, pady=(8, 34))

        ctk.CTkLabel(
            sidebar,
            text="TOAD TIP",
            text_color="#F87171",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w", padx=24)

        tip = (
            "Collect coins during the\n"
            "level and press B to buy\n"
            "emergency items."
        )
        ctk.CTkLabel(
            sidebar,
            text=tip,
            text_color="#D1D5DB",
            font=("Arial", 12),
            justify="left",
        ).pack(anchor="w", padx=24, pady=(4, 0))

        ctk.CTkButton(
            sidebar,
            text="START ADVENTURE",
            command=self.playGame,
            width=195,
            height=48,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Arial", 13, "bold"),
        ).pack(side="bottom", padx=24, pady=(0, 12))

        ctk.CTkButton(
            sidebar,
            text="EXIT GAME",
            command=self.closeLauncher,
            width=195,
            height=36,
            fg_color="transparent",
            hover_color="#374151",
            border_width=1,
            border_color="#4B5563",
        ).pack(side="bottom", padx=24, pady=(0, 10))

    def drawPlayTab(self, tab):
        ctk.CTkLabel(
            tab,
            text="CAMPAIGN MAP",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 3))

        ctk.CTkLabel(
            tab,
            text="Preview each route. Every adventure begins at WORLD 1-1.",
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=18, pady=(0, 12))

        levels = ctk.CTkScrollableFrame(
            tab,
            height=135,
            fg_color="#1F2937",
        )
        levels.pack(fill="x", padx=18)

        for index, levelName in enumerate(self.levelNames):
            button = ctk.CTkButton(
                levels,
                text=levelName.replace("Level", "WORLD "),
                command=lambda name=levelName: self.selectLevel(name),
                width=155,
                height=48,
                fg_color="#374151",
                hover_color="#4B5563",
                font=("Arial", 12, "bold"),
            )
            button.grid(row=index // 3, column=index % 3, padx=6, pady=6)
            self.levelButtons[levelName] = button

        self.levelInfo = ctk.CTkLabel(
            tab,
            text="",
            justify="left",
            anchor="w",
            font=("Courier New", 13, "bold"),
            text_color="#FDE68A",
        )
        self.levelInfo.pack(fill="x", padx=24, pady=(16, 4))

        ctk.CTkSwitch(
            tab,
            text="Launch in fullscreen mode",
            variable=self.fullscreen,
            progress_color="#DC2626",
        ).pack(anchor="w", padx=24, pady=(8, 0))

    def selectLevel(self, levelName):
        self.selectedLevel.set(levelName)

        for name, button in self.levelButtons.items():
            if name == levelName:
                button.configure(fg_color="#DC2626")
            else:
                button.configure(fg_color="#374151")

        levelInfo = self.loadLevelInfo(levelName)
        text = (
            levelName.replace("Level", "WORLD ")
            + "\n"
            + "DISTANCE  "
            + str(levelInfo["length"])
            + " tiles\n"
            + "COINS     "
            + str(levelInfo["coins"])
            + "\n"
            + "ENEMIES   "
            + str(levelInfo["enemies"])
            + "\n\n"
            + "Reach the red flag to continue. The third flag wins the campaign."
        )
        self.levelInfo.configure(text=text)

    def drawAudioTab(self, tab):
        ctk.CTkLabel(
            tab,
            text="AUDIO SETTINGS",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 3))

        ctk.CTkLabel(
            tab,
            text="Tune the game audio before the adventure begins.",
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=18, pady=(0, 18))

        self.drawVolumeCard(
            tab,
            "BACKGROUND MUSIC",
            "Classic level soundtrack",
            self.music,
            self.musicVolume,
        )
        self.drawVolumeCard(
            tab,
            "SOUND EFFECTS",
            "Coins, jumps, enemies, and power-ups",
            self.sfx,
            self.sfxVolume,
        )

    def drawVolumeCard(self, parent, title, description, enabled, volume):
        card = ctk.CTkFrame(parent, fg_color="#1F2937")
        card.pack(fill="x", padx=18, pady=8)

        ctk.CTkSwitch(
            card,
            text=title,
            variable=enabled,
            font=("Arial", 13, "bold"),
            progress_color="#DC2626",
        ).pack(anchor="w", padx=16, pady=(14, 2))

        ctk.CTkLabel(
            card,
            text=description,
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=16)

        sliderRow = ctk.CTkFrame(card, fg_color="transparent")
        sliderRow.pack(fill="x", padx=16, pady=(8, 14))

        ctk.CTkSlider(
            sliderRow,
            from_=0,
            to=100,
            variable=volume,
            progress_color="#FACC15",
            button_color="#FACC15",
            button_hover_color="#EAB308",
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            sliderRow,
            textvariable=volume,
            width=42,
            font=("Arial", 12, "bold"),
        ).pack(side="left", padx=(12, 0))

    def drawControlsTab(self, tab):
        ctk.CTkLabel(
            tab,
            text="PLAYER GUIDE",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 3))

        ctk.CTkLabel(
            tab,
            text="A quick reference for the controls you will use most.",
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=18, pady=(0, 14))

        controls = [
            ("LEFT / RIGHT", "Move Mario"),
            ("SPACE / UP", "Jump"),
            ("SHIFT", "Boost while running"),
            ("B", "Open the helper shop"),
            ("DOWN", "Enter a green warp pipe"),
            ("ESC / F5", "Pause the game"),
            ("ENTER", "Confirm a menu selection"),
        ]

        for key, description in controls:
            row = ctk.CTkFrame(tab, fg_color="#1F2937")
            row.pack(fill="x", padx=18, pady=4)

            ctk.CTkLabel(
                row,
                text=key,
                width=135,
                text_color="#FACC15",
                font=("Courier New", 12, "bold"),
                anchor="w",
            ).pack(side="left", padx=14, pady=9)

            ctk.CTkLabel(
                row,
                text=description,
                anchor="w",
            ).pack(side="left", padx=4)

    def playGame(self):
        self.saveSettings()
        self.startGame = True
        self.window.destroy()

    def closeLauncher(self):
        self.startGame = False
        self.window.destroy()

    def open(self):
        self.window.mainloop()

        if self.startGame:
            return self.getSettings()

        return None
