import tkinter as tk
from tkinter import font, messagebox
from typing import List, Optional, Dict, Tuple, Callable

class MemoryGameGUI:
    def __init__(self, root: tk.Tk, difficulty_levels: Dict[str, Tuple[int, int]]):
        """Ініціалізація графічного інтерфейсу гри.
        Args:
            root: Головне вікно програми (Tkinter root)
            difficulty_levels: Словник з рівнями складності (назва: (рядки, стовпці))
        """
        self.root = root
        self.root.title("Memory Game")
        self.difficulty_levels = difficulty_levels

        # Сучасна кольорова схема:
        self.bg_color = "#f5f5f5"  # колір фону
        self.card_bg = "#3a7ca5"  # колір карток
        self.card_fg = "white"  # колір тексту на картках
        self.card_font = ("Arial", 14, "bold")  # шрифт карток
        self.disabled_color = "#2fbf71"  # колір знайдених пар
        self.highlight_color = "#ffd166"  # колір підсвічування
        self.text_color = "#2b2d42"  # основний колір тексту
        self.button_hover = "#2a628f"  # колір кнопок при наведенні

        self.buttons: List[tk.Button] = []  # список кнопок-карток
        self.moves_label: Optional[tk.Label] = None  # мітка для відображення ходів
        self.difficulty_command: Optional[Callable] = None  # функція обробки вибору складності

    def setup_menu(self, difficulty_command: Callable) -> None:
        """Створення головного меню з вибором рівня складності.
        Args:
            difficulty_command: Функція, яка буде викликатись при виборі рівня
        """
        self.clear_window()
        self.difficulty_command = difficulty_command

        # Фрейм для меню
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(expand=True, padx=20, pady=20)

        # Заголовок гри
        title = tk.Label(
            menu_frame,
            text="Memory Game",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 30))

        # Кнопки рівнів складності
        for level, (rows, cols) in self.difficulty_levels.items():
            btn = tk.Button(
                menu_frame,
                text=f"{level} ({rows}×{cols})",  # Назва рівня та розмірність
                font=self.card_font,
                command=lambda r=rows, c=cols: self.difficulty_command(r, c),
                width=18,
                pady=8,
                bg=self.card_bg,
                fg="white",
                activebackground=self.button_hover,
                relief="flat",
                bd=0
            )
            btn.pack(pady=6)
            # Ефекти при наведенні курсора
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.button_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.card_bg))

        # Кнопка виходу
        exit_btn = tk.Button(
            menu_frame,
            text="Exit",
            font=self.card_font,
            command=self.root.quit,
            width=18,
            pady=8,
            bg="#d64045",  # червоний колір для кнопки виходу
            fg="white",
            activebackground="#c73232",
            relief="flat"
        )
        exit_btn.pack(pady=(20, 0))
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#c73232"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#d64045"))

    def setup_board(self, rows: int, cols: int, button_command: Callable) -> None:
        """Налаштування ігрового поля з картками.
        Args:
            rows: Кількість рядків
            cols: Кількість стовпців
            button_command: Функція-обробник кліку на картку
        """
        self.clear_window()

        # Верхня панель з лічильником ходів та кнопкою меню
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(10, 20), padx=20)
        self.moves_label = tk.Label(
            header_frame,
            text="Moves: 0",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.moves_label.pack(side="left")
        # Кнопка повернення до головного меню
        menu_btn = tk.Button(
            header_frame,
            text="Menu",
            font=("Arial", 12),
            command=lambda: self.setup_menu(self.difficulty_command),
            padx=15,
            pady=3,
            bg="#8d99ae",
            fg="white",
            activebackground="#6c757d",
            relief="flat"
        )
        menu_btn.pack(side="right")
        menu_btn.bind("<Enter>", lambda e: menu_btn.config(bg="#6c757d"))
        menu_btn.bind("<Leave>", lambda e: menu_btn.config(bg="#8d99ae"))

        # Ігрове поле
        board_frame = tk.Frame(self.root, bg=self.bg_color)
        board_frame.pack(expand=True, padx=20, pady=(0, 20))

        self.buttons = []  # Очищення списку кнопок
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j  # Лінійний індекс кнопки
                btn = tk.Button(
                    board_frame,
                    text="?",  # Початковий стан - знак питання
                    font=self.card_font,
                    width=4,
                    height=2,
                    bg=self.card_bg,
                    fg=self.card_fg,
                    activebackground=self.button_hover,
                    command=lambda x=idx: button_command(x),
                    relief="raised",
                    borderwidth=3
                )
                btn.grid(row=i, column=j, padx=5, pady=5, ipadx=5, ipady=5)
                self.buttons.append(btn)

    def update_button(self, idx: int, symbol: str, disabled: bool = False) -> None:
        """Оновлення вигляду картки.
        Args:
            idx: Індекс кнопки
            symbol: Символ, який відображатиметься
            disabled: Чи картка знайдена (неактивна)
        """
        btn = self.buttons[idx]
        if disabled:
            # Стан знайденої пари
            btn.config(
                text=symbol,
                state="disabled",
                disabledforeground="white",
                bg=self.disabled_color,
                relief="sunken"
            )
        else:
            # Стан відкритої картки
            btn.config(
                text=symbol,
                bg=self.highlight_color,
                fg="black",
                relief="sunken"
            )

    def reset_button(self, idx: int) -> None:
        """Повернення картки у початковий стан.
        Args:
            idx: Індекс кнопки
        """
        btn = self.buttons[idx]
        btn.config(
            text="?",
            bg=self.card_bg,
            fg=self.card_fg,
            state="normal",
            relief="raised"
        )

    def update_moves(self, moves: int) -> None:
        """Оновлення лічильника ходів.
        Args:
            moves: Поточна кількість ходів
        """
        self.moves_label.config(text=f"Moves: {moves}")

    def clear_window(self) -> None:
        """Очищення вікна від віджетів."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_win_message(self, moves: int) -> None:
        """Відображення повідомлення про перемогу.
        Args:
            moves: Кількість ходів, за які завершено гру
        """
        win_window = tk.Toplevel(self.root)
        win_window.title("Congratulations!")
        win_window.geometry("400x250")
        win_window.resizable(False, False)
        win_window.configure(bg=self.bg_color)
        win_window.grab_set()  # Модальне вікно

        # Центрування вікна
        win_window.update_idletasks()
        width = win_window.winfo_width()
        height = win_window.winfo_height()
        x = (win_window.winfo_screenwidth() // 2) - (width // 2)
        y = (win_window.winfo_screenheight() // 2) - (height // 2)
        win_window.geometry(f'+{x}+{y}')
        # Повідомлення про перемогу
        tk.Label(
            win_window,
            text="You Won! 🎉",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.disabled_color
        ).pack(pady=(20, 10))

        tk.Label(
            win_window,
            text=f"Completed in {moves} moves!",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=10)

        # Фрейм для кнопок
        button_frame = tk.Frame(win_window, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Кнопка "Грати знову"
        replay_btn = tk.Button(
            button_frame,
            text="Play Again",
            font=("Arial", 12, "bold"),
            command=lambda: [win_window.destroy(), self.setup_menu(self.difficulty_command)],
            bg=self.card_bg,
            fg="white",
            padx=20,
            pady=5,
            relief="flat"
        )
        replay_btn.pack(side="left", padx=10, ipadx=5, ipady=3)
        replay_btn.bind("<Enter>", lambda e: replay_btn.config(bg=self.button_hover))
        replay_btn.bind("<Leave>", lambda e: replay_btn.config(bg=self.card_bg))

        # Кнопка "Вийти"
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 12, "bold"),
            command=self.root.quit,
            bg="#d64045",
            fg="white",
            padx=20,
            pady=5,
            relief="flat"
        )
        exit_btn.pack(side="right", padx=10, ipadx=5, ipady=3)
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#c73232"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#d64045"))