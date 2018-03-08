from abc import ABC, abstractmethod
import math

class Operation:
    former = None
    after = None
    
    def __merge(self):
        f=None
        a=None
        if self.former and self.former.former:
            f = self.former.former
            self.former.former.after = self
            pass
        if self.after and self.after.after:
            a = self.after.after
            self.after.after.former = self
            pass
        self.former = f
        self.after = a
        pass

    def load(self, string):
        pass

    @abstractmethod
    def calculate(self):
        pass
    pass

class TwoSided(Operation):
    def calculate(self):
        self.value = self.postCalc(self.former.value, self.after.value)
        self._Operation__merge()
        return self.value

    @abstractmethod
    def postCalc(self, a, b):
        pass

class Number(Operation):
    def __init__(self, string):
        self.value = float(string)
        pass

    def calculate(self):
        return self.value
    pass

class Var(Number):
    def __init__(self, var):
        self.value = var
        pass

class Add(Operation):
    def calculate(self):
        if not type(self.former) is Number:
            self.value = self.after.value
            pass
        else:
            self.value = self.former.value+self.after.value
            pass
        self._Operation__merge()
        return self.value
    pass

class Minus(Operation):
    def calculate(self):
        if not type(self.former) is Number:
            self.value = -self.after.value
            pass
        else:
            self.value = self.former.value-self.after.value
            pass
        self._Operation__merge()
        return self.value
    pass

class Multiply(TwoSided):
    def postCalc(self, a, b):
        return a*b
    pass

class Divide(TwoSided):
    def postCalc(self, a, b):
        return a/b
    pass

class Power(TwoSided):
    def postCalc(self, a, b):
        return a**b
    pass

class OpGroup(Operation):
    def __init__(self, string):
        self.first = fullElems(string)[0]
        pass
    
    def calculate(self):
        if self.first.after:
            for opClasses in exeOrder:
                for op in iterate(self.first):
                    if isinstance(op, opClasses):
                        val = op.calculate()
                        pass
                    pass
                pass
            pass
        else:
            val = self.first.calculate()
            pass
        self.value = self.postCalc(val)
        return self.value

    def postCalc(self, a):
        return a
    pass

class Sin(OpGroup):
    def postCalc(self, a):
        return math.sin(a)
    pass

class Cos(OpGroup):
    def postCalc(self, a):
        return math.cos(a)
    pass

class Tan(OpGroup):
    def postCalc(self, a):
        return math.tan(a)
    pass

class Log(OpGroup):
    def postCalc(self, a):
        return math.log10(a)
    pass

class Ln(OpGroup):
    def postCalc(self, a):
        return math.log(a)

def calculate(string):
    print(OpGroup(string).calculate())
    pass

exeOrder = (
    (OpGroup,),
    (Power,),
    (Multiply, Divide),
    (Add, Minus)
    )

str2op = {
    "+" : Add,
    "-" : Minus,
    "*" : Multiply,
    "/" : Divide,
    "^" : Power
    }

str2group = {
    "(" : OpGroup,
    "sin(" : Sin,
    "cos(" : Cos,
    "tan(" : Tan,
    "log(" : Log,
    "ln(" : Ln
    }

str2var = {
    "pi" : math.pi,
    "e" : math.e
    }

numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.')

def elems(string):
    isGroup = False
    isNumber = False
    builder = ""
    for i in range(len(string)):
        char = string[i]
        if isGroup:
            if char is ')':
                isGroup = False
                yield group(builder)
                builder = ""
                continue
            builder += char
            continue
        elif isNumber:
            if not (char is 'e' or string[i-1] is 'e') and char not in numbers:
                isNumber = False
                yield Number(builder)
                builder = ""
                builder += char
                continue
            pass

        if builder in str2op:
            yield str2op[builder]()
            builder = ""
            pass
        elif builder in str2group:
            isGroup = True
            group = str2group[builder]
            builder = ""
            pass
        elif builder in str2var:
            yield Var(str2var[builder])
            builder = ""
            pass
        if char in numbers:
            isNumber = True
            pass
        builder += char
        pass
    if isNumber and builder is not "":
        yield Number(builder)
        pass
    elif builder in str2var:
        yield Var(str2var[builder])
        pass
    pass

def fullElems(string):
    former=None
    l=[]
    for e in elems(string):
        e.former = former
        if former:
            former.after = e
            pass
        former = e
        l.append(e)
        pass
    return l

def iterate(first):
    current = first
    yield current
    while (current.after is not None):
        current = current.after
        yield current
        pass
    pass

while(True):
    calculate(input())
    pass

#main("31+3*23/45")
#og=OpGroup(input())
#print(og.calculate())
