import csv

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
    if not bottom_up_rule_table:

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


def parser(tokens):
    global bottom_up_rule_table
    global rules
    if not bottom_up_rule_table:
        bottom_up_rule_table, rules = grammar_parser()

    # pure_tokens = []
    # for token in tokens:
    #     if token[6] == 100:
    #         pure_tokens.append("'IDN'")
    #     elif token[6] == 101:
    #         pure_tokens.append("'CON'")
    #     elif token[6] == 102:
    #         pure_tokens.append("'LAB'")

    tokens.append(['', '', '@', '', '', '', ''])
    stack_tkn_idn = [0, tokens[0][6], ]
    stack = ["@", "'" + tokens.pop(0)[2] + "'", ]
    base = [stack[1], ]
    # while True:
    # while stack != ['@', 'program']:
    for t in range(50):
        tkn_l = stack[-1]
        if stack_tkn_idn[-1] == 100:
            left_index = rules.index("'IDN'")
        elif stack_tkn_idn[-1] == 101:
            left_index = rules.index("'CON'")
        elif stack_tkn_idn[-1] == 102:
            left_index = rules.index("'LAB'")
        else:
            left_index = rules.index(tkn_l)

        tkn_r = "'" + tokens[0][2] + "'"
        if tokens[0][6] == 100:
            right_index = rules.index("'IDN'")
        elif tokens[0][6] == 101:
            right_index = rules.index("'CON'")
        elif tokens[0][6] == 102:
            right_index = rules.index("'LAB'")
        else:
            right_index = rules.index(tkn_r)

        print(bottom_up_rule_table[left_index][right_index])

        if bottom_up_rule_table[left_index][right_index] == '<':
            stack_tkn_idn.append(tokens[0][6])
            stack.append("'" + tokens.pop(0)[2] + "'")
            base.append(tkn_r)
        elif bottom_up_rule_table[left_index][right_index] == '=':
            stack_tkn_idn.append(tokens[0][6])
            stack.append("'" + tokens.pop(0)[2] + "'")
        else:
            print(stack)
            replacement = ""
            if base:
                base_index = stack.index(base[-1])
                for i in range(len(stack) - 1, base_index - 1, -1):
                    if stack_tkn_idn[i] == 100:
                        tail = "'IDN'"
                    elif stack_tkn_idn[i] == 101:
                        tail = "'CON'"
                    elif stack_tkn_idn[i] == 102:
                        tail = "'LAB'"
                    else:
                        tail = stack[i]
                    replacement = replacement.strip()
                    replacement = tail + ' ' + replacement
                    replacement = replacement.strip()
                del base[-1]
                    # print(replacement)
                for rule in grammar:
                    for rule_variant in grammar[rule]:
                        if replacement == rule_variant:
                            del stack_tkn_idn[base_index:]
                            stack_tkn_idn.append(0)
                            del stack[base_index:]
                            stack.append(rule)
                            # print(stack[i:])
                            # print(rule)
                            break
                    if replacement == rule_variant:
                        break
            else:
                for i in range(len(stack) - 1, -1, -1):
                    if stack_tkn_idn[i] == 100:
                        tail = "'IDN'"
                    elif stack_tkn_idn[i] == 101:
                        tail = "'CON'"
                    elif stack_tkn_idn[i] == 102:
                        tail = "'LAB'"
                    else:
                        tail = stack[i]
                    replacement = replacement.strip()
                    replacement = tail + ' ' + replacement
                    replacement = replacement.strip()
                # print(replacement)
                    for rule in grammar:
                        for rule_variant in grammar[rule]:
                            if replacement == rule_variant:
                                del stack_tkn_idn[base_index:]
                                stack_tkn_idn.append(0)
                                del stack[base_index:]
                                stack.append(rule)
                                # print(stack[i:])
                                # print(rule)
                                break
                        if replacement == rule_variant:
                            break
                    if replacement == rule_variant:
                        break
