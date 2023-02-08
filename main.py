import typing
import tkinter as tk
import time
import pygame
import sys


"""
FastTypeGame

This class creates a typing game where the user can test their typing speed and accuracy.

Attributes:
    window (tk.Tk): Tkinter window object
    words (typing.List[str]): List of words to type
    word_index (int): Index of the word to type
    time_limit (int): Time limit of the game (in seconds)
    start_time (float): Time when the game started
    elapsed_time (float): Time elapsed since the game started
    wpm (float): User's words per minute
    accuracy (float): User's accuracy
    typed_words (int): Number of words typed
    correct_words (int): Number of words typed correctly
    incorrect_words (int): Number of words typed incorrectly
    typed_characters (int): Number of characters typed
    correct_characters (int): Number of characters typed correctly
    incorrect_characters (int): Number of characters typed incorrectly
    word_length (int): Length of the current word
    max_len (int): Maximum length of the words list
    word_label (tk.Label): Label for the current word
    input_field (tk.Entry): Input field for user to type in
    timer_label (tk.Label): Label for the timer
    wpm_label (tk.Label): Label for the words per minute
    accuracy_label (tk.Label): Label for the accuracy
    typed_characters_label (tk.Label): Label for the typed characters
    correct_characters_label (tk.Label): Label for the correct characters
    incorrect_characters_label (tk.Label): Label for the incorrect characters

Methods:
    __init__(self) -> None
        Initializes the window, loads words and calls init_ui()

    load_words(self) -> None
        Loads words from words.txt file and adds them to the words list

    init_ui(self) -> None
        Sets up the UI elements and starts the game

    start_game(self) -> None
        Resets all the variables and starts the game

    new_word(self) -> None
        Gets a new word from the words list and updates the UI

    check_word(self) -> None
        Checks if the word typed is correct and updates the UI

    calculate_wpm(self) -> float
        Calculates the words per minute

    calculate_accuracy(self) -> float
        Calculates the accuracy of the user

    on_key_pressed(self, event: tk.Event) -> None
        Checks for key presses and updates the UI

    check_character(self) -> None
        Checks if the character typed is correct and updates the UI

    update_ui(self) -> None
        Updates the UI elements

    pause_game(self) -> None
        Pauses the game and shows the game paused screen

    end_game(self) -> None
        Ends the game and shows the game over screen
"""

class FastTypeGame:
    def __init__(self) -> None:
        
        # Setup window
        self.window = tk.Tk()
        self.window.title("Fast Type Game")
        self.window.geometry("500x1000")
        
        # Setup variables
        self.words: typing.List[str] = []
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
        self.load_words()
        self.init_ui()
        self.window.mainloop()

    def load_words(self) -> None:
        with open("words.txt", "r") as f:
            self.words = f.read().splitlines()

    def init_ui(self) -> None:
        # Setup UI
        # self.background_image = tk.PhotoImage(file="background\\background.png")
        # self.background_label = tk.Label(self.window, image=self.background_image)
        # self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.word_label = tk.Label(self.window, text="", font=("Helvetica", 40))
        self.word_label.pack(pady=30)

        self.input_field = tk.Entry(self.window, font=("Helvetica", 25))
        self.input_field.pack(pady=30)
        self.input_field.bind("<Key>", self.on_key_pressed)

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
        self.max_len = len(self.words)
        self.new_word()
        self.word_length = len(self.words[self.word_index])
        # Set time limit
        self.time_limit = 20
        self.update_ui()

    def new_word(self) -> None:
        self.word_label.configure(text=self.words[self.word_index])
        self.input_field.delete(0, tk.END)
        self.word_length = len(self.words[self.word_index])

    def check_word(self) -> None:
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
        if self.elapsed_time > 0:
            self.wpm = (self.typed_characters / 5) / self.elapsed_time * 60
        return self.wpm

    def calculate_accuracy(self) -> float:
        if self.typed_characters > 0:
            self.accuracy = (self.correct_characters / self.typed_characters) * 100
        return self.accuracy

    def on_key_pressed(self, event: tk.Event) -> None:
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
        typed_word = self.input_field.get()
        generated_word = self.words[self.word_index]
        if typed_word == generated_word[:len(typed_word)]:
            self.correct_characters += 1
        else:
            self.incorrect_characters += 1

    def update_ui(self) -> None:
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

    def pause_game(self) -> None:
        self.elapsed_time = time.time() - self.start_time
        self.wpm = self.calculate_wpm()
        self.accuracy = self.calculate_accuracy()
        self.wpm_label.configure(text=f"WPM: {int(self.wpm)}")
        self.accuracy_label.configure(text=f"Accuracy: {int(self.accuracy)}%")
        self.word_label.configure(text="Game Paused")
        # Show game over screen
        pygame.init()
        game_paused_screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Game Paused")

        font = pygame.font.Font("freesansbold.ttf", 24)
        text = font.render(f"WPM: {int(self.wpm)}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (250, 250)
        game_paused_screen.blit(text, text_rect)

        text = font.render(f"Accuracy: {int(self.accuracy)}%", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (250, 300)
        game_paused_screen.blit(text, text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.keysym == "p":
                    self.start_time = time.time() - self.elapsed_time
                    self.new_word()
                    break

    def end_game(self) -> None:
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

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.start_game()
                    break


if __name__ == "__main__":
    game = FastTypeGame()
