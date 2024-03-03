try:
    import mainLexical
except ImportError:
    import mainLexical as mainLexical

from mainSyntax import SyntaxAnalyzer
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import simpledialog
from idlelib.tooltip import Hovertip
filepath = ''

#Events
def lbutton_hover(event):
    lex_button.configure(image=compile1, bg='#323131')
def lbutton_leave(event):
    lex_button.configure(image=compile, bg='#323131')
def text_hover(event):
    toggle_btn.configure(fg="white")
def text_leave(event):
    toggle_btn.configure(fg="#E3e4e4")

#Assets
IDE = tk.Tk()
IDE.title('Mapitagan PL')
IDE.geometry('1225x680')
IDE.resizable(False, False)
IDE.iconphoto(False, tk.PhotoImage(file='blank.png'))
canvas = tk.Canvas(IDE, width=1275, height=700)
canvas.pack()
img = tk.PhotoImage(file="bg.png")
canvas.create_image(0, 0, anchor=tk.NW, image=img)
compile = PhotoImage(file="compile.png")
compile = compile.subsample(55, 55)
compile1 = PhotoImage(file="compile1.png")
compile1 = compile1.subsample(55, 55)
icon = PhotoImage(file="mapitaganicon.png")
icon = icon.subsample(50, 50)
cancel = PhotoImage(file="cancel.png")
cancel = cancel.subsample(70, 70)

# Initialize the tokenizer
tokenizer = mainLexical.CodeTokenizer()

# Function to update line numbers
def update_line_numbers(*args):
    editor_line_numbers.config(state=tk.NORMAL)
    editor_line_numbers.delete("1.0", tk.END)
    line_count = editor.get("1.0", tk.END).count('\n')
    for i in range(1, line_count + 1):
        editor_line_numbers.insert(tk.END, f"{i}\n")
    editor_line_numbers.config(state=tk.DISABLED)
    editor_line_numbers.yview_moveto(editor.yview()[0])

# Function to tokenize the input code
def tokenize(code): 
    tokens = tokenizer.tokenize_code(code)
    return tokens

def lexeme_to_syntax_tokens(tokens): #eto ung ginamit naten for syntax analysis
    tokens_only = [item[1] for item in tokens]
    return tokens_only

# Defined Functions
def exit_():
    IDE.destroy()

def set_file_path(path):
    global filepath
    filepath = path

def save_as():
    if filepath == '':
        path = asksaveasfilename(filetypes=[('KPP Files', '*.kpp')])
    else:
        path = filepath

    with open(path, 'w') as file:
        text = editor.get('1.0', tk.END)
        file.write(text)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[('KPP Files', '*.kpp')])
    with open(path, 'r') as file:
        text = file.read()
        editor.delete('1.0', tk.END)
        editor.insert('1.0', text)
        set_file_path(path)

def toggle_menu():
    def collapse():
        toggle_menu_fm.destroy()
        toggle_btn.configure(command=toggle_menu)
    def open_enter(e):
        open_button['background'] = '#29b0e3'
    def open_leave(e):
        open_button['background'] = 'gray22'
    def save_enter(e):
        save_button['background'] = '#29b0e3'
    def save_leave(e):
        save_button['background'] = 'gray22'
    def save_as_enter(e):
        save_as_button['background'] = '#29b0e3'
    def save_as_leave(e):
        save_as_button['background'] = 'gray22'
    def undo_enter(e):
        undo_button['background'] = '#29b0e3'
    def undo_leave(e):
        undo_button['background'] = 'gray22'
    def redo_enter(e):
        redo_button['background'] = '#29b0e3'
    def redo_leave(e):
        redo_button['background'] = 'gray22'
    def find_enter(e):
        find_button['background'] = '#29b0e3'
    def find_leave(e):
        find_button['background'] = 'gray22'
    def exit_enter(e):
        exit_button['background'] = '#29b0e3'
    def exit_leave(e):
        exit_button['background'] = 'gray22'

    toggle_menu_fm = tk.Frame(IDE, bg="gray22", highlightbackground="#8e8c8c", highlightthickness=1)

    style = ttk.Style()
    style.configure('Thick.TSeparator',thickness='1')
    # Create the buttons
    open_button = tk.Button(toggle_menu_fm, text="Open        Ctrl+O    ", command=open_file, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    open_button.place(x=5, y=10)
    open_button.bind("<Enter>", open_enter)
    open_button.bind("<Leave>", open_leave)
    save_button = tk.Button(toggle_menu_fm, text="Save         Ctrl+S    ", command=save_as, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    save_button.place(x=5, y=40)
    save_button.bind("<Enter>", save_enter)
    save_button.bind("<Leave>", save_leave)
    save_as_button = tk.Button(toggle_menu_fm, text="Save As    Ctrl+S    ", command=save_as, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    save_as_button.place(x=5, y=70)
    save_as_button.bind("<Enter>", save_as_enter)
    save_as_button.bind("<Leave>", save_as_leave)
    separator = ttk.Separator(toggle_menu_fm, orient='horizontal', style='Thick.TSeparator')
    separator.place(x=0, y=95, width=200)
    undo_button = tk.Button(toggle_menu_fm, text="Undo         Ctrl+Z    ", command=editor.edit_undo, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    undo_button.place(x=5, y=100)
    undo_button.bind("<Enter>", undo_enter)
    undo_button.bind("<Leave>", undo_leave)
    redo_button = tk.Button(toggle_menu_fm, text="Redo         Ctrl+Y    ", command=editor.edit_redo, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    redo_button.place(x=5, y=130)
    redo_button.bind("<Enter>", redo_enter)
    redo_button.bind("<Leave>", redo_leave)
    find_button = tk.Button(toggle_menu_fm, text="Find           Ctrl+F    ", command=toggle_search_word, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    find_button.place(x=5, y=160)
    find_button.bind("<Enter>", find_enter)
    find_button.bind("<Leave>", find_leave)
    separator = ttk.Separator(toggle_menu_fm, orient='horizontal', style='Thick.TSeparator')
    separator.place(x=0, y=185, width=200)
    exit_button = tk.Button(toggle_menu_fm, text="Exit            Ctrl+X    ", command=exit_, bg="gray22", fg="white", bd=0, font=custom_font, activebackground="white", activeforeground='white')
    exit_button.place(x=5, y=190)
    exit_button.bind("<Enter>", exit_enter)
    exit_button.bind("<Leave>", exit_leave)

    toggle_menu_fm.place(x=50, y=30, height=220, width=150)
    toggle_btn.configure(command=collapse)

# Modify the lex function to use the CodeTokenizer class
def lex():
    lexeme_token_dict = {} #optional logic for efficency
    token_copy = []
    input_text = editor.get("1.0", "end-1c")

    # Tokenize the input text
    tokens, lex_error_output = tokenizer.tokenize_code(input_text + '\n')

    # Clear previous content
    error_display.config(state=tk.NORMAL)
    error_display.delete("1.0", tk.END)
    table_frame.config(state=tk.NORMAL)
    table_frame.delete("1.0", tk.END)

    for lexeme, token, line_number in tokens:
        table_frame.insert(tk.END, f"{line_number}\t{lexeme}\t\t\t\t{token}\n")
        token_copy.append(token)

    for item in lex_error_output:
        if len(item) == 3:
            # Unpack with three values
            token, lexeme, line_number = item
            error_display.insert(tk.END, f"{line_number}\t{token}\t\t\t\t{lexeme}\n")
        elif len(item) == 4:
            # Unpack with four values
            token, lexeme, suggestion, line_number = item
            error_display.insert(tk.END, f"{line_number}\t{token}\t\t{lexeme}: {suggestion}.\n")
    
    # Disable editing in the text widgets
    error_display.config(state=tk.DISABLED)
    table_frame.config(state=tk.DISABLED)

    #Start of syntax analysis when there is no lexical error
    if not lex_error_output:

        error_display.config(state=tk.NORMAL)
        error_display.delete("1.0", tk.END)

        syntax_tokens = lexeme_to_syntax_tokens(tokens) #eto ung ginamit naten for syntax analysis
        print("Tokens from lexer")
        print(syntax_tokens) #eto ung ginamit naten for syntax analysis

        #Syntax Analysis
        analyzer = SyntaxAnalyzer(tokens)
        analyzer.analyze()
        if not analyzer.synErrors:
            print("\nSyntax analysis successful!")
        else:
            print("\nSyntax errors:")
            for error in analyzer.synErrors:
                print(error)
                error_display.insert(tk.END, f"{error}")
                error_display.config(state=tk.DISABLED)
    else:
        error_display.insert(tk.END, f"Lexical errors found. Syntax analysis will not be performed.")
        error_display.config(state=tk.DISABLED)
        return line_number
    
def toggle_search_word():
    search =  tk.Frame(IDE, bg="#323131", highlightbackground="#8e8c8c", highlightthickness=1)
    search.place(x=905, y=30, height=40, width=300)

    cancel_search = tk.Button(search, image=cancel, font="Helvetica 10", bg="#323131", fg="white", bd=0, activebackground="white", activeforeground='white', command=lambda: on_cancel())
    cancel_search.place(x=272, y=11)
    
    def clear_entry(event, entry):
        entry.delete(0, 'end')
        entry.configure(font="Helvetica 10")
            
    entry = tk.Entry(search, font="Helvetica 10 italic", width=30, bg="#86898a", fg="white", bd=1, relief=tk.RIDGE)
    entry.insert(0, "Enter word to find")
    entry.bind('<Button-1>', lambda event: clear_entry(event, entry))
    entry.place(x=5, y=10)
    result_label = tk.Label(search, text="", font="Helvetica 10", bg="#323131", fg="white")
    result_label.place(x=220, y=8)

    def find_word():
        word = entry.get()
        if word:
            editor.tag_remove('highlight', '1.0', 'end')
            start = '1.0'
            count = 0
            while True:
                pos = editor.search(word, start, stopindex='end')
                if not pos:
                    break
                end = f'{pos}+{len(word)}c'
                editor.tag_add('highlight', pos, end)
                start = end
                count += 1
            editor.tag_config('highlight', background='#028fc7')
            result_label.config(text=f"{count}")

    def on_cancel():
        editor.tag_remove('highlight', '1.0', 'end')
        search.destroy()

    entry.bind('<Return>', lambda event: find_word())
    search.bind('<Escape>', lambda event: on_cancel())

def change_highlight_color(event=None):
    editor.tag_config('highlight', background='#54a6c7')

# GUI customization
custom_font = ("Helvetica", 11)
custom_font1 = ("Helvetica", 10)
custom_fontMenu = ("Cascadia Mono Bold", 10)

# Create and configure Text widgets for line numbers, editor, and lexemes
editor_line_numbers = tk.Text(IDE, width=6, height=25, borderwidth=2, relief=tk.RIDGE, bg="gray22", fg="white", font=custom_font)
editor_line_numbers.place(y=77, x=18)
editor_line_numbers.config(state=tk.DISABLED)

editor = tk.Text(IDE, height=25, width=94, borderwidth=2, relief=tk.RIDGE, fg="white", bg="gray22", font=custom_font, wrap="none", undo=True)
editor.place(y=77, x=70)

# Bind shortcut keys
IDE.bind("<Control-z>", lambda event: editor.edit_undo())
IDE.bind("<Control-y>", lambda event: editor.edit_redo())
IDE.bind("<Control-o>", lambda event: open_file())
IDE.bind("<Control-s>", lambda event: save_as())
IDE.bind("<Control-x>", lambda event: exit_())
IDE.bind("<Control-r>", lambda event: lex())
IDE.bind('<Control-f>', lambda event: toggle_search_word())
editor.bind('<Button-1>', change_highlight_color)

error_display = tk.Text(IDE, height=9, width=115, borderwidth=2, relief=tk.RIDGE, bg="gray22", fg="white", font=custom_font1)
error_display.place(y=507, x=18)
error_display.config(bg="gray22")

table_frame = tk.Text(IDE, height=36, width=50, borderwidth=2, relief=tk.RIDGE, fg="white", font=custom_font1)
table_frame.place(y=75, x=850)
table_frame.configure(bg="gray22")

error_display.config(state=tk.DISABLED)
table_frame.config(state=tk.DISABLED)

header =  tk.Frame(IDE, bg="#323131", highlightbackground="#8e8c8c", highlightthickness=1)
icon_label = tk.Label(header, image=icon, bg="#323131")
icon_label.pack(side="left", padx=9)
toggle_btn = tk.Button(header, text="File", font=custom_font1, bg="#323131", bd=0, fg='#E3e4e4', activebackground="white", activeforeground='white', command=toggle_menu)
toggle_btn.pack(side="left", padx=10)
toggle_btn.bind("<Enter>", text_hover)
toggle_btn.bind("<Leave>", text_leave)

lex_button = tk.Button(header, image=compile, command=lex, borderwidth=0, relief=tk.RIDGE, bg="#323131")
lex_button.pack(side="right", padx=10)
lex_button.bind("<Enter>", lbutton_hover)
lex_button.bind("<Leave>", lbutton_leave)

header.place(x=0, y=0)
header.pack_propagate(0)
header.configure(height=30, width=1225)

# Bind events to the button
editor.bind("<KeyRelease>", update_line_numbers)
editor.bind("<MouseWheel>", update_line_numbers)
editor.bind("<Button-4>", update_line_numbers)
editor.bind("<Button-5>", update_line_numbers)
editor.bind('<Configure>', update_line_numbers)
editor_line_numbers.unbind("<MouseWheel>")
editor_line_numbers.unbind("<Button-4>")
editor_line_numbers.unbind("<Button-5>")
editor_line_numbers.unbind('<Configure>')
# Bind editor scrolling events
editor_line_numbers.bind("<MouseWheel>", update_line_numbers)
editor_line_numbers.bind("<Button-4>", update_line_numbers)
editor_line_numbers.bind("<Button-5>", update_line_numbers)
editor_line_numbers.bind('<Configure>', update_line_numbers)

IDE.mainloop()