import csv
import os


class ProgramFile:
    def __init__(self, program_file_path: str):
        self.result_path = './results/'
        self.program_file_path = program_file_path
        self.program_file_name = self.program_file_path.split('/')[-1]
        self.program_text: list = ...
        self.read_program_from_file()
        self.tokens = None
        self.automatic_parse_table = None
        self.bottom_up_table = None
        self.poliz = None
        self.poliz_table = None

    def read_program_from_file(self):
        """
        Function, thar reads program text from input .txt file
        :return:
        """
        with open(self.program_file_path, 'r') as f:
            self.program_text = [row.strip(' ') for row in f]

    def write_tokens_to_file(self):
        """
        Function, that writes tokens to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/tokens.csv', 'w', newline='') as f:
            for token in self.tokens:
                csv.writer(f).writerow([
                    token.count, token.line_number, token.token,
                    token.idn_id, token.con_id, token.lab_id, token.token_id
                ])

    def write_identifiers_to_file(self):
        """
        Function, that writes identifiers to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/IDN.csv', 'w', newline='') as f:
            for identifier in self.tokens.identifiers:
                csv.writer(f).writerow([
                    identifier.count, identifier.token, identifier.value, identifier.idn_type
                ])

    def write_constants_to_file(self):
        """
        Function, that writes identifiers to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/CONST.csv', 'w', newline='') as f:
            for const in self.tokens.constants:
                csv.writer(f).writerow([
                    const.count, const.token, const.con_type
                ])

    def write_labels_to_file(self):
        """
        Function, that writes labels to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/LAB.csv', 'w', newline='') as f:
            for label in self.tokens.labels:
                csv.writer(f).writerow([
                    label.count, label.token
                ])

    def write_automatic_parse_table_to_file(self):
        """
        Function, that writes automatic parse table table to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/automatic_parse_table.csv', 'w', newline='') as f:
            for row in self.automatic_parse_table:
                csv.writer(f).writerow(row)

    def write_bottom_up_table_to_file(self):
        """
        Function, that writes bottom up table table to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/bottom_up_table.csv', 'w', newline='') as f:
            for row in self.bottom_up_table:
                csv.writer(f).writerow(row)

    def write_poliz_table_to_file(self):
        """
        Function, that writes poliz table to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/poliz_table.csv', 'w', newline='') as f:
            for row in self.poliz_table:
                csv.writer(f).writerow(row)

    def write_poliz_to_file(self):
        """
        Function, that writes poliz to output file
        :return:
        """
        with open(self.result_path + self.program_file_name + '/poliz.txt', 'w') as f:
            f.write(str(self.poliz))

    def create_tables_dir(self):
        """
        Function, that creates directory for output tables
        :return:
        """
        program_tables_path = self.result_path + self.program_file_name
        if not os.path.isdir(self.result_path):
            try:
                os.mkdir(self.result_path)
            except OSError:
                raise("Creation of the directory %s failed" % self.result_path)
        if not os.path.isdir(program_tables_path):
            try:
                os.mkdir(program_tables_path)
            except OSError:
                raise("Creation of the directory %s failed" % program_tables_path)

    def write_results_to_files(self):
        """
        Function, that runs all functions, which writes to files
        :return:
        """
        self.create_tables_dir()
        self.write_tokens_to_file()
        self.write_identifiers_to_file()
        self.write_constants_to_file()
        self.write_labels_to_file()
        if self.automatic_parse_table:
            self.write_automatic_parse_table_to_file()
        if self.bottom_up_table:
            self.write_bottom_up_table_to_file()
        if self.poliz_table:
            self.write_poliz_table_to_file()
        if self.poliz:
            self.write_poliz_to_file()
