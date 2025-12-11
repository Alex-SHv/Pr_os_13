import tkinter as tk
from views.game_view import GameView
from views.field_view import FieldCell
from views.barn_view import BarnWindow
from views.shop_view import ShopWindow

from models.tomato_model import Tomato
from models.cucumber_model import Cucumber
from models.carrot_model import Carrot
from models.fertilizers_model import fertilizers


class GameController:
    def __init__(self):
        self.view = GameView(self)

        self.money = 50
        self.inventory = {}
        self.barn_storage = {}
        self.barn_window = None

        self.view.create_field_cells(FieldCell, self)

        self.refresh_money()
        self.refresh_inventory()

        self.view.start()


    def add_item(self, plant_name):
        self.barn_storage[plant_name] = self.barn_storage.get(plant_name, 0) + 1
        self.refresh_barn()

    def remove_item(self, name, count):
        if name in self.barn_storage and self.barn_storage[name] >= count:
            self.barn_storage[name] -= count
            if self.barn_storage[name] == 0:
                del self.barn_storage[name]
        self.refresh_barn()

    def refresh_barn(self):
        if self.barn_window and self.barn_window.top.winfo_exists():
            self.barn_window.refresh()

    def open_barn(self):
        if self.barn_window is None or not self.barn_window.top.winfo_exists():
            self.barn_window = BarnWindow(self.view.root, self.barn_storage)
        else:
            self.barn_window.top.deiconify()
            self.barn_window.top.lift()

        self.refresh_barn()


    def refresh_money(self):
        self.view.update_money(self.money)

    def refresh_inventory(self):
        if not self.inventory:
            self.view.update_inventory("Удобрения: -")
        else:
            txt = "Удобрения: " + ", ".join([f"{k} ({v})" for k, v in self.inventory.items()])
            self.view.update_inventory(txt)


    def open_shop(self):
        ShopWindow(self.view.root, self, self.view)

    def open_plant_select(self, field):
        plants = [Carrot, Tomato, Cucumber]

        self.view.open_plant_window(
            finish_callback=lambda win, plant, fert: self.finish_plant(win, field, plant, fert),
            inventory=self.inventory,
            plants=plants
        )

    def finish_plant(self, win, field, plant, fert_name):
        fert_data = None

        if fert_name != "Нет":
            fert_data = fertilizers[fert_name]
            self.inventory[fert_name] -= 1
            if self.inventory[fert_name] == 0:
                del self.inventory[fert_name]

        self.refresh_inventory()
        field.plant_seed(plant, fert_data)
        win.destroy()

GameController()