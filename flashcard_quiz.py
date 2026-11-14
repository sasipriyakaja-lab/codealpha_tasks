import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

DATA_FILE = "flashcards.json"

DEFAULT_CARDS = [
    {"question": "What keyword defines a function in Python?", "answer": "def"},
    {"question": "Which data type is immutable: list or tuple?", "answer": "tuple"},
    {"question": "What does PEP 8 refer to in Python?", "answer": "Python Enhancement Proposal (style guide)"},
    {"question": "Which built-in function returns the length of a list?", "answer": "len()"},
]


def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return list(DEFAULT_CARDS)


def save_cards(cards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2)


class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flashcard Quiz App | CodeAlpha")
        self.master.geometry("540x430")
        self.master.configure(bg="#f1f5f9")
        self.master.resizable(False, False)

        self.cards = load_cards()
        self.index = 0
        self.showing_answer = False

        top_bar = tk.Frame(master, bg="#f1f5f9")
        top_bar.pack(fill="x", padx=28, pady=(18, 8))

        tk.Label(
            top_bar,
            text="Flashcard Quiz",
            font=("Segoe UI", 15, "bold"),
            fg="#0f172a",
            bg="#f1f5f9",
        ).pack(side="left")

        self.counter_label = tk.Label(
            top_bar,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#475569",
            bg="#f1f5f9",
        )
        self.counter_label.pack(side="right")

        self.card_frame = tk.Frame(master, bg="#ffffff", bd=1, relief="solid")
        self.card_frame.pack(padx=28, pady=8, fill="both", expand=True)

        self.mode_badge = tk.Label(
            self.card_frame,
            text="QUESTION",
            font=("Segoe UI", 9, "bold"),
            fg="#1d4ed8",
            bg="#dbeafe",
            padx=10,
            pady=3,
        )
        self.mode_badge.pack(pady=(18, 10))

        self.content_label = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#1e293b",
            bg="#ffffff",
            wraplength=430,
            justify="center",
            height=5,
        )
        self.content_label.pack(padx=20)

        self.flip_btn = tk.Button(
            self.card_frame,
            text="Show Answer",
            command=self.flip_card,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
        )
        self.flip_btn.pack(pady=(8, 18))

        nav_frame = tk.Frame(master, bg="#f1f5f9")
        nav_frame.pack(pady=(6, 4))

        tk.Button(
            nav_frame, text="Previous", command=self.prev_card,
            font=("Segoe UI", 10, "bold"), bg="#e2e8f0", fg="#1e293b", bd=0, width=14, pady=7, cursor="hand2"
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            nav_frame, text="Next", command=self.next_card,
            font=("Segoe UI", 10, "bold"), bg="#e2e8f0", fg="#1e293b", bd=0, width=14, pady=7, cursor="hand2"
        ).grid(row=0, column=1, padx=6)

        crud_frame = tk.Frame(master, bg="#f1f5f9")
        crud_frame.pack(pady=(4, 18))

        tk.Button(
            crud_frame, text="Add Card", command=self.add_card,
            font=("Segoe UI", 9, "bold"), bg="#16a34a", fg="#ffffff", bd=0, width=12, pady=6, cursor="hand2"
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            crud_frame, text="Edit Card", command=self.edit_card,
            font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#2563eb", bd=1, width=12, pady=6, cursor="hand2"
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            crud_frame, text="Delete Card", command=self.delete_card,
            font=("Segoe UI", 9, "bold"), bg="#fee2e2", fg="#b91c1c", bd=0, width=12, pady=6, cursor="hand2"
        ).grid(row=0, column=2, padx=5)

        self.refresh_ui()

    def refresh_ui(self):
        if not self.cards:
            self.counter_label.config(text="0 Cards")
            self.mode_badge.config(text="EMPTY", bg="#e2e8f0", fg="#475569")
            self.content_label.config(text="No flashcards available. Click 'Add Card' below.")
            self.flip_btn.config(state="disabled")
            return

        self.flip_btn.config(state="normal")
        card = self.cards[self.index]
        self.counter_label.config(text=f"Card {self.index + 1} of {len(self.cards)}")

        if self.showing_answer:
            self.mode_badge.config(text="ANSWER", bg="#dcfce7", fg="#15803d")
            self.content_label.config(text=card["answer"])
            self.flip_btn.config(text="Show Question")
        else:
            self.mode_badge.config(text="QUESTION", bg="#dbeafe", fg="#1d4ed8")
            self.content_label.config(text=card["question"])
            self.flip_btn.config(text="Show Answer")

    def flip_card(self):
        self.showing_answer = not self.showing_answer
        self.refresh_ui()

    def prev_card(self):
        if not self.cards:
            return
        self.index = (self.index - 1) % len(self.cards)
        self.showing_answer = False
        self.refresh_ui()

    def next_card(self):
        if not self.cards:
            return
        self.index = (self.index + 1) % len(self.cards)
        self.showing_answer = False
        self.refresh_ui()

    def add_card(self):
        q = simpledialog.askstring("New Flashcard", "Enter the question:", parent=self.master)
        if not q or not q.strip():
            return
        a = simpledialog.askstring("New Flashcard", "Enter the answer:", parent=self.master)
        if not a or not a.strip():
            return
        self.cards.append({"question": q.strip(), "answer": a.strip()})
        self.index = len(self.cards) - 1
        self.showing_answer = False
        save_cards(self.cards)
        self.refresh_ui()

    def edit_card(self):
        if not self.cards:
            return
        current = self.cards[self.index]
        q = simpledialog.askstring("Edit Question", "Update question:", initialvalue=current["question"], parent=self.master)
        if not q or not q.strip():
            return
        a = simpledialog.askstring("Edit Answer", "Update answer:", initialvalue=current["answer"], parent=self.master)
        if not a or not a.strip():
            return
        self.cards[self.index] = {"question": q.strip(), "answer": a.strip()}
        self.showing_answer = False
        save_cards(self.cards)
        self.refresh_ui()

    def delete_card(self):
        if not self.cards:
            return
        if messagebox.askyesno("Delete Card", "Remove this flashcard?"):
            self.cards.pop(self.index)
            if self.index >= len(self.cards):
                self.index = max(0, len(self.cards) - 1)
            self.showing_answer = False
            save_cards(self.cards)
            self.refresh_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
