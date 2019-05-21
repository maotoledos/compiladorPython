import tkinter as tk
from tkinter import messagebox

# custom made class for managing ui languages
from languages import Language


class MainWindow(tk.Frame):
    menu_bar = None
    context_menu = None
    selected_text = None
    text_field = None

    def __init__(self, master, lang='en'):
        super().__init__(master)
        self.master = master

        # sets the language for using on the window
        self.lang = Language(lang)
        self.create_ui()

    def create_ui(self):
        self.create_window_menu()
        self.add_text_field()

    def create_window_menu(self):
        """
        Create window menu and submenus
        :return:
        """
        self.menu_bar = tk.Menu()

        file_menu = tk.Menu(self.menu_bar)
        file_menu.add_command(label=self.lang.render('close'), command=self.quit)
        self.menu_bar.add_cascade(label=self.lang.render('file'), menu=file_menu)

        lang_menu = tk.Menu(self.menu_bar)
        lang_menu.add_command(label=self.lang.render('es'), command=lambda: self.change_language('es'))
        lang_menu.add_command(label=self.lang.render('en'), command=lambda: self.change_language('en'))
        self.menu_bar.add_cascade(label=self.lang.render('language'), menu=lang_menu)

        self.master.config(menu=self.menu_bar)

    def add_text_field(self):
        """
        Add text field and create the context menu
        """
        self.text_field = tk.Text(self.master)
        self.text_field.pack()
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Perform action", command=self.context_action)
        # <Button-3> stands for right click
        self.text_field.bind("<Button-3>", self.show_context_menu)
        self.pack()

    def show_context_menu(self, event):
        """
        Pops-up the context menu and validates text selection from `self.text_field`
        """
        try:
            self.selected_text = self.text_field.get("sel.first", "sel.last")
        except Exception:
            self.selected_text = None
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def context_action(self):
        """
        Performs an arbitrary function if some text has been selected
        :return:
        """
        if self.selected_text:
            messagebox.showinfo("Info", self.selected_text)

    def change_language(self, code):
        self.lang.code = code
        sub_menus = self.menu_bar.winfo_children()
        self.menu_bar.entryconfigure(1, label=self.lang.render('file'))
        self.menu_bar.entryconfigure(2, label=self.lang.render('language'))
        sub_menus[0].entryconfigure(1, label=self.lang.render('close'))
        sub_menus[1].entryconfigure(1, label=self.lang.render('es'))
        sub_menus[1].entryconfigure(2, label=self.lang.render('en'))


root = tk.Tk()
app = MainWindow(root)
root.mainloop()
