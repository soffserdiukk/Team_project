import tkinter as tk
from MemoryGameLogic import MemoryGameLogic
from MemoryGameGUI import MemoryGameGUI
from typing import Optional, Tuple


class MemoryGameController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = MemoryGameLogic()
        self.gui = MemoryGameGUI(root, self.logic.difficulty_levels)
        self.pending_reset: Optional[Tuple[int, int]] = None

        # Start with menu
        self.gui.setup_menu(self.start_game)

    def start_game(self, rows: int, cols: int) -> None:
        """Start new game with given dimensions"""
        self.logic.setup_game(rows, cols)
        self.gui.setup_board(rows, cols, self.handle_click)

    def handle_click(self, idx: int) -> None:
        """Handle card click event"""
        # Check if we need to reset previous unmatched pair
        if self.pending_reset:
            self.reset_pending_pair()

        button_text = self.gui.buttons[idx]["text"]
        is_match, first_index, symbol = self.logic.handle_click(idx, button_text)

        if not symbol:  # Invalid click
            return

        self.gui.update_button(idx, symbol)

        if is_match:
            self.handle_match(idx)
        elif first_index is not None:
            self.schedule_reset(idx, first_index)

        self.gui.update_moves(self.logic.moves)

    def handle_match(self, idx: int) -> None:
        """Handle successful card match"""
        self.gui.update_button(idx, self.logic.first_symbol, True)
        self.gui.update_button(self.logic.first_index, self.logic.first_symbol, True)
        self.logic.first_symbol = None
        self.logic.first_index = None
        self.logic.reset_turn()

        # Check for win condition
        if self.check_win():
            self.gui.show_win_message(self.logic.moves)

    def schedule_reset(self, idx1: int, idx2: int) -> None:
        """Schedule reset for unmatched pair"""
        self.pending_reset = (idx1, idx2)
        self.root.after(800, self.reset_pending_pair)

    def reset_pending_pair(self) -> None:
        """Reset the pending unmatched pair"""
        if self.pending_reset:
            idx1, idx2 = self.pending_reset
            self.gui.reset_button(idx1)
            self.gui.reset_button(idx2)
            self.logic.reset_turn()
            self.pending_reset = None

    def check_win(self) -> bool:
        """Check if all pairs have been found"""
        buttons_state = [btn["state"] for btn in self.gui.buttons]
        return self.logic.check_win(buttons_state)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x650")
    root.config(bg="#f5f5f5")
    game = MemoryGameController(root)
    root.mainloop()