class Mips(object):
    """ Mips
    A utility class that makes writing mips assembly commands simpler
    """

    def __init__(self, file="a.s"):
        self.file = file
        self.program = open(file, mode="w")

    def write(self, text, newline=True):
        """ write
        Most basic interaction with the Mips file.
        The user can use it, but they shouldn't.
        """
        self.program.write("{}{}".format(text, ("\n" if newline else " ")))

    def function(self, name, globl=True):
        if globl:
            self.write(".globl {}".format(name))
        self.write(name + ":")

    def addi(self, register, register2, value, isfloat=False):
        self.write("addi{} ${}, ${}, {}".format(
            ".s" if isfloat else "",
            register, register2, value
        ))

    def add(self, register, register2, register3, isfloat=False):
        self.write("add{} ${}, ${}, ${}".format(
            ".s" if isfloat else "",
            register, register2, register3
        ))

    def save_word(self, register, offset, register2):
        self.write("sw ${}, {}(${})".format(register, offset, register2))

    def load_imm(self, register, value, isfloat=False):
        self.write("li{} ${}, {}".format(
            ".s" if isfloat else "",
            register, value
        ))

    def load_word(self, register, offset, register2):
        self.write("lw ${}, {}(${})".format(register, offset, register2))

    def syscall(self):
        self.write("syscall")

    def comment(self, text):
        self.write("# {}".format(text))
