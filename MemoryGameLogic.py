from typing import List, Dict, Tuple, Optional
import random


class MemoryGameLogic:
    def __init__(self):
        # Game settings
        self.difficulty_levels: Dict[str, Tuple[int, int]] = {
            "Easy": (3, 4),
            "Medium": (4, 5),
            "Hard": (5, 6)
        }

        # Game state
        self.rows: int = 0
        self.cols: int = 0
        self.pairs_needed: int = 0
        self.symbols: List[str] = []
        self.moves: int = 0
        self.first_symbol: Optional[str] = None
        self.first_index: Optional[int] = None
        self.can_click: bool = True

    def setup_game(self, rows: int, cols: int) -> None:
        """Initialize game with selected difficulty"""
        self.rows = rows
        self.cols = cols
        self.pairs_needed = (rows * cols) // 2

        # Generate symbols
        emoji_symbols = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
                         "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
                         "🐧", "🐦", "🐤", "🦄", "🐝", "🐛", "🦋", "🐌"]

        selected_symbols = random.sample(emoji_symbols, self.pairs_needed)
        self.symbols = selected_symbols * 2
        random.shuffle(self.symbols)

    def handle_click(self, idx: int, button_text: str) -> Tuple[bool, Optional[int], str]:
        """Process button click and return (is_match, first_index, symbol)"""
        if not self.can_click or button_text != "?":
            return (False, None, "")

        current_symbol = self.symbols[idx]

        if self.first_symbol is None:
            self.first_symbol = current_symbol
            self.first_index = idx
            return (False, None, current_symbol)
        else:
            self.moves += 1
            self.can_click = False

            if self.first_symbol == current_symbol:
                return (True, None, current_symbol)
            else:
                first_index = self.first_index
                self.first_symbol = None
                self.first_index = None
                return (False, first_index, current_symbol)

    def reset_turn(self) -> None:
        """Reset turn state after mismatch"""
        self.can_click = True

    def check_win(self, buttons_state: List[str]) -> bool:
        """Check if all pairs have been found"""
        return all(state == "disabled" for state in buttons_state)