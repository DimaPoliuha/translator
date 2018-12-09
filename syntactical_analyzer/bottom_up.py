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
