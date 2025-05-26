import tkinter as tk
from MemoryGameLogic import MemoryGameLogic
from MemoryGameGUI import MemoryGameGUI
from typing import Optional, Tuple
import pygame

class MemoryGameController:
    def __init__(self, root: tk.Tk):
        """Ініціалізація контролера гри, який зв'язує логіку та GUI."""
        self.root = root
        self.logic = MemoryGameLogic()  # Об'єкт логіки гри
        self.gui = MemoryGameGUI(root, self.logic.difficulty_levels)  # Об'єкт інтерфейсу
        self.pending_reset: Optional[Tuple[int, int]] = None  # Пара карток для скидання

        # Ініціалізація звукових ефектів
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sounds/click.wav")  # Звук кліку
        self.match_sound = pygame.mixer.Sound("sounds/match.wav")  # Звук знаходження пари
        self.win_sound = pygame.mixer.Sound("sounds/win.wav")  # Звук перемоги

        # Налаштування стартового меню
        self.gui.setup_menu(self.start_game)

    def start_game(self, rows: int, cols: int) -> None:
        """Почати нову гру з заданими розмірами сітки."""
        self.logic.setup_game(rows, cols)
        self.logic.moves = 0  # Скидання лічильника ходів
        self.gui.setup_board(rows, cols, self.handle_click)  # Створення ігрового поля
        self.gui.update_moves(0)  # Оновлення лічильника ходів

    def handle_click(self, idx: int) -> None:
        """Обробник кліку на картку."""
        button_text = self.gui.buttons[idx]["text"]

        # Якщо є пара карток, які потребують скидання
        if self.pending_reset:
            idx1, idx2 = self.pending_reset
            self.reset_turn(idx1, idx2)
            self.pending_reset = None

        # Відтворення звуку кліку
        self.click_sound.play()

        # Обробка кліку в логіці гри
        is_match, first_index, symbol = self.logic.handle_click(idx, button_text)

        if symbol:
            self.gui.update_button(idx, symbol)  # Оновлення вигляду картки

        if is_match:
            # Якщо знайдено пару
            self.gui.update_button(idx, symbol, True)
            self.gui.update_button(self.logic.first_index, self.logic.first_symbol, True)
            self.logic.first_symbol = None
            self.logic.first_index = None
            self.logic.reset_turn()

            self.match_sound.play()  # Звук знаходження пари

            # Перевірка перемоги
            buttons_state = [btn["state"] for btn in self.gui.buttons]
            if self.logic.check_win(buttons_state):
                self.win_sound.play()  # Звук перемоги
                self.gui.update_moves(self.logic.moves)
                self.gui.show_win_message(self.logic.moves)

        elif first_index is not None:
            # Якщо пару не знайдено, запам'ятовуємо картки для скидання
            self.pending_reset = (idx, first_index)
            self.root.after(500, lambda: self.check_and_reset_pending())

        self.gui.update_moves(self.logic.moves)  # Оновлення лічильника ходів

    def check_and_reset_pending(self) -> None:
        """Скинути пару карток, якщо вони все ще потребують скидання"""
        if self.pending_reset:
            idx1, idx2 = self.pending_reset
            self.reset_turn(idx1, idx2)
            self.pending_reset = None

    def reset_turn(self, idx1: int, idx2: int) -> None:
        """Скинути дві картки після невдалої спроби знайти пару"""
        self.gui.reset_button(idx1)
        self.gui.reset_button(idx2)
        self.logic.reset_turn()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.config(bg="#f0f0f0")
    game = MemoryGameController(root)
    root.mainloop()