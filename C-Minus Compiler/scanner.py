from models import SymbolTable, Token

keywords = ['break', 'else', 'if', 'int', 'while', 'return', 'void']
symbols = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '/', '=='}
line_num = 1
current_char = ""
last_char = ''


class Error:
    def __int__(self):
        self.lexeme = ''
        self.message = "There is no lexical error."
        self.line_num = 0


class Scanner:
    def __init__(self, input_path="input.txt"):

        if not input_path:
            raise FileNotFoundError("Input file is not available")

        self.input_file = open(input_path)

        self.symbol_table = SymbolTable()
        self.line_num = 1
        self.tokens = []

        self.lexical_errors = []
        self.token_obj = Token()



    def read_next_char(self):
        """
               Read the next character from the input file.

               :return: The next character in the input file.
        """
        char = self.input_file.read(1)
        return char

    def get_next_token(self):
        """
                Retrieve the next valid token from the input by calling the read_next_token method.
                If no tokens are found, return an EOF token.

                :return: The next token or EOF token when input is exhausted.
        """
        previous_len = len(self.tokens)
        while self.read_next_token():
            if len(self.tokens) > previous_len:
                previous_len = len(self.tokens)
                return self.tokens[-1]
        eof = Token()
        eof.lexeme = "EOF"
        eof.line_num = line_num
        eof.context = "$"
        return eof
            

    def read_next_token(self):
        """
                Analyze the next character to determine whether it is part of a number, keyword, identifier,
                symbol, or whitespace. Handles lexical errors when invalid input is encountered.

                :return: True if more tokens are available, False if the end of the input file is reached.
        """

        global line_num
        global current_char
        global last_char

        if not last_char:
            current_char = self.read_next_char()
        else:
            last_char = ''

        if is_number(current_char):
            self.extract_number(current_char, line_num)

        elif current_char.isalpha():
            self.extract_key_id(line_num)

        elif is_symbol(current_char):
            self.extract_symbol(current_char, line_num)

        elif is_whitespace(current_char):
            if current_char == '\n':
                line_num += 1
            last_char = ''

        elif current_char == '':
            self.input_file.close()
            return False
        else:
            error = Error()
            error.lexeme = current_char
            error.line_num = line_num
            error.message = "Invalid input"
            self.lexical_errors.append(error)

        return True

    def extract_number(self, lexeme, line_num):
        """
                Extract a number token from the input, and handle lexical errors for invalid numbers.

                :param lexeme: The initial lexeme containing the first digit.
                :param line_num: The current line number for error reporting.
                :return: The lexeme representing the valid number.
        """
        global current_char
        global last_char
        while is_number(current_char):
            current_char = self.read_next_char()

            if current_char.isalpha():
                error = Error()
                error.lexeme = lexeme + current_char
                error.line_num = line_num
                error.message = "Invalid number"
                self.lexical_errors.append(error)
                break

            if not is_number(current_char):
                token_obj = Token()
                token_obj.lexeme = lexeme
                token_obj.type = "NUM"
                token_obj.context = "NUM"
                token_obj.line_num = line_num
                self.tokens.append(token_obj)
                lexeme = current_char
                last_char = current_char
                break

            lexeme += current_char

        return lexeme

    def extract_symbol(self, lexeme, line_num):
        """
                Extract a symbol token from the input, including handling multi-character symbols like '=='
                and errors for invalid symbols.

                :param lexeme: The initial lexeme containing the symbol.
                :param line_num: The current line number for context.
        """
        global current_char
        global last_char
        if current_char == "=":
            current_char = self.read_next_char()
            if current_char == "=":
                lexeme = "=="
            else:
                last_char = current_char

        elif current_char == "*":
            current_char = self.read_next_char()
            if current_char == "/":
                error = Error()
                error.lexeme = "*/"
                error.line_num = line_num
                error.message = "Unmatched comment"
                self.lexical_errors.append(error)
                return

            elif not current_char.isdigit() and not current_char.isalpha() and not is_whitespace(
                    current_char) and current_char not in symbols:
                error = Error()
                error.lexeme = lexeme + current_char
                error.line_num = line_num
                error.message = "Invalid input"
                self.lexical_errors.append(error)
                return
            else:
                last_char = current_char

        elif current_char == "/":
            current_char = self.read_next_char()
            if current_char == "*":
                while True:
                    if current_char == '':
                        error = Error()
                        error.lexeme = current_char
                        error.line_num = line_num
                        error.message = "Unclosed comment"
                        self.lexical_errors.append(error)
                        return

                    current_char = self.read_next_char()
                    if current_char == "*":
                        current_char = self.read_next_char()

                        if current_char == "/":
                            lexeme = ""
                            break
            else:
                last_char = current_char

        if lexeme:
            token_obj = Token()
            token_obj.lexeme = lexeme
            token_obj.type = "SYMBOL"
            token_obj.context = lexeme
            token_obj.line_num = line_num
            self.tokens.append(token_obj)
            if lexeme != "=" and lexeme != "*" and lexeme != "/":
                last_char = ''

    def extract_key_id(self, line_num):
        """
                Extract either a keyword or an identifier from the input and add the token to the tokens list.
                Handle errors for invalid input sequences.

                :param line_num: The current line number for context.
        """
        global current_char
        global last_char
        lexeme = ''
        while current_char.isalpha() or current_char.isdigit():
            lexeme += current_char
            current_char = self.read_next_char()
            if is_whitespace(current_char) or is_symbol(current_char):
                if is_keyword(lexeme):
                    token_obj = Token()
                    token_obj.lexeme = lexeme
                    token_obj.type = "KEYWORD"
                    token_obj.context = lexeme
                    token_obj.line_num = line_num
                    self.tokens.append(token_obj)
                    last_char = current_char
                elif is_identifier(lexeme):
                    token_obj = Token()
                    token_obj.lexeme = lexeme
                    token_obj.type = "ID"
                    token_obj.context = "ID"
                    token_obj.line_num = line_num
                    self.tokens.append(token_obj)
                    last_char = current_char
                lexeme = current_char
                return
        error = Error()
        error.lexeme = lexeme + current_char
        error.line_num = line_num
        error.message = "Invalid input"
        self.lexical_errors.append(error)

        return lexeme


def is_number(token):
    """
    Check if the given token is a digit.

    :param token: The character to check.
    :return: True if the token is a digit, False otherwise.
    """
    return token.isdigit()


def is_identifier(token):
    """
    Check if the given token is a valid identifier, starting with an alphabetic character or underscore.

    :param token: The string to check.
    :return: True if the token is a valid identifier, False otherwise.
    """
    if token[0].isalpha() or token[0] == '_':
        for char in token[1:]:
            if not (char.isalnum() or char == '_'):
                return False
        return True
    return False


def is_symbol(token):
    """
    Check if the given token is a symbol.

    :param token: The character to check.
    :return: True if the token is a recognized symbol, False otherwise.
    """
    return token in symbols


def is_whitespace(token):
    """
    Check if the given token is a whitespace character.

    :param token: The character to check.
    :return: True if the token is a whitespace character, False otherwise.
    """
    return token.isspace()


def is_keyword(token):
    """
    Check if the given token is a keyword.

    :param token: The string to check.
    :return: True if the token is a recognized keyword, False otherwise.
    """
    return token in keywords

