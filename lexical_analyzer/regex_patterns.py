"""
Regex patterns for lexical analyse
"""
regex_patterns = {
    'white_separator': r"^\s$",
    'character': r"^[A-Za-z]$",
    'identifier': r"^\w$",
    'digit': r"^\d$",
    'single_separator': r"^[,;:()\-+*\/\[\]]$",
    'dot': r"^[.]$",
    'more': r"^[>]$",
    'less': r"^[<]$",
    'equal': r"^[=]$",
    'not_equal': r"^[!]$",
    'number_sign': r"^[#]$",
}
