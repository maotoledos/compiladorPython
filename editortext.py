from tkinter import *
from tkinter.filedialog import *
from esp import Encabezado as ESP
from eng import Encabezado as ENG
from tkinter import messagebox

from functions import changeValues, stringLex, convertToJava

import re

import random
import time


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
    inputValue = text.get("1.0", "end-1c")
    value, identificadores, operadores, reservados = stringLex(inputValue)
    print(operadores)
    LexWindow = Toplevel(root)
    LexWindow.title("Analizador Lexico")
    frame1 = Frame(LexWindow)
    frame1.pack(side=TOP)
    msg = Text(frame1)
    msg.insert(INSERT, value)
    msg.pack(side=TOP, anchor=N, padx=5, pady=5)
    frame2 = Frame(LexWindow)
    frame2.pack(side=BOTTOM)
    msg2 = Text(frame2, height=50, width=25)
    msg2.insert(INSERT,identificadores)
    msg2.pack(side=LEFT)
    msg3 = Text(frame2, height=50, width=25)
    msg3.insert(INSERT,operadores)
    msg3.pack(side=LEFT)
    msg4 = Text(frame2, height=50, width=25)
    msg4.insert(INSERT,reservados)
    msg4.pack(side=LEFT)
    exitButton = Button(frame2, text="Salir", command=LexWindow.destroy)
    exitButton.pack(side=BOTTOM)


def open_symb_table():
    inputValue = text.get("1.0", "end-1c")
    output = ""
    token = ""    

    splitLines = inputValue.splitlines()
    for numLine, textLine in enumerate(splitLines):
        token= ""
        for charLength, letter in enumerate(textLine):
            spaceOrTab = False
            spaceOrTab = re.match(r'(\s|\t)',letter)
            if spaceOrTab:
                continue
            
            output = output + letter
def open_tree_expression(markedText):
    
    LexWindow = Toplevel(root)
    LexWindow.title("Tabla de simbolos")
    LexWindow.minsize(width=400, height=300)
    LexWindow.maxsize(width=400, height=600)
    msg = Message(LexWindow, width=400, text=markedText)
    msg.pack()
    exitButton = Button(LexWindow, text="Salir", command=LexWindow.destroy)
    exitButton.pack()
    OPERATORS = set(['+', '-', '*', '/', '(', ')'])
    PRIORITY = {'+':1, '-':1, '*':2, '/':2}


    ### INFIX ===> POSTFIX ###
    '''
    1)Fix a priority level for each operator. For example, from high to low:
        3.    - (unary negation)
        2.    * /
        1.    + - (subtraction)
    2) If the token is an operand, do not stack it. Pass it to the output. 
    3) If token is an operator or parenthesis:
        3.1) if it is '(', push
        3.2) if it is ')', pop until '('
        3.3) push the incoming operator if its priority > top operator; otherwise pop.
        *The popped stack elements will be written to output. 
    4) Pop the remainder of the stack and write to the output (except left parenthesis)
    '''
    def infix_to_postfix(formula):
        stack = [] # only pop when the coming op has priority 
        output = ''
        for ch in formula:
            if ch not in OPERATORS:
                output += ch
            elif ch == '(':
                stack.append('(')
            elif ch == ')':
                while stack and stack[-1] != '(':
                    output += stack.pop()
                stack.pop() # pop '('
            else:
                while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                    output += stack.pop()
                stack.append(ch)
        # leftover
        while stack: output += stack.pop()
        print(output)
        return output


    ### POSTFIX ===> INFIX ###
    '''
    1) When see an operand, push
    2) When see an operator, pop out two numbers, connect them into a substring and push back to the stack
    3) the top of the stack is the final infix expression.
    '''
    def postfix_to_infix(formula):
        stack = []
        prev_op = None
        for ch in formula:
            if not ch in OPERATORS:
                stack.append(ch)
            else:
                b = stack.pop()
                a = stack.pop()
                if prev_op and len(a) > 1 and PRIORITY[ch] > PRIORITY[prev_op]:
                    # if previous operator has lower priority
                    # add '()' to the previous a
                    expr = '('+a+')' + ch + b
                else:
                    expr = a + ch + b
                stack.append(expr)
                prev_op = ch
        print( stack[-1])
        return stack[-1]


    ### INFIX ===> PREFIX ###
    def infix_to_prefix(formula):
        op_stack = []
        exp_stack = []
        for ch in formula:
            if not ch in OPERATORS:
                exp_stack.append(ch)
            elif ch == '(':
                op_stack.append(ch)
            elif ch == ')':
                while op_stack[-1] != '(':
                    op = op_stack.pop()
                    a = exp_stack.pop()
                    b = exp_stack.pop()
                    exp_stack.append( op+b+a )
                op_stack.pop() # pop '('
            else:
                while op_stack and op_stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[op_stack[-1]]:
                    op = op_stack.pop()
                    a = exp_stack.pop()
                    b = exp_stack.pop()
                    exp_stack.append( op+b+a )
                op_stack.append(ch)
        
        # leftover
        while op_stack:
            op = op_stack.pop()
            a = exp_stack.pop()
            b = exp_stack.pop()
            exp_stack.append( op+b+a )
        print( exp_stack[-1])
        return exp_stack[-1]


    ### PREFIX ===> INFIX ###
    '''
    Scan the formula reversely
    1) When the token is an operand, push into stack
    2) When the token is an operator, pop out 2 numbers from stack, merge them and push back to the stack
    '''
    def prefix_to_infix(formula):
        stack = []
        prev_op = None
        for ch in reversed(formula):
            if not ch in OPERATORS:
                stack.append(ch)
            else:
                a = stack.pop()
                b = stack.pop()
                if prev_op and PRIORITY[prev_op] < PRIORITY[ch]:
                    exp = '('+a+')'+ch+b
                else:
                    exp = a+ch+b
                stack.append(exp)
                prev_op = ch
        print( stack[-1])
        return stack[-1]


    '''
    Scan the formula:
    1) When the token is an operand, push into stack; 
    2) When an operator is encountered: 
        2.1) If the operator is binary, then pop the stack twice 
        2.2) If the operator is unary (e.g. unary minus), pop once 
    3) Perform the indicated operation on two poped numbers, and push the result back
    4) The final result is the stack top.
    '''
    def evaluate_postfix(formula):
        stack = []
        for ch in formula:
            if ch not in OPERATORS:
                stack.append(float(ch))
            else:
                b = stack.pop()
                a = stack.pop()
                c = {'+':a+b, '-':a-b, '*':a*b, '/':a/b}[ch]
                stack.append(c)
        print( stack[-1])
        return stack[-1]


    def evaluate_infix(formula):
        return evaluate_postflix(inflix_to_postfix(formula))


    ''' Whenever we see an operator following by two numbers, 
    we can compute the result.'''
    def evaluate_prefix(formula):
        exps = list(formula)
        while len(exps) > 1:
            for i in range(len(exps)-2):
                if exps[i] in OPERATORS:
                    if not exps[i+1] in OPERATORS and not exps[i+2] in OPERATORS:
                        op, a, b = exps[i:i+3]
                        a,b = map(float, [a,b])
                        c = {'+':a+b, '-':a-b, '*':a*b, '/':a/b}[op]
                        exps = exps[:i] + [c] + exps[i+3:]
                        break
            print( exps)
        return exps[-1]


    if __name__ == '__main__':
        infix_to_postfix(markedText)
    ruut=Tk()
    ruut.geometry("1200x600")
    myCanvas = Canvas(ruut, width=1200,height=600,bg="black")
    myCanvas.pack()
    ruut.configure(background="black")
    ruut.attributes("-topmost", True)
    x_first=600
    y_first=50
    vals=infix_to_postfix(markedText)
    circles=dict()
    j=0
    def create_circle(x,y,r,canvasName):
        x0=x-r
        y0=y-r
        x1=x+r
        y1=y+r
        return canvasName.create_oval(x0,y0,x1,y1,fill="red")
    def line(x1,y1,x2,y2,canvasName):
        return canvasName.create_line(x1,y1,x2,y2,fill="white",width=2,smooth=True)
    c=x_first
    d=y_first
    cf=1/(len(vals)-1)
    def create_tree(c,d,i=0,mc=1.2):
        
        if i<len(vals):
            z=create_circle(c,d,20,myCanvas)
            ruut.update()
            m=Label(ruut,text=vals[i],bg="red",fg="white")
            m.config(font=("courier 16 bold"))
            m.place(x=c-8,y=d-12)
            circles[vals[i]]=(z,m)
            ruut.update()
            #time.sleep(0.5)
            if 2*i+1 <len(vals):
                x=line(c,d+20,c-100*mc,d+100,myCanvas)
                ruut.update()
                #time.sleep(0.5)
            create_tree(c-(100*mc),d+100,2*i+1,mc-mc*cf)
            if 2*i+2<len(vals):
                x=line(c,d+20,c+100*mc,d+100,myCanvas)
                ruut.update()
                #time.sleep(0.5)
            create_tree(c+(100*mc),d+100,2*i+2,mc-mc*2*cf)
            ruut.update()
    create_tree(c,d)

    class tree:
        def __init__(self,val,i=0):
            if i<len(val):
                self.val=val[i]
                self.left=tree(val,2*i+1)
                self.right=tree(val,2*i+2)
            else:
                self.left=None
                self.right=None
        def inorder(self):
            global inorder,circles,myCanvas,ruut,xc
            if self.left is not None and self.right is not None:
                self.left.inorder()
                c=circles[self.val]
                myCanvas.itemconfig(c[0],fill="yellow")
                c[1].configure(bg="yellow",fg="black")
                m=Label(ruut,text=self.val,fg="white",bg="black",font="courier 15 bold")
                m.place(x=xc,y=460)
                ruut.update()
                time.sleep(0.5)
                xc+=30
                self.right.inorder()
        def preorder(self,level=0):
            global inorder,circles,myCanvas,ruut,xc
            if self.left is not None and self.right is not None:
                c=circles[self.val]
                myCanvas.itemconfig(c[0],fill="yellow")
                c[1].configure(bg="yellow",fg="black")
                m=Label(ruut,text=self.val,fg="white",bg="black",font="courier 15 bold")
                m.place(x=xc,y=460)
                ruut.update()
                time.sleep(0.5)
                xc+=30
                self.left.preorder(level+1)
                self.right.preorder(level+1)
        def postorder(self):
            global inorder,circles,myCanvas,ruut,xc
            if self.left is not None and self.right is not None:
                self.left.postorder()
                self.right.postorder()
                c=circles[self.val]
                myCanvas.itemconfig(c[0],fill="yellow")
                c[1].configure(bg="yellow",fg="black")
                m=Label(ruut,text=self.val,fg="white",bg="black",font="courier 15 bold")
                m.place(x=xc,y=460)
                ruut.update()
                time.sleep(0.5)
                xc+=30

    tr=tree(vals)
    m=Label(ruut,text="Traversal:",fg="white",bg="black",font="courier 15 bold")
    m.place(x=10,y=460)
    xc=160
    tr.postorder()
    ruut.mainloop()

def context_action(self):
    """
    Performs an arbitrary function if some text has been selected
    :return:
    """
    if self.selected_text:
        messagebox.showinfo("Info", self.selected_text)

def changeToJava():
    inputValue = text.get("1.0", "end-1c")
    finalLex, identificadores, operadores, reservados = convertToJava(inputValue)
    print(finalLex)
    text.delete(0.0, END)
    text.insert("1.0",finalLex)






root = Tk()

mb = Menubutton(root, text="condiments", relief=RAISED)

root.title("Editor de texto de Python")

root.minsize(width=400, height=400)
root.maxsize(width=600, height=600)

text = Text(root, width=200, height=200)
"""
    Text selection
"""
def show(event):
    """
    Pops-up the context menu and validates text selection from `self.text`
    """
    try:
        selected_text = text.get("sel.first", "sel.last")
    except Exception:
        selected_text = None
    context_menu.tk_popup(event.x_root, event.y_root)
    messagebox.showinfo("Info", selected_text)
    open_tree_expression(selected_text)



text.pack()  # displays textbox
context_menu = Menu(tearoff=0)
text.bind("<Button-3>",show)
text.pack()






menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
icons = PhotoImage(file='python.gif')
icons = icons.subsample(8, 8)
openfile = PhotoImage(file='help.gif')
openfile = openfile.subsample(8, 8)
menu.add_cascade(label=ESP.archivo, image=icons, compound=LEFT, menu=filemenu)

filemenu.add_command(label=ESP.nuevo, command=newFile)
filemenu.add_command(label=ESP.abrir, command=openFile)
filemenu.add_command(label=ESP.guardar, command=saveFile)
filemenu.add_command(label=ESP.guardarComo, command=saveAs)
filemenu.add_separator()
filemenu.add_command(label=ESP.cerrar, command=root.quit)



helpmenu = Menu(menu)
menu.add_cascade(label=ESP.ayuda, image=openfile, compound=LEFT, menu=helpmenu)
helpmenu.add_command(label=ESP.acerca, command=clicked)

languages = Menu(menu)
menu.add_cascade(label=ESP.idiomas, image=icons, compound=LEFT, menu=languages)
languages.add_command(label="Español", command=lambda: changeLanguage(1, menu, filemenu, helpmenu, languages))
languages.add_command(label="Ingles", command=lambda: changeLanguage(2, menu, filemenu, helpmenu, languages))

lex = Menu(menu)
menu.add_cascade(label="LEX", image=icons, compound=LEFT, menu=lex)
lex.add_command(label="Abrir", command=lambda: retrieve_input())

tbs = Menu(menu)
menu.add_cascade(label="Expresion", image=icons, compound=LEFT, menu=tbs)
tbs.add_command(label="Abrir", command=lambda: open_symb_table())

switchLanguage = Menu(menu)
menu.add_cascade(label="Switch", image=icons, compound=LEFT, menu=switchLanguage)
switchLanguage.add_command(label="Java", command=lambda: changeToJava())

mainloop()




