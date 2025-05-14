import tkinter as tk
from MemoryGameLogic import MemoryGameLogic
from MemoryGameGUI import MemoryGameGUI


class MemoryGameController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = MemoryGameLogic()
        self.gui = MemoryGameGUI(root, self.logic.difficulty_levels)

        self.gui.setup_menu(self.start_game)

    def start_game(self, rows: int, cols: int) -> None:
        """Start new game with given dimensions"""
        self.logic.setup_game(rows, cols)
        self.gui.setup_board(rows, cols, self.handle_click)

    def handle_click(self, idx: int) -> None:
        """Handle button click event"""
        button_text = self.gui.buttons[idx]["text"]
        is_match, first_index, symbol = self.logic.handle_click(idx, button_text)

        if symbol:
            self.gui.update_button(idx, symbol)

        if is_match:
            self.gui.update_button(idx, symbol, True)
            self.gui.update_button(self.logic.first_index, self.logic.first_symbol, True)
            self.logic.first_symbol = None
            self.logic.first_index = None
            self.logic.reset_turn()

            # Check for win
            buttons_state = [btn["state"] for btn in self.gui.buttons]
            if self.logic.check_win(buttons_state):
                self.gui.show_win_message(self.logic.moves)
        elif first_index is not None:
            self.root.after(1000, lambda: self.reset_turn(idx, first_index))

        self.gui.update_moves(self.logic.moves)

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