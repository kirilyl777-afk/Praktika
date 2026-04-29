import tkinter as tk
from tkinter import ttk
import math

class CircleButton:
    """Красивая круглая кнопка на Canvas с hover и анимацией клика."""
    def __init__(self, canvas, x, y, radius, text, color='#FFD700',
                 hover_color='#FFEA00', click_color='#FFA500', command=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.radius = radius
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.command = command

        # Основной круг
        self.circle = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline='#B8860B', width=4
        )
        # Тень (сдвинутый тёмный круг позади)
        self.shadow = canvas.create_oval(
            x - radius + 4, y - radius + 4, x + radius + 4, y + radius + 4,
            fill='#000000', outline='' 
        )
        canvas.tag_lower(self.shadow, self.circle)  # тень под кнопкой

        # Текст на кнопке
        self.label = canvas.create_text(
            x, y, text=text, font=('Arial', 16, 'bold'), fill='#2b2b2b'
        )

        # Привязка событий
        for item in (self.circle, self.label):
            canvas.tag_bind(item, '<Button-1>', self.on_click)
            canvas.tag_bind(item, '<Enter>', self.on_enter)
            canvas.tag_bind(item, '<Leave>', self.on_leave)

    def on_click(self, event):
        if self.command:
            self.command()
        self.animate_click()

    def on_enter(self, event):
        self.canvas.itemconfig(self.circle, fill=self.hover_color)

    def on_leave(self, event):
        self.canvas.itemconfig(self.circle, fill=self.color)

    def animate_click(self):
        # Уменьшаем радиус на 6 пикселей для эффекта нажатия
        r = self.radius - 6
        self.canvas.coords(self.circle,
                           self.x - r, self.y - r,
                           self.x + r, self.y + r)
        self.canvas.itemconfig(self.circle, fill=self.click_color)
        self.canvas.after(100, self.restore_size)

    def restore_size(self):
        r = self.radius
        self.canvas.coords(self.circle,
                           self.x - r, self.y - r,
                           self.x + r, self.y + r)
        self.canvas.itemconfig(self.circle, fill=self.color)


class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Кликер с улучшениями 💰")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Игровые переменные
        self.money = 0
        self.click_value = 1
        self.auto_income = 0

        # Стили для улучшений
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            'Upgrade.TButton',
            font=('Arial', 11, 'bold'),
            foreground='#FFD700',
            background='#3a3a5c',
            borderwidth=2,
            relief='raised',
            padding=10
        )
        self.style.map(
            'Upgrade.TButton',
            background=[('active', '#5a5a8c'), ('disabled', '#2a2a3c')],
            foreground=[('disabled', '#888888')]
        )
        self.style.configure('Upgrade.TFrame', background='#1a1a2e')

        # Строим интерфейс
        self.create_widgets()
        self.update_display()

        # Запуск авто-дохода
        self.auto_income_tick()

    def draw_gradient(self, canvas, width, height, c1, c2):
        """Рисует вертикальный градиент с шагом 2 пикселя (оптимизация)."""
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        for i in range(0, height, 2):
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_rectangle(0, i, width, i + 2, fill=color, outline='')

    def create_widgets(self):
        # Главный холст
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Градиентный фон (от тёмно-фиолетового к синему)
        self.draw_gradient(self.canvas, 800, 600, '#1a1a2e', '#16213e')

        # Декоративные элементы (полупрозрачные круги имитация свечения)
        for i in range(3):
            self.canvas.create_oval(
                100 + i*250, 50, 300 + i*250, 250,
                fill='', outline='#ffffff', width=1, dash=(4, 4)
            )

        # Заголовок и счётчики
        self.canvas.create_text(
            400, 40, text="К Л И К Е Р", font=('Arial', 28, 'bold'), fill='#FFD700'
        )
        self.money_text = self.canvas.create_text(
            400, 90, text="Монеты: 0", font=('Arial', 22, 'bold'), fill='white'
        )
        self.income_text = self.canvas.create_text(
            400, 125, text="Доход за клик: 1 | Авто-доход: 0/сек",
            font=('Arial', 13), fill='#cccccc'
        )

        # Центральная кнопка-кликер (кастомная)
        self.click_btn = CircleButton(
            self.canvas, 400, 300, 80, "Click me!",
            color='#FFD700', hover_color='#FFEA00',
            click_color='#FFA500', command=self.click_action
        )

        # Панель улучшений (фрейм поверх Canvas)
        self.upgrade_frame = ttk.Frame(self.canvas, style='Upgrade.TFrame')
        self.canvas.create_window(
            400, 500, window=self.upgrade_frame, width=700, height=100
        )

        # Создаём кнопки улучшений
        self.upgrade_buttons = []
        upgrades_info = [
            {"name": "Усилитель клика", "base_cost": 10, "cost_mult": 1.5, "level": 0,
             "action": lambda: setattr(self, 'click_value', self.click_value + 1)},
            {"name": "Авто-сборщик", "base_cost": 50, "cost_mult": 1.8, "level": 0,
             "action": lambda: setattr(self, 'auto_income', self.auto_income + 1)}
        ]
        for i, upg in enumerate(upgrades_info):
            btn = ttk.Button(
                self.upgrade_frame,
                text=self._upgrade_text(upg),
                style='Upgrade.TButton',
                command=lambda idx=i: self.buy_upgrade(idx)
            )
            btn.pack(side=tk.LEFT, padx=20, pady=10, expand=True)
            self.upgrade_buttons.append({"btn": btn, "data": upg})

    def _upgrade_text(self, upg):
        """Формирует подпись кнопки улучшения."""
        cost = int(upg["base_cost"] * (upg["cost_mult"] ** upg["level"]))
        return f"{upg['name']} (ур.{upg['level']})\nЦена: {cost} монет"

    def buy_upgrade(self, index):
        """Покупка улучшения."""
        btn_info = self.upgrade_buttons[index]
        upg = btn_info["data"]
        cost = int(upg["base_cost"] * (upg["cost_mult"] ** upg["level"]))
        if self.money >= cost:
            self.money -= cost
            upg["level"] += 1
            upg["action"]()                # применяем эффект
            self.update_display()
        # Иначе ничего не делаем (кнопка и так будет disabled при недостатке)

    def click_action(self):
        """Обработка клика по центральной кнопке."""
        self.money += self.click_value
        self.update_display()

    def auto_income_tick(self):
        """Каждую секунду начисляем пассивный доход."""
        if self.auto_income > 0:
            self.money += self.auto_income
            self.update_display()
        self.root.after(1000, self.auto_income_tick)

    def update_display(self):
        """Обновляет все текстовые элементы и состояние кнопок."""
        self.canvas.itemconfig(
            self.money_text,
            text=f"Монеты: {self.money}"
        )
        self.canvas.itemconfig(
            self.income_text,
            text=f"Доход за клик: {self.click_value} | Авто-доход: {self.auto_income}/сек"
        )

        # Обновляем текст и доступность кнопок улучшений
        for btn_info in self.upgrade_buttons:
            upg = btn_info["data"]
            btn = btn_info["btn"]
            cost = int(upg["base_cost"] * (upg["cost_mult"] ** upg["level"]))
            btn.config(text=self._upgrade_text(upg))
            if self.money >= cost:
                btn.config(state=tk.NORMAL)
            else:
                btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGame(root)
    root.mainloop()