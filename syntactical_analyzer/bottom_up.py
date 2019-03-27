import csv
from lexical_analyzer.tokens_identifiers import tokens_identifiers_reversed as tokens_identifiers

grammar = {
    "program": [
        "declaration_list 'begin' operators_list1 'end'",
    ],
    "declaration_list": [
        "declaration_list declaration ';'",
        "declaration ';'",
    ],
    "declaration": [
        "variable_type variables_list",
    ],
    "variable_type": [
        "'int'",
        "'float'",
    ],
    "variables_list": [
        "'IDN'",
        "'IDN' ',' variables_list",
    ],
    "operators_list1": [
        "operators_list"
    ],
    "operators_list": [
        "operators_list operator ';'",
        "operators_list 'LAB' ':'",
        "operator ';'",
        "'LAB' ':'",
    ],
    "operator": [
        "assignment",
        "user_input",
        "user_output",
        "loop",
        "conditional_statement",
        "'goto' 'LAB'",
    ],
    "user_input": [
        "'cin' '>>' 'IDN'",
        "user_input '>>' 'IDN'",
    ],
    "user_output": [
        "'cout' '<<' 'IDN'",
        "user_output '<<' 'IDN'",
    ],
    "loop": [
        "'for' 'IDN' '=' expression1 'by' expression1 'to' expression1 'do' operators_list1 'rof'",
    ],
    "conditional_statement": [
        "'if' LR1 'then' operators_list1 'fi'",
    ],
    "assignment": [
        "'IDN' '=' expression1",
    ],
    "expression1": [
        "expression"
    ],
    "expression": [
        "T1",
        "expression '+' T1",
        "expression '-' T1",
        "'-' T1"
    ],
    "T1": [
        "T"
    ],
    "T": [
        "F",
        "T '*' F",
        "T '/' F",
    ],
    "F": [
        "'IDN'",
        "'CON'",
        "'(' expression1 ')'",
    ],
    "LR1": [
        "LR"
    ],
    "LR": [
        "LR 'or' LT1",
        "LT1",
    ],
    "LT1": [
        "LT"
    ],
    "LT": [
        "LT 'and' LF",
        "LF",
    ],
    "LF": [
        "relation",
        "'[' LR1 ']'",
        "'not' LF",
    ],
    "relation": [
        "expression1 relation_sign expression1",
    ],
    "relation_sign": [
        "'<'",
        "'>'",
        "'<='",
        "'>='",
        "'=='",
        "'!='",
    ],
}

bottom_up_rule_table = None
rules = None
rule_var_list = grammar["variables_list"].copy()


def get_grammar():
    return grammar


def get_first_plus(index):
    first_tokens = set()
    main_rule = rules_array[index]
    for rule in grammar[main_rule]:
        # get first tokens from rules
        first_tokens.add(rule.split()[0])

    first_tokens = list(first_tokens)
    loop_continue = True
    repeatable_tokens = []
    while loop_continue:
        loop_continue = False
        for token in first_tokens:
            if not token[0] == "'" and token not in repeatable_tokens:
                loop_continue = True
                repeatable_tokens.append(token)
                for rule in grammar[token]:
                    # get first tokens from rules
                    first_tokens.append(rule.split()[0])

    first_tokens = set(first_tokens)
    return first_tokens


def get_last_plus(index):
    last_tokens = set()
    main_rule = rules_array[index]
    for rule in grammar[main_rule]:
        # get last tokens from rules
        last_tokens.add(rule.split()[-1])

    last_tokens = list(last_tokens)
    loop_continue = True
    repeatable_tokens = []
    while loop_continue:
        loop_continue = False
        for token in last_tokens:
            if not token[0] == "'" and token not in repeatable_tokens:
                loop_continue = True
                repeatable_tokens.append(token)
                for rule in grammar[token]:
                    # get last tokens from rules
                    last_tokens.append(rule.split()[-1])

    last_tokens = set(last_tokens)
    return last_tokens


def grammar_parser():
    global rules_array
    rules_array = []

    for rule in grammar:
        for rule_variant in grammar[rule]:
            for tkn in rule_variant.split():
                rules_array.append(tkn)
                # print(tkn.strip("'"))

    rules_array.append('program')
    rules_array = sorted(set(rules_array))
    rules_array.reverse()
    # print(rules_array)
    
    bottom_up_table = [['' for item in rules_array] for it in rules_array]

    # relations =
    for rule in grammar:
        for rule_variant in grammar[rule]:
            rule_variant_tokens = rule_variant.split()
            if len(rule_variant_tokens) > 1:
                for i in range(len(rule_variant_tokens) - 1):
                    l = rules_array.index(rule_variant_tokens[i])
                    k = rules_array.index(rule_variant_tokens[i + 1])
                    bottom_up_table[l][k] = '='

    for border in range(len(rules_array)):
        if rules_array[border][0] == "'":
            break
    # print(border)

    # relation <
    for i in range(len(bottom_up_table[0])):
        for j in range(border):
            if bottom_up_table[i][j]:
                # i - index of row
                left_part = rules_array[i]
                right_part = get_first_plus(j)
                # print(left_part, '<', right_part)
                for item in right_part:
                    col_index = rules_array.index(item)
                    if not bottom_up_table[i][col_index]:
                        bottom_up_table[i][col_index] = '<'
                    elif bottom_up_table[i][col_index] == '=':
                        bottom_up_table[i][col_index] += '<'
                        print(left_part, '<=', item, 'CONFLICT')

    # relation >
    for i in range(border):
        for j in range(len(bottom_up_table[0])):
            if bottom_up_table[i][j]:
                # j - index of col
                left_part = get_last_plus(i)
                right_part = rules_array[j]
                for item in left_part:
                    row_index = rules_array.index(item)
                    if not bottom_up_table[row_index][j]:
                        bottom_up_table[row_index][j] = '>'
                    elif bottom_up_table[row_index][j] == '=':
                        bottom_up_table[row_index][j] += '>'
                        print(item, '>=', right_part, 'CONFLICT')
                    elif bottom_up_table[row_index][j] == '<':
                        bottom_up_table[row_index][j] += '>'
                        print(item, '<>', right_part, 'CONFLICT')
                    elif bottom_up_table[row_index][j] == '=<':
                        bottom_up_table[row_index][j] += '>'
                        print(item, '<=>', right_part, 'CONFLICT')
                # print(left_part, '<', right_part)

                if not rules_array[j][0] == "'":
                    right_part = get_first_plus(j)
                    for item in left_part:
                        for it in right_part:
                            row_index = rules_array.index(item)
                            col_index = rules_array.index(it)
                            if not bottom_up_table[row_index][col_index]:
                                bottom_up_table[row_index][col_index] = '>'
                            elif bottom_up_table[row_index][col_index] == '=':
                                bottom_up_table[row_index][col_index] += '>'
                                print(item, '>=', it, 'CONFLICT')
                            elif bottom_up_table[row_index][col_index] == '<':
                                bottom_up_table[row_index][col_index] += '>'
                                print(item, '<>', it, 'CONFLICT')
                            elif bottom_up_table[row_index][col_index] == '=<':
                                bottom_up_table[row_index][col_index] += '>'
                                print(item, '<=>', it, 'CONFLICT')
                    # print(left_part, '>', right_part)
    return bottom_up_table, rules_array


def get_table():
    global bottom_up_rule_table
    global rules

    bottom_up_rule_table, rules = grammar_parser()

    with open('./papers/bottom_up.csv', 'w', newline=''):
        pass

    with open('./papers/bottom_up.csv', 'a', newline='') as f:
        rules.insert(0, '')
        csv.writer(f).writerow(rules)
        for index, row in enumerate(bottom_up_rule_table):
            row.insert(0, rules[index + 1])
            csv.writer(f).writerow(row)
    return bottom_up_rule_table, rules


def get_poliz_sign(basis, rule, return_val):
    basis = ' '.join(basis)
    print(basis, '   |   ', rule)
    if basis == "expression '+' T1" and rule == 'expression':
        return '+'
    elif basis == "expression '-' T1" and rule == 'expression':
        return '-'
    elif basis == "'-' T1" and rule == 'expression':
        return '@'
    elif basis == "T '*' F" and rule == 'T':
        return '*'
    elif basis == "T '/' F" and rule == 'T':
        return '/'
    elif basis == "'IDN'" and rule == 'F':
        return return_val
    elif basis == "'CON'" and rule == 'F':
        return return_val
    else:
        return ''


def parser(tokens):
    global bottom_up_rule_table
    global rules
    global rule_var_list
    bottom_up_rule_table, rules = grammar_parser()
    tokens = [[token[0], token[1], token[2], token[3], token[4], token[5], token[6], "'" + tokens_identifiers[token[6]] + "'"] for token in tokens]

    tokens.append([None, None, '#', None, None, None, None, '#'])
    tokens.insert(0, [None, None, '#', None, None, None, None, '#'])
    output_right_arr = [str(token[2]) for token in tokens]
    syntactical_table = [['', '', ' '.join(output_right_arr), '']]

    stack = [tokens.pop(0)]
    output_right_arr = [str(token[2]) for token in tokens]
    syntactical_table.append(['#', '<', ' '.join(output_right_arr), ''])

    stack.append(tokens.pop(0))
    output_left_arr = [str(stk[2]) for stk in stack]
    output_right_arr = [str(token[2]) for token in tokens]
    syntactical_table.append([' '.join(output_left_arr), '<', ' '.join(output_right_arr), ''])

    err_msg = ''
    poliz_arr = ['', ]

    while len(stack) != 2 or len(tokens) != 1:
        left_i = rules.index(stack[-1][-1])
        if tokens[0][-1] == '#':
            main_relation = '>'
        else:
            right_i = rules.index(tokens[0][-1])
            main_relation = bottom_up_rule_table[left_i][right_i]

        if main_relation in ('<', '='):
            if tokens[0][-1] == "'begin'":
                del grammar["variables_list"]
            stack.append(tokens.pop(0))

            output_left_arr = [str(stk[2]) for stk in stack]
            output_right_arr = [str(token[2]) for token in tokens]
            syntactical_table.append([' '.join(output_left_arr), main_relation, ' '.join(output_right_arr), ' '.join(poliz_arr)])

        elif main_relation == '>':
            basis = []
            for i in range(len(stack) - 1, 0, -1):
                if stack[i-1][-1] == '#':
                    basis = stack[i:]
                    basis = [bss[-1] for bss in basis]
                else:
                    stack_left_i = rules.index(stack[i - 1][-1])
                    stack_right_i = rules.index(stack[i][-1])
                    relation = bottom_up_rule_table[stack_left_i][stack_right_i]
                    if relation == '<':
                        basis = stack[i:]
                        basis = [bss[-1] for bss in basis]
                        break
            for rule in sorted(grammar.keys(), reverse=True):
                for rule_variant in grammar[rule]:
                    if ' '.join(basis) == rule_variant:
                        poliz_arr.append(get_poliz_sign(basis, rule, stack[-1][2]))
                        del stack[i:]
                        stack.append([None, None, rule, None, None, None, None, rule])
                        output_left_arr = [str(stk[2]) for stk in stack]
                        output_right_arr = [str(token[2]) for token in tokens]
                        syntactical_table.append([' '.join(output_left_arr), main_relation, ' '.join(output_right_arr), ' '.join(poliz_arr)])
                        break
                if ' '.join(basis) == rule_variant:
                    break
            if ' '.join(basis) != rule_variant:
                err_msg = 'Incorrect end of program {0}'.format(stack[-1][-1])
                break
        else:
            err_msg = 'Empty cell in table between {0} and {1}\nLine: {2}'.format(stack[-1][-1], tokens[0][-1], tokens[0][1])
            break
    grammar["variables_list"] = rule_var_list
    for i in range(len(syntactical_table) - 1):
        syntactical_table[i][1] = syntactical_table[i+1][1]
    if err_msg:
        syntactical_table[-1][1] = ''
    return syntactical_table, err_msg
