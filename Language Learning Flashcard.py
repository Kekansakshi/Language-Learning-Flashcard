import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Flashcard:
    def __init__(self, front, back):
        self.front = front  # Foreign language word
        self.back = back    # Translation in native language

class FlashcardDeck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            messagebox.showerror("Error", "Card not found in the deck.")

    def display_all_cards(self):
        for card in self.cards:
            print("German Word:", card.front, "\tEnglish Word:", card.back)

    def study(self):
        for card in self.cards:
            print("German Word:", card.front)
            input("Press Enter to see the back of the card...")
            print("English Word:", card.back)
            input("Press Enter for the next card...")

    def generate_quiz(self, num_questions=5):
        random_cards = random.sample(self.cards, min(num_questions, len(self.cards)))
        quiz = []
        for card in random_cards:
            quiz.append((card.front, card.back))
        return quiz
        
class FlashcardGUI:
    def __init__(self, root, flashcard_list=None):
        self.root = root
        self.flashcard_list = flashcard_list if flashcard_list else []

        self.deck = FlashcardDeck()
        for front, back in self.flashcard_list:
            card = Flashcard(front, back)
            self.deck.add_card(card)

        self.create_widgets()

    def create_widgets(self):
        self.root.title("Flashcard Application")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.main_frame, text="Language Learning Flashcard Application", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(self.main_frame, text="View all flashcards", command=self.view_flashcards)
        self.view_button.grid(row=1, column=0, padx=5, pady=5)

        self.create_button = tk.Button(self.main_frame, text="Create a new flashcard", command=self.create_flashcard)
        self.create_button.grid(row=1, column=1, padx=5, pady=5)

        self.study_button = tk.Button(self.main_frame, text="Study flashcards", command=self.study_flashcards)
        self.study_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.quiz_button = tk.Button(self.main_frame, text="Take Quiz", command=self.take_quiz)
        self.quiz_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def view_flashcards(self):
        all_cards = self.deck.cards + [Flashcard(front, back) for front, back in self.flashcard_list]
        if not all_cards:
            messagebox.showinfo("No Flashcards", "No flashcards available. Please create some.")
        else:
            flashcards_window = tk.Toplevel(self.root)
            flashcards_window.title("All Flashcards")
            for i, card in enumerate(all_cards):
                flashcard_label = tk.Label(flashcards_window, text=f"German Word: {card.front}, English Word: {card.back}")
                flashcard_label.grid(row=i, column=0, padx=5, pady=5)

    def create_flashcard(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Create New Flashcard")

        front_label = tk.Label(create_window, text="Foreign language word:")
        front_label.grid(row=0, column=0, padx=5, pady=5)
        self.front_entry = tk.Entry(create_window)
        self.front_entry.grid(row=0, column=1, padx=5, pady=5)

        back_label = tk.Label(create_window, text="Translation in your native language:")
        back_label.grid(row=1, column=0, padx=5, pady=5)
        self.back_entry = tk.Entry(create_window)
        self.back_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = tk.Button(create_window, text="Add Flashcard", command=self.add_flashcard)
        add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def add_flashcard(self):
        front = self.front_entry.get()
        back = self.back_entry.get()
        if front and back:
            card = Flashcard(front, back)
            self.deck.add_card(card)
            messagebox.showinfo("Success", "Flashcard added successfully!")
            self.front_entry.delete(0, tk.END)
            self.back_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter both front and back of the flashcard.")

    def study_flashcards(self):
        if not self.deck.cards:
            messagebox.showinfo("No Flashcards", "No flashcards available. Please create some.")
        else:
            study_window = tk.Toplevel(self.root)
            study_window.title("Study Flashcards")
            for card in self.deck.cards:
                front_label = tk.Label(study_window, text=f"German Word: {card.front}")
                front_label.pack(padx=5, pady=5)
                back_button = tk.Button(study_window, text="Show Back", command=lambda b=card.back: self.show_back(b))
                back_button.pack(padx=5, pady=5)
                next_button = tk.Button(study_window, text="Next Card", command=study_window.destroy)
                next_button.pack(padx=5, pady=5)

    def show_back(self, back):
        messagebox.showinfo("Back of the Card", f"Back: {back}")

    def take_quiz(self):
        if not self.deck.cards:
            messagebox.showinfo("No Flashcards", "No flashcards available. Please create some.")
        else:
            self.quiz = self.deck.generate_quiz()
            self.display_quiz()

    def display_quiz(self):
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Quiz")

        self.answer_entries = []
        self.score = 0  # Initialize score
        self.total_questions = len(self.quiz)

        for i, (front, back) in enumerate(self.quiz):
            front_label = tk.Label(quiz_window, text=f"Question {i + 1}: What is the translation of '{front}'?")
            front_label.grid(row=i, column=0, padx=5, pady=5)
            answer_entry = tk.Entry(quiz_window)
            answer_entry.grid(row=i, column=1, padx=5, pady=5)
            self.answer_entries.append(answer_entry)

        submit_button = tk.Button(quiz_window, text="Submit", command=self.submit_quiz)
        submit_button.grid(row=len(self.quiz), columnspan=2, padx=5, pady=5)

        self.score_label = tk.Label(quiz_window, text="")
        self.score_label.grid(row=len(self.quiz) + 1, columnspan=2, padx=5, pady=5)

    def submit_quiz(self):
        self.score = 0
        for i, (front, back) in enumerate(self.quiz):
            user_answer = self.answer_entries[i].get().strip()
            if user_answer.lower() == back.lower():
                self.score += 1  # Increase score for correct answer

        # Update score label
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")

def main():
    flashcard_list = [('eins','one'),('zwel','two'),('drei','three'),('vier','four'),('fünf','five'),('sechs','six'),('sieben','seven'),('acht','eight'),('neun','nine'),('zehn','ten'),('zwanzig','twenty'),('fünfzig','fifty'),('hundert','hundred'),('tausend','thousand'),('Farbe','color'),('weiß','white'),('schwarz','black'),('rot','red'),('blau','blue'),('grün','green'),('gelb','yellow'),('bunt','colourful'),('gut','good'),('schlecht','bad'),('neu','new'),('alt','old'),('jung','young'),('groß','big'),('klein','small'),('schön','beautiful'),('billig','cheap'),('teuer','expensive'),('dunkel','dark'),('hell','bright'),('zusammen','together'),('getrennt','separate'),('wichtig','important'),('müde','tired'),('arbeiten','to work'),('besuchen','to visit'),('bleiben','to stay'),('brauchen','to need'),('essen','food'),('fragen','to ask'),('geben','to give')]
    root = tk.Tk()
    flashcard_gui = FlashcardGUI(root, flashcard_list)
    root.mainloop()   

if __name__ == "__main__":
    main()
