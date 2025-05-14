import tkinter as tk
from tkinter import font
from typing import List, Optional, Dict, Tuple


class MemoryGameGUI:
    def __init__(self, root: tk.Tk, difficulty_levels: Dict[str, Tuple[int, int]]):
        self.root = root
        self.root.title("Memory Game")
        self.difficulty_levels = difficulty_levels

        # Colors and styles
        self.bg_color = "#f0f0f0"
        self.card_bg = "#3498db"
        self.card_fg = "white"
        self.card_font = ("Arial", 12, "bold")
        self.disabled_color = "#2ecc71"

        self.buttons: List[tk.Button] = []
        self.moves_label: Optional[tk.Label] = None

    def setup_menu(self, difficulty_command) -> None:
        """Create start menu with difficulty options"""
        self.clear_window()

        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(expand=True)

        tk.Label(
            menu_frame,
            text="Memory Game",
            font=("Arial", 24, "bold"),
            bg=self.bg_color
        ).pack(pady=20)

        for level, (rows, cols) in self.difficulty_levels.items():
            tk.Button(
                menu_frame,
                text=f"{level} ({rows}x{cols})",
                font=self.card_font,
                command=lambda r=rows, c=cols: difficulty_command(r, c),
                width=15,
                padx=10,
                pady=5
            ).pack(pady=5)

        tk.Button(
            menu_frame,
            text="Exit",
            font=self.card_font,
            command=self.root.quit,
            width=15,
            padx=10,
            pady=5
        ).pack(pady=20)

    def setup_board(self, rows: int, cols: int, button_command) -> None:
        """Setup the game board with styled buttons"""
        self.clear_window()

        # Header with moves counter
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", pady=10)

        self.moves_label = tk.Label(
            header_frame,
            text="Moves: 0",
            font=self.card_font,
            bg=self.bg_color
        )
        self.moves_label.pack(side="left", padx=20)

        tk.Button(
            header_frame,
            text="Menu",
            font=self.card_font,
            command=self.setup_menu,
            padx=10
        ).pack(side="right", padx=20)

        # Game board
        board_frame = tk.Frame(self.root, bg=self.bg_color)
        board_frame.pack(expand=True)

        self.buttons = []
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                btn = tk.Button(
                    board_frame,
                    text="?",
                    font=self.card_font,
                    width=4,
                    height=2,
                    bg=self.card_bg,
                    fg=self.card_fg,
                    activebackground="#2980b9",
                    command=lambda x=idx: button_command(x)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

    def update_button(self, idx: int, symbol: str, disabled: bool = False) -> None:
        """Update button appearance"""
        btn = self.buttons[idx]
        if disabled:
            btn.config(
                text=symbol,
                state="disabled",
                disabledforeground="white",
                bg=self.disabled_color
            )
        else:
            btn.config(
                text=symbol,
                bg="#f1c40f",
                fg="black"
            )

    def reset_button(self, idx: int) -> None:
        """Reset button to initial state"""
        btn = self.buttons[idx]
        btn.config(text="?", bg=self.card_bg, fg=self.card_fg)

    def update_moves(self, moves: int) -> None:
        """Update moves counter"""
        self.moves_label.config(text=f"Moves: {moves}")

    def clear_window(self) -> None:
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    def show_win_message(self, moves: int) -> None:
        """Show win message"""
        tk.messagebox.showinfo(
            "Congratulations!",
            f"You've won in {moves} moves!"
        )