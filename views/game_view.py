import tkinter as tk


class GameView:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Ферма")
        self.root.geometry("1000x500")

        tk.Button(self.root, text="Открыть амбар", font=("Arial", 12), command=self.controller.open_barn).place(x=800, y=100)
        tk.Button(self.root, text="Открыть магазин", font=("Arial", 12), command=self.controller.open_shop).place(x=800, y=140)
        tk.Button(self.root, text="Выход", font=("Arial", 12), command=self.root.destroy).place(x=800, y=180)

        self.money_label = tk.Label(self.root, text="", font=("Arial", 15))
        self.money_label.place(x=800, y=230)

        self.inv_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.inv_label.place(x=800, y=270)

        self.fields = []

    def create_field_cells(self, FieldCellClass, game):
        start_x = 100
        gap_x = 205
        y = 100

        for i in range(3):
            x = start_x + i * gap_x
            cell = FieldCellClass(self.root, x, y, i, game)
            self.fields.append(cell)

    def update_money(self, money):
        self.money_label.config(text=f"Баланс: {money}₴")

    def update_inventory(self, inv_text):
        self.inv_label.config(text=inv_text)

    def open_plant_window(self, finish_callback, inventory, plants):
        win = tk.Toplevel(self.root)
        win.title("Посадка")
        win.geometry("500x500")

        tk.Label(win, text="Выберите растение:", font=("Arial", 14)).pack(pady=10)

        fert_var = tk.StringVar(value="Нет")
        tk.Label(win, text="Удобрение:", font=("Arial", 12)).pack()

        opts = ["Нет"] + list(inventory.keys())
        tk.OptionMenu(win, fert_var, *opts).pack()

        tk.Label(win, text="", font=("Arial", 8)).pack()

        for plant in plants:
            p_obj = plant()
            tk.Button(win, text=p_obj.name, command=lambda p=p_obj: finish_callback(win, p, fert_var.get())).pack(pady=5)

        return win

    def start(self):
        self.root.mainloop()