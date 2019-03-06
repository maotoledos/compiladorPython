from specialWords import operators, letters
import re

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
    arrayLex = inputText.splitlines()
    for line, textLine in enumerate(arrayLex):
        token=""
        finalLex = finalLex+'Linea '+str(line+1)+': '
        for i, char in  enumerate(textLine):
            spaceOrTab = False
            spaceOrTab = re.match(r'(\s|\t)',char)
            # Si hay espacio
            if spaceOrTab:
                print(str(i)+token)
                tokenText = validateToken(token)
                if tokenText != False:
                    finalLex = finalLex + tokenText
                token = ''
                continue
            # Fin de linea
            if i == len(textLine)-1:
                token = token + char
                tokenText = validateToken(token)
                if tokenText != False:
                    finalLex = finalLex + tokenText
                token = ''
                continue

            # braces commas and python's enemy (;)
            braces = re.match(r'(\(|\)|\{|\}|\;|,|=)', char)
            if braces:
                tokenText = validateToken(token)
                if tokenText != False:
                    finalLex = finalLex + tokenText
                finalLex = finalLex + ' braces('+braces.group()+')'
                token = ''
                continue
            
            
            token = token + char
    return finalLex

def validateToken(token):
    lexPatt = re.match(r'(int|double|float|bool|String|char|long|void|byte|const)$', token)
    if lexPatt:
        return ' varType('+lexPatt.group()+')'
    # funciones con parentesis van al inicio
    lexPatt = re.match(r'(for|while|if|catch)$', token)
    if lexPatt:
        return ' funcPar('+lexPatt.group()+')'
    # funciones sin parentesis van al inicio
    lexPatt = re.match(r'(else|do|try|throw|struct)$', token)
    if lexPatt:
        return ' funcNonPar('+lexPatt.group()+')'
    # numeros
    lexPatt = re.match(r'([-+]?\d*\.\d+|[-]?\d+)$',token)
    if lexPatt:
        return' number('+lexPatt.group()+')'
    # operador de asignacion
    lexPatt = re.match(r'=|\+\+|\-\-|\*\*$',token)
    if lexPatt:
        return' asigOp('+lexPatt.group()+')'
    # variables
    lexPatt = re.match(r'[A-Za-z_]+?\w*',token)
    if lexPatt:
        return' ID('+lexPatt.group()+')'
    # Operadores Aritmeticos
    lexPatt = re.match(r"[\+|\-|\*|\/|\%]{1}$",token)
    if lexPatt:
        return ' opArit('+lexPatt.group()+')'
    # Operadores bitwise
    lexPatt = re.finditer(r"[\&|\||\^|\~|\<\<|\>\>]{1,2}",token)
    for pat in lexPatt:
        return ' opBit('+pat.group()+')'
    # Operadores booleanos
    lexPatt = re.finditer(r"[\=\=|\!\=|\<|\>|\<\=|\>\=]{2}",token)
    for pat in lexPatt:
        return ' opBool('+pat.group()+')'
    # Operadores de asignacion
    lexPatt = re.finditer(r"(\(|\)|\{|\}|\;|,|=)$",token)
    for pat in lexPatt:
        return ' asigOp('+pat.group()+')'
    return False