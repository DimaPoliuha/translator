# automatic_machine_table = {
#     1: {
#         'int': [None, 2, False],
#         'float': [None, 2, False]
#     },
#     2: {
#         'identifier': [None, 3, False]
#     },
#     3: {
#         ',': [None, 2, False],
#         ';': [None, 4, False]
#     },
#     4: {
#         'int': [None, 2, False],
#         'float': [None, 2, False],
#         'begin': [None, 5, False],
#     },
#     5: {
#         'label': [None, 6, False],
#         '': [7, 20, False]
#     },
#     6: {
#         ':': [None, 8, False]
#     },
#     7: {
#         ';': [None, 8, False]
#     },
#     8: {
#         'label': [None, 6, False],
#         'end': [None, 9, False],
#         '': [7, 20, False]
#     },
#     9: {
#         '': [None, None, True]
#     },
#
#     # operation
#     20: {
#         'identifier': [None, 21, False],
#         'goto': [None, 23, False],
#         'cin': [None, 25, False],
#         'cout': [None, 28, False],
#         'for': [None, 31, False],
#         'if': [42, 70, False],
#     },
#     21: {
#         '=': [22, 60, False]
#     },
#     22: {
#         '': [None, None, True]
#     },
#     23: {
#         'label': [None, 24, False]
#     },
#     24: {
#         '': [None, None, True]
#     },
#     25: {
#         '>>': [None, 26, False]
#     },
#     26: {
#         'identifier': [None, 27, False]
#     },
#     27: {
#         '>>': [None, 26, True]
#     },
#     28: {
#         '<<': [None, 29, False]
#     },
#     29: {
#         'identifier': [None, 30, False]
#     },
#     30: {
#         '<<': [None, 28, True]
#     },
#     31: {
#         'identifier': [None, 32, False]
#     },
#     32: {
#         '=': [33, 60, False]
#     },
#     33: {
#         'by': [34, 60, False]
#     },
#     34: {
#         'to': [35, 60, False]
#     },
#     35: {
#         'do': [None, 36, False]
#     },
#     36: {
#         ':': [None, 37, False]
#     },
#     37: {
#         'label': [None, 38, False],
#         '': [39, 20, False]
#     },
#     38: {
#         ':': [None, 40, False]
#     },
#     39: {
#         ';': [None, 40, False]
#     },
#     40: {
#         'label': [None, 38, False],
#         'rof': [None, 41, False],
#         '': [39, 20, False]
#     },
#     41: {
#         '': [None, None, True]
#     },
#     42: {
#         'then': [None, 43, False]
#     },
#     43: {
#         ':': [None, 44, False]
#     },
#     44: {
#         'label': [None, 45, False],
#         '': [46, 20, False]
#     },
#     45: {
#         ':': [None, 47, False]
#     },
#     46: {
#         ';': [None, 47, False]
#     },
#     47: {
#         'label': [None, 45, False],
#         'fi': [None, 48, False],
#         '': [46, 20, False]
#     },
#     48: {
#         '': [None, None, True]
#     },
#
#     # expression
#     60: {
#         '-': [None, 61, False],
#         '(': [62, 60, False],
#         'identifier': [None, 63, False],
#         'constant': [None, 63, False],
#     },
#     61: {
#         '(': [62, 60, False],
#         'identifier': [None, 63, False],
#         'constant': [None, 63, False],
#     },
#     62: {
#         ')': [None, 63, False]
#     },
#     63: {
#         '+': [None, 61, True],
#         '-': [None, 61, True],
#         '*': [None, 61, True],
#         '/': [None, 61, True],
#     },
#
#     # LR
#     70: {
#         'not': [None, 70, False],
#         '[': [72, 70, False],
#         '': [71, 60, False]
#     },
#     71: {
#         '>': [73, 60, False],
#         '<': [73, 60, False],
#         '>=': [73, 60, False],
#         '<=': [73, 60, False],
#         '==': [73, 60, False],
#         '!=': [73, 60, False],
#     },
#     72: {
#         ']': [None, 73, False]
#     },
#     73: {
#         'and': [None, 70, True],
#         'or': [None, 70, True],
#     }
# }

automatic_machine_table = {
    1: {
        1: [None, 2, False],
        2: [None, 2, False]
    },
    2: {
        100: [None, 3, False]
    },
    3: {
        18: [None, 2, False],
        16: [None, 4, False]
    },
    4: {
        1: [None, 2, False],
        2: [None, 2, False],
        3: [None, 5, False],
    },
    5: {
        102: [None, 6, False],
        '': [7, 20, False]
    },
    6: {
        17: [None, 8, False]
    },
    7: {
        16: [None, 8, False]
    },
    8: {
        102: [None, 6, False],
        4: [None, 9, False],
        '': [7, 20, False]
    },
    9: {
        '': [None, None, True]
    },

    # operation
    20: {
        100: [None, 21, False],
        5: [None, 23, False],
        6: [None, 25, False],
        7: [None, 28, False],
        8: [None, 31, False],
        13: [42, 70, False],
    },
    21: {
        19: [22, 60, False]
    },
    22: {
        '': [None, None, True]
    },
    23: {
        102: [None, 24, False]
    },
    24: {
        '': [None, None, True]
    },
    25: {
        20: [None, 26, False]
    },
    26: {
        100: [None, 27, False]
    },
    27: {
        20: [None, 26, True]
    },
    28: {
        21: [None, 29, False]
    },
    29: {
        100: [None, 30, False]
    },
    30: {
        21: [None, 28, True]
    },
    31: {
        100: [None, 32, False]
    },
    32: {
        19: [33, 60, False]
    },
    33: {
        9: [34, 60, False]
    },
    34: {
        10: [35, 60, False]
    },
    35: {
        11: [None, 36, False]
    },
    36: {
        17: [None, 37, False]
    },
    37: {
        102: [None, 38, False],
        '': [39, 20, False]
    },
    38: {
        17: [None, 40, False]
    },
    39: {
        16: [None, 40, False]
    },
    40: {
        102: [None, 38, False],
        12: [None, 41, False],
        '': [39, 20, False]
    },
    41: {
        '': [None, None, True]
    },
    42: {
        14: [None, 43, False]
    },
    43: {
        17: [None, 44, False]
    },
    44: {
        102: [None, 45, False],
        '': [46, 20, False]
    },
    45: {
        17: [None, 47, False]
    },
    46: {
        16: [None, 47, False]
    },
    47: {
        102: [None, 45, False],
        15: [None, 48, False],
        '': [46, 20, False]
    },
    48: {
        '': [None, None, True]
    },

    # expression
    60: {
        29: [None, 61, False],
        32: [62, 60, False],
        100: [None, 63, False],
        101: [None, 63, False],
    },
    61: {
        32: [62, 60, False],
        100: [None, 63, False],
        101: [None, 63, False],
    },
    62: {
        33: [None, 63, False]
    },
    63: {
        28: [None, 61, True],
        29: [None, 61, True],
        30: [None, 61, True],
        31: [None, 61, True],
    },

    # LR
    70: {
        36: [None, 70, False],
        37: [72, 70, False],
        '': [71, 60, False]
    },
    71: {
        22: [73, 60, False],
        23: [73, 60, False],
        24: [73, 60, False],
        25: [73, 60, False],
        26: [73, 60, False],
        27: [73, 60, False],
    },
    72: {
        38: [None, 73, False]
    },
    73: {
        35: [None, 70, True],
        34: [None, 70, True],
    }
}


def raise_exception(msg=''):
    raise Exception('Syntactical analyzer exception\n\n' +
                    msg +
                    '\nline: ' + str(tokens[i][1]) +
                    '\ntoken number: ' + str(tokens[i][0]) +
                    '\ntoken: ' + repr(tokens[i][2]))


def parser(tkns):
    global tokens
    tokens = tkns
    global i
    i = 0
    alpha = 1
    stack = []
    while i < len(tokens):
        label = tokens[i][6]
        print(alpha, tokens[i][2], stack)
        if label in automatic_machine_table[alpha]:
            if automatic_machine_table[alpha][label][0]:
                stack.append(automatic_machine_table[alpha][label][0])
            alpha = automatic_machine_table[alpha][label][1]
            i += 1
        elif '' in automatic_machine_table[alpha]:
            if automatic_machine_table[alpha][''][0]:
                stack.append(automatic_machine_table[alpha][''][0])
                alpha = automatic_machine_table[alpha][''][1]
            elif automatic_machine_table[alpha][''][2]:
                alpha = stack.pop()
        elif label not in automatic_machine_table[alpha]:
            t = list(automatic_machine_table[alpha].values())
            if t[0][2]:
                alpha = stack.pop()
            else:
                raise_exception('Current alpha: {0}\nCurrent stack: {1}'.format(alpha,stack))
                break
