
# for nice output
def indentString(str):
    return "\n".join(" -> "+x for x in str.split("\n"))

# Class to store an error
class Error:
    def __init__(self, typ, message, location):
        self.type = typ             # string
        self.message = message      # string
        self.location = location    # tuple (line, column)

    def __repr__(self):
        out = ""
        out += self.type + ": " + self.location + ", " + self.message
        return out

    def __str__(self):
        out = ""
        out += self.type + " error on line " + str(self.location[0]) + ", column " + str(self.location[1]) + ":\n"
        out += indentString(self.message)
        return out

# Class to store errors
class ErrorHandler:

    def __init__(self):
        self.errors = []

    # Create a new error
    def add(self, typ, message, location):
        self.errors.append(Error(typ, message, location))

    # true if there has been an error, else false
    def __bool__(self):
        return bool(self.errors)

    def __str__(self):
        if len(self.errors) != 1:
            out = str(len(self.errors)) + " ERRORS HAVE OCCURRED:\n\n"
        else:
            out = str(len(self.errors)) + " ERROR HAS OCCURRED:\n\n"
        for error in self.errors:
            out += str(error) + "\n\n"
        out = out[:-2]
        return out

    def __repr__(self):
        return str(self.errors)