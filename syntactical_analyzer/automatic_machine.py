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
