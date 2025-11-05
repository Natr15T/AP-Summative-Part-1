import tkinter as tk
from tkinter import messagebox
import random, os

# --- Load jokes from file ---
def load_jokes(filename):
    jokes = []
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "resources", filename)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "?" in line:
                    setup, punch = line.strip().split("?")
                    jokes.append((setup + "?", punch))
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found in resources folder.")
    return jokes

# --- Show random joke setup ---
def tell_joke():
    global current_joke
    if not jokes:
        messagebox.showinfo("No Jokes", "No jokes loaded.")
        return
    current_joke = random.choice(jokes)
    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"{current_joke[0]}\n\n(Press 'Show Punchline' to see the answer)")
    output_box.config(state="disabled")

# --- Show punchline ---
def show_punchline():
    if current_joke:
        output_box.config(state="normal")
        output_box.insert(tk.END, f"\n\n💬 {current_joke[1]}")
        output_box.config(state="disabled")

# --- Quit program ---
def quit_app():
    root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("Alexa Joke Teller")
root.geometry("500x400")
root.configure(bg="#8B0000")  # red background

tk.Label(root, text="Alexa Joke Teller 🤖", font=("Arial", 20, "bold"),
         bg="#8B0000", fg="white").pack(pady=15)

output_box = tk.Text(root, height=10, width=50, wrap="word", bg="white",
                     font=("Arial", 12), state="disabled")
output_box.pack(pady=10)

button_frame = tk.Frame(root, bg="#8B0000")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Alexa, tell me a joke", font=("Arial", 12, "bold"),
          bg="white", fg="#8B0000", command=tell_joke).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Show Punchline", font=("Arial", 12, "bold"),
          bg="white", fg="#8B0000", command=show_punchline).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Quit", font=("Arial", 12, "bold"),
          bg="white", fg="#8B0000", command=quit_app).grid(row=0, column=2, padx=5)

# --- Load jokes and run ---
current_joke = None
jokes = load_jokes("randomJokes.txt")

root.mainloop()