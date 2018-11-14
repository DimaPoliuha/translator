from lexical_analyzer.add_token import tokens
i = 0
relation_signs = [">", "<", ">=", "<=", "==", "!="]


def parser():
    try:
        program()
    except Exception as err_type:
        print('Syntactical analyzer exception:\n' +
              str(err_type) +
              '\ntoken number: ' + str(tokens[i][0]) +
              '\nline number: ' + str(tokens[i][1]) +
              '\ntoken: ' + repr(tokens[i][2]))


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
                    print('err program without end ' + str(tokens[i][2]))
                    return False
            else:
                print('err operators list (out) ' + str(tokens[i][2]))
                return False
        else:
            print('err program without begin ' + str(tokens[i][2]))
            return False
    else:
        print('err program ' + str(tokens[i][2]))
        return False


def declaration_list():
    global i
    if declaration():
        if tokens[i][2] == ';':
            i += 1
            while declaration(True):
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
        print('err declaration list ' + str(tokens[i][2]))
        return False


def declaration(option=False):
    global i
    temp = i
    if variable_type(option):
        if variables_list(option):
            return True
        else:
            if option:
                i = temp
                return False
            print('err variables list (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err declaration ' + str(tokens[i][2]))
        return False


def variable_type(option=False):
    global i
    temp = i
    if tokens[i][2] == 'int' or tokens[i][2] == 'float':
        i += 1
        return True
    else:
        if option:
            i = temp
            return False
        print('err variable type ' + str(tokens[i][2]))
        return False


def variables_list(option=False):
    global i
    temp = i
    if identifier(option):
        if tokens[i][2] == ',':
            i += 1
            if variables_list(option):
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err variables list (out) ' + str(tokens[i][2]))
                return False
        else:
            return True
    else:
        if option:
            i = temp
            return False
        print('err variables list ' + str(tokens[i][2]))
        return False


def operators_list(option=False):
    global i
    temp = i
    if operator(True):
        if tokens[i][2] == ';':
            i += 1
        else:
            if option:
                i = temp
                return False
            print('err operator without ; ' + str(tokens[i][2]))
            return False
    elif label(True):
        if tokens[i][2] == ':':
            i += 1
        else:
            if option:
                i = temp
                return False
            print('err label without : ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err operators list ' + str(tokens[i][2]))
        return False
    loop_count = 0
    while True:
        loop_count += 1
        while operator(True):
            loop_count = 0
            if tokens[i][2] == ';':
                i += 1
            else:
                if option:
                    i = temp
                    return False
                print('err operator (out) ' + str(tokens[i][2]))
                return False
        while label(True):
            loop_count = 0
            if tokens[i][2] == ':':
                i += 1
            else:
                if option:
                    i = temp
                    return False
                print('err label (out) ' + str(tokens[i][2]))
                return False
        if loop_count > 2:
            break
    return True


def operator(option=False):
    global i
    temp = i
    if assignment(True) or user_input(True) or user_output(True) or loop(True) or conditional_statement(True):
        return True
    elif tokens[i][2] == 'goto':
        i += 1
        if label(option):
            return True
        else:
            if option:
                i = temp
                return False
            print('err label (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err operator ' + str(tokens[i][2]))
        return False


def user_input(option=False):
    global i
    temp = i
    if tokens[i][2] == 'cin':
        i += 1
        if tokens[i][2] == '>>':
            i += 1
            if identifier(option):
                while tokens[i][2] == '>>':
                    i += 1
                    if identifier(option):
                        continue
                    else:
                        if option:
                            i = temp
                            return False
                        print('err identifier (out) ' + str(tokens[i][2]))
                        return False
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err identifier (out) ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err cin without >> ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err user input ' + str(tokens[i][2]))
        return False


def user_output(option=False):
    global i
    temp = i
    if tokens[i][2] == 'cout':
        i += 1
        if tokens[i][2] == '<<':
            i += 1
            if identifier(option):
                while tokens[i][2] == '<<':
                    i += 1
                    if identifier(option):
                        continue
                    else:
                        if option:
                            i = temp
                            return False
                        print('err identifier (out) ' + str(tokens[i][2]))
                        return False
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err identifier (out) ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err cout without << ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err user output ' + str(tokens[i][2]))
        return False


def loop(option=False):
    global i
    temp = i
    if tokens[i][2] == 'for':
        i += 1
        if identifier(option):
            if tokens[i][2] == '=':
                i += 1
                if expression(option):
                    if tokens[i][2] == 'by':
                        i += 1
                        if expression(option):
                            if tokens[i][2] == 'to':
                                i += 1
                                if expression(option):
                                    if tokens[i][2] == 'do':
                                        i += 1
                                        if operators_list(option):
                                            if tokens[i][2] == 'rof':
                                                i += 1
                                                return True
                                            else:
                                                if option:
                                                    i = temp
                                                    return False
                                                print('err for without rof ' + str(tokens[i][2]))
                                                return False
                                        else:
                                            if option:
                                                i = temp
                                                return False
                                            print('err operators list (out) ' + str(tokens[i][2]))
                                            return False
                                    else:
                                        if option:
                                            i = temp
                                            return False
                                        print('err for without do ' + str(tokens[i][2]))
                                        return False
                                else:
                                    if option:
                                        i = temp
                                        return False
                                    print('err expression (out) ' + str(tokens[i][2]))
                                    return False
                            else:
                                if option:
                                    i = temp
                                    return False
                                print('err for without to ' + str(tokens[i][2]))
                                return False
                        else:
                            if option:
                                i = temp
                                return False
                            print('err expression (out) ' + str(tokens[i][2]))
                            return False
                    else:
                        if option:
                            i = temp
                            return False
                        print('err for without by ' + str(tokens[i][2]))
                        return False
                else:
                    if option:
                        i = temp
                        return False
                    print('err expression (out) ' + str(tokens[i][2]))
                    return False
            else:
                if option:
                    i = temp
                    return False
                print('err = in for ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err identifiers (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err loop ' + str(tokens[i][2]))
        return False


def conditional_statement(option=False):
    global i
    temp = i
    if tokens[i][2] == 'if':
        i += 1
        if ratio():
            if tokens[i][2] == 'then':
                i += 1
                if tokens[i][2] == ':':
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
                    print('err conditional statement without : ' + str(tokens[i][2]))
                    return False
            else:
                print('err conditional statement without then ' + str(tokens[i][2]))
                return False
        else:
            print('err ratio (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err conditional statement ' + str(tokens[i][2]))
        return False


def assignment(option=False):
    global i
    temp = i
    if identifier(option):
        if tokens[i][2] == '=':
            i += 1
            if expression(option):
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err expression (out) ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err assignment without = ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err assignment ' + str(tokens[i][2]))
        return False


def expression(option=False):
    global i
    temp = i
    if t(True):
        True
    elif tokens[i][2] == '-':
        i += 1
        if t(option):
            True
        else:
            if option:
                i = temp
                return False
            print('err t (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err expression ' + str(tokens[i][2]))
        return False
    while tokens[i][2] == '+' or tokens[i][2] == '-':
        i += 1
        if t(option):
            continue
        else:
            if option:
                i = temp
                return False
            print('err t (out) ' + str(tokens[i][2]))
            return False
    return True


def t(option=False):
    global i
    temp = i
    if f(option):
        while tokens[i][2] == '*' or tokens[i][2] == '/':
            i += 1
            if f(option):
                continue
            else:
                if option:
                    i = temp
                    return False
                print('err f (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        if option:
            i = temp
            return False
        print('err t ' + str(tokens[i][2]))
        return False


def f(option=False):
    global i
    temp = i
    if identifier(True) or constant_fixed_accuracy(True):
        return True
    elif tokens[i][2] == '(':
        i += 1
        if expression(option):
            if tokens[i][2] == ')':
                i += 1
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err without ) ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err expression (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err f ' + str(tokens[i][2]))
        return False


def identifier(option=False):
    global i
    temp = i
    if tokens[i][6] == 100:
        i += 1
        return True
    else:
        if option:
            i = temp
            return False
        print('err identifier ' + str(tokens[i][2]))
        return False


def constant_fixed_accuracy(option=False):
    global i
    temp = i
    if tokens[i][6] == 101:
        i += 1
        return True
    else:
        if option:
            i = temp
            return False
        print('err constant fixed accuracy ' + str(tokens[i][2]))
        return False


def ratio(option=False):
    global i
    temp = i
    if lt(option):
        while tokens[i][2] == 'or':
            i += 1
            if lt(option):
                continue
            else:
                if option:
                    i = temp
                    return False
                print('err lt (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        if option:
            i = temp
            return False
        print('err ratio ' + str(tokens[i][2]))
        return False


def lt(option=False):
    global i
    temp = i
    if lf(option):
        while tokens[i][2] == 'and':
            i += 1
            if lf(option):
                continue
            else:
                if option:
                    i = temp
                    return False
                print('err lf (out) ' + str(tokens[i][2]))
                return False
        return True
    else:
        if option:
            i = temp
            return False
        print('err lt ' + str(tokens[i][2]))
        return False


def lf(option=False):
    global i
    temp = i
    if relation(True):
        return True
    elif tokens[i][2] == '[':
        i += 1
        if ratio(option):
            if tokens[i][2] == ']':
                i += 1
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err without ] ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err ratio (out) ' + str(tokens[i][2]))
            return False
    elif tokens[i][2] == 'not':
        i += 1
        if lf(option):
            return True
        else:
            if option:
                i = temp
                return False
            print('err lf (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err lf ' + str(tokens[i][2]))
        return False


def relation(option=False):
    global i
    temp = i
    if expression(option):
        if relation_sign(option):
            if expression(option):
                return True
            else:
                if option:
                    i = temp
                    return False
                print('err expression (out) ' + str(tokens[i][2]))
                return False
        else:
            if option:
                i = temp
                return False
            print('err relation sign  (out) ' + str(tokens[i][2]))
            return False
    else:
        if option:
            i = temp
            return False
        print('err relation ' + str(tokens[i][2]))
        return False


def relation_sign(option=False):
    global i
    temp = i
    if tokens[i][2] in relation_signs:
        i += 1
        return True
    else:
        if option:
            i = temp
            return False
        print('err relation sign ' + str(tokens[i][2]))
        return False


def label(option=False):
    global i
    temp = i
    if tokens[i][6] == 102:
        i += 1
        return True
    else:
        if option:
            i = temp
            return False
        print('err label ' + str(tokens[i][2]))
        return False
