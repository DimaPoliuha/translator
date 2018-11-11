from lexical_analyzer.analyzer import generate_tokens
from syntactical_analyzer.parser import parser

if __name__ == "__main__":
    tokens = generate_tokens()
    parser(tokens)
