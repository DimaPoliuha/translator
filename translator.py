from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
import csv

from lexical_analyzer.analyzer import generate_tokens
from syntactical_analyzer.parser import parser


# GUI
class Window(Frame):

    def __init__(self, master=None, **kw):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)
        # reference to the master widget, which is the tk window
        super().__init__(master, **kw)
        # global params
        self.master = master
        self.text_editor = Text(self)
        self.text_editor.config(undo=True, autoseparators=True, maxundo=-1)
        self.file_path = None
        self.tokens = None

        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Translator")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file submenu in menu
        file_menu = Menu(menu, tearoff=0)
        # file_menu.add_command(label="New")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+A")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        # added "file_menu" to our menu
        menu.add_cascade(label="File", menu=file_menu)

        run_menu = Menu(menu, tearoff=0)
        run_menu.add_command(label="Lexical analyzer", command=self.lexical_analyzer)

        syntactical_analyse_menu = Menu(run_menu, tearoff=0)
        syntactical_analyse_menu.add_command(label="Recursive descent", command=self.syntactical_analyzer)
        syntactical_analyse_menu.add_command(label="2")
        syntactical_analyse_menu.add_command(label="3")

        run_menu.add_cascade(label="Syntactical analyse", menu=syntactical_analyse_menu)
        menu.add_cascade(label="Run", menu=run_menu)

        tables_menu = Menu(menu, tearoff=0)
        tables_menu.add_command(label="Tokens table", command=self.tokens_table)
        tables_menu.add_command(label="IDNs table", command=self.idn_table)
        tables_menu.add_command(label="CONs table", command=self.con_table)
        tables_menu.add_command(label="LABs table", command=self.lab_table)
        menu.add_cascade(label="Tables", menu=tables_menu)

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="How to use")
        help_menu.add_command(label="About us", command=self.help_text)
        menu.add_cascade(label="Help", menu=help_menu)

        self.master.bind("<Control-o>", self.open_file)
        self.master.bind("<Control-O>", self.open_file)
        self.master.bind("<Control-S>", self.save_file)
        self.master.bind("<Control-s>", self.save_file)
        self.master.bind("<Control-A>", self.save_file_as)
        self.master.bind("<Control-a>", self.save_file_as)
        self.text_editor.bind("<Control-y>", self.redo)
        self.text_editor.bind("<Control-Y>", self.redo)
        self.text_editor.bind("<Control-Z>", self.undo)
        self.text_editor.bind("<Control-z>", self.undo)

        # text input widget
        self.text_editor.pack()

        # save_file_btn = Button(self, text="Save file",
        #                        command=self.save_file,
        #                        )
        # save_file_btn.pack()

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
        with open(self.file_path, 'w+') as file:
            file.write(text)

    def redo(self, event=None):
        self.text_editor.edit_redo()

    def undo(self, event=None):
        self.text_editor.edit_undo()

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

    def lexical_analyzer(self):
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


if __name__ == "__main__":

    root = Tk()
    root.geometry("1200x600")
    app = Window(root)

    root.mainloop()
