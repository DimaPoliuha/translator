from lexical_analyzer.add_token import tokens
i = 0
relation_signs = [">", "<", ">=", "<=", "==", "!="]


def parser():
    global i
    program()


def program():
    global i
    if declaration_list():
        if tokens[i][2] == 'begin':
            i += 1
            if operators_list():
                if tokens[i][2] == 'end':
                    i += 1
                    return True
                else:
                    print('program without end ' + str(tokens[i][2]))
                    return False
            else:
                print('err operators list (out) ' + str(tokens[i][2]))
                return False
        else:
            print('program without begin ' + str(tokens[i][2]))
            return False
    else:
        print('err declaration list (out) ' + str(tokens[i][2]))
        return False


def declaration_list():
    global i
    if declaration():
        if tokens[i][2] == ';':
            i += 1
            while declaration():
                if tokens[i][2] == ';':
                    i += 1
                else:
                    print('err declaration without ; ' + str(tokens[i][2]))
                    return False
            return True
        else:
            print('err declaration without ; ' + str(tokens[i][2]))
            return False
    else:
        print('err declaration (out) ' + str(tokens[i][2]))
        return False


def declaration():
    global i
    if variable_type():
        if variables_list():
            return True
        else:
            print('err variables list (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err variable type (out) ' + str(tokens[i][2]))
        return False


def variable_type():
    global i
    if tokens[i][2] == 'int':
        i += 1
        return True
    elif tokens[i][2] == 'float':
        i += 1
        return True
    else:
        print('err variable type ' + str(tokens[i][2]))
        return False


def variables_list():
    global i
    if identifier():
        if tokens[i][2] == ',':
            i += 1
            if not variables_list():
                print('err variables list (out) ' + str(tokens[i][2]))
                return False
            return True
        else:
            return True
    else:
        print('err identifier (out) ' + str(tokens[i][2]))
        return False


def operators_list():
    global i
    if operator():
        if tokens[i][2] == ';':
            i += 1
        else:
            print('err operator without ; ' + str(tokens[i][2]))
            return False
    elif label():
        if tokens[i][2] == ':':
            i += 1
        else:
            print('err label without : ' + str(tokens[i][2]))
            return False
    else:
        print('err operators list ' + str(tokens[i][2]))
        return False
    while operator():
        if tokens[i][2] == ';':
            i += 1
        else:
            print('err operator (out) ' + str(tokens[i][2]))
            return False
    while label():
        if tokens[i][2] == ':':
            i += 1
        else:
            print('err label (out) ' + str(tokens[i][2]))
            return False
    return True


def operator():
    global i
    if assignment():
        return True
    elif user_input():
        return True
    elif user_output():
        return True
    elif loop():
        return True
    elif conditional_statement():
        return True
    elif tokens[i][2] == 'goto':
        i += 1
        if label():
            return True
        else:
            print('err label (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err operator ' + str(tokens[i][2]))
        return False


def user_input():
    global i
    if tokens[i][2] == 'cin':
        i += 1
        if tokens[i][2] == '>>':
            i += 1
            if identifier():
                while tokens[i][2] == '>>':
                    i += 1
                    if not identifier():
                        print('err identifier (out) ' + str(tokens[i][2]))
                        return False
                return True
            else:
                print('err identifier (out) ' + str(tokens[i][2]))
                return False
        else:
            print('err cin without >> ' + str(tokens[i][2]))
            return False
    else:
        print('err user input ' + str(tokens[i][2]))
        return False


def user_output():
    global i
    if tokens[i][2] == 'cout':
        i += 1
        if tokens[i][2] == '<<':
            i += 1
            if identifier():
                while tokens[i][2] == '<<':
                    i += 1
                    if not identifier():
                        print('err identifier (out) ' + str(tokens[i][2]))
                        return False
                return True
            else:
                print('err identifier (out) ' + str(tokens[i][2]))
                return False
        else:
            print('err cout without << ' + str(tokens[i][2]))
            return False
    else:
        print('err user output ' + str(tokens[i][2]))
        return False


def loop():
    global i
    if tokens[i][2] == 'for':
        i += 1
        if identifier():
            if tokens[i][2] == '=':
                i += 1
                if expression():
                    if tokens[i][2] == 'by':
                        i += 1
                        if expression():
                            if tokens[i][2] == 'to':
                                i += 1
                                if expression():
                                    if tokens[i][2] == 'do':
                                        i += 1
                                        if operators_list():
                                            if tokens[i][2] == 'rof':
                                                i += 1
                                                return True
                                            else:
                                                print('err for without rof ' + str(tokens[i][2]))
                                                return False
                                        else:
                                            print('err operators list (out) ' + str(tokens[i][2]))
                                            return False
                                    else:
                                        print('err for without do ' + str(tokens[i][2]))
                                        return False
                                else:
                                    print('err expression (out) ' + str(tokens[i][2]))
                                    return False
                            else:
                                print('err for without to ' + str(tokens[i][2]))
                                return False
                        else:
                            print('err expression (out) ' + str(tokens[i][2]))
                            return False
                    else:
                        print('err for without by ' + str(tokens[i][2]))
                        return False
                else:
                    print('err expression (out) ' + str(tokens[i][2]))
                    return False
            else:
                print('err = in for ' + str(tokens[i][2]))
                return False
        else:
            print('err identifiers (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err loop ' + str(tokens[i][2]))
        return False


def conditional_statement():
    global i
    if tokens[i][2] == 'if':
        i += 1
        if ratio():
            if tokens[i][2] == 'then':
                i += 1
                if operators_list():
                    if tokens[i][2] == 'fi':
                        i += 1
                        return True
                    else:
                        print('err conditional statement without fi ' + str(tokens[i][2]))
                        return False
                else:
                    print('err operators list (out) ' + str(tokens[i][2]))
                    return False
            else:
                print('err conditional statement without then ' + str(tokens[i][2]))
                return False
        else:
            print('err ratio (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err conditional statement ' + str(tokens[i][2]))
        return False


def assignment():
    global i
    if identifier():
        if tokens[i][2] == '=':
            i += 1
            if expression():
                return True
            else:
                print('err expression (out) ' + str(tokens[i][2]))
                return False
        else:
            print('err assignment without = ' + str(tokens[i][2]))
            return False
    else:
        print('err identifier (out) ' + str(tokens[i][2]))
        return False


def expression():
    global i
    if t():
        True
    elif tokens[i][2] == '-':
        i += 1
        if t():
            True
        else:
            print('err t (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err expression ' + str(tokens[i][2]))
        return False
    while tokens[i][2] == '+':
        i += 1
        if not t():
            print('err t (out) ' + str(tokens[i][2]))
            return False
    while tokens[i][2] == '-':
        i += 1
        if not t():
            print('err t (out) ' + str(tokens[i][2]))
            return False
    return True


def t():
    global i
    if f():
        while tokens[i][2] == '*':
            i += 1
            if f():
                True
            else:
                print('err f (out) ' + str(tokens[i][2]))
                return False
        while tokens[i][2] == '/':
            i += 1
            if f():
                True
            else:
                print('err f (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        print('err t ' + str(tokens[i][2]))
        return False


def f():
    global i
    if identifier():
        return True
    elif constant_fixed_accuracy():
        return True
    elif tokens[i][2] == '(':
        i += 1
        if expression():
            if tokens[i][2] == ')':
                i += 1
                return True
            else:
                print('err without ) ' + str(tokens[i][2]))
                return False
        else:
            print('err expression (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err f ' + str(tokens[i][2]))
        return False


def identifier():
    global i
    if character():
        while character() or digit():
            continue
        return True
    else:
        print('err identifier ' + str(tokens[i][2]))
        return False


def character():
    global i
    if tokens[i][2].isalpha():
        i += 1
        return True
    else:
        print('err character ' + str(tokens[i][2]))
        return False


def digit():
    global i
    if tokens[i][2].isdigit():
        i += 1
        return True
    else:
        print('err digit ' + str(tokens[i][2]))
        return False


def constant_fixed_accuracy():
    global i
    if number():
        if tokens[i][2] == '.':
            i += 1
            if number():
                return True
            return True
        return True
    elif tokens[i][2] == '.':
        i += 1
        if number():
            return True
        else:
            print('err number (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err constant fixed accuracy ' + str(tokens[i][2]))
        return False


def number():
    global i
    if digit():
        while digit():
            continue
        return True
    else:
        print('err number ' + str(tokens[i][2]))
        return False


def ratio():
    global i
    if lt():
        while tokens[i][2] == 'or':
            i += 1
            if not lt():
                print('err lt (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        print('err lt (out) ' + str(tokens[i][2]))
        return False


def lt():
    global i
    if lf():
        while tokens[i][2] == 'and':
            i += 1
            if not lf():
                print('err lf (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        print('err lf (out) ' + str(tokens[i][2]))
        return False


def lf():
    global i
    if relation():
        return True
    elif tokens[i][2] == '[':
        i += 1
        if ratio():
            if tokens[i][2] == ']':
                i += 1
                return True
            else:
                print('err without ] ' + str(tokens[i][2]))
                return False
        else:
            print('err ratio (out) ' + str(tokens[i][2]))
            return False
    elif tokens[i][2] == 'not':
        i += 1
        if lf():
            return True
        else:
            print('err lf (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err lf ' + str(tokens[i][2]))
        return False


def relation():
    global i
    if expression():
        if relation_sign():
            if expression():
                return True
            else:
                print('err expression (out) ' + str(tokens[i][2]))
                return False
        else:
            print('err relation sign  (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err relation ' + str(tokens[i][2]))
        return False


def relation_sign():
    global i
    if tokens[i][2] in relation_signs:
        i += 1
        return True
    else:
        print('err relation sign ' + str(tokens[i][2]))
        return False


def label():
    global i
    if tokens[i][2] == '#':
        i += 1
        if identifier():
            return True
        else:
            print('err identifier  (out) ' + str(tokens[i][2]))
            return False
    else:
        print('err label ' + str(tokens[i][2]))
        return False
