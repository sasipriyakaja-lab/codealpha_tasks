import random
import tkinter as tk
from tkinter import messagebox

quotes_list = [
    ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
    ("Make each day your masterpiece.", "John Wooden"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("Learning never exhausts the mind.", "Leonardo da Vinci"),
    ("Action is the foundational key to all success.", "Pablo Picasso"),
    ("Dream big, start small, act now.", "Robin Sharma"),
    ("Focus on being productive instead of busy.", "Tim Ferriss"),
    ("Discipline is choosing between what you want now and what you want most.", "Abraham Lincoln"),
    ("Everything you can imagine is real.", "Pablo Picasso"),
    ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Small steps in the right direction can turn out to be the biggest step of your life.", "Naeem Callaway"),
]

current_index = -1


def show_new_quote():
    global current_index
    next_index = random.randrange(len(quotes_list))
    if next_index == current_index:
        next_index = (next_index + 1) % len(quotes_list)
    current_index = next_index

    quote_text, author_name = quotes_list[current_index]
    quote_label.config(text=f'"{quote_text}"')
    author_label.config(text=f"— {author_name}")


def copy_quote():
    full_text = f"{quote_label.cget('text')} {author_label.cget('text')}"
    root.clipboard_clear()
    root.clipboard_append(full_text)
    messagebox.showinfo("Copied", "Quote copied to clipboard!")


root = tk.Tk()
root.title("Random Quote Generator | CodeAlpha")
root.geometry("540x320")
root.configure(bg="#1e293b")
root.resizable(False, False)

card = tk.Frame(root, bg="#ffffff", padx=28, pady=24)
card.place(relx=0.5, rely=0.5, anchor="center", width=480, height=260)

header = tk.Label(
    card,
    text="DAILY INSPIRATION",
    font=("Segoe UI", 9, "bold"),
    fg="#2563eb",
    bg="#eff6ff",
    padx=10,
    pady=3,
)
header.pack(pady=(0, 14))

quote_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 13, "bold"),
    fg="#0f172a",
    bg="#ffffff",
    wraplength=420,
    justify="center",
    height=4,
)
quote_label.pack()

author_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 10, "italic"),
    fg="#64748b",
    bg="#ffffff",
)
author_label.pack(pady=(4, 16))

btn_frame = tk.Frame(card, bg="#ffffff")
btn_frame.pack()

new_btn = tk.Button(
    btn_frame,
    text="New Quote",
    command=show_new_quote,
    font=("Segoe UI", 10, "bold"),
    bg="#2563eb",
    fg="#ffffff",
    activebackground="#1d4ed8",
    activeforeground="#ffffff",
    bd=0,
    padx=18,
    pady=8,
    cursor="hand2",
)
new_btn.grid(row=0, column=0, padx=6)

copy_btn = tk.Button(
    btn_frame,
    text="Copy",
    command=copy_quote,
    font=("Segoe UI", 10, "bold"),
    bg="#e2e8f0",
    fg="#1e293b",
    activebackground="#cbd5e1",
    bd=0,
    padx=18,
    pady=8,
    cursor="hand2",
)
copy_btn.grid(row=0, column=1, padx=6)

show_new_quote()
root.mainloop()
