automatic_machine_table = {
    # state: {
    #     token_id (from tokens_identifiers.py): [stack, next state, (False - error, True - exit)]
    # }
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


def parser(tkns):
    global tokens
    tokens = tkns
    global i
    i = 0
    state = 1
    stack = []
    automatic_table = []
    while i < len(tokens):
        label = tokens[i][6]    # token_id (from tokens_identifiers.py)
        # print(state, tokens[i][2], stack)
        automatic_table.append([state, tokens[i][2], stack[:]])

        # if label is in current state
        if label in automatic_machine_table[state]:
            # if is needed to push something to stack
            if automatic_machine_table[state][label][0]:
                # push to stack value from label
                stack.append(automatic_machine_table[state][label][0])
            # update state to next state from this label
            state = automatic_machine_table[state][label][1]
            # to get next token
            i += 1
        # if we have blank line current state
        elif '' in automatic_machine_table[state]:
            # if is needed to push something to stack
            if automatic_machine_table[state][''][0]:
                # push to stack value from label
                stack.append(automatic_machine_table[state][''][0])
                # update state to next state from this label
                state = automatic_machine_table[state][''][1]
            # if is needed to exit from current automatic machine
            elif automatic_machine_table[state][''][2]:
                # update state to value from stack
                state = stack.pop()
        # if label is not in current state
        elif label not in automatic_machine_table[state]:
            # get list of all labels from current stack
            t = list(automatic_machine_table[state].values())
            # check is needed to exit from current automatic machine
            if t[0][2]:
                # update state to value from stack
                state = stack.pop()
            else:
                return automatic_table
    return automatic_table
