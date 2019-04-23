import copy


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

    def get_operand(self, operand):
        print(operand, type(operand))
        if not operand.idn_id == '':
            value = self.program_file.tokens.identifiers[operand.idn_id].value
        elif not operand.con_id == '':
            if self.program_file.tokens.constants[operand.con_id].con_type == 'int':
                value = int(self.program_file.tokens.constants[operand.con_id].token)
            elif self.program_file.tokens.constants[operand.con_id].con_type == 'float':
                value = float(self.program_file.tokens.constants[operand.con_id].token)
            else:
                raise TypeError('strange type of constant')
        else:
            value = None
            # raise Exception('wrong operand')
        return value

    def run_program(self):
        for const in self.program_file.tokens.constants:
            if const.con_type is 'int':
                const.token = int(const.token)
            elif const.con_type is 'float':
                const.token = float(const.token)

        stack = []
        type_stack = []
        token_out = False
        token_in = False
        announcement_block = True
        # for token in self.poliz:
        #     print(token, type(token))
        for i, token in enumerate(self.poliz):
            curr_token = str(token)
            print(curr_token)

            if announcement_block:
                if curr_token == 'EA':
                    announcement_block = False
                # identifier type
                if curr_token == 'int':
                    for token_identifier in type_stack:
                        self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'int'
                    type_stack = []
                elif curr_token == 'float':
                    for token_identifier in type_stack:
                        self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'float'
                    type_stack = []
                else:
                    type_stack.append(token)
            else:
                # cin
                if curr_token == 'INS':
                    token_in = True
                elif curr_token == 'INE':
                    token_in = False
                elif token_in:
                    # input
                    value = input()
                    value_type = self.program_file.tokens.identifiers[token.idn_id].idn_type
                    if value_type == 'int':
                        if value.isdigit():
                            self.program_file.tokens.identifiers[token.idn_id].value = int(value)
                        else:
                            raise TypeError('expected int')
                    elif value_type == 'float':
                        if str(float(value)) == value:
                            self.program_file.tokens.identifiers[token.idn_id].value = float(value)
                        elif str(int(value)) == value:
                            self.program_file.tokens.identifiers[token.idn_id].value = float(value)
                        else:
                            raise TypeError('expected float')
                    else:
                        raise TypeError('strange type of identifier')
                    continue

                # cout
                if curr_token == 'OUTS':
                    token_out = True
                elif curr_token == 'OUTE':
                    token_out = False
                elif token_out:
                    # output
                    print(str(self.program_file.tokens.identifiers[token.idn_id].value))
                    continue

                if curr_token in self.op_1:
                    pass
                #     operand = self.get_operand(stack.pop())
                #     result = self.op_1[curr_token](operand)
                #     stack.append(result)
                #     print(result)
                # elif curr_token in self.op_2:
                #     operand_r = self.get_operand(stack.pop())
                #     operand_l = self.get_operand(stack.pop())
                #     result = self.op_2[curr_token](operand_l, operand_r)
                #     stack.append(result)
                #     print(result)
                else:
                    if type(token) is not str:
                        if not token.idn_id == '':
                            stack.append(self.program_file.tokens.identifiers[token.idn_id].value)
                        elif not token.con_id == '':
                            stack.append(self.program_file.tokens.identifiers[token.con_id].value)
                    elif curr_token not in self.poliz_auxiliary:
                        print(curr_token)
                        stack.append(curr_token)

        print(stack)
