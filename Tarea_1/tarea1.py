def cubo(num: int)->int: 
    return num **3

def factorial(num: int)->int: 
    if num > 0: 
        return num * factorial(num-1)
    elif num == 0: 
        return 1
    return None

def cuenta_patron(patron: str, cadena: str)->int: 
    rep = 0
    i = 0
    j = 0
    while i < len(cadena) - len(patron) + 1: 
        if cadena[i: i + len(patron)] == patron: 
            rep += 1
        i += 1
    return rep

def arbol_ref(arbol: list, rama: tuple): 
    tree = arbol
    for r in rama: 
        if isinstance(tree, list) and len(tree) >= r+1: 
            tree = tree[r]
        else: 
            return None
    return tree

#Establece el orden de operaciones
def notacion_postfija(expresion: str)->list: 
    numero = ""
    operadores = []
    postfija = []
    i = 0
    prioridades = {"(": 0, ")": 0, "+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    while i < len(expresion): 
        if expresion[i] in "0123456789": 
            numero += expresion[i]
        elif expresion[i] in "abcdefghijklmnopqrstuvwxyz": 
            if len(numero) > 0: 
                postfija.append(["NUM", numero])
                numero = ""
            postfija.append(["VAR", expresion[i]])
        elif expresion[i] == "(":
            if len(numero) > 0: 
                postfija.append(["NUM", numero])
                numero = ""
            operadores.append(["OP", expresion[i]])
        elif expresion[i] == ")":
            if len(numero) > 0: 
                postfija.append(["NUM", numero])
                numero = ""
            j = len(operadores)-1
            while operadores[j][1] != "(": 
                postfija.append(operadores.pop())
                j -= 1
            operadores.pop()
        elif expresion[i] in "+-*/^":
            if len(numero) > 0: 
                postfija.append(["NUM", numero])
                numero = ""
            while len(operadores) > 0 and prioridades[expresion[i][0]] <= prioridades[operadores[len(operadores)-1][1]]: 
                postfija.append(operadores.pop())
            else: 
                operadores.append(["OP", expresion[i]])
        i+=1
    if len(numero) > 0: 
        postfija.append(["NUM", numero])
    while len(operadores) > 0: 
        postfija.append(operadores.pop())
    return postfija

#Organiza la lista postfija para preparar la evaluación
def agrupar(postfija: list)->list: 
    i = 0
    while i < len(postfija):
        if postfija[i][1] == "+" or postfija[i][1] == "-": 
            postfija[i] = ["ADD" if postfija[i][1] == "+" else "SUB", postfija[i-2], postfija[i-1]]
            i -= 2
            postfija.pop(i)
            postfija.pop(i)
        elif postfija[i][1] == "*" or postfija[i][1] == "/": 
            postfija[i] = ["MUL" if postfija[i][1] == "*" else "DIV", postfija[i-2], postfija[i-1]]
            i -= 2
            postfija.pop(i)
            postfija.pop(i)
        elif postfija[i][1] == "^": 
            postfija[i] = ["POW", postfija[i-2], postfija[i-1]]
            i -= 2
            postfija.pop(i)
            postfija.pop(i)
        i += 1
    return postfija[0]

#Distribuye las multiplicaciones y divisiones sobre las sumas y restas
def distribuir(postfija: list): 
    if len(postfija) > 2: 
        if postfija[0] == "MUL" or postfija[0] == "DIV":
            if postfija[1][0] == "ADD" or postfija[1][0] == "SUB": 
                op = postfija[1][0]
                p1 = [postfija[0], postfija[2], postfija[1][1]]
                p2 = [postfija[0], postfija[2], postfija[1][2]]
                postfija = [op, p1, p2]
            elif postfija[2][0] == "ADD" or postfija[2][0] == "SUB": 
                op = postfija[2][0]
                p1 = [postfija[0], postfija[1], postfija[2][1]]
                p2 = [postfija[0], postfija[1], postfija[2][2]]
                postfija = [op, p1, p2]
        postfija[1] = distribuir(postfija[1])
        postfija[2] = distribuir(postfija[2])    
    return postfija

#Desarrolla la lista postfija para regresar la expresión deseada
def resolver(postfija: list):
    if len(postfija) > 2: 
        if postfija[0] == "ADD":
            return resolver(postfija[1]) + "+" + resolver(postfija[2])
        elif postfija[0] == "SUB": 
            return resolver(postfija[2]) + "-(" + resolver(postfija[2])+")"
        elif postfija[0] == "MUL" or postfija[0] == "DIV":
            if (
                (postfija[1][0] == "NUM" or postfija[1][0] == "MUL" or postfija[1][0] == "DIV" or postfija[1][0] == "POW" or postfija[1][0] == "VAR") 
                and (postfija[2][0] == "NUM" or postfija[2][0] == "MUL" or postfija[2][0] == "DIV" or postfija[2][0] == "POW" or postfija[2][0] == "VAR")
            ):
                return resolver(postfija[1]) + ("*" if postfija[0] == "MUL" else "/") + resolver(postfija[2])
            else: 
                if postfija[1][0] == "ADD" or postfija[1][0] == "SUB": 
                    return resolver([postfija[0], postfija[1][1], postfija[2]]) + ("+" if postfija[1][0] == "ADD" else "-") + resolver([postfija[0], postfija[1][2], postfija[2]])
                else:
                    return resolver([postfija[0], postfija[1], postfija[2][1]]) + ("+" if postfija[2][0] == "ADD" else "-") + resolver([postfija[0], postfija[1], postfija[2][2]])
        elif postfija[0] == "POW": 
            return "("+resolver(postfija[1])+")^("+resolver(postfija[2])+")"
        else: 
            # "It shouldn't come here"
            pass
        return
    return postfija[1]

def desarrollar_expresion(expresion: str):
    return resolver(distribuir(agrupar(notacion_postfija(expresion))))

if __name__=="__main__":
    print("Cubo de 8: "+str(cubo(8)))

    print("Factorial de 15: "+str(factorial(15)))

    print("Cuántas veces ocurre el patrón 'aba' en la cadena 'gabababa': "+str(cuenta_patron("aba", "gabababa")))

    arbol = [[[1, 2], 3], [4, [5, 6]], 7, [8, 9, 10]]
    print("Árbol: "+str(arbol))

    print("Rama (1, 1, 1) del árbol: "+str(arbol_ref(arbol, (1, 1, 1))))

    exp = "((2 * (x + 1)) ^ (y + 3))/(8-7*z)"
    print("\nExpresión: "+exp)
    print("Expresión desarrollada: "+desarrollar_expresion(exp))