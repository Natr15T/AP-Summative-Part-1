import tkinter as tk
from tkinter import ttk, messagebox
import os

def load_data(filename):
    students = []
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) == 6:
                    code, name = parts[0], parts[1]
                    c1, c2, c3, exam = map(int, parts[2:])
                    coursework_total = c1 + c2 + c3
                    percent = ((coursework_total + exam) / 160) * 100
                    grade = (
                        'A' if percent >= 70 else
                        'B' if percent >= 60 else
                        'C' if percent >= 50 else
                        'D' if percent >= 40 else 'F'
                    )
                    students.append({
                        'code': code, 'name': name,
                        'c1': c1, 'c2': c2, 'c3': c3,
                        'coursework': coursework_total,
                        'exam': exam,
                        'percent': percent,
                        'grade': grade
                    })
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find {filename} in program folder.")
    return students

def save_data(filename, students):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"{len(students)}\n")
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

def format_student(student):
    return (f"Name: {student['name']}\n"
            f"ID: {student['code']}\n"
            f"Coursework Total: {student['coursework']}\n"
            f"Exam Mark: {student['exam']}\n"
            f"Overall %: {student['percent']:.0f}\n"
            f"Grade: {student['grade']}\n"
            "----------------------\n")

def refresh_dropdown():
    global student_names
    student_names = [s['name'] for s in students]
    menu = dropdown["menu"]
    menu.delete(0, "end")
    for name in student_names:
        menu.add_command(label=name, command=lambda value=name: student_var.set(value))

def view_all():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No student data loaded.\n")
        return
    total = 0
    for s in students:
        output_box.insert(tk.END, format_student(s))
        total += s['percent']
    avg = total / len(students)
    output_box.insert(tk.END, f"\nTotal Students: {len(students)}")
    output_box.insert(tk.END, f"\nAverage Percentage: {avg:.0f}%\n")

def view_individual():
    selected = student_var.get()
    output_box.delete(1.0, tk.END)
    if not selected:
        output_box.insert(tk.END, "Please select a student.")
        return
    for s in students:
        if s['name'] == selected:
            output_box.insert(tk.END, format_student(s))
            return
    output_box.insert(tk.END, "Student not found.")

def view_highest():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No data available.\n")
        return
    top = max(students, key=lambda s: s['percent'])
    output_box.insert(tk.END, "Highest Scoring Student:\n")
    output_box.insert(tk.END, format_student(top))

def view_lowest():
    output_box.delete(1.0, tk.END)
    if not students:
        output_box.insert(tk.END, "No data available.\n")
        return
    low = min(students, key=lambda s: s['percent'])
    output_box.insert(tk.END, "Lowest Scoring Student:\n")
    output_box.insert(tk.END, format_student(low))

def sort_students():
    if not students:
        messagebox.showinfo("Info", "No data to sort.")
        return
    choice = messagebox.askquestion("Sort Order", "Sort by Overall Percentage Ascending?")
    if choice == "yes":
        sorted_list = sorted(students, key=lambda s: s['percent'])
    else:
        sorted_list = sorted(students, key=lambda s: s['percent'], reverse=True)
    output_box.delete(1.0, tk.END)
    for s in sorted_list:
        output_box.insert(tk.END, format_student(s))

def add_student():
    popup = tk.Toplevel()
    popup.title("Add Student")
    popup.geometry("300x350")

    fields = ["Code", "Name", "Coursework1", "Coursework2", "Coursework3", "Exam"]
    entries = {}

    for i, f in enumerate(fields):
        tk.Label(popup, text=f).pack()
        entry = tk.Entry(popup)
        entry.pack()
        entries[f] = entry

    def save_new():
        try:
            code = entries["Code"].get()
            name = entries["Name"].get()
            c1 = int(entries["Coursework1"].get())
            c2 = int(entries["Coursework2"].get())
            c3 = int(entries["Coursework3"].get())
            exam = int(entries["Exam"].get())
            coursework_total = c1 + c2 + c3
            percent = ((coursework_total + exam) / 160) * 100
            grade = (
                'A' if percent >= 70 else
                'B' if percent >= 60 else
                'C' if percent >= 50 else
                'D' if percent >= 40 else 'F'
            )
            students.append({
                'code': code, 'name': name,
                'c1': c1, 'c2': c2, 'c3': c3,
                'coursework': coursework_total,
                'exam': exam,
                'percent': percent,
                'grade': grade
            })
            save_data("studentMarks.txt", students)
            refresh_dropdown()
            popup.destroy()
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, f"Student {name} added successfully.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    tk.Button(popup, text="Save", command=save_new).pack(pady=10)

def delete_student():
    selected = student_var.get()
    if not selected:
        messagebox.showinfo("Info", "Please select a student to delete.")
        return
    for i, s in enumerate(students):
        if s['name'] == selected:
            confirm = messagebox.askyesno("Confirm Delete", f"Delete {s['name']}?")
            if confirm:
                del students[i]
                save_data("studentMarks.txt", students)
                refresh_dropdown()
                output_box.delete(1.0, tk.END)
                output_box.insert(tk.END, f"Student {selected} deleted.\n")
            return
    output_box.insert(tk.END, "Student not found.\n")

def update_student():
    selected = student_var.get()
    if not selected:
        messagebox.showinfo("Info", "Please select a student to update.")
        return
    for s in students:
        if s['name'] == selected:
            popup = tk.Toplevel()
            popup.title("Update Student")
            popup.geometry("300x350")
            fields = ["Code", "Name", "Coursework1", "Coursework2", "Coursework3", "Exam"]
            entries = {}
            for f in fields:
                tk.Label(popup, text=f).pack()
                entry = tk.Entry(popup)
                entry.pack()
                if f == "Code":
                    entry.insert(0, s['code'])
                elif f == "Name":
                    entry.insert(0, s['name'])
                elif f == "Coursework1":
                    entry.insert(0, s['c1'])
                elif f == "Coursework2":
                    entry.insert(0, s['c2'])
                elif f == "Coursework3":
                    entry.insert(0, s['c3'])
                elif f == "Exam":
                    entry.insert(0, s['exam'])
                entries[f] = entry

            def save_update():
                try:
                    s['code'] = entries["Code"].get()
                    s['name'] = entries["Name"].get()
                    s['c1'] = int(entries["Coursework1"].get())
                    s['c2'] = int(entries["Coursework2"].get())
                    s['c3'] = int(entries["Coursework3"].get())
                    s['exam'] = int(entries["Exam"].get())
                    s['coursework'] = s['c1'] + s['c2'] + s['c3']
                    s['percent'] = ((s['coursework'] + s['exam']) / 160) * 100
                    s['grade'] = (
                        'A' if s['percent'] >= 70 else
                        'B' if s['percent'] >= 60 else
                        'C' if s['percent'] >= 50 else
                        'D' if s['percent'] >= 40 else 'F'
                    )
                    save_data("studentMarks.txt", students)
                    refresh_dropdown()
                    popup.destroy()
                    output_box.delete(1.0, tk.END)
                    output_box.insert(tk.END, f"Student {s['name']} updated successfully.\n")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid input: {e}")

            tk.Button(popup, text="Save Changes", command=save_update).pack(pady=10)
            return

# === GUI Setup ===
root = tk.Tk()
root.title("Student Manager Program")
root.geometry("650x650")
root.resizable(False, False)
root.configure(bg="#8B0000")  # 🔴 Changed to dark red

style = ttk.Style()
style.configure(".", font=("Calibri", 12))

students = load_data("studentMarks.txt")

student_var = tk.StringVar()
student_names = [s['name'] for s in students]

ttk.Label(root, text="Select a Student:", background="#8B0000", foreground="white",
          font=("Calibri", 24, "bold")).pack(pady=15)

dropdown = ttk.OptionMenu(root, student_var, *student_names)
dropdown.pack()

btn_frame = tk.Frame(root, background="#8B0000")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="View All", command=view_all).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="View Individual", command=view_individual).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Highest", command=view_highest).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Lowest", command=view_lowest).grid(row=0, column=3, padx=5)
ttk.Button(btn_frame, text="Sort", command=sort_students).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="Add", command=add_student).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="Delete", command=delete_student).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(btn_frame, text="Update", command=update_student).grid(row=1, column=3, padx=5, pady=5)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_box = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=15, width=75)
output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=output_box.yview)

root.mainloop()
