relation_signs = [">", "<", ">=", "<=", "==", "!="]


def raise_exception(tokens, i, msg=''):
    raise Exception('Syntactical analyzer exception\n\n' +
                    msg +
                    '\nline: ' + str(tokens[i][1]) +
                    '\ntoken number: ' + str(tokens[i][0]) +
                    '\ntoken: ' + repr(tokens[i][2]))


def parser(tkns):
    global tokens
    tokens = tkns
    program()


def program():
    global i
    i = 0
    if declaration_list():
        if tokens[i][2] == 'begin':
            i += 1
            if operators_list():
                if tokens[i][2] == 'end':
                    i += 1
                    return True
                else:
                    raise_exception(tokens, i, 'err program without end')
        else:
            raise_exception(tokens, i, 'err program without begin')


def declaration_list():
    global i
    if declaration():
        if tokens[i][2] == ';':
            i += 1
            while declaration(True):
                if tokens[i][2] == ';':
                    i += 1
                else:
                    raise_exception(tokens, i, 'err declaration without ;')
            return True
        else:
            raise_exception(tokens, i, 'err declaration without ;')


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
        raise_exception(tokens, i, 'err variable type')


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
            raise_exception(tokens, i, 'err operator without ;')
    elif label(True):
        if tokens[i][2] == ':':
            i += 1
        else:
            if option:
                i = temp
                return False
            raise_exception(tokens, i, 'err label without :')
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err operators list')

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
                raise_exception(tokens, i, 'err operator without ;')
        while label(True):
            loop_count = 0
            if tokens[i][2] == ':':
                i += 1
            else:
                if option:
                    i = temp
                    return False
                raise_exception(tokens, i, 'err label without :')
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
        if label():
            return True
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err operator')


def user_input(option=False):
    global i
    temp = i
    if tokens[i][2] == 'cin':
        i += 1
        if tokens[i][2] == '>>':
            i += 1
            if identifier():
                while tokens[i][2] == '>>':
                    i += 1
                    if identifier():
                        continue
                return True
        else:
            raise_exception(tokens, i, 'err user input without >>')
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err user input without cin')


def user_output(option=False):
    global i
    temp = i
    if tokens[i][2] == 'cout':
        i += 1
        if tokens[i][2] == '<<':
            i += 1
            if identifier():
                while tokens[i][2] == '<<':
                    i += 1
                    if identifier():
                        continue
                return True
        else:
            raise_exception(tokens, i, 'err user output without <<')
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err user input without cout')


def loop(option=False):
    global i
    temp = i
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
                                        if tokens[i][2] == ':':
                                            i += 1
                                            if operators_list():
                                                if tokens[i][2] == 'rof':
                                                    i += 1
                                                    return True
                                                else:
                                                    raise_exception(tokens, i, 'err loop without rof')
                                        else:
                                            raise_exception(tokens, i, 'err loop :')
                                    else:
                                        raise_exception(tokens, i, 'err loop without do')
                            else:
                                raise_exception(tokens, i, 'err loop without to')
                    else:
                        raise_exception(tokens, i, 'err loop without by')
            else:
                raise_exception(tokens, i, 'err loop without =')
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err loop without for')


def conditional_statement(option=False):
    global i
    temp = i
    if tokens[i][2] == 'if':
        i += 1
        if le():
            if tokens[i][2] == 'then':
                i += 1
                if tokens[i][2] == ':':
                    i += 1
                    if operators_list():
                        if tokens[i][2] == 'fi':
                            i += 1
                            return True
                        else:
                            raise_exception(tokens, i, 'err conditional statement without fi')
                else:
                    raise_exception(tokens, i, 'err conditional statement without :')
            else:
                raise_exception(tokens, i, 'err conditional statement without then')
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err conditional statement without if')


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
            raise_exception(tokens, i, 'err assignment without =')
    else:
        if option:
            i = temp
            return False


def expression(option=False):
    global i
    temp = i
    if t(True):
        pass
    elif tokens[i][2] == '-':
        i += 1
        if t(option):
            pass
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err expression')
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
                raise_exception(tokens, i, 'err f without )')
        else:
            if option:
                i = temp
                return False
    else:
        if option:
            i = temp
            return False
        raise_exception(tokens, i, 'err f')


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
        raise_exception(tokens, i, 'err identifier')


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
        raise_exception(tokens, i, 'err constant fixed accuracy')


def le(option=False):
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
        if le(option):
            if tokens[i][2] == ']':
                i += 1
                return True
            else:
                if option:
                    i = temp
                    return False
                raise_exception(tokens, i, 'err lf without ]')
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
        raise_exception(tokens, i, 'err lf')


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
        raise_exception(tokens, i, 'err relation sign')


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
        raise_exception(tokens, i, 'err label')
