import source.locUtils as Loc
from .tokens import *
import string

# TODO: comments

class Lexer():
    def __init__(self, program, errorHandler):
        # The program
        self.program = program
        # Our position in the program
        self.pos = 0
        # tuple of line number and column number
        self.loc = (1, 0)
        # The current token we are on
        self.cur_tok = None
        # The error handler
        self.errorHandler = errorHandler

    def get_token(self):
        """
        This method moves us up, and breaks out another token
        """

        # if it's a space then skip the character
        while self.pos < len(self.program) and self.program[self.pos] in string.whitespace:
            if self.program[self.pos] == "\n":
                self.loc = Loc.nextLine(self.loc)
                self.loc = Loc.setColumn(self.loc, 0)
            else:
                self.loc = Loc.nextColumn(self.loc)
            self.pos += 1

        if self.pos >= len(self.program):
            return Token(Special.EOF, True, self.loc)

        cur_char = self.program[self.pos]

        if self.maybe_operator(cur_char):
            return self.lex_op()

        if cur_char.isdigit():
            return self.lex_num()

        if cur_char in string.ascii_letters + "_":
            return self.lex_name()

        if cur_char == "'":
            # That means that this is a char
            return self.lex_char()

        if cur_char == '"':
            # This is a string
            return self.lex_str()

        if cur_char == '|':
            return self.lex_type()

        self.pos += 1
        self.loc = Loc.nextColumn(self.loc)
        self.errorHandler.add("Syntax", "Unknown character \'"+cur_char+"\'", self.loc)
        return Token(Special.Unknown, None, self.loc)

    def lex_name(self):
        loc = self.loc
        name = ""
        while self.pos < len(self.program) and self.program[self.pos] in string.ascii_letters+"_"+string.digits:
            name += self.program[self.pos]
            self.pos += 1
            self.loc = Loc.nextColumn(self.loc)
        return Token(Special.Name, name, loc)

    def lex_type(self):
        loc = self.loc
        self.pos += 1   # Skip past the |
        self.loc = Loc.nextColumn(self.loc)
        program = self.program

        string = ""  # store name of type
        while self.pos < len(self.program):
            if program[self.pos] == '|':  # We've reached the end
                self.pos += 1  # Skip over the |
                self.loc = Loc.nextColumn(self.loc)
                return Token(Special.TypeName, string, loc)

            string += program[self.pos]  # Append to the type name
            self.pos += 1  # Move over a char
            self.loc = Loc.nextColumn(self.loc)

        self.errorHandler.add("Syntax", "Invalid type", loc)
        return Token(Special.Unknown, None, loc)


    def lex_num(self):
        cur_char = self.program[self.pos]
        loc = self.loc
        integer = ""
        float = False

        # loop while there is still an integer left
        while self.pos < len(self.program):
            if not (self.program[self.pos].isdigit() or (self.program[self.pos] == '.' and not float)):
                break
            if self.program[self.pos] == '.':
                if not float:
                    float = True
            integer += self.program[self.pos]
            self.pos += 1
            self.loc = Loc.nextColumn(self.loc)

        if float:
            return Token(Type.Float, integer, loc)
        else:
            return Token(Type.Integer32, integer, loc)

    def lex_char(self):

        # Set the next value to be the item contained within the char
        loc = self.loc
        char = self.program[self.pos + 1]
        self.pos += 2  # Increment to the next ', if it exists
        self.loc = Loc.moveColumnBy(self.loc, 2)

        if self.pos >= len(self.program) or self.program[self.pos] != "'":
            self.errorHandler.add("Syntax", "Char literal was not closed", loc)
            return Token(Special.Unknown, None, loc)
        self.pos += 1  # Get to the next position
        self.loc = Loc.nextColumn(self.loc)

        return Token(Type.Char, char, loc)

    def lex_str(self):
        self.pos += 1   # Skip past that "
        loc = self.loc
        self.loc = Loc.nextColumn(self.loc)
        program = self.program

        string = ""  # A running total
        while self.pos < len(self.program):
            if program[self.pos] == '\\' and program[self.pos + 1] == '"':
                self.pos += 2  # Skip over the \ and "
                self.loc = Loc.moveColumnBy(self.loc, 2)

            if program[self.pos] == '"':  # We've reached the end
                self.pos += 1  # Skip over the " again
                loc = self.loc
                self.loc = Loc.nextColumn(self.loc)
                return Token(Type.String, string, loc)

            string += program[self.pos]  # Append to our running total
            self.pos += 1  # Move over a char
            self.loc = Loc.nextColumn(self.loc)

        self.errorHandler.add("Syntax", "String literal was not closed", loc)
        return Token(Special.Unknown, None, loc)

    def lex_op(self):
        matches = []  # maintain a list of all matches
        _loc = self.loc

        for op in Symbol:
            pos = self.pos
            loc = self.loc
            index = 0

            if index >= len(op.value):  # This is not the operator you are looking for
                continue  # move to the next operator

            # loop through the operator, checking each char
            while index < len(op.value) and pos < len(self.program) and self.program[pos] == op.value[index]:
                pos += 1
                loc = Loc.nextColumn(loc)
                index += 1

            # (len(op.value) - 1) + 1, the length of string, plus the earlier matched portion
            if index == len(op.value):  # The whole string matched, plus the one we matched earlier
                matches.append(Token(op, op.value, _loc))

        if(len(matches) == 0):
            self.errorHandler.add("Syntax", "Symbol "+self.program[self.pos]+" does not exist", self.loc)
            self.pos += 1
            self.loc = Loc.nextColumn(self.loc)
            return Token(Special.Unknown, False, _loc)
        self.pos += len(max(matches, key=len).value)
        self.loc = Loc.moveColumnBy(self.loc, len(max(matches, key=len).value))
        return max(matches, key=len)  # return the match that fit the most

    def maybe_operator(self, char):
        for op in Symbol:
            pos = self.pos
            index = 0

            if index >= len(op.value):  # This is not the operator you are looking for
                continue  # move to the next operator

            # loop through the operator, checking each char
            while index < len(op.value) and pos < len(self.program) and self.program[pos] == op.value[index]:
                pos += 1
                index += 1

            # (len(op.value) - 1) + 1, the length of string, plus the earlier matched portion
            if index == len(op.value):  # The whole string matched, plus the one we matched earlier
                return True
        return False

    def tokenize(self):
        tokens = []
        token = self.get_token()
        tokens.append(token)
        while token.type != Special.EOF:
            token = self.get_token()
            tokens.append(token)
        return tokens
