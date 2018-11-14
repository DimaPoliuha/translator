from lexical_analyzer.add_token import tokens
i = 0
relation_signs = [">", "<", ">=", "<=", "==", "!="]


def parser():
    try:
        program()
    except Exception as err_type:
        print('Syntactical analyzer exception: ' +
              str(err_type) +
              '\n\ntoken number: ' + str(tokens[i][0]) +
              '\nline number: ' + str(tokens[i][1]) +
              '\ntoken: ' + repr(tokens[i][2]))
        return False
    else:
        return True


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
                    raise Exception('err program without end')
        else:
            raise Exception('err program without begin')


def declaration_list():
    global i
    if declaration():
        if tokens[i][2] == ';':
            i += 1
            while declaration(True):
                if tokens[i][2] == ';':
                    i += 1
                else:
                    raise Exception('err declaration without ;')
            return True
        else:
            raise Exception('err declaration without ;')


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
    else:
        if option:
            i = temp
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
        raise Exception('err variable type')


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
        else:
            return True
    else:
        if option:
            i = temp
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
            raise Exception('err operator without ;')
    elif label(True):
        if tokens[i][2] == ':':
            i += 1
        else:
            if option:
                i = temp
                return False
            raise Exception('err label without :')
    else:
        if option:
            i = temp
            return False
        raise Exception('err operators list')

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
                raise Exception('err operator without ;')
        while label(True):
            loop_count = 0
            if tokens[i][2] == ':':
                i += 1
            else:
                if option:
                    i = temp
                    return False
                raise Exception('err label without :')
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
    else:
        if option:
            i = temp
            return False
        raise Exception('err operator')


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
                return True
            else:
                if option:
                    i = temp
                    return False
        else:
            if option:
                i = temp
                return False
            raise Exception('err user input without >>')
    else:
        if option:
            i = temp
            return False
        raise Exception('err user input without cin')


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
                return True
            else:
                if option:
                    i = temp
                    return False
        else:
            if option:
                i = temp
                return False
            raise Exception('err user output without <<')
    else:
        if option:
            i = temp
            return False
        raise Exception('err user input without cout')


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
                                                raise Exception('err loop without rof')
                                        else:
                                            if option:
                                                i = temp
                                                return False
                                    else:
                                        if option:
                                            i = temp
                                            return False
                                        raise Exception('err loop without do')
                                else:
                                    if option:
                                        i = temp
                                        return False
                            else:
                                if option:
                                    i = temp
                                    return False
                                raise Exception('err loop without to')
                        else:
                            if option:
                                i = temp
                                return False
                    else:
                        if option:
                            i = temp
                            return False
                        raise Exception('err loop without by')
                else:
                    if option:
                        i = temp
                        return False
            else:
                if option:
                    i = temp
                    return False
                raise Exception('err loop without =')
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
            return False
        raise Exception('err loop without for')


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
                            raise Exception('err conditional statement without fi')
                else:
                    raise Exception('err conditional statement without :')
            else:
                raise Exception('err conditional statement without then')
    else:
        if option:
            i = temp
            return False
        raise Exception('err conditional statement without if')


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
        else:
            if option:
                i = temp
                return False
            raise Exception('err assignment without =')
    else:
        if option:
            i = temp
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
    else:
        if option:
            i = temp
            return False
        raise Exception('err expression')
    while tokens[i][2] == '+' or tokens[i][2] == '-':
        i += 1
        if t(option):
            continue
        else:
            if option:
                i = temp
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
        return True
    else:
        if option:
            i = temp
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
                raise Exception('err f without )')
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
            return False
        raise Exception('err f')


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
        raise Exception('err identifier')


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
        raise Exception('err constant fixed accuracy')


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
        return True
    else:
        if option:
            i = temp
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
        return True
    else:
        if option:
            i = temp
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
                raise Exception('err lf without ]')
        else:
            if option:
                i = temp
                return False
    elif tokens[i][2] == 'not':
        i += 1
        if lf(option):
            return True
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
            return False
        raise Exception('err lf')


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
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
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
        raise Exception('err relation sign')


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
        raise Exception('err label')
