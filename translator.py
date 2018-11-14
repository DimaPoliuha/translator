import sys
from lexical_analyzer.analyzer import generate_tokens
from syntactical_analyzer.parser import parser

if __name__ == "__main__":
    if not generate_tokens():
        sys.exit(-1)
    if not parser():
        sys.exit(-2)
