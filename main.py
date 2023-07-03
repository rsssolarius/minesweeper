import tkinter as tk
from tkinter import messagebox
from random import Random

color_of_digits = {
    1: 'blue',
    2: 'green',
    3: 'red',
    4: '#1A119F',
    5: 'brown',
    6: '#5AEFEA',
    7: 'black',
    8: 'white',
}

"""Усовершенствуем класс Кнопки, добавив в него координаты на поле (x, y),
количество мин среди соседей (neighbor_mines) или 
является ли сама Кнопка миной (is_mine), номер клетки (number)"""


class MyButton(tk.Button):

    def __init__(self, master, x, y, number, *args, **kwargs):
        super().__init__(master, width=3, font=('Calibri 15 bold'), bd=5, *args, **kwargs)
        self.x = x
        self.y = y
        self.neighbor_mines = 0
        self.number = number
        self.is_mine = False
        self.is_open = False

    def __repr__(self):
        # return f'Button {self.number} - ({self.x},{self.y}) - {self.is_mine}'
        return f'{self.neighbor_mines}' if not self.is_mine else '*'


"""Наш основной класс - Сапер. Имеет классовые атрибуты - переменную GUI, строки,
столбцы, мины. При инициализации создаем экз Кнопки и набиваем их в массив buttons
Размещаем мины рандомно. Обсчитываем кол-во мин среди соседей. Выводим в терминал инфу 
о поле. Создаем таблицу с кнопками в GUI. Задаем метод, определяющий нажатие на кнопку.
И старт игры обьединяющий все вместе."""


class MineSweeper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 7
    MINES = 10

    def __init__(self):
        self.buttons = []
        count = 1
        for i in range(MineSweeper.ROW):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                button = MyButton(MineSweeper.window, i, j, count)
                button.config(command=lambda btn=button: self.push_button(btn))
                button.bind('<Button-3>', self.mark_mine)
                temp.append(button)
                count += 1
            self.buttons.append(temp)

    def plant_mines(self):
        rng = Random()
        m = MineSweeper.MINES
        while m > 0:
            i = rng.randrange(MineSweeper.ROW)
            j = rng.randrange(MineSweeper.COLUMNS)
            btn = self.buttons[i][j]
            if not btn.is_mine:
                btn.is_mine = True
                m -= 1

    def neighbors_mines(self):
        for temp in self.buttons:
            for btn in temp:
                m = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        k = dx + btn.x
                        n = dy + btn.y
                        if k < 0 or k >= MineSweeper.ROW or n < 0 or n >= MineSweeper.COLUMNS:
                            continue
                        if self.buttons[k][n].is_mine:
                            m += 1
                btn.neighbor_mines = m

    def print_buttons(self):
        for x in self.buttons:
            print(x)

    def create_widget(self):

        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        settings = tk.Menu(menu, tearoff=0)
        settings.add_command(label='Новая игра', command=self.reload)
        settings.add_command(label='Настройки', command=self.settings)
        settings.add_command(label='Выход', command=self.window.destroy)
        menu.add_cascade(label='Меню', menu=settings)

        for i in range(self.ROW):
            for j in range(self.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, sticky='wens')

        for i in range(self.ROW):
            MineSweeper.window.grid_rowconfigure(i, weight=1)
        for j in range(self.COLUMNS):
            MineSweeper.window.grid_columnconfigure(j, weight=1)

    def settings(self):
        window_settings = tk.Toplevel(self.window)
        window_settings.wm_title('Настройки')

        tk.Label(window_settings, text='Количество строк').grid(row=0, column=0, padx=20, pady=20)
        tk.Label(window_settings, text='Количество столбцов').grid(row=1, column=0, padx=20, pady=20)
        tk.Label(window_settings, text='Количество мин').grid(row=2, column=0, padx=20, pady=20)

        row_entry = tk.Entry(window_settings)
        row_entry.insert(0, str(self.ROW))
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        column_entry = tk.Entry(window_settings)
        column_entry.insert(0, str(self.COLUMNS))
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        mines_entry = tk.Entry(window_settings)
        mines_entry.insert(0, str(self.MINES))
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        tk.Button(window_settings, text='Начать игру с текущими настройками',
                  command=lambda: self.change_settings(row_entry.get(), column_entry.get(), mines_entry.get())) \
            .grid(row=3, column=0, columnspan=4, padx=20, pady=20)

    def change_settings(self, r, c, m):
        # print(r, c, m)
        MineSweeper.ROW = int(r)
        MineSweeper.COLUMNS = int(c)
        MineSweeper.MINES = int(m)
        self.reload()

    def reload(self):
        for x in self.window.winfo_children():
            x.destroy()
        self.__init__()
        self.plant_mines()
        self.neighbors_mines()
        self.print_buttons()
        self.create_widget()

    def push_button(self, pushed_button: MyButton):
        print(pushed_button)
        if pushed_button.is_mine:
            pushed_button.config(text='*', background='red', disabledforeground='black')
            messagebox.showinfo('=(', 'Вы проиграли!')
            for i in range(self.ROW):
                for j in range(self.COLUMNS):
                    if self.buttons[i][j].is_mine:
                        self.buttons[i][j].config(text='*', disabledforeground='black')
                    self.buttons[i][j].config(state='disabled')
            # MineSweeper.window.destroy()
        else:
            queue = [pushed_button]
            while queue:

                current_btn = queue.pop()

                if current_btn.neighbor_mines:
                    current_btn.config(text=current_btn.neighbor_mines,
                                       disabledforeground=color_of_digits[current_btn.neighbor_mines])

                else:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            # if abs(dx + dy) == 1:
                            k = dx + current_btn.x
                            n = dy + current_btn.y

                            if k < 0 or k >= MineSweeper.ROW or n < 0 or n >= MineSweeper.COLUMNS:
                                continue
                            next_btn = self.buttons[dx + current_btn.x][dy + current_btn.y]

                            if not next_btn.is_open:
                                queue.append(next_btn)

                current_btn.is_open = True
                current_btn.config(state='disabled', relief=tk.SUNKEN)
        pushed_button.config(state='disabled', relief=tk.SUNKEN)

        count = 0
        for temp in self.buttons:
            for btn in temp:
                if btn['text'] == '🚩' and btn.is_mine:
                    count += 1
        if count == MineSweeper.MINES:
            messagebox.showinfo('=)', 'Победа!')

    def mark_mine(self, event):
        btn = event.widget
        if btn['state'] == 'normal':
            btn['state'] = 'disabled'
            btn['text'] = '🚩'
            btn['disabledforeground'] = 'red'
        elif btn['text'] == '🚩':
            btn['text'] = ''
            btn['state'] = 'normal'

        count = 0
        for temp in self.buttons:
            for btn in temp:
                if btn['text'] == '🚩' and btn.is_mine:
                    count += 1
        if count == MineSweeper.MINES:
            messagebox.showinfo('=)', 'Победа!')

    def start(self):
        self.plant_mines()
        self.neighbors_mines()
        self.print_buttons()
        self.create_widget()
        self.window.mainloop()


game = MineSweeper()
game.start()
