grammar = {
    "program": [
        "declaration_list 'begin' operators_list 'end'",
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
        "'for' 'IDN' '=' expression 'by' expression 'to' expression 'do' ':' operators_list 'rof'",
    ],
    "conditional_statement": [
        "'if' LR 'then' ':' operators_list 'fi'",
    ],
    "assignment": [
        "'IDN' '=' expression",
    ],
    "expression": [
        "T",
        "expression '+' T",
        "expression '-' T",
        "'-' T"
    ],
    "T": [
        "F",
        "T '*' F",
        "T '/' F",
    ],
    "F": [
        "'IDN'",
        "'CON'",
        "'(' expression ')'",
    ],
    "LR": [
        "LR 'or' LT",
        "LT",
    ],
    "LT": [
        "LT 'and' LF",
        "LF",
    ],
    "LF": [
        "relation",
        "'[' LR ']'",
        "'not' LF",
    ],
    "relation": [
        "expression relation_sign expression",
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


def grammar_parser():
    bottom_up_array = []

    for rule in grammar:
        for rule_variant in grammar[rule]:
            for tkn in rule_variant.split():
                bottom_up_array.append(tkn)
                # print(tkn.strip("'"))

    bottom_up_array.append('program')
    bottom_up_array = sorted(set(bottom_up_array))
    bottom_up_array.reverse()
    print(bottom_up_array)
    
    bottom_up_table = [[None for item in bottom_up_array] for it in bottom_up_array]

    for rule in grammar:
        for rule_variant in grammar[rule]:
            rule_variant_tokens = rule_variant.split()
            if len(rule_variant_tokens) > 1:
                for i in range(len(rule_variant_tokens)):
                    print(rule_variant_tokens[i])
                print('|')
        print()

    # print(bottom_up_array.index('user_output'))
    # for i in range(len(a)):
    #     for j in range(len(a[i])):
    #         print(a[i][j], end=' ')
    #     print()
    return bottom_up_table


def parser(tokens):
    main_table = grammar_parser()
