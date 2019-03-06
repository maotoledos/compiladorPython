from tkinter import *
from tkinter.filedialog import *
from esp import Encabezado as ESP
from eng import Encabezado as ENG
from functions import changeValues, stringLex

fileName = None


def newFile():
    global fileName
    fileName = "Sin nombre"
    text.delete(0.0, END)


def saveFile():
    global fileName
    t = text.get(0.0, END)
    f = open(fileName, 'w')
    f.write(t)
    f.close()


def saveAs():
    f = asksaveasfile(mode='w', defaultextension='.txt')
    t = text.get(0.0, END)
    try:
        f.write(t.rstrip())  # delete white spaces
    except:
        showerror(title="Error!", message="No se pudo guardar el archivo...")


def openFile():
    f = askopenfile(mode='r')
    t = f.read()
    text.delete(0.0, END)
    text.insert(0.0, t)


def about():
    print("¡El idioma ha sido cambiado!")


def clicked(menu, filemenu):
    print("About")


def changeLanguage(idiomNum, menu, firstCasc, secondCasc, thirdCasc):
    idiomObj = ESP if idiomNum == 1 else ENG
    
    class Cascades:
        menu = menu
        first = firstCasc
        second = secondCasc
        third = thirdCasc
    changeValues(Cascades, idiomObj)

def retrieve_input():
    inputValue=text.get("1.0","end-1c")
    

    value = stringLex(inputValue)
    
    LexWindow = Toplevel(root)
    LexWindow.title("Analizador Lexico")
    LexWindow.minsize(width=300, height=300)
    LexWindow.maxsize(width=600, height=600)
    msg = Message(LexWindow, width=300, text=value)
    msg.pack()
    exitButton = Button(LexWindow, text="Salir", command=LexWindow.destroy)
    exitButton.pack()

def open_symb_table():
    inputValue='''
    Tipo de Variables:
    [int,double,float,bool,String,char,long,void,byte,const]\n
    Palabras reservadas:
    [for,while,if,catch,else,do,try,throw,struct]\n
    Operadores:
    [+,-,*,/,%,**,++,--,^]\n
    Operadores booleanos
    [==,!=, <>, <=, >=, !]
    '''
    

    
    LexWindow = Toplevel(root)
    LexWindow.title("Tabla de simbolos")
    LexWindow.minsize(width=400, height=300)
    LexWindow.maxsize(width=400, height=600)
    msg = Message(LexWindow, width=400, text=inputValue)
    msg.pack()
    exitButton = Button(LexWindow, text="Salir", command=LexWindow.destroy)
    exitButton.pack()

root = Tk()

mb=  Menubutton ( root, text="condiments", relief=RAISED )

root.title("Editor de texto de Python")

# icon = PhotoImage(file='me.gif')   
# root.tk.call('wm', 'iconphoto', root._w, icon)
# root.iconbitmap('@python.xbm')
# root.wm_iconbitmap('@/home/mauricio/Pictures/python.xbm')
root.minsize(width=400, height=400)
root.maxsize(width=600, height=600)

text = Text(root, width=200, height=200)
text.pack()  # displays textbox

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
icons = PhotoImage(file='python.gif')
icons = icons.subsample(8,8)
menu.add_cascade(label=ESP.archivo, image=icons, compound = LEFT, menu=filemenu)

filemenu.add_command(label=ESP.nuevo, command=newFile)
filemenu.add_command(label=ESP.abrir, command=openFile)
filemenu.add_command(label=ESP.guardar, command=saveFile)
filemenu.add_command(label=ESP.guardarComo, command=saveAs)
filemenu.add_separator()
filemenu.add_command(label=ESP.cerrar, command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label=ESP.ayuda,image=icons, compound = LEFT, menu=helpmenu)
helpmenu.add_command(label=ESP.acerca, command=clicked)

languages = Menu(menu)
menu.add_cascade(label=ESP.idiomas,image=icons, compound = LEFT, menu=languages)
languages.add_command(label="Español", command=lambda: changeLanguage(
    1, menu, filemenu, helpmenu, languages))
languages.add_command(label="Ingles", command=lambda: changeLanguage(
    2, menu, filemenu, helpmenu, languages))

lex = Menu(menu)
menu.add_cascade(label="LEX",image=icons, compound = LEFT, menu=lex)
lex.add_command(label="Abrir",command=lambda: retrieve_input())

tbs = Menu(menu)
menu.add_cascade(label="TBS",image=icons, compound = LEFT, menu=tbs)
tbs.add_command(label="Abrir",command=lambda: open_symb_table())

mainloop()
