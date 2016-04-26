from enum import Enum

class Operator(Enum):
    plus = '+'
    sub = '-'
    mult = '*'
    div = '/'
    func_one = '='
    func_multi = '=>'
    arg_list = '->'
    type_sep = '|'

class Special(Enum):
    EOF = 0
    Whitespace = 1

class Type(Enum):
    Integer = 0
    Char = 1
    String = 2

class Keyword(Enum):
    Return = 0


class Token():
    def __init__(self, type, value):
        # For now, one of the Operators or an EOF
        self.type = type
        self.value = value
    def __repr__(self):
        return "({}, {})".format(self.type.name, self.value)
    def __str__(self):
        return self.__repr__()
    def __len__(self):
        return len(self.value)

class Lexer():
    def __init__(self, program):
        # The program
        self.program = program
        # Our position in the program
        self.pos = 0
        # The current token we are on
        self.cur_tok = None
        """
        TODO:
            A current line number var maybe? For printing out errors later.
        """

    def raise_error(self):
        raise Exception("Ohnoes, an error occurred at position {}.".format(self.pos))

    def get_token(self):
        """
        This method moves us up, and breaks out another token
        """
        program = self.program

        if self.pos >= len(program):
            return Token(Special.EOF, None)

        cur_char = program[self.pos]

        if cur_char.isdigit():
            return self.lex_int()

        if cur_char == "'":
            # That means that this is a char
            return self.lex_char()
        if cur_char == '"':
            # This is a string
            return self.lex_str()

        if cur_char.isspace():
            self.pos += 1
            return Token(Special.Whitespace, None)

        if self.maybe_operator(cur_char):
            return self.lex_op()

    def eat(self, token_type):
        """
        Compares the current token type to the one given
        Raises error if they don't match, otherwise it consumes the token
        """
        if self.cur_tok.type == token_type:
            self.cur_tok = self.get_token()
        else:
            self.raise_error()


    def lex_int(self):
        program = self.program
        cur_char = program[self.pos]

        integer = ""

        # loop while there is still an integer left
        while self.pos < len(program) and program[self.pos].isdigit():
            integer += program[self.pos]
            self.pos += 1

        return Token(Type.Integer, int(integer))

    def lex_char(self):

        char = self.program[self.pos + 1] # Set the next value to be the item contained within the char
        self.pos += 2 # Increment to the next ', if it exists

        if self.pos >= len(self.program) or self.program[self.pos] != "'":
            self.raise_error() # Error checking
        self.pos += 1 # Get to the next position

        return Token(Type.Char, char)

    def lex_str(self):
        self.pos += 1 # Skip past that "
        program = self.program

        string = "" # A running total
        while program[self.pos] != '"':
            if program[self.pos] == '\\' and program[self.pos + 1] == '"':
                self.pos += 2 # Skip over the \ and "

            string += program[self.pos] # Append to our running total
            self.pos += 1 # Move over a char

            if program[self.pos] == '"': # We've reached the end
                self.pos += 1 # Skip over the " again
                return Token(Type.String, string)

        self.raise_error()

    def lex_op(self):
        program = self.program
        index = 0

        matches = [] # maintain a list of all matches

        for op in Operator:

            if index > len(op.value): # This is not the operator you are looking for
                continue # move to the next operator

            while index < len(op.value) and program[self.pos] == op.value[index]: # loop through the operator, checking each char
                self.pos += 1
                index += 1

            # (len(op.value) - 1) + 1, the length of string, plus the earlier matched portion
            if index == len(op.value): # The whole string matched, plus the one we matched earlier
                matches.append(Token(op, op.value))

        if(len(matches) == 0):
            self.raise_error() # We couldn't find any matches
        return max(matches, key=len) # return the match that fit the most

    def maybe_operator(self, char):
        for op in Operator:
            if char == op.value[0]:
                return True
        return False

def main():
    #file = open("test", 'r')
    #lines = file.readlines(file)
    lines = ["F|int| => |int x| |int y| -> int z = x * y; return z;"]
    print("Original code: ", lines)
    lexCommands = []
    for line in lines:
        command = ""
        for ch in line:

            if (ch == ';' or ch == ':' or ch == ' ' or ch == '|'):
                #Delimter, add current command to list
                if (command != ''):
                    lexCommands.append(command)
                if (ch == ';' or ch == '|'):
                    lexCommands.append(ch)
                if (command == '=' or command =='-' and ch == '>'):
                    lexCommands.append(command + ch)
                command = ""

            else:
                command += ch
    print("Seperated commands: ", lexCommands)
    lexify(lexCommands)

def lexify(commands):
    newCommandSet = []
    lastLexCommand = (" ")
    for command in commands:
        lexCommand = ()
        if (command == "string" or command == "int" or command == "char" or command == "float"):
            lexCommand = ("DATA", command)
        elif (command == "|"):
            lexCommand = ("SEPERATOR", command)
        elif (command == ";"):
            lexCommand = ("ENDOFLINE")
        elif (command == "=>" or command == "->" or command == "+" or command == "-" or command == "*" or command == "/"):
            lexCommand = ("OPERATOR", command)
        elif (command == "return"):
            lexCommand = ("KEYWORD", command)
        elif (command.isalnum):
            if (lastLexCommand[0] == "DATA"):
                lexCommand = ("VARIABLE", command)
            else:
                lexCommand = ("ALPHANUM")
        lastLexCommand = lexCommand
        newCommandSet.append(lexCommand)
    print("Made into actual readable commands: " , newCommandSet)


lexer = Lexer("4*5")

token = Token(None, None)

lexer.cur_tok = lexer.get_token()

while lexer.cur_tok.type != Special.EOF:

    # A very simple program, currently demonstrates aspects of what the Parser should do
    # It parses non-spaced mathematical expressions

    left = lexer.cur_tok
    lexer.eat(Type.Integer)

    op = lexer.cur_tok
    if op.type == Operator.plus:
        lexer.eat(Operator.plus)
    elif op.type == Operator.sub:
        lexer.eat(Operator.sub)
    elif op.type == Operator.mult:
        lexer.eat(Operator.mult)
    else:
        lexer.eat(Operator.div)

    right = lexer.cur_tok
    lexer.eat(Type.Integer)

    if op.type == Operator.plus:
        print(left.value + right.value)
    elif op.type == Operator.sub:
        print(left.value - right.value)
    elif op.type == Operator.mult:
        print(left.value * right.value)
    else:
        print(left.value / right.value)