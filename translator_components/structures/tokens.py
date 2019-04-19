from translator_components.structures.tokens_identifiers import tokens_identifiers, tokens_identifiers_reversed


class TokenTemplate:
    """
    Base class for tokens
    """
    def __init__(self, token):
        self.token = token

    def __str__(self):
        """
        Represents token as part of input program
        Examples:
        a -> a
        0.7 -> 0.7
        #Label -> #Label
        if -> if
        = -> =
        :return:
        """
        return str(self.token)

    def __repr__(self):
        return str(self.token)


class Token(TokenTemplate):
    """
    Class, that helps to organise all information about token
    """
    count = 0

    def __init__(self, line_num, token, idn_id='', con_id='', lab_id=''):
        TokenTemplate.__init__(self, token)
        self.count = Token.count
        Token.count += 1
        self.line_number = line_num
        self.idn_id = idn_id
        self.con_id = con_id
        self.lab_id = lab_id
        if not idn_id == '':
            self.token_id = tokens_identifiers['IDN']
        elif not con_id == '':
            self.token_id = tokens_identifiers['CON']
        elif not lab_id == '':
            self.token_id = tokens_identifiers['LAB']
        else:
            self.token_id = tokens_identifiers[self.token]

    def __repr__(self):
        """
        Represents token as part of grammar
        Examples:
        a -> IDN
        0.7 -> CON
        #Label -> LAB
        if -> if
        = -> =
        :return:
        """
        return tokens_identifiers_reversed[self.token_id]


class Idn(TokenTemplate):
    """
    Class, that helps to organise all information about identifier
    """
    count = 0

    def __init__(self, token):
        TokenTemplate.__init__(self, token)
        self.count = Idn.count
        Idn.count += 1
        self.value = ''
        self.idn_type = ''


class Con(TokenTemplate):
    """
    Class, that helps to organise all information about constant
    """
    count = 0

    def __init__(self, token, con_type=''):
        TokenTemplate.__init__(self, token)
        self.count = Con.count
        Con.count += 1
        self.con_type = con_type


class Lab(TokenTemplate):
    """
    Class, that helps to organise all information about label
    """
    count = 0

    def __init__(self, token):
        TokenTemplate.__init__(self, token)
        self.count = Lab.count
        Lab.count += 1


class Tokens(list):
    """
    Class, thar wraps list for storing tokens (class Token)
    """
    def __init__(self):
        list.__init__(self)
        self.identifiers = []
        self.constants = []
        self.labels = []

    def __str__(self):
        """
        Represents tokens as part of input program
        Examples:
        [int, a] -> int a
        [sum, =, 0.7, +, 1] -> sum = 0.7 + 1
        [goto, #Label] -> goto #Label
        if -> if
        = -> =
        :return:
        """
        return ' '.join([str(token) for token in self])

    def __repr__(self):
        """
        Represents tokens as part of grammar
        Examples:
        [int, a] -> int IDN
        [sum, =, 0.7, +, 1] -> sum = CON + CON
        [goto, #Label] -> goto LAB
        if -> if
        = -> =
        :return:
        """
        return ' '.join([repr(token) for token in self])
