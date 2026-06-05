import tkinter as tk

import customtkinter as ctk

from classes.UiAssets import UiAssets


class Shop:
    """Mario-themed companion panel for buying items, inventory, and quests."""

    def __init__(self, mario):
        self.mario = mario
        self.assets = UiAssets()

        ctk.set_appearance_mode("dark")

        self.window = ctk.CTk()
        self.window.title("Toad House Companion")
        self.window.geometry("860x650")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.closeShop)

        self.coinText = tk.StringVar(self.window)
        self.checkpointText = tk.StringVar(self.window)
        self.statusText = tk.StringVar(
            self.window,
            value=self.getOpeningMessage(),
        )

        self.inventoryLabels = {}
        self.questLabels = {}

        self.drawShop()
        self.refresh()

    def getOpeningMessage(self):
        if self.mario.shopMessage != "":
            message = self.mario.shopMessage
            self.mario.shopMessage = ""
            return message

        return "Welcome! Buy supplies, prepare your bag, then continue the level."

    def drawShop(self):
        self.window.configure(fg_color="#5C94FC")

        header = ctk.CTkFrame(
            self.window,
            height=112,
            corner_radius=0,
            fg_color="#E52521",
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="",
            image=self.assets.mario,
        ).pack(side="left", padx=(22, 8), pady=12)

        headerText = ctk.CTkFrame(header, fg_color="transparent")
        headerText.pack(side="left", pady=18)

        ctk.CTkLabel(
            headerText,
            text="TOAD HOUSE",
            font=("Arial Black", 27, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w")

        ctk.CTkLabel(
            headerText,
            text="Your in-level adventure companion",
            text_color="#FEE2E2",
        ).pack(anchor="w")

        balance = ctk.CTkFrame(header, fg_color="#B91C1C")
        balance.pack(side="right", padx=20, pady=22)

        ctk.CTkLabel(
            balance,
            text="",
            image=self.assets.coin,
        ).pack(side="left", padx=(10, 2), pady=5)

        ctk.CTkLabel(
            balance,
            textvariable=self.coinText,
            text_color="#FDE047",
            font=("Arial", 17, "bold"),
        ).pack(side="left", padx=(2, 12))

        content = ctk.CTkFrame(
            self.window,
            fg_color="#F7C873",
            corner_radius=0,
        )
        content.pack(fill="both", expand=True)

        tabs = ctk.CTkTabview(
            content,
            fg_color="#FFF3C4",
            segmented_button_selected_color="#E52521",
            segmented_button_selected_hover_color="#C41E1A",
            text_color="#1F2937",
        )
        tabs.pack(fill="both", expand=True, padx=18, pady=14)

        shopTab = tabs.add("SHOP")
        inventoryTab = tabs.add("INVENTORY")
        questsTab = tabs.add("QUESTS")

        self.drawShopTab(shopTab)
        self.drawInventoryTab(inventoryTab)
        self.drawQuestsTab(questsTab)

        footer = ctk.CTkFrame(
            content,
            fg_color="#8B4513",
            corner_radius=0,
        )
        footer.pack(fill="x")

        ctk.CTkLabel(
            footer,
            textvariable=self.statusText,
            text_color="#FFF7D6",
            font=("Arial", 12, "bold"),
        ).pack(side="left", padx=16, pady=13)

        ctk.CTkButton(
            footer,
            text="CONTINUE LEVEL",
            command=self.closeShop,
            width=170,
            height=34,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Arial", 12, "bold"),
        ).pack(side="right", padx=14, pady=8)

    def drawShopTab(self, tab):
        tab.configure(fg_color="#FFF3C4")

        items = [
            ("MUSHROOM", "Store a growth power-up in your bag.", 5, "#E52521", self.mario.buyMushroom),
            ("STAR SHIELD", "Store 10 seconds of enemy immunity.", 8, "#2563EB", self.mario.buyShield),
            ("SUPER JUMP", "Store an emergency vertical launch.", 3, "#16A34A", self.mario.buySuperJump),
            ("ENEMY CLEANER", "Store a nearby enemy remover.", 10, "#7C3AED", self.mario.buyEnemyCleaner),
        ]

        itemGrid = ctk.CTkFrame(tab, fg_color="transparent")
        itemGrid.pack(fill="x", padx=8, pady=(10, 4))

        for index, item in enumerate(items):
            self.drawShopItem(
                itemGrid,
                index // 2,
                index % 2,
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
            )

        checkpoint = ctk.CTkFrame(
            tab,
            fg_color="#8B4513",
            border_width=3,
            border_color="#5B2C06",
        )
        checkpoint.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(
            checkpoint,
            text="CHECKPOINT PIPE",
            text_color="#FDE047",
            font=("Arial", 14, "bold"),
        ).pack(side="left", padx=15, pady=14)

        ctk.CTkLabel(
            checkpoint,
            textvariable=self.checkpointText,
            text_color="#FFF7D6",
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            checkpoint,
            text="BUY  6 COINS",
            command=lambda: self.runAction(self.mario.buyCheckpoint),
            fg_color="#16A34A",
            hover_color="#15803D",
            width=120,
        ).pack(side="right", padx=14)

    def drawShopItem(self, parent, row, column, name, description, price, color, command):
        card = ctk.CTkFrame(
            parent,
            width=375,
            height=132,
            fg_color="#FFFFFF",
            border_width=3,
            border_color="#8B4513",
        )
        card.grid(row=row, column=column, padx=6, pady=6)
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text="",
            image=self.assets.mushroom,
        ).pack(side="left", padx=(12, 5))

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=4, pady=11)

        ctk.CTkLabel(
            info,
            text=name,
            text_color="#7C2D12",
            font=("Arial", 13, "bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=description,
            text_color="#4B5563",
            justify="left",
            wraplength=190,
        ).pack(anchor="w", pady=(2, 6))

        ctk.CTkButton(
            info,
            text="BUY  " + str(price),
            command=lambda: self.runAction(command),
            width=92,
            height=26,
            fg_color=color,
            hover_color=color,
            font=("Arial", 11, "bold"),
        ).pack(anchor="w")

    def drawInventoryTab(self, tab):
        tab.configure(fg_color="#FFF3C4")

        ctk.CTkLabel(
            tab,
            text="ITEM BAG",
            text_color="#7C2D12",
            font=("Arial Black", 19, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 2))

        ctk.CTkLabel(
            tab,
            text="Purchased items wait here until you activate them.",
            text_color="#4B5563",
        ).pack(anchor="w", padx=18, pady=(0, 12))

        items = [
            ("Mushroom", self.mario.useMushroom),
            ("Star Shield", self.mario.useShield),
            ("Super Jump", self.mario.useSuperJump),
            ("Enemy Cleaner", self.mario.useEnemyCleaner),
        ]

        for itemName, command in items:
            row = ctk.CTkFrame(
                tab,
                fg_color="#FFFFFF",
                border_width=2,
                border_color="#D97706",
            )
            row.pack(fill="x", padx=18, pady=5)

            ctk.CTkLabel(
                row,
                text=itemName.upper(),
                text_color="#7C2D12",
                font=("Arial", 13, "bold"),
                width=180,
                anchor="w",
            ).pack(side="left", padx=12, pady=11)

            amountText = tk.StringVar(self.window)
            self.inventoryLabels[itemName] = amountText
            ctk.CTkLabel(
                row,
                textvariable=amountText,
                text_color="#4B5563",
                width=80,
            ).pack(side="left")

            ctk.CTkButton(
                row,
                text="USE ITEM",
                command=lambda action=command: self.runAction(action),
                width=110,
                height=28,
                fg_color="#16A34A",
                hover_color="#15803D",
            ).pack(side="right", padx=12)

    def drawQuestsTab(self, tab):
        tab.configure(fg_color="#FFF3C4")

        ctk.CTkLabel(
            tab,
            text="TOAD MISSIONS",
            text_color="#7C2D12",
            font=("Arial Black", 19, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 2))

        ctk.CTkLabel(
            tab,
            text="Complete optional goals to earn bonus shop coins.",
            text_color="#4B5563",
        ).pack(anchor="w", padx=18, pady=(0, 12))

        for quest in self.mario.quests.getQuests():
            card = ctk.CTkFrame(
                tab,
                fg_color="#FFFFFF",
                border_width=2,
                border_color="#D97706",
            )
            card.pack(fill="x", padx=18, pady=6)

            ctk.CTkLabel(
                card,
                text=quest.title.upper(),
                text_color="#7C2D12",
                font=("Arial", 13, "bold"),
            ).pack(anchor="w", padx=14, pady=(10, 1))

            ctk.CTkLabel(
                card,
                text=quest.description + "  Reward: " + str(quest.reward) + " coins",
                text_color="#4B5563",
            ).pack(anchor="w", padx=14)

            progressText = tk.StringVar(self.window)
            self.questLabels[quest.title] = progressText
            ctk.CTkLabel(
                card,
                textvariable=progressText,
                text_color="#16A34A",
                font=("Arial", 12, "bold"),
            ).pack(anchor="w", padx=14, pady=(2, 9))

    def runAction(self, command):
        self.statusText.set(command())
        self.refresh()

    def refresh(self):
        self.coinText.set(str(self.mario.dashboard.coins) + " COINS")
        self.checkpointText.set("STATUS: " + self.mario.checkpoints.getStatus())

        for itemName, label in self.inventoryLabels.items():
            label.set("x" + str(self.mario.inventory.getAmount(itemName)))

        for quest in self.mario.quests.getQuests():
            label = self.questLabels[quest.title]

            if quest.completed:
                label.set("COMPLETED")
            else:
                label.set(str(quest.progress) + " / " + str(quest.target))

    def closeShop(self):
        self.window.destroy()

    def open(self):
        self.window.mainloop()
