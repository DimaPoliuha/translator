import copy
import re
from translator_components.structures.tokens import Token, TokenTemplate


class PolizProcessing:
    def __init__(self):
        self.op_1 = {
            '@': (lambda a: - a),
            'not': (lambda a: not a),
        }
        self.op_2 = {
            '+': (lambda a, b: a + b),
            '-': (lambda a, b: a - b),
            '*': (lambda a, b: a * b),
            '/': (lambda a, b: a / b),
            '>': (lambda a, b: a > b),
            '>=': (lambda a, b: a >= b),
            '<': (lambda a, b: a < b),
            '<=': (lambda a, b: a <= b),
            '==': (lambda a, b: a == b),
            '!=': (lambda a, b: a != b),
            'and': (lambda a, b: a and b),
            'or': (lambda a, b: a or b),
        }
        self.poliz_auxiliary = [
            'UPH', 'OUTE', 'INE', 'BP', 'OUTS', 'INS', 'EA'
        ]

    def __call__(self, program_file):
        self.program_file = program_file
        self.poliz = copy.deepcopy(self.program_file.poliz)
        self.run_program()

    def check_tag(self, token):
        if re.match(r'^m#.+:$', token):
            return 'start_user_tag'
        elif re.match(r'^m#.+$', token):
            return 'user_tag'
        elif re.match(r'^m.+:$', token):
            return 'start_tag'
        elif re.match(r'^m.+$', token):
            return 'tag'
        else:
            raise Exception('Tag error')

    def get_operand(self, operand):
        if type(operand) is Token:
            if not operand.idn_id == '':
                var_name = str(operand)
                operand = self.program_file.tokens.identifiers[operand.idn_id].value
                if not operand:
                    raise UnboundLocalError('local variable `{}` referenced before assignment'.format(var_name))
            elif not operand.con_id == '':
                if self.program_file.tokens.constants[operand.con_id].con_type == 'int':
                    operand = int(self.program_file.tokens.constants[operand.con_id].token)
                elif self.program_file.tokens.constants[operand.con_id].con_type == 'float':
                    operand = float(self.program_file.tokens.constants[operand.con_id].token)
                else:
                    raise TypeError('strange type of constant')
            else:
                raise Exception('strange error here')
        return operand

    def run_program(self):
        for const in self.program_file.tokens.constants:
            if const.con_type is 'int':
                const.token = int(const.token)
            elif const.con_type is 'float':
                const.token = float(const.token)

        stack = []
        type_identifiers_stack = []
        token_out = False
        token_in = False
        announcement_block = True
        pass_code = False
        pass_to_label = None

        for i, token in enumerate(self.poliz):
            curr_token = str(token)
            # print(curr_token)
            if pass_code:
                if pass_to_label == curr_token[:-1]:
                    pass_code = False
                continue

            if announcement_block:
                if curr_token == 'EA':
                    announcement_block = False
                # identifier type
                if curr_token == 'int':
                    for token_identifier in type_identifiers_stack:
                        self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'int'
                    type_identifiers_stack = []
                elif curr_token == 'float':
                    for token_identifier in type_identifiers_stack:
                        self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'float'
                    type_identifiers_stack = []
                else:
                    type_identifiers_stack.append(token)
            elif token_in:
                # input
                if curr_token == 'INE':
                    token_in = False
                    continue
                value_type = self.program_file.tokens.identifiers[token.idn_id].idn_type
                value = input('Input {} <type {}>: '.format(curr_token, value_type))
                if value_type == 'int':
                    if value.isdigit():
                        self.program_file.tokens.identifiers[token.idn_id].value = int(value)
                    elif len(value) > 1 and value[1:].isdigit():
                        self.program_file.tokens.identifiers[token.idn_id].value = int(value)
                    else:
                        raise TypeError('expected integer value')
                elif value_type == 'float':
                    if str(float(value)) == value:
                        self.program_file.tokens.identifiers[token.idn_id].value = float(value)
                    elif str(int(value)) == value:
                        self.program_file.tokens.identifiers[token.idn_id].value = float(value)
                    else:
                        raise TypeError('expected float value')
                else:
                    raise TypeError('strange type of identifier')
            elif token_out:
                # output
                if curr_token == 'OUTE':
                    token_out = False
                    continue
                print('{} = {}'.format(token, str(self.program_file.tokens.identifiers[token.idn_id].value)))
            elif curr_token == '=':
                operand_r = self.get_operand(stack.pop())
                operand_l = stack.pop()
                value_type = self.program_file.tokens.identifiers[operand_l.idn_id].idn_type
                if value_type == 'int':
                    if type(operand_r) == int:
                        self.program_file.tokens.identifiers[operand_l.idn_id].value = int(operand_r)
                    else:
                        raise TypeError('expected integer value')
                elif value_type == 'float':
                    if type(operand_r) in (int, float):
                        self.program_file.tokens.identifiers[operand_l.idn_id].value = float(operand_r)
                else:
                    raise TypeError('strange type of identifier')
            else:
                if curr_token in self.poliz_auxiliary:
                    # cin
                    if curr_token == 'INS':
                        token_in = True
                    # cout
                    elif curr_token == 'OUTS':
                        token_out = True
                    elif curr_token == 'BP':
                        pass_code = True
                        pass_to_label = stack.pop()
                    elif curr_token == 'UPH':
                        pass_to_label = stack.pop()
                        if stack.pop() is False:
                            pass_code = True
                    else:
                        print('poliz_auxiliary', curr_token)
                elif curr_token in self.op_1:
                    operand = self.get_operand(stack.pop())
                    result = self.op_1[curr_token](operand)
                    stack.append(result)
                elif curr_token in self.op_2:
                    operand_r = self.get_operand(stack.pop())
                    operand_l = self.get_operand(stack.pop())
                    result = self.op_2[curr_token](operand_l, operand_r)
                    stack.append(result)
                else:
                    if type(token) is Token:
                        if not token.idn_id == '':
                            stack.append(token)
                        elif not token.con_id == '':
                            stack.append(self.program_file.tokens.constants[token.con_id].token)
                    elif type(token) is TokenTemplate:
                        stack.append(curr_token)

                        # tag_flag = self.check_tag(curr_token)
                        # if tag_flag == 'tag' and stack.pop() is False:
                        #     pass_code = True
                        #     pass_to_label = curr_token
                        # elif tag_flag == 'user_tag':
                        #     pass_code = True
                        #     pass_to_label = curr_token
                        # elif tag_flag == 'start_tag':
                        #     pass
                        # elif tag_flag == 'start_user_tag':
                        #     pass

                    elif curr_token not in self.poliz_auxiliary:
                        print('WARNING |STRANGE TOKEN| =>', repr(curr_token))
                        # stack.append(token)
                    else:
                        raise Exception('Unknown error')

            print(stack)
