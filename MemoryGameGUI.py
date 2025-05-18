import tkinter as tk
from tkinter import font, messagebox
from typing import List, Optional, Dict, Tuple, Callable


class MemoryGameGUI:
    def __init__(self, root: tk.Tk, difficulty_levels: Dict[str, Tuple[int, int]]):
        self.root = root
        self.root.title("Memory Game")
        self.difficulty_levels = difficulty_levels

        # Modern color scheme
        self.bg_color = "#f5f5f5"
        self.card_bg = "#3a7ca5"
        self.card_fg = "white"
        self.card_font = ("Arial", 14, "bold")
        self.disabled_color = "#2fbf71"
        self.highlight_color = "#ffd166"
        self.text_color = "#2b2d42"
        self.button_hover = "#2a628f"

        self.buttons: List[tk.Button] = []
        self.moves_label: Optional[tk.Label] = None
        self.difficulty_command: Optional[Callable] = None

    def setup_menu(self, difficulty_command: Callable) -> None:
        """Create modern start menu with difficulty options"""
        self.clear_window()
        self.difficulty_command = difficulty_command

        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(expand=True, padx=20, pady=20)

        # Game title
        title = tk.Label(
            menu_frame,
            text="Memory Game",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 30))

        # Difficulty buttons
        for level, (rows, cols) in self.difficulty_levels.items():
            btn = tk.Button(
                menu_frame,
                text=f"{level} ({rows}×{cols})",
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
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.button_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.card_bg))

        # Exit button
        exit_btn = tk.Button(
            menu_frame,
            text="Exit",
            font=self.card_font,
            command=self.root.quit,
            width=18,
            pady=8,
            bg="#d64045",
            fg="white",
            activebackground="#c73232",
            relief="flat"
        )
        exit_btn.pack(pady=(20, 0))
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#c73232"))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#d64045"))

    def setup_board(self, rows: int, cols: int, button_command: Callable) -> None:
        """Setup modern game board with cards"""
        self.clear_window()

        # Header with moves counter and menu button
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

        # Game board with cards
        board_frame = tk.Frame(self.root, bg=self.bg_color)
        board_frame.pack(expand=True, padx=20, pady=(0, 20))

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
                    activebackground=self.button_hover,
                    command=lambda x=idx: button_command(x),
                    relief="raised",
                    borderwidth=3
                )
                btn.grid(row=i, column=j, padx=5, pady=5, ipadx=5, ipady=5)
                self.buttons.append(btn)

    def update_button(self, idx: int, symbol: str, disabled: bool = False) -> None:
        """Update card appearance with animation effect"""
        btn = self.buttons[idx]
        if disabled:
            btn.config(
                text=symbol,
                state="disabled",
                disabledforeground="white",
                bg=self.disabled_color,
                relief="sunken"
            )
        else:
            btn.config(
                text=symbol,
                bg=self.highlight_color,
                fg="black",
                relief="sunken"
            )

    def reset_button(self, idx: int) -> None:
        """Reset card to initial state with animation effect"""
        btn = self.buttons[idx]
        btn.config(
            text="?",
            bg=self.card_bg,
            fg=self.card_fg,
            state="normal",
            relief="raised"
        )

    def update_moves(self, moves: int) -> None:
        """Update moves counter"""
        self.moves_label.config(text=f"Moves: {moves}")

    def clear_window(self) -> None:
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_win_message(self, moves: int) -> None:
        """Show modern win message with options"""
        win_window = tk.Toplevel(self.root)
        win_window.title("Congratulations!")
        win_window.geometry("400x250")
        win_window.resizable(False, False)
        win_window.configure(bg=self.bg_color)
        win_window.grab_set()

        # Center the window
        win_window.update_idletasks()
        width = win_window.winfo_width()
        height = win_window.winfo_height()
        x = (win_window.winfo_screenwidth() // 2) - (width // 2)
        y = (win_window.winfo_screenheight() // 2) - (height // 2)
        win_window.geometry(f'+{x}+{y}')

        # Win message
        tk.Label(
            win_window,
            text="You Won! 🎉",  # Fixed emoji position
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

        # Buttons frame
        button_frame = tk.Frame(win_window, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Play again button
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

        # Exit button
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