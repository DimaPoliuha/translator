import copy


class PolizProcessing:
    def __init__(self):
        pass

    def __call__(self, program_file):
        self.program_file = program_file
        self.poliz = copy.deepcopy(self.program_file.poliz)
        self.run_program()

    def run_program(self):
        announcements = []
        for token in self.poliz:
            curr_token = str(token)
            
            if curr_token == 'EA':
                break
            if curr_token == 'int':
                for token_identifier in announcements:
                    self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'int'
                announcements = []
            elif curr_token == 'float':
                for token_identifier in announcements:
                    self.program_file.tokens.identifiers[token_identifier.idn_id].idn_type = 'float'
                announcements = []
            else:
                announcements.append(token)
