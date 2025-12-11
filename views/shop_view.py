import tkinter as tk
import threading
import time
from models.fertilizers_model import fertilizers
from tkinter import messagebox

class ShopWindow:
    def __init__(self, parent, game, game_view):
        self.game = game
        self.game_view = game_view

        self.top = tk.Toplevel(parent)
        self.top.title("Магазин")
        self.top.geometry("500x500")

        tk.Label(self.top, text="Баланс:", font=("Arial", 14)).pack()
        self.money_label = tk.Label(self.top, text=f"{self.game.money} ₴", font=("Arial", 14))
        self.money_label.pack()

        tk.Label(self.top, text="\nУдобрения:", font=("Arial", 16)).pack()

        for name, data in fertilizers.items():
            price = data["price"]
            tk.Button(
                self.top,
                text=f"{name} ({price} ₴)",
                command=lambda n=name: self.buy_fertilizer(n)
            ).pack(pady=3)

        tk.Label(self.top, text="\nПродажа урожая:", font=("Arial", 16)).pack()

        self.sell_frame = tk.Frame(self.top)
        self.sell_frame.pack()

        self.refresh_sell_buttons()

    def refresh_sell_buttons(self):
        for widget in self.sell_frame.winfo_children():
            widget.destroy()

        if not self.game.barn_storage:
            tk.Label(self.sell_frame, text="Амбар пуст").pack()
            return

        for name, count in self.game.barn_storage.items():
            tk.Button(self.sell_frame, text=f"Продать {name} ({count} шт)", command=lambda n=name: self.sell(n)).pack(pady=3)

    def sell(self, name):
        price = 12 

        self.game.remove_item(name, 1)
        self.game.money += price

        self.money_label.config(text=f"{self.game.money} ₴")
        self.game_view.update_money(self.game.money)

        self.refresh_sell_buttons()

    def buy_fertilizer(self, name):
        cost = fertilizers[name]["price"]

        if self.game.money < cost:
            messagebox.showinfo("Ошибка", "Недостаточно денег!")
            return

        self.game.money -= cost

        self.game.inventory[name] = self.game.inventory.get(name, 0) + 1

        self.money_label.config(text=f"{self.game.money} ₴")
        self.game_view.update_money(self.game.money)
        self.game.refresh_inventory()