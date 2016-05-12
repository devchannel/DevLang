from tokens import Special

class Result():
    def __init__(self, value, loc=(-1, -1), error="", errorRank=1):
        self.value = value
        self.error = error
        self.location = loc
        self.errorRank = errorRank

    def __bool__(self):
        return self.value != None

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        # if self.location[0] < other.location[0]:
        #     return True
        # elif self.location[0] == other.location[0] and self.location[1] < other.location[1]:
        #     return True
        # return False
        return self.errorRank < other.errorRank

    def __gt__(self, other):
        # if self.location[0] > other.location[0]:
        #     return True
        # elif self.location[0] == other.location[0] and self.location[1] > other.location[1]:
        #     return True
        # return False
        return self.errorRank > other.errorRank

# Basic parser class
class Parser:
    # Will be overridden by subclasses
    def run(self, token_list):
        return None

    # called by + operator
    def __add__(self, other):
        return Concatenate(self, other)

    # called by * operator
    def __mul__(self, other):
        return Error(self, other)

    # called by | operator
    def __or__(self, other):
        return Alternate(self, other)

    # called by ^ operator
    def __xor__(self, function):
        return Process(self, function)


class Default(Parser):
    def __init__(self, val):
        self.val = val

    def run(self, token_list):
        return Result(self.val)


class Tag(Parser):
    def __init__(self, token_type):
        self.token_type = token_type

    def run(self, token_list):
        if token_list.peek().type == self.token_type:
            tk = token_list.next()
            return Result(tk.value, tk.loc)
        return Result(None, token_list.peek().loc)

    def __str__(self):
        return "Tag("+str(self.token_type)+")"


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def run(self, token_list):
        pos = token_list.pos
        left_result = self.left.run(token_list)
        if left_result:
            return left_result
        else:
            token_list.pos = pos
            right_result = self.right.run(token_list)
            if right_result:
                return right_result
            else:
                # print(left_result.errorRank, self.left, "\n|||", right_result.errorRank, self.right, "\n")
                # if right_result.errorRank > left_result.errorRank:
                #     return right_result
                e = ""
                if left_result.error and right_result.error:
                    e = left_result.error+" or "+right_result.error
                elif left_result.error:
                    e = left_result.error
                elif right_result.error:
                    e = right_result.error
                return Result(None, right_result.location, e, right_result.errorRank)

    def __str__(self):
        return str(self.left)+" | "+str(self.right)

# Returns a tuple of the results of two parsers
# return None if either parser fails
# does not advance the tokenlist on failure
class Concatenate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def run(self, token_list):
        left_result = self.left.run(token_list)
        if left_result:
            right_result = self.right.run(token_list)
            if right_result:
                return Result(self.vals_to_tuple(left_result.value, right_result.value), errorRank=left_result.errorRank+right_result.errorRank)
            return Result(right_result.value, right_result.location, right_result.error, right_result.errorRank)
        return left_result

    def vals_to_tuple(self,left,right):
        if type(left) is tuple:
            return left + (right,)
        else:
            return (left, right)

    def __str__(self):
        return str(self.left)+" + "+str(self.right)

class Repeat(Parser):
    def __init__(self, parser):
        self.parser = parser

    def run(self, token_list):
        results = []
        pos = token_list.pos
        count = 0
        result = self.parser.run(token_list)
        while result:
            count += result.errorRank
            results.append(result)
            pos = token_list.pos
            result = self.parser.run(token_list)

        token_list.pos = pos
        if len(results) == 0:
            return result
        r = Result(results, results[-1].location, result.error, count)
        return r

class RepeatUntil(Parser):
    def __init__(self, parser, endParser):
        self.parser = parser
        self.endParser = endParser

    def run(self, token_list):
        results = []
        pos = token_list.pos
        count = 0
        result = self.parser.run(token_list)
        while result:
            count += result.errorRank
            results.append(result)
            pos = token_list.pos
            if self.endParser.run(token_list.copy()):
                break
            result = self.parser.run(token_list)

        token_list.pos = pos
        if len(results) == 0:
            return result
        endResult = self.endParser.run(token_list)
        if not endResult:
            return Result(None, result.location, result.error, count)
        return Result(results, results[-1].location, result.error, count)

class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def run(self, token_list):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser.run(token_list)


class Process(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def run(self, token_list):
        result = self.parser.run(token_list)
        if result:
            result.value = self.func(result.value)
            return result
        return result

    def __str__(self):
        return str(self.parser)+" ^ "+self.func.__name__


# figure out how to get location - add to result class?
class Error(Parser):
    def __init__(self, parser, errorMessage):
        self.parser = parser
        self.message = errorMessage

    def run(self, token_list):
        result = self.parser.run(token_list)
        if result.error:
            result.error = self.message + "\n" + result.error
        else:
            result.error = self.message
        return result

    def __str__(self):
        return str(self.parser)+" * "+self.message

# make sure the entire file is read
class All(Parser):
    def __init__(self, parser):
        self.parser = parser

    def run(self, token_list):
        result = self.parser.run(token_list)
        e = Tag(Special.EOF).run(token_list)
        if e:
            return result
        return Result(None, e.location, result.error)