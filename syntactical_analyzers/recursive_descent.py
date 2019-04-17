import copy


class RecursiveDescent:
    """
    Class that makes syntactical analyse using recursive descent method
    YOU NEED TO USE ONLY __call__ METHOD OF CLASS TO SYNTACTICAL ANALYSE
    Usage:
    syntactical_analyzer = RecursiveDescent()
    syntactical_analyzer(tokens)
    """
    def __init__(self):
        """
        Initialise all attributes
        """
        self.i: int = ...
        self.relation_signs = [">", "<", ">=", "<=", "==", "!="]

    def __call__(self, tokens):
        """
        Run all required methods
        :param tokens:
        :return:
        """
        self.tokens = copy.deepcopy(tokens)
        self.i = 0
        self.program()
    
    def raise_exception(self, msg=None):
        """
        Function, that helps to raise exceptions with error message, that contains all information about error
        :param msg:
        :return:
        """
        raise Exception(('line: {}\n'
                         'token number: {}\n'
                         'token: {}\n\n'
                         '{}'
                         ).format(
                                str(self.tokens[self.i].line_number),
                                str(self.tokens[self.i].count),
                                str(self.tokens[self.i].token),
                                msg
        ))
    
    def program(self):
        if self.declaration_list():
            if self.tokens[self.i].token == 'begin':
                self.i += 1
                if self.operators_list():
                    if self.tokens[self.i].token == 'end':
                        self.i += 1
                        return True
                    else:
                        self.raise_exception('err program without end')
            else:
                self.raise_exception('err program without begin')

    def declaration_list(self):
        if self.declaration():
            if self.tokens[self.i].token == ';':
                self.i += 1
                while self.declaration(True):
                    if self.tokens[self.i].token == ';':
                        self.i += 1
                    else:
                        self.raise_exception('err declaration without ;')
                return True
            else:
                self.raise_exception('err declaration without ;')
    
    def declaration(self, option=False):
        temp = self.i
        if self.variable_type(option):
            if self.variables_list(option):
                return True
            else:
                if option:
                    self.i = temp
                    return False
        else:
            if option:
                self.i = temp
                return False
    
    def variable_type(self, option=False):
        temp = self.i
        if self.tokens[self.i].token == 'int' or self.tokens[self.i].token == 'float':
            self.i += 1
            return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err variable type')
    
    def variables_list(self, option=False):
        temp = self.i
        if self.identifier(option):
            if self.tokens[self.i].token == ',':
                self.i += 1
                if self.variables_list(option):
                    return True
                else:
                    if option:
                        self.i = temp
                        return False
            else:
                return True
        else:
            if option:
                self.i = temp
                return False
    
    def operators_list(self, option=False):
        temp = self.i
        if self.operator(True):
            if self.tokens[self.i].token == ';':
                self.i += 1
            else:
                if option:
                    self.i = temp
                    return False
                self.raise_exception('err operator without ;')
        elif self.label(True):
            if self.tokens[self.i].token == ':':
                self.i += 1
            else:
                if option:
                    self.i = temp
                    return False
                self.raise_exception('err label without :')
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err operators list')
    
        loop_count = 0
        while True:
            loop_count += 1
            while self.operator(True):
                loop_count = 0
                if self.tokens[self.i].token == ';':
                    self.i += 1
                else:
                    if option:
                        self.i = temp
                        return False
                    self.raise_exception('err operator without ;')
            while self.label(True):
                loop_count = 0
                if self.tokens[self.i].token == ':':
                    self.i += 1
                else:
                    if option:
                        self.i = temp
                        return False
                    self.raise_exception('err label without :')
            if loop_count > 2:
                break
        return True
    
    def operator(self, option=False):
        temp = self.i
        if (self.assignment(True) or
                self.user_input(True) or
                self.user_output(True) or
                self.loop(True) or
                self.conditional_statement(True)):
            return True
        elif self.tokens[self.i].token == 'goto':
            self.i += 1
            if self.label():
                return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err operator')
    
    def user_input(self, option=False):
        temp = self.i
        if self.tokens[self.i].token == 'cin':
            self.i += 1
            if self.tokens[self.i].token == '>>':
                self.i += 1
                if self.identifier():
                    while self.tokens[self.i].token == '>>':
                        self.i += 1
                        if self.identifier():
                            continue
                    return True
            else:
                self.raise_exception('err user input without >>')
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err user input without cin')
    
    def user_output(self, option=False):
        temp = self.i
        if self.tokens[self.i].token == 'cout':
            self.i += 1
            if self.tokens[self.i].token == '<<':
                self.i += 1
                if self.identifier():
                    while self.tokens[self.i].token == '<<':
                        self.i += 1
                        if self.identifier():
                            continue
                    return True
            else:
                self.raise_exception('err user output without <<')
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err user input without cout')
    
    def loop(self, option=False):
        temp = self.i
        if self.tokens[self.i].token == 'for':
            self.i += 1
            if self.identifier():
                if self.tokens[self.i].token == '=':
                    self.i += 1
                    if self.expression():
                        if self.tokens[self.i].token == 'by':
                            self.i += 1
                            if self.expression():
                                if self.tokens[self.i].token == 'to':
                                    self.i += 1
                                    if self.expression():
                                        if self.tokens[self.i].token == 'do':
                                            self.i += 1
                                            if self.operators_list():
                                                if self.tokens[self.i].token == 'rof':
                                                    self.i += 1
                                                    return True
                                                else:
                                                    self.raise_exception('err loop without rof')
                                        else:
                                            self.raise_exception('err loop without do')
                                else:
                                    self.raise_exception('err loop without to')
                        else:
                            self.raise_exception('err loop without by')
                else:
                    self.raise_exception('err loop without =')
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err loop without for')

    def conditional_statement(self, option=False):
        temp = self.i
        if self.tokens[self.i].token == 'if':
            self.i += 1
            if self.le():
                if self.tokens[self.i].token == 'then':
                    self.i += 1
                    if self.operators_list():
                        if self.tokens[self.i].token == 'fi':
                            self.i += 1
                            return True
                        else:
                            self.raise_exception('err conditional statement without fi')
                else:
                    self.raise_exception('err conditional statement without then')
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err conditional statement without if')

    def assignment(self, option=False):
        temp = self.i
        if self.identifier(option):
            if self.tokens[self.i].token == '=':
                self.i += 1
                if self.expression(option):
                    return True
                else:
                    if option:
                        self.i = temp
                        return False
            else:
                if option:
                    self.i = temp
                    return False
                self.raise_exception('err assignment without =')
        else:
            if option:
                self.i = temp
                return False

    def expression(self, option=False):
        temp = self.i
        if self.t(True):
            pass
        elif self.tokens[self.i].token == '-':
            self.i += 1
            if self.t(option):
                pass
            else:
                if option:
                    self.i = temp
                    return False
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err expression')
        while self.tokens[self.i].token == '+' or self.tokens[self.i].token == '-':
            self.i += 1
            if self.t(option):
                continue
            else:
                if option:
                    self.i = temp
                    return False
        return True
    
    def t(self, option=False):
        temp = self.i
        if self.f(option):
            while self.tokens[self.i].token == '*' or self.tokens[self.i].token == '/':
                self.i += 1
                if self.f(option):
                    continue
                else:
                    if option:
                        self.i = temp
                        return False
            return True
        else:
            if option:
                self.i = temp
                return False
    
    def f(self, option=False):
        temp = self.i
        if self.identifier(True) or self.constant_fixed_accuracy(True):
            return True
        elif self.tokens[self.i].token == '(':
            self.i += 1
            if self.expression(option):
                if self.tokens[self.i].token == ')':
                    self.i += 1
                    return True
                else:
                    if option:
                        self.i = temp
                        return False
                    self.raise_exception('err f without )')
            else:
                if option:
                    self.i = temp
                    return False
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err f')
    
    def identifier(self, option=False):
        temp = self.i
        if self.tokens[self.i].token_id == 100:
            self.i += 1
            return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err identifier')

    def constant_fixed_accuracy(self, option=False):
        temp = self.i
        if self.tokens[self.i].token_id == 101:
            self.i += 1
            return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err constant fixed accuracy')

    def le(self, option=False):
        temp = self.i
        if self.lt(option):
            while self.tokens[self.i].token == 'or':
                self.i += 1
                if self.lt(option):
                    continue
                else:
                    if option:
                        self.i = temp
                        return False
            return True
        else:
            if option:
                self.i = temp
                return False

    def lt(self, option=False):
        temp = self.i
        if self.lf(option):
            while self.tokens[self.i].token == 'and':
                self.i += 1
                if self.lf(option):
                    continue
                else:
                    if option:
                        self.i = temp
                        return False
            return True
        else:
            if option:
                self.i = temp
                return False

    def lf(self, option=False):
        temp = self.i
        if self.relation(True):
            return True
        elif self.tokens[self.i].token == '[':
            self.i += 1
            if self.le(option):
                if self.tokens[self.i].token == ']':
                    self.i += 1
                    return True
                else:
                    if option:
                        self.i = temp
                        return False
                    self.raise_exception('err lf without ]')
            else:
                if option:
                    self.i = temp
                    return False
        elif self.tokens[self.i].token == 'not':
            self.i += 1
            if self.lf(option):
                return True
            else:
                if option:
                    self.i = temp
                    return False
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err lf')
    
    def relation(self, option=False):
        temp = self.i
        if self.expression(option):
            if self.relation_sign(option):
                if self.expression(option):
                    return True
                else:
                    if option:
                        self.i = temp
                        return False
            else:
                if option:
                    self.i = temp
                    return False
        else:
            if option:
                self.i = temp
                return False
    
    def relation_sign(self, option=False):
        temp = self.i
        if self.tokens[self.i].token in self.relation_signs:
            self.i += 1
            return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err relation sign')
    
    def label(self, option=False):
        temp = self.i
        if self.tokens[self.i].token_id == 102:
            self.i += 1
            return True
        else:
            if option:
                self.i = temp
                return False
            self.raise_exception('err label')
