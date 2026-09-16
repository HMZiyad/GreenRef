import tkinter as tk
from tkinter import messagebox, filedialog
import os

class Notepad:
    def __init__(self, width=300, height=300):
        self.root = tk.Tk()
        self.file_path = None

        self.width = width
        self.height = height
        self._setup_ui()

    def _setup_ui(self):
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        self.root.title("Untitled - Notepad")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        left = int((screen_width - self.width) / 2)
        top = int((screen_height - self.height) / 2)

        self.root.geometry(f'{self.width}x{self.height}+{left}+{top}')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.text_area = tk.Text(self.root)
        self.text_area.grid(sticky=tk.N + tk.E + tk.S + tk.W)

        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self._create_menus()
        self.root.config(menu=self.menu_bar)

    def _create_menus(self):
        self.menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self._new_file)
        file_menu.add_command(label="Open", command=self._open_file)
        file_menu.add_command(label="Save", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=lambda: messagebox.showinfo("Notepad", "Created by Ferdinand Silva"))
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def _new_file(self):
        self.root.title("Untitled - Notepad")
        self.file_path = None
        self.text_area.delete(1.0, tk.END)

    def _open_file(self):
        path = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if not path:
            return

        try:
            with open(path, "r") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, f.read())
            self.file_path = path
            self.root.title(f"{os.path.basename(path)} - Notepad")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {e}")

    def _save_file(self):
        if not self.file_path:
            path = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if not path:
                return
            self.file_path = path

        try:
            with open(self.file_path, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"{os.path.basename(self.file_path)} - Notepad")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file: {e}")

    def run(self):
        self.root.mainloop()


# Run the app
if __name__ == "__main__":
    Notepad(width=600, height=400).run()
