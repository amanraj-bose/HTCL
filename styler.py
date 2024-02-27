import math
import string
import pickle
import os


"""
# Define Keywords
- start-><uline></uline><-end  => Underline
- <new> => newline
- <bold></bold> => Bold Text
- <backgroumd=color_name></background> => Background Color
- <color=color_name></color> => Font Color

"""


class CryptoMachine(object):
    def __init__(self, lambda_value:float=0.5, *, sentence_seperator:str="-", word_seperator:str="x") -> None:
        super(CryptoMachine, self).__init__()
        self.sentence_seperator = sentence_seperator
        self.word_seperator = word_seperator
        enumerator = string.ascii_letters+string.digits+string.punctuation+"\n"
        self.alpha_to_number = {j:i for i, j in enumerate(enumerator, 1)}
        self.number_to_alpha = {i:j for i, j in enumerate(enumerator, 1)}
        self.lambda_value = lambda_value
    
    def encryptor_mask(self, input_text:str) -> str:
        x = input_text
        y = list()
        for i in x:
            if i == ' ':y.append(f"{self.sentence_seperator}{self.word_seperator}")
            else:y.append(str(self.encryptor(self.alpha_to_number[i])) + self.word_seperator)

        return "".join(y)
    
    def encryptor(self, number:int):
        x = number
        x = (math.log(x) + 2)
        x = x/256
        x = math.pow(x, 1/5) 
        x = x* self.lambda_value
        x = x ** 2
        return x
    
    def decryptor(self, number:float or int):
        x = number
        x = x**0.5
        x = (x/self.lambda_value)**5
        x = (x*256) - 2
        x = round(math.exp(x))
        return x
    
    def decryptor_mask(self, input_text:str) -> str:
        x = input_text.split(self.word_seperator)
        y = list()
        for i in x:
            if i == self.sentence_seperator:
                y.append(" ")
            else:
                if bool(i) is not False:
                    y.append(self.number_to_alpha[int(self.decryptor(float(i)))])
        return "".join(y)
    
    def save_encoded(self, value, filename:os.PathLike or str="encoded.bt") -> str:
        with open(filename+f"-{self.lambda_value}", "wb") as f:
            pickle.dump(str(value), f, protocol=pickle.HIGHEST_PROTOCOL)
        return f"[+] File saved {filename} !!"
    
    def load_encoded(self, filename:os.PathLike or str) -> str:
        with open(filename, "rb") as f:
            x = pickle.load(f)
        return str(x)


class EscapeSequences:
    NEWLINE = "\n"
    TAB = "\t"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    DIMMER = "\033[2m"
    BOLDER = "\033[1m"
    OFF = "\033[0m"
    # Backgroud
    BACKGROUD = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m"
    }

    # ForeGround
    FOREGROUND = {
        "black": "\033[90m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }


class Converter(EscapeSequences):
    def __init__(self) -> None:
        super(Converter, self).__init__()
        self.tags = {
            "<new": self.NEWLINE,
            "\n<new": self.NEWLINE,

            "<uline": self.UNDERLINE,
            "\n<uline": "\n"+self.UNDERLINE,
            "\n <uline": "\n"+self.UNDERLINE,

            "<t": self.TAB,
            "\n<t": "\n"+self.TAB,
            "\n <t": "\n"+self.TAB,

            "<it": self.ITALIC,
            "\n<it": "\n"+self.ITALIC,
            "\n <it": "\n"+self.ITALIC,
            
            "<bold": self.BOLDER,
            "\n<bold": "\n"+self.BOLDER,
            "\n <bold": "\n"+self.BOLDER,

            "<dim": self.DIMMER,
            "\n<dim": "\n"+self.DIMMER,
            "\n <din": "\n"+self.DIMMER,

            "<g": self.OFF,
            "<red": self.FOREGROUND["red"],
            "<green": self.FOREGROUND["green"],
            "<yellow": self.FOREGROUND["yellow"],
            "<cyan": self.FOREGROUND["cyan"],
            "<blue": self.FOREGROUND["blue"],
            "<black": self.FOREGROUND["black"],

            "<highlight": self.BACKGROUD["yellow"],
            "<highlight=green": self.BACKGROUD['green'],
            "<highlight=blue": self.BACKGROUD['blue'],
            "<highlight=cyan": self.BACKGROUD['cyan'],
            "<highlight=red": self.BACKGROUD['red'],
            "<highlight=magenta": self.BACKGROUD['magenta'],
            "<highlight=black": self.BACKGROUD['black'],
            "<highlight=white": self.BACKGROUD['white'],
            "<highlight=yellow": self.BACKGROUD["yellow"],
        }

        self.block = {
            "/uline",
            "/it",
            "/bold",
            "/dim",

            "/red",
            "/green",
            "/yellow",
            "/cyan",
            "/blue",
            "/black",

            "/highlight",
            "/g"
        }
    
    def __put__(self, text:str) -> str:
        x = text.split(">")
        z = []
        for i in x:
            try:z.append(self.tags[i])
            except KeyError:
                l = i.split("<")
                for n in l:
                    if n in self.block:z.append(self.OFF)
                    else:z.append(n)
        return "".join(z)

    def change(self, x):
        return self.__put__(x)

class Renderer(CryptoMachine):
    def __init__(self, lambda_value: float = 0.5, *, sentence_seperator: str = "-", word_seperator: str = "x") -> None:
        super(Renderer, self).__init__(lambda_value, sentence_seperator=sentence_seperator, word_seperator=word_seperator)
        self.converter = Converter()
    
    def render(self, filename:os.PathLike or str):
        x = self.load_encoded(filename)
        x = self.decryptor_mask(x)
        x = self.converter.change(x)

        return x
    
    def writer(self, filename:os.PathLike):
        with open(filename, "r") as f:
            self.save_encoded(self.encryptor_mask(str(f.read())), filename=str(filename).split(".")[0]+".bt")
    
    def compiler(self, filename:os.PathLike):
        self.writer(filename)
        return self.render(str(filename).split(".")[0]+f".bt-{self.lambda_value}")

if __name__ == '__main__':
    value = "<uline><it>How are you ?</it><bold> boys</bold></uline>\n <t><highlight>Aman</highlight><g>---</g><highlight=green>Raj</highlight>"
    c = Converter()
    print(c.change(value))