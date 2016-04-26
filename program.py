import lexer as L
import parser_ as P



def main():
    lexer = L.Lexer("4\n* 5")
    tokens = lexer.tokenize()
    parser = P.Parser(tokens)
    parser.parse()

main()


# Are these still being used??
# def main():
#     # file = open("test", 'r')
#     # lines = file.readlines(file)
#     lines = ["F|int| => |int x| |int y| -> int z = x * y; return z;"]
#     print("Original code: ", lines)
#     lexCommands = []
#     for line in lines:
#         command = ""
#         for ch in line:

#             if (ch == ';' or ch == ':' or ch == ' ' or ch == '|'):
#                 # Delimter, add current command to list
#                 if (command != ''):
#                     lexCommands.append(command)
#                 if (ch == ';' or ch == '|'):
#                     lexCommands.append(ch)
#                 if (command == '=' or command == '-' and ch == '>'):
#                     lexCommands.append(command + ch)
#                 command = ""

#             else:
#                 command += ch
#     print("Seperated commands: ", lexCommands)
#     lexify(lexCommands)


# def lexify(commands):
#     newCommandSet = []
#     lastLexCommand = (" ")
#     for command in commands:
#         lexCommand = ()
#         if (command == "string" or command == "int" or command == "char" or command == "float"):
#             lexCommand = ("DATA", command)
#         elif (command == "|"):
#             lexCommand = ("SEPERATOR", command)
#         elif (command == ";"):
#             lexCommand = ("ENDOFLINE")
#         elif (command == "=>" or command == "->" or command == "+" or
#               command == "-" or command == "*" or command == "/"):
#             lexCommand = ("OPERATOR", command)
#         elif (command == "return" or "end"):
#             lexCommand = ("KEYWORD", command)
#         elif (command.isalnum):
#             if (lastLexCommand[0] == "DATA"):
#                 lexCommand = ("VARIABLE", command)
#             else:
#                 lexCommand = ("ALPHANUM")
#         lastLexCommand = lexCommand
#         newCommandSet.append(lexCommand)
#     print("Made into actual readable commands: ", newCommandSet)