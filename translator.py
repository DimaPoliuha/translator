from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox, filedialog
from functools import partial
import csv
import os

from lexical_analyzer.analyzer import generate_tokens
from syntactical_analyzer.recursive_descent import parser as recursive_parser
from syntactical_analyzer.automatic_machine import parser as automatic_parser


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

        toolbar = Frame(bg='#d7d8e0', height=60)
        toolbar.pack(side=TOP, fill=X)

        lexical_analyse_btn = Button(toolbar, text="Lexical analyse", command=self.lexical_analyzer, bd=1, bg='white')
        lexical_analyse_btn.pack(side=LEFT)

        recursive_descent_btn = Button(toolbar, text="Recursive descent", command=self.recursive_descent, bd=1, bg='white')
        recursive_descent_btn.pack(side=LEFT)

        automatic_machine_btn = Button(toolbar, text="Recursive descent", command=self.automatic_machine, bd=1, bg='white')
        automatic_machine_btn.pack(side=LEFT)

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
            text = self.text_editor.get("1.0", "end-1c")
            if text:
                self.save_file_as()
            else:
                self.open_file()
        try:
            self.tokens = generate_tokens(self.file_path.split('/')[-1])
        except IndexError:
            messagebox.showinfo("Lexical analyzer exception", "Index error")
        except Exception as err_type:
            messagebox.showinfo("Lexical analyzer exception", str(err_type))
        else:
            messagebox.showinfo("Lexical analyzer", "Success!")

    def recursive_descent(self):
        if self.tokens is None:
            messagebox.showinfo("Syntactical analyzer exception", "You need to run lexical analyzer first")
        else:
            try:
                recursive_parser(self.tokens)
            except IndexError:
                messagebox.showinfo("Syntactical analyzer (recursive descent) exception", "Index error (Program without 'end')")
            except Exception as err_type:
                messagebox.showinfo("Syntactical analyzer (recursive descent) exception", str(err_type))
            else:
                messagebox.showinfo("Syntactical analyzer (recursive descent)", "Success!")

    def automatic_machine(self):
        if self.tokens is None:
            messagebox.showinfo("Syntactical analyzer exception", "You need to run lexical analyzer first")
        else:
            try:
                automatic_parser(self.tokens)
            except IndexError:
                messagebox.showinfo("Syntactical analyzer (automatic machine) exception", "Index error")
            except Exception as err_type:
                messagebox.showinfo("Syntactical analyzer (automatic machine) exception", str(err_type))
            else:
                messagebox.showinfo("Syntactical analyzer (automatic machine)", "Success!")


class TablesWindow(Toplevel):
    def __init__(self):
        super().__init__(root)

        self.init_tables_window()

    def init_tables_window(self):
        self.title("Recent files")
        self.geometry("150x600")
        self.resizable(False, False)
        self.show_files()

    def show_files(self):
        programs = next(os.walk('./tables'))[1]
        for program in programs:
            Button(self, text=program, bd=1, bg='white', command=partial(self.show_tables, program)).pack(side=TOP)

    def show_tables(self, program_name):
        self.frame = Toplevel(self)
        self.frame.geometry("1000x400")
        self.frame.title("Tables")
        self.frame.resizable(False, False)

        toolbar = Frame(self.frame)
        toolbar.pack(side=TOP, fill=X)

        Label(toolbar, text="Tokens", width=70).pack(side=LEFT)
        Label(toolbar, text="Identifiers", width=30).pack(side=LEFT)
        Label(toolbar, text="Constants", width=25).pack(side=LEFT)
        Label(toolbar, text="Labels", width=15).pack(side=LEFT)

        self.tokens_table(program_name)
        self.idn_table(program_name)
        self.con_table(program_name)
        self.lab_table(program_name)

    def tokens_table(self, program_name):
        TableMargin = Frame(self.frame, width=500)
        TableMargin.pack(side=LEFT)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = Treeview(TableMargin,
                        columns=("Token number", "Line number", "Token", "IDN id", "CON id", "LAB id", "TOK id"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Token number', text="Token number", anchor=W)
        tree.heading('Line number', text="Line number", anchor=W)
        tree.heading('Token', text="Token", anchor=W)
        tree.heading('IDN id', text="IDN id", anchor=W)
        tree.heading('CON id', text="CON id", anchor=W)
        tree.heading('LAB id', text="LAB id", anchor=W)
        tree.heading('TOK id', text="TOK id", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=90)
        tree.column('#2', stretch=NO, minwidth=0, width=80)
        tree.column('#3', stretch=NO, minwidth=0, width=110)
        tree.column('#4', stretch=NO, minwidth=0, width=50)
        tree.column('#5', stretch=NO, minwidth=0, width=50)
        tree.column('#6', stretch=NO, minwidth=0, width=50)
        tree.column('#7', stretch=NO, minwidth=0, width=50)
        tree.pack()

        with open("./tables/" + program_name + "/tokens.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    def idn_table(self, program_name):
        TableMargin = Frame(self.frame, width=300)
        TableMargin.pack(side=LEFT)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = Treeview(TableMargin,
                        columns=("Id", "Name", "Value", "Type"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Id', text="Id", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Value', text="Value", anchor=W)
        tree.heading('Type', text="Type", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=30)
        tree.column('#2', stretch=NO, minwidth=0, width=70)
        tree.column('#3', stretch=NO, minwidth=0, width=70)
        tree.column('#4', stretch=NO, minwidth=0, width=40)
        tree.pack()

        with open("./tables/" + program_name + "/IDN.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1],
                                               # row[2], row[3]
                                               ))

    def con_table(self, program_name):
        TableMargin = Frame(self.frame, width=300)
        TableMargin.pack(side=LEFT)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = Treeview(TableMargin,
                        columns=("Id", "Value", "Type"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Id', text="Id", anchor=W)
        tree.heading('Value', text="Value", anchor=W)
        tree.heading('Type', text="Type", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=30)
        tree.column('#2', stretch=NO, minwidth=0, width=70)
        tree.column('#3', stretch=NO, minwidth=0, width=40)
        tree.pack()

        with open("./tables/" + program_name + "/CONST.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2]))

    def lab_table(self, program_name):
        TableMargin = Frame(self.frame, width=300)
        TableMargin.pack(side=LEFT)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = Treeview(TableMargin,
                        columns=("Id", "Name"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Id', text="Id", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=30)
        tree.column('#2', stretch=NO, minwidth=0, width=60)
        tree.pack()

        with open("./tables/" + program_name + "/LAB.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1]))


if __name__ == "__main__":

    # root = Tk()
    # app = Window(root)
    #
    # root.geometry("1200x600")
    # root.resizable(False, False)
    # root.mainloop()

    try:
        tokens = generate_tokens('program.txt')
        automatic_parser(tokens)
    except IndexError:
        print("exception: ", "Index error")
    except Exception as err_type:
        print("exception: ", str(err_type))
