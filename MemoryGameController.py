import tkinter as tk
from MemoryGameLogic import MemoryGameLogic
from MemoryGameGUI import MemoryGameGUI
from typing import Optional, Tuple
import pygame


class MemoryGameController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = MemoryGameLogic()
        self.gui = MemoryGameGUI(root, self.logic.difficulty_levels)
        self.pending_reset: Optional[Tuple[int, int]] = None

        # Додано звуки
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sounds/click.wav")
        self.match_sound = pygame.mixer.Sound("sounds/match.wav")
        self.win_sound = pygame.mixer.Sound("sounds/win.wav")

        self.gui.setup_menu(self.start_game)

    def start_game(self, rows: int, cols: int) -> None:
        """Start new game with given dimensions"""
        self.logic.setup_game(rows, cols)
        self.gui.setup_board(rows, cols, self.handle_click)

    def handle_click(self, idx: int) -> None:
        """Handle button click event"""
        button_text = self.gui.buttons[idx]["text"]

        if self.pending_reset:
            idx1, idx2 = self.pending_reset
            self.reset_turn(idx1, idx2)
            self.pending_reset = None

        self.click_sound.play()

        is_match, first_index, symbol = self.logic.handle_click(idx, button_text)

        if symbol:
            self.gui.update_button(idx, symbol)

        if is_match:
            self.gui.update_button(idx, symbol, True)
            self.gui.update_button(self.logic.first_index, self.logic.first_symbol, True)
            self.logic.first_symbol = None
            self.logic.first_index = None
            self.logic.reset_turn()

            self.match_sound.play()

            # Перевірка перемоги
            buttons_state = [btn["state"] for btn in self.gui.buttons]
            if self.logic.check_win(buttons_state):
                self.win_sound.play()
                self.gui.show_win_message(self.logic.moves)

        elif first_index is not None:
            self.pending_reset = (idx, first_index)
            self.root.after(500, lambda: self.check_and_reset_pending())

        self.gui.update_moves(self.logic.moves)

    def check_and_reset_pending(self) -> None:
        """Reset pending pair if still scheduled"""
        if self.pending_reset:
            idx1, idx2 = self.pending_reset
            self.reset_turn(idx1, idx2)
            self.pending_reset = None

    def reset_turn(self, idx1: int, idx2: int) -> None:
        """Reset two cards after unsuccessful match"""
        self.gui.reset_button(idx1)
        self.gui.reset_button(idx2)
        self.logic.reset_turn()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.config(bg="#f0f0f0")
    game = MemoryGameController(root)
    root.mainloop()
