from tkinter import *
from tkinter import messagebox, filedialog
import csv
import os

from lexical_analyzer.analyzer import generate_tokens
from syntactical_analyzer.parser import parser


# GUI
class Window(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        # global params
        self.master = master
        self.text_editor = Text(self)
        self.file_path = None
        self.tokens = None

        self.init_window()

    def init_window(self):
        self.master.title("Translator")
        self.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.init_menu()
        self.init_hotkeys()

        toolbar = Frame(bg='#d7d8e0', bd=2, height=60)
        toolbar.pack(side=TOP, fill=X)

        lexical_analyse_btn = Button(toolbar, text="Lexical analyse", command=self.lexical_analyzer, bd=1, bg='white')
        lexical_analyse_btn.pack(side=LEFT)

        syntactical_analyzer_btn = Button(toolbar, text="Recursive descent", command=self.syntactical_analyzer, bd=1, bg='white')
        syntactical_analyzer_btn.pack(side=LEFT)

        open_tables_btn = Button(toolbar, text="Open tables", command=self.open_tables_window, bd=0, bg='white')
        open_tables_btn.pack(side=RIGHT)

        self.text_editor.config(autoseparators=True, undo=True, width=144, height=35)
        self.text_editor.pack()

    def init_menu(self):
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file submenu in menu
        file_menu = Menu(menu, tearoff=0)
        # file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        # added "file_menu" to our menu
        menu.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="How to use")
        help_menu.add_command(label="About us", command=self.help_text)
        menu.add_cascade(label="Help", menu=help_menu)

    def init_hotkeys(self):
        self.master.bind("<Control-o>", self.open_file)
        self.master.bind("<Control-O>", self.open_file)
        self.master.bind("<Control-S>", self.save_file)
        self.master.bind("<Control-s>", self.save_file)
        self.master.bind("<Control-E>", self.save_file_as)
        self.master.bind("<Control-e>", self.save_file_as)

    def help_text(self):
        text = Label(self, text="Help!!!!!!!!!")
        text.pack()

    def open_file(self, event=None):
        self.file_path = filedialog.askopenfilename(
            initialdir="./",
            title="Select file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
        )
        try:
            with open(self.file_path, 'r') as file:
                text = file.read()
            if text is not None:
                self.text_editor.delete(0.0, END)
                self.text_editor.insert(END, text)
        except FileNotFoundError:
            messagebox.showinfo("File open exception:", "File not found")

    def save_file(self, event=None):
        if self.file_path is None:
            self.save_file_as()
        else:
            self.save_file_as(file_path=self.file_path)

    def save_file_as(self, event=None, file_path=None):
        text = self.text_editor.get("1.0", "end-1c")
        if file_path is None:
            self.file_path = filedialog.asksaveasfilename(
                initialdir="./",
                title="Save as",
                filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
                defaultextension=".txt",
            )
        try:
            with open(self.file_path, 'w+') as file:
                file.write(text)
        except FileNotFoundError:
            messagebox.showinfo("File save exception:", "Blank name")

    @staticmethod
    def open_tables_window():
        TablesWindow()

    def lexical_analyzer(self):
        if self.file_path is None:
            self.save_file_as()
        try:
            self.tokens = generate_tokens(self.file_path.split('/')[-1])
        except IndexError:
            messagebox.showinfo("Lexical analyzer exception:", "index error")
        except Exception as err_type:
            messagebox.showinfo("Lexical analyzer exception", str(err_type))

    def syntactical_analyzer(self):
        if self.tokens is None:
            messagebox.showinfo("Syntactical analyzer exception:", "You need to run lexical analyzer first")
        else:
            try:
                parser(self.tokens)
            except IndexError:
                messagebox.showinfo("Syntactical analyzer exception:", "Program without 'end'")
            except Exception as err_type:
                messagebox.showinfo("Syntactical analyzer exception", str(err_type))


class TablesWindow(Toplevel):
    def __init__(self):
        super().__init__(root)

        self.init_tables_window()

    def init_tables_window(self):
        self.title("Tables")
        self.geometry("1200x600")
        self.resizable(False, False)
        # self.grab_set()
        # self.focus_set()
        self.show_files()

    def show_files(self):
        programs = next(os.walk('./tables'))[1]
        for program in programs:
            Button(self, text=program, bd=0, bg='white').pack(side=TOP)

    def show_table(self, table_name):
        frame = Toplevel(self.master)
        frame.geometry("1200x600")

        with open("./tables/" + self.file_path.split('/')[-1] + '/' + table_name + ".csv", newline="") as file:
            reader = csv.reader(file)
            # r and c tell us where to grid the labels
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    # i've added some styling
                    label = Label(frame, text=row)
                    if c == 6:
                        label = Label(frame, text='   |   ')
                        label.grid(row=r, column=c + 1)

                    if r > 33:
                        label.grid(row=r - 33, column=c + 20)
                    else:
                        label.grid(row=r, column=c)
                    c += 1
                r += 1

    def tokens_table(self):
        self.show_table('tokens')

    def idn_table(self):
        self.show_table('IDN')

    def con_table(self):
        self.show_table('CONST')

    def lab_table(self):
        self.show_table('LAB')


if __name__ == "__main__":

    root = Tk()
    app = Window(root)

    root.geometry("1200x600")
    root.resizable(False, False)
    root.mainloop()
