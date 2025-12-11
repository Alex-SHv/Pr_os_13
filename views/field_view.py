import tkinter as tk
import threading
import time

class FieldCell:
    def __init__(self, root, x, y, index, game):
        self.state = "empty"
        self.plant = None         
        self.fertilizer = None     
        self.game = game
        self.index = index

        self.img_empty = None

        self.img_carrot_small      = tk.PhotoImage(file="Images/carrot/carrot.png")
        self.img_carrot_big        = tk.PhotoImage(file="Images/carrot/carrot_big.png")
        self.img_cucumber_small    = tk.PhotoImage(file="Images/cucumber/cucumber.png")
        self.img_cucumber_big      = tk.PhotoImage(file="Images/cucumber/cucumber_big.png")
        self.img_tomato_small      = tk.PhotoImage(file="Images/tomato/tomato.png")
        self.img_tomato_big        = tk.PhotoImage(file="Images/tomato/tomato_big.png")

        self.btn = tk.Button(root, text=f"Грядка {index+1}", bg="sienna4", fg="white", command=self.on_click)
        self.btn.place(x=x, y=y, width=200, height=200)

        self.label = tk.Label(root, text="Стадия: пусто", font=("Arial", 14))
        self.label.place(x=x, y=y+210, width=200, height=55)

        self.index = index

    def on_click(self):
        if self.state == "empty":
            self.game.open_plant_select(self)
        elif self.state == "ready":
            self.collect()

    def plant_seed(self, plant, fertilizer):
        self.state = "growing"
        self.plant = plant
        self.fertilizer = fertilizer

        img_small = {
            "Морковь": self.img_carrot_small,
            "Огурец": self.img_cucumber_small,
            "Помидор": self.img_tomato_small,
        }.get(plant.name)

        self.btn.config(image=img_small, bg="yellow", fg="black", text=plant.name)
        self.label.config(text="Стадия: растёт")

        grow_time = plant.baseGrowTime

        if fertilizer:
            grow_time *= fertilizer["multiplier"]

        threading.Thread(target=self.grow_timer, args=(grow_time,), daemon=True).start()

    def grow_timer(self, sleep_time):
        time.sleep(sleep_time)

        self.state = "ready"

        img_big = {
            "Морковь": self.img_carrot_big,
            "Огурец": self.img_cucumber_big,
            "Помидор": self.img_tomato_big,
        }.get(self.plant.name)

        self.btn.config(
            image=img_big,
            bg="green4",
            fg="white",
            text=f"{self.plant.name} (готово)"
        )
        self.label.config(text="Стадия: созрело")

    def collect(self):
        self.game.add_item(self.plant.name)

        self.state = "empty"
        self.btn.config(image="", bg="sienna4", fg="white", text=f"Грядка {self.index+1}")
        self.label.config(text="Стадия: пусто")

        self.plant = None
        self.fertilizer = None