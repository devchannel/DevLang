import locUtils as Loc
from tokens import *


class Lexer():
    def __init__(self, program):
        # The program
        self.program = program
        # Our position in the program
        self.pos = 0
        # tuple of line number and column number
        self.loc = (0, 0)
        # The current token we are on
        self.cur_tok = None

    def raise_error(self):
        raise Exception("Ohnoes, an error occurred at position {}.".format(self.pos))

    def get_token(self):
        """
        This method moves us up, and breaks out another token
        """
        program = self.program

        if self.pos >= len(program):
            return Token(Special.EOF, None, self.loc)

        # if it's a space then skip the character
        while self.pos < len(program) and program[self.pos] == ' ':
            self.pos += 1
            self.loc = Loc.nextColumn(self.loc)

        if self.pos >= len(program):
            return Token(Special.EOF, None, self.loc)

        cur_char = program[self.pos]

        if cur_char.isdigit():
            return self.lex_int()

        if cur_char == "'":
            # That means that this is a char
            return self.lex_char()
        if cur_char == '"':
            # This is a string
            return self.lex_str()

        # We should probably declare this list somewhere better
        # Separate enum for these chars?????
        # Do we really need to return a token for spaces?
        if cur_char in ['(', ')', ';']:
            self.pos += 1
            loc = self.loc
            self.loc = Loc.nextColumn(self.loc)
            return Token(Special(['(', ')', ';'].index(cur_char)), cur_char, loc)

        if cur_char == "\n":
            self.pos += 1
            loc = self.loc
            self.loc = Loc.nextLine(self.loc)
            self.loc = Loc.setColumn(self.loc, 0)
            return Token(Special.NewLine, "\n", loc)

        if self.maybe_operator(cur_char):
            return self.lex_op()

    def lex_int(self):
        program = self.program
        cur_char = program[self.pos]
        loc = self.loc
        integer = ""

        # loop while there is still an integer left
        while self.pos < len(program) and program[self.pos].isdigit():
            integer += cur_char
            self.pos += 1
            self.loc = Loc.nextColumn(self.loc)

        return Token(Type.Integer, integer, loc)

    def lex_char(self):

        # Set the next value to be the item contained within the char
        loc = self.loc
        char = self.program[self.pos + 1]
        self.pos += 2  # Increment to the next ', if it exists
        self.loc = Loc.moveColumnBy(self.loc, 2)

        if self.pos >= len(self.program) or self.program[self.pos] != "'":
            self.raise_error()  # Error checking
        self.pos += 1  # Get to the next position
        self.loc = Loc.nextColumn(self.loc)

        return Token(Type.Char, char, loc)

    def lex_str(self):
        self.pos += 1   # Skip past that "
        self.loc = Loc.nextColumn(self.loc)
        program = self.program

        string = ""  # A running total
        while program[self.pos] != '"':
            if program[self.pos] == '\\' and program[self.pos + 1] == '"':
                self.pos += 2  # Skip over the \ and "
                self.loc = Loc.moveColumnBy(self.loc, 2)

            string += program[self.pos]  # Append to our running total
            self.pos += 1  # Move over a char
            self.loc = Loc.nextColumn(self.loc)

            if program[self.pos] == '"':  # We've reached the end
                self.pos += 1  # Skip over the " again
                loc = self.loc
                self.loc = Loc.nextColumn(self.loc)
                return Token(Type.String, string, loc)

        self.raise_error()

    def lex_op(self):
        program = self.program
        index = 0
        loc = self.loc
        matches = []  # maintain a list of all matches

        for op in Operator:

            if index > len(op.value):  # This is not the operator you are looking for
                continue  # move to the next operator

            # loop through the operator, checking each char
            while index < len(op.value) and program[self.pos] == op.value[index]:
                self.pos += 1
                self.loc = Loc.nextColumn(self.loc)
                index += 1

            # (len(op.value) - 1) + 1, the length of string, plus the earlier matched portion
            if index == len(op.value):  # The whole string matched, plus the one we matched earlier

                matches.append(Token(op, op.value, loc))

        if(len(matches) == 0):
            self.raise_error()  # We couldn't find any matches
        return max(matches, key=len)  # return the match that fit the most

    def maybe_operator(self, char):
        for op in Operator:
            if char == op.value[0]:
                return True
        return False

    def tokenize(self):
        tokens = []
        token = self.get_token()
        tokens.append(token)
        while token.type != Special.EOF:
            token = self.get_token()
            tokens.append(token)
        # It returns a stack!!!
        return list(reversed(tokens))
