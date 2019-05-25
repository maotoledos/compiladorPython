from specialWords import operators, letters
import re
from languages import Language

lang = Language('c++')

def changeValues(cascades, idiomObj):
    #Encabezados
    cascades.menu.entryconfigure(1, label=idiomObj.archivo)
    cascades.menu.entryconfigure(2, label=idiomObj.ayuda)
    cascades.menu.entryconfigure(3, label=idiomObj.idiomas)
    #Menus desplegables
    cascades.first.entryconfigure(1, label=idiomObj.nuevo)
    cascades.first.entryconfigure(2, label=idiomObj.abrir)
    cascades.first.entryconfigure(3, label=idiomObj.guardar)
    cascades.first.entryconfigure(4, label=idiomObj.guardarComo)
    cascades.first.entryconfigure(6, label=idiomObj.cerrar)

    cascades.second.entryconfigure(1, label=idiomObj.acerca)

    cascades.third.entryconfigure(1, label=idiomObj.espanol)
    
def stringLex(inputText):
    finalLex = ""
    token = ""
    identificadores = ""
    operadores = ""
    reservados=""
    arrayLex = inputText.splitlines()
    for line, textLine in enumerate(arrayLex):
        token=""
        finalLex = finalLex+str(line+1)+'>>'
        for i, char in  enumerate(textLine):
            spaceOrTab = False
            spaceOrTab = re.match(r'(\s|\t)',char)
            # Si hay espacio
            if spaceOrTab:
                tokenText, numero = validateToken(token)

                if numero == 1:
                    identificadores= identificadores + tokenText+'\n'
                elif numero == 2:
                    operadores= operadores + tokenText+'\n'
                elif numero == 3:
                    reservados= reservados + tokenText+'\n'
                    
                if tokenText != False:
                    finalLex = finalLex + tokenText
                token = ''
                continue
            # Fin de linea
            if i == len(textLine)-1:
                token = token + char
                tokenText, numero= validateToken(token)
                if numero == 1:
                    identificadores= identificadores + tokenText+'\n'
                elif numero == 2:
                    operadores= operadores + tokenText+'\n'
                elif numero == 3:
                    reservados= reservados + tokenText+'\n'

                if tokenText != False:
                    finalLex = finalLex + tokenText
                token = ''
                continue

            # braces commas and python's enemy (;)
            braces = re.match(r'(\(|\)|\{|\}|\|,|=|>|<)', char)
            if braces:
                tokenText, numero = validateToken(token)
                if numero == 1:
                    identificadores= identificadores + tokenText+'\n'
                elif numero == 2:
                    operadores= operadores + tokenText+'\n'
                elif numero == 3:
                    reservados= reservados + tokenText+'\n'

                if tokenText != False:
                    finalLex = finalLex + tokenText
                finalLex = finalLex + ' separator('+braces.group()+')'
                token = ''
                continue
            
            
            token = token + char
        finalLex = finalLex+'\n'
    return finalLex, identificadores, operadores, reservados

def validateToken(token):
    lexPatt = re.match(r'(int|double|float|bool|String|char|long|void|byte|const|using|iostream|namespace|std|argc|NULL|printf|IOException|vector|wchar_t)$', token)
    if lexPatt:
        return ' palabra_reservada('+lexPatt.group()+')',3
    # funciones con parentesis van al inicio
    lexPatt = re.match(r'(for|while|if|catch)$', token)
    if lexPatt:
        return ' bucle_o_condicion('+lexPatt.group()+')',3
    # funciones sin parentesis van al inicio
    lexPatt = re.match(r'(else|do|try|throw|struct)$', token)
    if lexPatt:
        return ' funcion('+lexPatt.group()+')',3
    # numeros
    lexPatt = re.match(r'([-+]?\d*\.\d+|[-]?\d+)$',token)
    if lexPatt:
        return' numero('+lexPatt.group()+')',1
    # operador de asignacion
    lexPatt = re.match(r'=|\+\+|\-\-|\*\*$',token)
    if lexPatt:
        return' incremento_decremento('+lexPatt.group()+')',2
    # variables
    lexPatt = re.match(r'[A-Za-z_]+?\w*',token)
    if lexPatt:
        return ' variable('+lexPatt.group()+')',1
    # Operadores Aritmeticos
    lexPatt = re.match(r"[\+|\-|\*|\/|\%]{1}$",token)
    if lexPatt:
        return ' operador_aritmetico('+lexPatt.group()+')',2
    # Operadores bitwise
    lexPatt = re.finditer(r"[\&|\||\^|\~|\<\<|\>\>]{1,2}",token)
    for pat in lexPatt:
        return ' operador_bitwise('+pat.group()+')',2
    # Operadores booleanos
    lexPatt = re.finditer(r"[\=\=|\!\=|\<|\>|\<\=|\>\=]{2}",token)
    for pat in lexPatt:
        return ' comparador_booleano('+pat.group()+')',2
    # Operadores de asignacion
    lexPatt = re.finditer(r"(\(|\)|\{|\}|\;|,|=)$",token)
    for pat in lexPatt:
        return ' operador_asignacion('+pat.group()+')',3
    return False, 0


def convertToJava(inputText):
    finalLex = 'package net.mauricio.compilador;\nimport java.util.*;'
    token = ""
    identificadores = ""
    operadores = ""
    reservados=""
    arrayLex = inputText.splitlines()
    for line, textLine in enumerate(arrayLex):
        token=""
        arrayCpp = ['printf', 'int main(int argc, char* argv[])','#include','<iostream>','using namespace std','NULL','bool','const','throw','vector','<int>::iterator','cout <<',
        'string','void','virtual void','A::','wchar_t','struct','};']
        arrayJava = ['System.out.println', 'public static void main(String args[])','','','','null','boolean','final','throws','ArrayList','Iterator','System.out.println(',
        'String','final void','abstract','super.','int','class','}']
        for i, text in enumerate(arrayCpp):
            textLine = textLine.replace(arrayCpp[i],arrayJava[i])

        
        # for i, char in  enumerate(textLine):
        #     spaceOrTab = False
        #     spaceOrTab = re.match(r'(\s|\t)',char)
        #     # Si hay espacio
        #     if spaceOrTab:
        #         print(str(i)+token)
        #         tokenText, numero = validateLanguage(token)

        #         if numero == 1:
        #             identificadores= identificadores + tokenText+'\n'
        #         elif numero == 2:
        #             operadores= operadores + tokenText+'\n'
        #         elif numero == 3:
        #             reservados= reservados + tokenText+'\n'
                    
        #         print(numero)
        #         if tokenText != False:
        #             finalLex = finalLex + tokenText
        #         token = ''
        #         continue
        #     # Fin de linea
        #     if i == len(textLine)-1:
        #         token = token + char
        #         tokenText, numero= validateLanguage(token)
        #         if numero == 1:
        #             identificadores= identificadores + tokenText+'\n'
        #         elif numero == 2:
        #             operadores= operadores + tokenText+'\n'
        #         elif numero == 3:
        #             reservados= reservados + tokenText+'\n'

        #         if tokenText != False:
        #             finalLex = finalLex + tokenText
        #         token = ''
        #         continue

        #     # braces commas and python's enemy (;)
        #     braces = re.match(r'(\(|\)|\{|\}|\;|,|=)', char)
        #     if braces:
        #         tokenText, numero = validateLanguage(token)
        #         if numero == 1:
        #             identificadores= identificadores + tokenText+'\n'
        #         elif numero == 2:
        #             operadores= operadores + tokenText+'\n'
        #         elif numero == 3:
        #             reservados= reservados + tokenText+'\n'

        #         if tokenText != False:
        #             finalLex = finalLex + tokenText
        #         finalLex = finalLex + ' '+braces.group()
        #         token = ''
        #         continue
            
            
        #     token = token + char
        if textLine != '':
            finalLex = finalLex+textLine+'\n'
    return finalLex, identificadores, operadores, reservados

def validateLanguage(token):
    lang = Language('java')
    lexPatt = re.match(r'(int|double|float|bool|string|char|long|byte|const|unsigned|signed|short|wchar_t|cout<<)$', token)
    if lexPatt:
        return ' '+lang.render(lexPatt.group()),3
    # funciones con parentesis van al inicio
    lexPatt = re.match(r'(for|while|if|catch|void)$', token)
    if lexPatt:
        return ' '+lexPatt.group(),3
    # funciones sin parentesis van al inicio
    lexPatt = re.match(r'(else|do|try|throw|struct)$', token)
    if lexPatt:
        return ' '+lexPatt.group(),3
    # numeros
    lexPatt = re.match(r'([-+]?\d*\.\d+|[-]?\d+)$',token)
    if lexPatt:
        return' '+lexPatt.group(),1
    # operador de asignacion
    lexPatt = re.match(r'=|\+\+|\-\-|\*\*$',token)
    if lexPatt:
        return' '+lexPatt.group(),2
    # variables
    lexPatt = re.match(r'[A-Za-z_]+?\w*',token)
    if lexPatt:
        return ' '+lexPatt.group(),1
    # Operadores Aritmeticos
    lexPatt = re.match(r"[\+|\-|\*|\/|\%]{1}$",token)
    if lexPatt:
        return ' '+lexPatt.group(),2
    # Operadores bitwise
    lexPatt = re.finditer(r"[\&|\||\^|\~|\<\<|\>\>]{1,2}",token)
    for pat in lexPatt:
        return ' '+pat.group(),2
    # Operadores booleanos
    lexPatt = re.finditer(r"[\=\=|\!\=|\<|\>|\<\=|\>\=]{2}",token)
    for pat in lexPatt:
        return ' '+pat.group(),2
    # Operadores de asignacion
    lexPatt = re.finditer(r"(\(|\)|\{|\}|\;|,|=)$",token)
    for pat in lexPatt:
        return ' '+pat.group(),3
    return False, 0