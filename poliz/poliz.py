import copy
import re
from tokens.tokens import Tokens, TokenTemplate


class Poliz:
    def __init__(self):
        self.priorities = {
            'mitka': [0, 0],
            '(': [0, 100],
            '[': [0, 100],
            'if': [0, 100],
            'for': [0, 100],
            'cout': [0, 100],
            'cin': [0, 100],
            ')': [1, 1],
            ']': [1, 1],
            'goto': [1, 1],
            'then': [1, 1],
            'by': [1, 1],
            'to': [1, 1],
            'do': [1, 1],
            '=': [2, 1000],
            'or': [3, 3],
            'and': [4, 4],
            'not': [5, 5],
            '<': [6, 6],
            '<=': [6, 6],
            '>': [6, 6],
            '>=': [6, 6],
            '==': [6, 6],
            '!=': [6, 6],
            '+': [7, 7],
            '-': [7, 7],
            '*': [8, 8],
            '/': [8, 8],
            '@': [8, 8],
        }
        self.loop_feature: int = ...
        self.loop_variable = ...

    def __call__(self, tokens):
        self.tokens = copy.deepcopy(tokens)
        self.poliz = Tokens()
        self.poliz_table = []
        self.stack = []
        self.tags = []
        self.template_tags = []
        self.loop_help_flags = []
        self.get_poliz()
        return self.poliz, self.poliz_table

    def check_tag(self, token):
        return re.match(r'^m.+$', token)

    def end_expression_stack_pop(self, token=None):
        if token == 'rof':
            self.poliz.append(self.template_tags[-3])
            self.poliz.append('BP')
            self.poliz.append(self.template_tags[-1] + ':')
            del self.template_tags[-3:]
            self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
        while self.stack:
            curr_stack_token = self.stack[-1]
            if self.check_tag(curr_stack_token):
                if token == ';':
                    break
                elif token == 'fi':
                    self.poliz.append(TokenTemplate(self.stack.pop() + ':'))
                    del self.template_tags[-1:]
                    self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
                    break
            if curr_stack_token in ('(', '[', 'if', 'for'):
                self.stack.pop()
            elif curr_stack_token == 'cout':
                self.poliz.append(TokenTemplate('OUTE'))
                self.stack.pop()
            elif curr_stack_token == 'cin':
                self.poliz.append(TokenTemplate('INE'))
                self.stack.pop()
            else:
                self.poliz.append(self.stack.pop())
            self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
        self.tokens.pop(0)

    def get_poliz(self):
        self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
        for index in range(1, len(self.tokens)):
            if repr(self.tokens[index]) == '-':
                if repr(self.tokens[index - 1]) not in (')', 'IDN', 'CON'):
                    self.tokens[index] = TokenTemplate('@')
        self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
        while self.tokens:
            curr_token = repr(self.tokens[0])
            if curr_token in ('IDN', 'CON'):
                self.poliz.append(self.tokens.pop(0))
            elif curr_token == 'LAB' and repr(self.tokens[1]) == ':':
                tag = 'm' + str(self.tokens.pop(0)) + ':'
                self.poliz.append(TokenTemplate(tag))
            elif curr_token in self.priorities.keys():
                if curr_token == '=':
                    if self.loop_feature == 1:
                        self.loop_variable = self.poliz[-1]
                        self.loop_feature = 0
                if self.stack:
                    curr_stack_token = self.stack[-1]
                    if self.check_tag(curr_stack_token):
                        curr_stack_token = 'mitka'
                if self.stack and (self.priorities[curr_stack_token][0] >= self.priorities[curr_token][1]):
                    if curr_stack_token in ('(', '[', 'if', 'for'):
                        self.stack.pop()
                    else:
                        self.poliz.append(self.stack.pop())
                else:
                    if curr_token in (')', ']', 'then', 'goto', 'by', 'to', 'do'):
                        if curr_token == 'then':
                            tag = 'm' + str(len(self.tags))
                            self.tags.append(tag)
                            self.template_tags.append(tag)
                            self.poliz.append(TokenTemplate(tag))
                            self.poliz.append(TokenTemplate('UPH'))
                            self.stack.append(tag)
                        elif curr_token == 'goto':
                            tag = 'm' + str(self.tokens[1])
                            self.tags.append(tag)
                            # self.template_tags.append(tag)
                            self.poliz.append(TokenTemplate(tag))
                            self.poliz.append(TokenTemplate('BP'))
                        elif curr_token == 'by':
                            for i in range(2):
                                flag = 'r' + str(len(self.loop_help_flags))
                                self.loop_help_flags.append(flag)
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-2]))
                            self.poliz.append(TokenTemplate(1))
                            self.poliz.append(TokenTemplate('='))
                            self.poliz.append(TokenTemplate(self.tags[-3] + ':'))
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-1]))
                        elif curr_token == 'to':
                            self.poliz.append(TokenTemplate('='))
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-2]))
                            self.poliz.append(TokenTemplate(0))
                            self.poliz.append(TokenTemplate('=='))   #= or :=
                            self.poliz.append(TokenTemplate(self.tags[-2]))
                            self.poliz.append(TokenTemplate('UPH'))
                            self.poliz.append(TokenTemplate(self.loop_variable))
                            self.poliz.append(TokenTemplate(self.loop_variable))
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-1]))
                            self.poliz.append(TokenTemplate('+'))
                            self.poliz.append(TokenTemplate('='))
                            self.poliz.append(TokenTemplate(self.tags[-2] + ':'))
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-2]))
                            self.poliz.append(TokenTemplate(0))
                            self.poliz.append(TokenTemplate('='))
                            self.poliz.append(TokenTemplate(self.loop_variable))
                        elif curr_token == 'do':
                            self.poliz.append(TokenTemplate('-'))
                            self.poliz.append(TokenTemplate(self.loop_help_flags[-1]))
                            self.poliz.append(TokenTemplate('*'))
                            self.poliz.append(TokenTemplate(0))
                            self.poliz.append(TokenTemplate('<='))
                            self.poliz.append(TokenTemplate(self.tags[-1]))
                            self.poliz.append(TokenTemplate('UPH'))

                        self.tokens.pop(0)
                    else:
                        curr_token = repr(self.tokens.pop(0))
                        self.stack.append(curr_token)
                        if curr_token == 'for':
                            self.loop_feature = 1
                            for i in range(3):
                                tag = 'm' + str(len(self.tags))
                                self.tags.append(tag)
                                self.template_tags.append(tag)
                                # self.stack.append(tag)
                                #tags to stack
                        elif curr_token == 'cout':
                            self.poliz.append(TokenTemplate('OUTS'))
                        elif curr_token == 'cin':
                            self.poliz.append(TokenTemplate('INS'))
            elif curr_token == 'rof':
                self.end_expression_stack_pop(curr_token)
            elif curr_token == 'fi':
                self.end_expression_stack_pop(curr_token)
            elif curr_token == ';':
                self.end_expression_stack_pop(curr_token)
            else:
                self.tokens.pop(0)
            self.poliz_table.append([str(self.tokens), ' '.join(self.stack), str(self.poliz)])
