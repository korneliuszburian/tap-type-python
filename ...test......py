import tkinter as tk
from tkinter import ttk
from typing import List, TextIO
import time
import pygame
import random

class FastTypeGame:
    """A class for the Fast Type Game GUI and its game logic."""
    
    def __init__(self) -> None:
        """Initialize the game window, set up the UI and start the game."""
        self.window = tk.Tk()
        self.window.title("Fast Type Game")
        self.setup_window_size()
        self.set_background_photo("background.png")
        self.words: List[str] = []
        self.word_index: int = 0
        self.time_limit: int = 0
        self.start_time: float = 0
        self.elapsed_time: float = 0
        self.wpm: float = 0
        self.accuracy: float = 0
        self.typed_words: int = 0
        self.correct_words: int = 0
        self.incorrect_words: int = 0
        self.typed_characters: int = 0
        self.correct_characters: int = 0
        self.incorrect_characters: int = 0
        self.word_length: int = 0
        self.game_over: bool = False
        self.load_words()
        self.init_ui()
        self.window.mainloop()

    def setup_window_size(self, ) -> None:
        """Set up the window size."""
        window_width = 500
        window_height = 1000
        self.window.geometry(f"{window_width}x{window_height}")

    def load_words(self, file: TextIO = "words.txt") -> None:
        """Load words from words.txt file and store them in a list."""
        with open(file, "r") as f:
            self.words = f.read().splitlines()
            # shuffle the words
            random.shuffle(self.words)
            
    def set_time_limit(self, time_limit: int) -> None:
        """Set the time limit for the game."""
        self.time_limit = time_limit
        
    def set_background_photo(self, photo: str = "backgrounds\\background.png") -> None:
        """Set the background photo for the game."""
        try:
            self.background_photo = tk.PhotoImage(file=photo)
            self.background_label = tk.Label(self.window, image=self.background_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except tk.TclError:
            print("Unable to load background photo. Setting white background instead.")
            self.background_label = tk.Label(self.window, bg="white")
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def init_ui(self) -> None:
        """Set up the UI elements."""
        # Setup UI
        self.game_name_label = tk.Label(self.window, text="💻 TapType Game 💻", font=("Helvetica", 37))
        self.game_name_label.pack(pady=30)

        self.separator = ttk.Separator(self.window, orient='horizontal')
        self.separator.pack(fill='x')

        self.word_label = tk.Label(self.window, text="", font=("Helvetica", 35))
        self.word_label.pack(pady=30)

        self.input_field = tk.Entry(self.window, font=("Helvetica", 25))
        self.input_field.pack(pady=30)
        self.input_field.bind("<Key>", self.on_key_pressed), self.input_field.focus()

        self.timer_label = tk.Label(self.window, text="", font=("Helvetica", 20))
        self.timer_label.pack(pady=30)

        self.wpm_label = tk.Label(self.window, text="WPM: 0", font=("Helvetica", 25))
        self.wpm_label.pack(pady=30)

        self.accuracy_label = tk.Label(self.window, text="Accuracy: 0%", font=("Helvetica", 25))
        self.accuracy_label.pack(pady=30)

        self.typed_characters_label = tk.Label(self.window, text="Typed Characters: 0", font=("Helvetica", 20))
        self.typed_characters_label.pack(pady=30)

        self.correct_characters_label = tk.Label(self.window, text="Correct Characters: 0", font=("Helvetica", 20))
        self.correct_characters_label.pack(pady=30)

        self.incorrect_characters_label = tk.Label(self.window, text="Incorrect Characters: 0", font=("Helvetica", 20))
        self.incorrect_characters_label.pack(pady=30)

        # Start game
        self.start_game()

    def start_game(self) -> None:
        """Reset game variables and start the game."""
        self.start_time = time.time()
        self.elapsed_time = 0
        self.wpm = 0
        self.accuracy = 0
        self.typed_words = 0
        self.correct_words = 0
        self.incorrect_words = 0
        self.correct_characters = 0
        self.incorrect_characters = 0
        self.word_index = 0
        self.time_limit = 5
        self.max_len = len(self.words)
        self.new_word()
        self.word_length = len(self.words[self.word_index])
        self.update_ui()

    def new_word(self) -> None:
        """Get the next word from the list and set up the UI for it."""
        self.word_label.configure(text=self.words[self.word_index])
        self.input_field.delete(0, tk.END)
        self.word_length = len(self.words[self.word_index])

    def check_word(self) -> None:
        """Check if the typed word is correct and update game variables accordingly."""
        self.typed_words += 1
        if self.input_field.get() == self.words[self.word_index]:
            self.correct_words += 1
        else:
            self.incorrect_words += 1

        self.word_index += 1

        if self.word_index >= len(self.words):
            self.end_game()
        else:
            self.new_word()

    def calculate_wpm(self) -> float:
        """Calculate words per minute."""
        if self.elapsed_time > 0:
            self.wpm = (self.typed_characters / 5) / (self.elapsed_time / 60)
        return self.wpm

    def calculate_accuracy(self) -> float:
        """Calculate accuracy rate."""
        if self.typed_characters > 0:
            self.accuracy = (self.correct_characters / self.typed_characters) * 100
        return self.accuracy

    def on_key_pressed(self, event: tk.Event) -> None:
        """Handle key press events from the input field."""
        if event.keysym == "Return":
            self.check_word()
            self.new_word()
        elif event.keysym == "BackSpace":
            self.typed_characters += 1
            self.incorrect_characters += 1
        elif event.keysym == "Escape":
            self.end_game()
        else:
            self.typed_characters += 1
            self.check_character()
        self.update_ui()

    def check_character(self) -> None:
        """Check if the typed character is correct."""
        typed_word = self.input_field.get()
        generated_word = self.words[self.word_index]
        if typed_word == generated_word[:len(typed_word)]:
            self.correct_characters += 1
        else:
            self.incorrect_characters += 1

    def update_ui(self) -> None:
        """Update the UI elements."""
        self.wpm = self.calculate_wpm()
        self.accuracy = self.calculate_accuracy()
        self.elapsed_time = time.time() - self.start_time

        self.timer_label.configure(text=f"Time: {int(self.time_limit - self.elapsed_time)}")
        self.wpm_label.configure(text=f"WPM: {int(self.wpm)}")
        self.accuracy_label.configure(text=f"Accuracy: {int(self.accuracy)}%")
        self.typed_characters_label.configure(text=f"Typed Characters: {int(self.typed_characters)}")
        self.correct_characters_label.configure(text=f"Correct Characters: {int(self.correct_characters)}")
        self.incorrect_characters_label.configure(text=f"Incorrect Characters: {int(self.incorrect_characters)}")

        if self.elapsed_time > self.time_limit:
            self.end_game()
        self.window.after(100, self.update_ui)

    def end_game(self) -> None:
        """End the game and show the game over screen."""
        self.wpm = self.calculate_wpm()
        self.accuracy = self.calculate_accuracy()
        self.wpm_label.configure(text=f"WPM: {int(self.wpm)}")
        self.accuracy_label.configure(text=f"Accuracy: {int(self.accuracy)}%")
        self.word_label.configure(text="Game Over")
        # Show game over screen
        pygame.init()
        game_over_screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Game Over")

        font = pygame.font.Font("freesansbold.ttf", 24)
        text = font.render(f"WPM: {int(self.wpm)}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (250, 250)
        game_over_screen.blit(text, text_rect)

        text = font.render(f"Accuracy: {int(self.accuracy)}%", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (250, 300)
        game_over_screen.blit(text, text_rect)
        
        text = font.render("Press ESC to quit", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (250, 350)
        game_over_screen.blit(text, text_rect)
        pygame.display.update()

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pygame.quit()
                    quit()
                # if user click ESC key, quit the game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        pygame.quit()
                        quit()
        
    @staticmethod
    def run_game() -> None:
        """Run the game."""
        game = FastTypeGame()
        game.window.mainloop()
        

if __name__ == "__main__":
    FastTypeGame.run_game()
