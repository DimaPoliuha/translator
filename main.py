"""
Main module with GUI logic
"""
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox, filedialog
from functools import partial
import csv
import os

from translator_components.structures.program_file_processing import ProgramFile
from translator_components.structures.tokens_identifiers import tokens_identifiers
from translator_components.lexical_analyzer.analyzer import LexicalAnalyzer
from translator_components.syntactical_analyzers.recursive_descent import RecursiveDescent
from translator_components.syntactical_analyzers.automatic_machine import AutomaticMachine
from translator_components.syntactical_analyzers.bottom_up import BottomUp
from translator_components.poliz.poliz import Poliz
from translator_components.poliz.poliz_processing import PolizProcessing


# GUI
class Window(Frame):
    """
    Main frame GUI
    """

    def __init__(self, master=None):
        super().__init__(master)

        self.program_file = None
        self.lexical_analyzer = LexicalAnalyzer()
        self.recursive_descent = RecursiveDescent()
        self.automatic_machine = AutomaticMachine()
        self.bottom_up = BottomUp()
        self.poliz = Poliz()
        self.poliz_processing = PolizProcessing()

        # global params
        self.master = master
        self.text_editor = Text(self)
        self.file_path = None
        self.tokens = None
        self.frame = None

        self.init_window()

    def init_window(self):
        self.master.title("Translator")
        self.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.init_menu()
        self.init_hot_keys()

        toolbar = Frame(bg='#d7d8e0', height=60)
        toolbar.pack(side=TOP, fill=X)

        run_btn = Button(toolbar, text="Run", command=self.run, bd=1, bg='white')
        run_btn.pack(side=LEFT)

        grammar_btn = Button(toolbar, text="Grammar", command=self.show_grammar, bd=1, bg='white')
        grammar_btn.pack(side=RIGHT)

        # bottom_up_grammar_table_btn = Button(
        #     toolbar, text="Bottom up table", command=self.open_bottom_up_grammar_table, bd=1, bg='white'
        # )
        # bottom_up_grammar_table_btn.pack(side=RIGHT)

        open_automatic_machine_table_btn = Button(
            toolbar, text="Automatic machine table", command=self.open_automatic_machine_table, bd=1, bg='white'
        )
        open_automatic_machine_table_btn.pack(side=RIGHT)

        open_tables_btn = Button(
            toolbar, text="Open lexical results", command=self.open_tables_window, bd=1, bg='white'
        )
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

        run_menu = Menu(menu, tearoff=0)
        run_menu.add_command(label="Run", command=self.run, accelerator="Ctrl+R")
        run_menu.add_command(label="Lexical analyse", command=self.run_lexical_analyzer)
        run_menu.add_command(label="Recursive descent", command=self.run_recursive_descent)
        run_menu.add_command(label="Automatic machine", command=self.run_automatic_machine)
        run_menu.add_command(label="Bottom up", command=self.run_bottom_up)
        run_menu.add_command(label="Poliz", command=self.run_poliz)
        menu.add_cascade(label="Run", menu=run_menu)

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="How to use")
        help_menu.add_command(label="About us", command=self.help_text)
        menu.add_cascade(label="Help", menu=help_menu)

    def init_hot_keys(self):
        self.master.bind("<Control-o>", self.open_file)
        self.master.bind("<Control-O>", self.open_file)
        self.master.bind("<Control-S>", self.save_file)
        self.master.bind("<Control-s>", self.save_file)
        self.master.bind("<Control-E>", self.save_file_as)
        self.master.bind("<Control-e>", self.save_file_as)
        self.master.bind("<Control-R>", self.run)
        self.master.bind("<Control-r>", self.run)

    def help_text(self):
        text = Label(self, text="Help!!!!!!!!!")
        text.pack()

    def open_file(self, *args, **kwargs):
        self.file_path = filedialog.askopenfilename(
            initialdir="./programs/",
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

    def save_file(self, *args, **kwargs):
        if self.file_path is None:
            self.save_file_as()
        else:
            self.save_file_as(file_path=self.file_path)

    def save_file_as(self, file_path=None, *args, **kwargs):
        text = self.text_editor.get("1.0", "end-1c")
        if file_path is None:
            self.file_path = filedialog.asksaveasfilename(
                initialdir="./programs/",
                title="Save as",
                filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
                defaultextension=".txt",
            )
        try:
            with open(self.file_path, 'w+') as file:
                file.write(text)
        except FileNotFoundError:
            messagebox.showinfo("File save exception:", "Blank name")

    def open_automatic_table(self, automatic_table):
        self.frame = Toplevel(self)
        self.frame.geometry("230x400")
        self.frame.title("Automatic machine")
        self.frame.resizable(False, False)

        table_margin = Frame(self.frame, width=500)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        columns=("State", "Label", "Stack"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('State', text="State", anchor=W)
        tree.heading('Label', text="Label", anchor=W)
        tree.heading('Stack', text="Stack", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=70)
        tree.column('#2', stretch=NO, minwidth=0, width=70)
        tree.column('#3', stretch=NO, minwidth=0, width=70)
        tree.pack()

        for row in automatic_table:
            tree.insert("", "end", values=(row[0], row[1], row[2]))

    def open_automatic_machine_table(self):
        self.frame = Toplevel(self)
        self.frame.geometry("370x400")
        self.frame.title("Automatic machine")
        self.frame.resizable(False, False)

        table_margin = Frame(self.frame, width=500)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        columns=("State", "Label", "Stack", "Next state", "!="),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('State', text="State", anchor=W)
        tree.heading('Label', text="Label", anchor=W)
        tree.heading('Stack', text="Stack", anchor=W)
        tree.heading('Next state', text="Next state", anchor=W)
        tree.heading('!=', text="!=", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=70)
        tree.column('#2', stretch=NO, minwidth=0, width=70)
        tree.column('#3', stretch=NO, minwidth=0, width=70)
        tree.column('#4', stretch=NO, minwidth=0, width=70)
        tree.column('#5', stretch=NO, minwidth=0, width=70)
        tree.pack()

        for state in self.automatic_machine.automatic_machine_table.keys():
            for label in self.automatic_machine.automatic_machine_table[state].keys():
                lab = ''
                if label:
                    lab = list(tokens_identifiers.keys())[list(tokens_identifiers.values()).index(label)]

                stack = self.automatic_machine.automatic_machine_table[state][label][0]
                if not stack:
                    stack = ''
                next_state = self.automatic_machine.automatic_machine_table[state][label][1]
                if not next_state:
                    next_state = ''
                subprogram = 'exit' if self.automatic_machine.automatic_machine_table[state][label][2] else 'err'

                tree.insert("", "end", values=(state, lab, stack, next_state, subprogram))

    def show_grammar(self):
        self.frame = Toplevel(self)
        self.frame.geometry("770x600")
        self.frame.title("Grammar")

        table_margin = Frame(self.frame, width=1000)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        columns=("rule", "tokens"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        tree.heading('rule', text="rule", anchor=W)
        tree.heading('tokens', text="tokens", anchor=W)

        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=10, width=150)
        tree.column('#2', stretch=NO, minwidth=100, width=600)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.pack()

        for key in self.bottom_up.grammar:
            rules = ''
            for variant in self.bottom_up.grammar[key]:
                rules += variant + ' | '
            rules = rules[:-3]
            tree.insert("", "end", values=(key, rules))

    def open_bottom_up_grammar_table(self):
        self.frame = Toplevel(self)
        self.frame.geometry("1300x700")
        self.frame.title("Bottom up table")

        table_margin = Frame(self.frame, width=1000)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        tree["columns"] = tuple(range(1, 68))
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.heading(1, text="", anchor=W)
        tree.column(1, stretch=NO, minwidth=20, width=70)
        for i in range(2, 68):
            tree.heading(i, text=self.bottom_up.rules_array[i-1], anchor=W)
            tree.column(i, stretch=NO, minwidth=20, width=70)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.pack()

        for row in self.bottom_up.bottom_up_grammar_table:
            tree.insert("", "end", values=row)

    def open_bottom_up_parse_table(self, bottom_up_table):
        self.frame = Toplevel(self)
        self.frame.geometry("1300x700")
        self.frame.title("Bottom up")

        table_margin = Frame(self.frame, width=1000)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        columns=("num", "stack", "rel", "input tokens"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        tree.heading('num', text="num", anchor=W)
        tree.heading('stack', text="stack", anchor=W)
        tree.heading('rel', text="rel", anchor=W)
        tree.heading('input tokens', text="input tokens", anchor=W)

        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=10, width=30)
        tree.column('#2', stretch=NO, minwidth=100, width=400)
        tree.column('#3', stretch=NO, minwidth=10, width=20)
        tree.column('#4', stretch=NO, minwidth=100, width=10000)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.pack()

        for index, row in enumerate(bottom_up_table):
            row.insert(0, index)
            tree.insert("", "end", values=row)

    def open_poliz_table(self, poliz_table):
        self.frame = Toplevel(self)
        self.frame.geometry("1300x700")
        self.frame.title("Poliz")

        table_margin = Frame(self.frame, width=1000)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
                        columns=('num', "input tokens", "stack", "poliz"),
                        height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

        tree.heading('num', text="num", anchor=W)
        tree.heading('input tokens', text="input tokens", anchor=W)
        tree.heading('stack', text="stack", anchor=W)
        tree.heading('poliz', text="poliz", anchor=W)

        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=10, width=30)
        tree.column('#2', stretch=NO, minwidth=100, width=400)
        tree.column('#3', stretch=NO, minwidth=10, width=200)
        tree.column('#4', stretch=NO, minwidth=100, width=10000)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.pack()

        for index, row in enumerate(poliz_table):
            row.insert(0, index)
            tree.insert("", "end", values=row)

    @staticmethod
    def open_tables_window():
        TablesWindow()

    def process_input_file(self):
        err_flag = False
        if self.file_path is None:
            text = self.text_editor.get("1.0", "end-1c")
            if text:
                self.save_file_as()
            else:
                self.open_file()

        try:
            self.program_file = ProgramFile(self.file_path)
        except OSError as err:
            err_flag = True
            messagebox.showinfo("Processing program file exception", str(err))
        return err_flag

    def run_lexical_analyzer(self, silent=False):
        err_flag = self.process_input_file()
        if not err_flag:
            try:
                self.tokens = self.lexical_analyzer(self.program_file)
            except IndexError:
                err_flag = True
                messagebox.showinfo("Lexical analyzer exception", "Index error")
            except Exception as err_type:
                err_flag = True
                messagebox.showinfo("Lexical analyzer exception", str(err_type))
            else:
                if not silent:
                    messagebox.showinfo("Lexical analyzer", "Success!")
                    self.program_file.write_results_to_files()
        return err_flag

    def run_recursive_descent(self, silent=False):
        err_flag = self.run_lexical_analyzer(silent=True)
        if not err_flag:
            try:
                self.recursive_descent(self.program_file)
            except IndexError:
                err_flag = True
                messagebox.showinfo("Recursive descent exception", "Index error (Program without 'end')")
            except Exception as err_type:
                err_flag = True
                messagebox.showinfo("Recursive descent exception", str(err_type))
            else:
                if not silent:
                    messagebox.showinfo("Recursive descent", "Success!")
            if not silent:
                self.program_file.write_results_to_files()
        return err_flag

    def run_automatic_machine(self, silent=False):
        err_flag = self.run_lexical_analyzer(silent=True)
        if not err_flag:
            msg = self.automatic_machine(self.program_file)
            if msg:
                err_flag = True
                messagebox.showinfo("Automatic machine exception", msg)
            elif not self.program_file.automatic_parse_table:
                err_flag = True
                messagebox.showinfo("Automatic machine exception", "Exception in state 1\nCheck begin of the program!")
            elif not (self.program_file.automatic_parse_table[-1][1] == 'end' and self.program_file.automatic_parse_table[-1][0] == 8):
                err_flag = True
                messagebox.showinfo("Automatic machine exception", 'Program without end, or incorrect last state')
            else:
                if not silent:
                    messagebox.showinfo("Automatic machine", "Success!")
            if not silent:
                self.open_automatic_table(self.program_file.automatic_parse_table)
                self.program_file.write_results_to_files()
        return err_flag

    def run_bottom_up(self, silent=False):
        err_flag = self.run_lexical_analyzer(silent=True)
        if not err_flag:
            msg = self.bottom_up(self.program_file)
            if msg:
                err_flag = True
                messagebox.showinfo("Bottom up exception", msg)
            else:
                if not silent:
                    messagebox.showinfo("Bottom up", "Success!")
            if not silent:
                self.open_bottom_up_parse_table(self.program_file.bottom_up_table)
                self.program_file.write_results_to_files()
        return err_flag

    def run_poliz(self, silent=False):
        err_flag = self.run_bottom_up(silent=True)
        if not err_flag:
            self.poliz(self.program_file)
            if not silent:
                messagebox.showinfo("Poliz", "Success!")
                self.open_poliz_table(self.program_file.poliz_table)
                self.program_file.write_results_to_files()
        return err_flag

    def run_poliz_processing(self, silent=False):
        err_flag = self.run_poliz(silent=True)
        if not err_flag:
            self.poliz_processing(self.program_file)
            if not silent:
                self.program_file.write_results_to_files()

    def run(self, *args, **kwargs):
        try:
            self.run_poliz_processing(silent=True)
        except Exception as err_type:
            messagebox.showinfo("Running exception", str(err_type))
        finally:
            self.program_file.write_results_to_files()


class TablesWindow(Toplevel):
    """
    Recursive descent results GUI
    """
    def __init__(self):
        super().__init__(root)

        self.init_tables_window()

    def init_tables_window(self):
        self.title("Recent files")
        self.geometry("150x600")
        self.resizable(False, False)
        self.show_files()

    def show_files(self):
        try:
            programs = next(os.walk('./results'))[1]
            for program in programs:
                Button(self, text=program, bd=1, bg='white', command=partial(self.show_tables, program)).pack(side=TOP)
        except StopIteration:
            messagebox.showinfo("File exception", "There is no results!")

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
        table_margin = Frame(self.frame, width=500)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
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

        with open("./results/" + program_name + "/tokens.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    def idn_table(self, program_name):
        table_margin = Frame(self.frame, width=300)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
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

        with open("./results/" + program_name + "/IDN.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    def con_table(self, program_name):
        table_margin = Frame(self.frame, width=300)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
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

        with open("./results/" + program_name + "/CONST.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2]))

    def lab_table(self, program_name):
        table_margin = Frame(self.frame, width=300)
        table_margin.pack(side=LEFT)
        scrollbarx = Scrollbar(table_margin, orient=HORIZONTAL)
        scrollbary = Scrollbar(table_margin, orient=VERTICAL)
        tree = Treeview(table_margin,
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

        with open("./results/" + program_name + "/LAB.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1]))


if __name__ == "__main__":

    root = Tk()
    app = Window(root)

    root.geometry("1200x600")
    root.resizable(False, False)
    root.mainloop()
