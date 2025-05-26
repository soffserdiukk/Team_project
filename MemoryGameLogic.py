from typing import List, Dict, Tuple, Optional
import random

class MemoryGameLogic:
    def __init__(self):
        # Налаштування гри: рівні складності та відповідні розміри сітки (рядки, стовпці)
        self.difficulty_levels: Dict[str, Tuple[int, int]] = {
            "Easy": (3, 4),  # Легкий: 3 рядки, 4 стовпці (12 карток)
            "Medium": (4, 5),  # Середній: 4 рядки, 5 стовпців (20 карток)
            "Hard": (5, 6)  # Важкий: 5 рядків, 6 стовпців (30 карток)
        }

        # Стан гри
        self.rows: int = 0  # Кількість рядків у грі
        self.cols: int = 0  # Кількість стовпців у грі
        self.pairs_needed: int = 0  # Необхідна кількість пар для поточної гри
        self.symbols: List[str] = []  # Список символів на картках
        self.moves: int = 0  # Лічильник ходів
        self.first_symbol: Optional[str] = None  # Перший відкритий символ
        self.first_index: Optional[int] = None  # Індекс першої відкритої картки
        self.can_click: bool = True  # Чи можна клікати на картки зараз

    def setup_game(self, rows: int, cols: int) -> None:
        """Ініціалізує гру з обраним рівнем складності.

        Args:
            rows (int): Кількість рядків сітки
            cols (int): Кількість стовпців сітки

        Дії:
            1. Встановлює розміри сітки
            2. Розраховує необхідну кількість пар символів
            3. Генерує випадковий набір символів з emoji
            4. Подвоює символи для створення пар та перемішує їх
        """
        self.rows = rows
        self.cols = cols
        self.pairs_needed = (rows * cols) // 2

        emoji_symbols = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
                         "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
                         "🐧", "🐦", "🐤", "🦄", "🐝", "🐛", "🦋", "🐌"]

        # Вибираємо випадкові символи (кількість = pairs_needed)
        selected_symbols = random.sample(emoji_symbols, self.pairs_needed)
        # Подвоюємо символи для пар та перемішуємо
        self.symbols = selected_symbols * 2
        random.shuffle(self.symbols)

    def handle_click(self, idx: int, button_text: str) -> Tuple[bool, Optional[int], str]:
        """Обробляє клік на картку та повертає результат.

        Args:
            idx (int): Індекс клікнутої картки
            button_text (str): Поточний текст на кнопці

        Returns:
            Tuple[bool, Optional[int], str]:
                - bool: Чи знайдено пару
                - Optional[int]: Індекс першої картки (якщо не знайдено пару)
                - str: Символ на клікнутій картці

        Логіка:
            1. Якщо кліки заборонені або картка вже відкрита - ігноруємо
            2. Якщо це перший клік - запам'ятовуємо символ
            3. Якщо це другий клік:
               - Збільшуємо лічильник ходів
               - Блокуємо подальші кліки
               - Перевіряємо чи знайдено пару
        """
        if not self.can_click or button_text != "?":
            return (False, None, "")

        current_symbol = self.symbols[idx]

        if self.first_symbol is None:  # Перший клік
            self.first_symbol = current_symbol
            self.first_index = idx
            return (False, None, current_symbol)
        else:  # Другий клік
            self.moves += 1
            self.can_click = False

            if self.first_symbol == current_symbol:  # Знайдено пару
                return (True, None, current_symbol)
            else:  # Не знайдено пару
                first_index = self.first_index
                self.first_symbol = None
                self.first_index = None
                return (False, first_index, current_symbol)

    def reset_turn(self) -> None:
        """Скидає стан ходу після невдалої спроби знайти пару.
        Дозволяє знову клікати на картки.
        """
        self.can_click = True

    def check_win(self, buttons_state: List[str]) -> bool:
        """Перевіряє, чи всі пари знайдені (умова перемоги).

        Args:
            buttons_state (List[str]): Список станів кнопок
        Returns:
            bool: True якщо всі картки відкриті (стани = "disabled")
        """
        return all(state == "disabled" for state in buttons_state)