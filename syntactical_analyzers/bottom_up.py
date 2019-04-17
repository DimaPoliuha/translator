import csv
import copy
from tokens.tokens import TokenTemplate, Tokens


class BottomUp:
    """
    Class that makes syntactical analyse using bottom up method
    This class contains simplified grammar of this programming language
    YOU NEED TO USE ONLY __call__ METHOD OF CLASS TO SYNTACTICAL ANALYSE
    Usage:
    syntactical_analyzer = BottomUp()
    syntactical_analyzer(tokens)
    """
    def __init__(self):
        """
        Initialise all attributes
        """
        self.grammar = {
            "'program'": [
                "'declaration_list' begin 'operators_list1' end",
            ],
            "'declaration_list'": [
                "'declaration_list' 'declaration' ;",
                "'declaration' ;",
            ],
            "'declaration'": [
                "'variable_type' 'variables_list'",
            ],
            "'variable_type'": [
                "int",
                "float",
            ],
            "'variables_list'": [
                "IDN",
                "IDN , 'variables_list'",
            ],
            "'operators_list1'": [
                "'operators_list'"
            ],
            "'operators_list'": [
                "'operators_list' 'operator' ;",
                "'operators_list' LAB :",
                "'operator' ;",
                "LAB :",
            ],
            "'operator'": [
                "'assignment'",
                "'user_input'",
                "'user_output'",
                "'loop'",
                "'conditional_statement'",
                "goto LAB",
            ],
            "'user_input'": [
                "cin >> IDN",
                "'user_input' >> IDN",
            ],
            "'user_output'": [
                "cout << IDN",
                "'user_output' << IDN",
            ],
            "'loop'": [
                "for IDN = 'expression1' by 'expression1' to 'expression1' do 'operators_list1' rof",
            ],
            "'conditional_statement'": [
                "if 'LR1' then 'operators_list1' fi",
            ],
            "'assignment'": [
                "IDN = 'expression1'",
            ],
            "'expression1'": [
                "'expression'"
            ],
            "'expression'": [
                "'T1'",
                "'expression' + 'T1'",
                "'expression' - 'T1'",
                "- 'T1'"
            ],
            "'T1'": [
                "'T'"
            ],
            "'T'": [
                "'F'",
                "'T' * 'F'",
                "'T' / 'F'",
            ],
            "'F'": [
                "IDN",
                "CON",
                "( 'expression1' )",
            ],
            "'LR1'": [
                "'LR'"
            ],
            "'LR'": [
                "'LR' or 'LT1'",
                "'LT1'",
            ],
            "'LT1'": [
                "'LT'"
            ],
            "'LT'": [
                "'LT' and 'LF'",
                "'LF'",
            ],
            "'LF'": [
                "'relation'",
                "[ 'LR1' ]",
                "not 'LF'",
            ],
            "'relation'": [
                "'expression1' 'relation_sign' 'expression1'",
            ],
            "'relation_sign'": [
                "<",
                ">",
                "<=",
                ">=",
                "==",
                "!=",
            ],
        }
        self.bottom_up_grammar_table = []
        self.rules_array = []
        self.rule_var_list = self.grammar["'variables_list'"].copy()
        self.err_msg: str = ...
        self.bottom_up_table: list = ...
        
        self.get_bottom_up_grammar_table()
        # self.write_table_to_file()

    def __call__(self, tokens):
        """
        Run all required methods
        :param tokens:
        :return:
        """
        self.tokens = copy.deepcopy(tokens)
        self.err_msg = ''
        self.bottom_up_table = []
        
        self.parse()
        return self.bottom_up_table, self.err_msg
    
    def get_first_plus(self, index):
        """
        Function, that finds first plus of rule
        :param index:
        :return:
        """
        first_tokens = set()
        main_rule = self.rules_array[index]
        for rule in self.grammar[main_rule]:
            # get first tokens from rules
            first_tokens.add(rule.split()[0])
    
        first_tokens = list(first_tokens)
        loop_continue = True
        repeatable_tokens = []
        while loop_continue:
            loop_continue = False
            for token in first_tokens:
                if token[0] == "'" and token not in repeatable_tokens:
                    loop_continue = True
                    repeatable_tokens.append(token)
                    for rule in self.grammar[token]:
                        # get first tokens from rules
                        first_tokens.append(rule.split()[0])
    
        first_tokens = set(first_tokens)
        return first_tokens
    
    def get_last_plus(self, index):
        """
        Function, that finds last plus of rule
        :param index:
        :return:
        """
        last_tokens = set()
        main_rule = self.rules_array[index]
        for rule in self.grammar[main_rule]:
            # get last tokens from rules
            last_tokens.add(rule.split()[-1])
    
        last_tokens = list(last_tokens)
        loop_continue = True
        repeatable_tokens = []
        while loop_continue:
            loop_continue = False
            for token in last_tokens:
                if token[0] == "'" and token not in repeatable_tokens:
                    loop_continue = True
                    repeatable_tokens.append(token)
                    for rule in self.grammar[token]:
                        # get last tokens from rules
                        last_tokens.append(rule.split()[-1])

        last_tokens = set(last_tokens)
        return last_tokens
    
    def get_bottom_up_grammar_table(self):
        """
        Function, that creates bottom up grammar table
        :return:
        """
        for rule in self.grammar:
            for rule_variant in self.grammar[rule]:
                for tkn in rule_variant.split():
                    self.rules_array.append(tkn)
    
        self.rules_array.append("'program'")
        self.rules_array = sorted(set(self.rules_array))
        self.rules_array.append(self.rules_array.pop(0))

        self.bottom_up_grammar_table = [['' for item in self.rules_array] for it in self.rules_array]
    
        # relations =
        for rule in self.grammar:
            for rule_variant in self.grammar[rule]:
                rule_variant_tokens = rule_variant.split()
                if len(rule_variant_tokens) > 1:
                    for i in range(len(rule_variant_tokens) - 1):
                        l = self.rules_array.index(rule_variant_tokens[i])
                        k = self.rules_array.index(rule_variant_tokens[i + 1])
                        self.bottom_up_grammar_table[l][k] = '='

        for border in range(len(self.rules_array)):
            if not self.rules_array[border][0] == "'":
                break

        # relation <
        for i in range(len(self.bottom_up_grammar_table[0])):
            for j in range(border):
                if self.bottom_up_grammar_table[i][j]:
                    # i - index of row
                    left_part = self.rules_array[i]
                    right_part = self.get_first_plus(j)

                    for item in right_part:
                        col_index = self.rules_array.index(item)
                        if not self.bottom_up_grammar_table[i][col_index]:
                            self.bottom_up_grammar_table[i][col_index] = '<'
                        elif self.bottom_up_grammar_table[i][col_index] == '=':
                            self.bottom_up_grammar_table[i][col_index] += '<'
                            print(left_part, '<=', item, 'CONFLICT')
    
        # relation >
        for i in range(border):
            for j in range(len(self.bottom_up_grammar_table[0])):
                if self.bottom_up_grammar_table[i][j]:
                    # j - index of col
                    left_part = self.get_last_plus(i)
                    right_part = self.rules_array[j]
                    for item in left_part:
                        row_index = self.rules_array.index(item)
                        if not self.bottom_up_grammar_table[row_index][j]:
                            self.bottom_up_grammar_table[row_index][j] = '>'
                        elif self.bottom_up_grammar_table[row_index][j] == '=':
                            self.bottom_up_grammar_table[row_index][j] += '>'
                            print(item, '>=', right_part, 'CONFLICT')
                        elif self.bottom_up_grammar_table[row_index][j] == '<':
                            self.bottom_up_grammar_table[row_index][j] += '>'
                            print(item, '<>', right_part, 'CONFLICT')
                        elif self.bottom_up_grammar_table[row_index][j] == '=<':
                            self.bottom_up_grammar_table[row_index][j] += '>'
                            print(item, '<=>', right_part, 'CONFLICT')
    
                    if self.rules_array[j][0] == "'":
                        right_part = self.get_first_plus(j)
                        for item in left_part:
                            for it in right_part:
                                row_index = self.rules_array.index(item)
                                col_index = self.rules_array.index(it)
                                if not self.bottom_up_grammar_table[row_index][col_index]:
                                    self.bottom_up_grammar_table[row_index][col_index] = '>'
                                elif self.bottom_up_grammar_table[row_index][col_index] == '=':
                                    self.bottom_up_grammar_table[row_index][col_index] += '>'
                                    print(item, '>=', it, 'CONFLICT')
                                elif self.bottom_up_grammar_table[row_index][col_index] == '<':
                                    self.bottom_up_grammar_table[row_index][col_index] += '>'
                                    print(item, '<>', it, 'CONFLICT')
                                elif self.bottom_up_grammar_table[row_index][col_index] == '=<':
                                    self.bottom_up_grammar_table[row_index][col_index] += '>'
                                    print(item, '<=>', it, 'CONFLICT')

    def write_table_to_file(self):
        """
        Function, that writes bottom up grammar table to file
        RUN ONLY SEPARATELY FROM self.parse
        :return:
        """
        with open('./papers/bottom_up.csv', 'w', newline='') as f:
            self.rules_array.insert(0, '')
            csv.writer(f).writerow(self.rules_array)
            for index, row in enumerate(self.bottom_up_grammar_table):
                row.insert(0, self.rules_array[index + 1])
                csv.writer(f).writerow(row)
    
    def parse(self):
        """
        Function, that makes syntactical analyse using bottom up method
        :return:
        """
        self.tokens.append(TokenTemplate('#'))
        self.tokens.insert(0, TokenTemplate('#'))
        self.bottom_up_table = [['', '', str(self.tokens)]]

        stack = Tokens()
        stack.append(self.tokens.pop(0))
        self.bottom_up_table.append(['#', '<', str(self.tokens)])

        stack.append(self.tokens.pop(0))
        self.bottom_up_table.append([str(stack), '<', str(self.tokens)])

        while not repr(stack) == "# 'program'" or not repr(self.tokens) == '#':
            left_i = self.rules_array.index(repr(stack[-1]))
            if repr(self.tokens[0]) == '#':
                main_relation = '>'
            else:
                right_i = self.rules_array.index(repr(self.tokens[0]))
                main_relation = self.bottom_up_grammar_table[left_i][right_i]

            if main_relation in ('<', '='):
                if repr(self.tokens[0]) == "begin":
                    del self.grammar["'variables_list'"]
                stack.append(self.tokens.pop(0))

                self.bottom_up_table.append([str(stack), main_relation, str(self.tokens)])

            elif main_relation == '>':
                basis = []
                for i in range(len(stack) - 1, 0, -1):
                    if repr(stack[i-1]) == '#':
                        basis = stack[i:]
                        basis = [repr(token) for token in basis]
                    else:
                        stack_left_i = self.rules_array.index(repr(stack[i-1]))
                        stack_right_i = self.rules_array.index(repr(stack[i]))
                        relation = self.bottom_up_grammar_table[stack_left_i][stack_right_i]
                        if relation == '<':
                            basis = stack[i:]
                            basis = [repr(token) for token in basis]
                            break
                for rule in sorted(self.grammar.keys(), reverse=True):
                    for rule_variant in self.grammar[rule]:
                        if ' '.join(basis) == rule_variant:
                            del stack[i:]
                            stack.append(TokenTemplate(rule))
                            self.bottom_up_table.append(
                                [str(stack), main_relation, str(self.tokens)]
                            )
                            break
                    if ' '.join(basis) == rule_variant:
                        break
                if ' '.join(basis) != rule_variant:
                    self.err_msg = 'Incorrect end of program {0}'.format(repr(stack[-1]))
                    break
            else:
                self.err_msg = (
                    'line: {}\n\n'
                    'Empty cell in table between {} and {}\n'
                        ).format(
                            self.tokens[0].line_number,
                            repr(stack[-1]),
                            repr(self.tokens[0])
                )
                break
        self.grammar["'variables_list'"] = self.rule_var_list
        for i in range(len(self.bottom_up_table) - 1):
            self.bottom_up_table[i][1] = self.bottom_up_table[i+1][1]
        if self.err_msg:
            self.bottom_up_table[-1][1] = ''
