from math import *
from decimal import Decimal
import urllib
from urllib.request import urlopen
from xml.etree.ElementTree import parse

def xmlurl( inunit, outunit):
    try:
        var_url = urlopen('https://'+inunit+'.fxexchangerate.com/rss.xml')
    except urllib.error.HTTPError:
        return 'Input Unit is Invalid!'
    xmldoc = parse(var_url)
    for item in xmldoc.iterfind('channel/item'):
        if outunit.upper() in item.findtext('title'):
            exrate = item.findtext('description').split()
            return Decimal(exrate[exrate.index('=')+1])

    return 'Output Unit is Invalid!'

class Matrix():
    def inverse(value):
        try:
            inverse = []

            for x in range(len(value)):
                row = []
                for y in range(len(value[x])): 
                    if x==y:
                        row.append(1.0)
                    else:
                        row.append(0.0)
                inverse.append(row)

            def convert_to_zero(val,inval):

                zero_val = list(val)
                inv_val  = list(inval)
                for p in range(len(val)):

                    val[p] = Decimal(eval(str(zero_val[p]-(zero_val[index_y]*value[index_x][p]))))
                    inval[p] = Decimal(eval(str(inv_val[p]-(zero_val[index_y]*inverse[index_x][p]))))
                    
                    
            for index_x,x in enumerate(value):
                for index_y,y in enumerate(x):
                    value[index_x][index_y] = Decimal(str(y))
                    inverse[index_x][index_y] = Decimal(str(inverse[index_x][index_y]))
            for index_x,x in enumerate(value):
                for index_y,y in enumerate(x):

                    if index_x == index_y:

                        for z in range(-1,-(1+len(x)),-1):

                            value[index_x][z] = Decimal(eval(str(Decimal(str(value[index_x][z])) / Decimal(str(y)))))
                            inverse[index_x][z] = Decimal(eval(str(Decimal(str(inverse[index_x][z]))/ Decimal(str(y)))))
                            
                        for t in range(len(x)):
                            if t != index_x:
                            
                                convert_to_zero(value[t],inverse[t])
                                
                                
            for x in range(len(value)):
                for y in range(len(value[x])):
                
                    value[x][y] = round(eval(str(value[x][y])),5)
                    inverse[x][y] = round(eval(str(inverse[x][y])),5)

            return inverse
        
        except:
                return "Inverse not possible"
            
    def transpose(value):

        transpose = []

        for x in range(len(value[0])):
            t_row = []
            
            for y in range(len(value)):
                t_row.append(value[y][x])
                
            transpose.append(t_row)
            
        return transpose

    def solve(value1, value2, operator):

        result = []

        if operator in ('+','-'):
            if len(value1) == len(value2) and len(value1[0]) == len(value2[0]):

                for index_x,x in enumerate(value1):
                    result_row = []
                    
                    for index_y,y in enumerate(x):
                        result_row.append(eval(str(y)+operator+str(value2[index_x][index_y])))

                    result.append(result_row)
                    
                return result
            
            else:
                return 'Matricies must be of the same dimensions!'
            
        elif operator == '*':
            if len(value1) == len(value2[0]):
                
                for i in range(len(value1)):
                    result_row = []
                    for x in range(len(value1)):
                        value = ''
                        
                        for y in range(len(value2)):
                            value+=(str(value1[i][index_y])+operator+str(value2[index_y][index_x])+'+')

                        result_row.append(eval(value.rstrip('+')))
                    result.append(result_row)
                        
                return result
            else:
                return 'Number of rows of first Matrix should be equal to number of columns in the second!'


class Basic():
    def fac_solve(self, expression):
        for x in ('+','-','/','*','**'):
            expression = expression.replace(x,' {} '.format(x))
        expression = expression.split()

        for x_index,x in enumerate(expression):
            if '!' in x:
                if x[-1] == '!':
                    expression[x_index] = "factorial({})".format(x.replace('!',''))
                else:
                    return "symbol error"
        
        if 'factorial()' in expression:
            return "empty error"
        else:
            return str(''.join(expression))
    def par_solve(self, expression):
        for x_index,x in enumerate(expression):
            if 'list' in str(type(x)):
                try:
                    expression[x_index] = str(eval(''.join(x)))
                except ValueError:
                    expression = "Domain error"
                if expression[x_index-1][-3:] in ('sin', 'cos', 'tan','sec', 'cot'):
                    if expression[x_index-1][-4:] in ('asin', 'acos', 'atan','asec', 'acot'):
                        expression[x_index] = eval('["'+expression[x_index-1][-4:]+'('+expression[x_index]+')'+'"]')
                        expression.insert(x_index-1,expression[x_index-1][:-4])
                    else:
                        expression[x_index] = eval('["'+expression[x_index-1][-3:]+self.unit+'('+expression[x_index]+')'+self.unit_end+'"]')
                        expression.insert(x_index-1,expression[x_index-1][:-3])
                    expression.remove(expression[x_index])
                    trig = self.par_solve(self, expression)
                    if trig == "Domain error":
                        return trig
                elif 'factorial' in expression[x_index-1]:
                    expression[x_index] = eval('["factorial('+expression[x_index]+')"]')
                    expression.insert(x_index-1,expression[x_index-1][:-9])
                    expression.remove(expression[x_index])
                    self.par_solve(self, expression)
        return expression

    def solve(self, expression):
        
        if expression.count('(')>1:
            expression = expression.replace('(',' (')
            expression = expression.replace(')',') ')
            expression = expression.split()

        for x_index,x in enumerate(expression):
            if '(' in x and ')' in x:
                expression[x_index] = x.split()

        if len(expression)!=1:
            solution = self.par_solve(self, expression)
            
            if solution == "Domain error":
                return solution
        try:
            expression = str(eval(''.join(expression)))
        except ZeroDivisionError:
            expression = "Can't divide by zero!"
        return(expression)
    
    def __new__(cls, expression, radians_var, base):

        for x in ('sin¯', 'cos¯', 'tan¯','sec¯', 'cosec¯', 'cot¯'):
            expression = expression.replace(x, 'a'+x[:-1])
            
        expression = expression.replace('π','pi')
        
        if '!' in expression:
            expression = cls.fac_solve(cls, expression)
            if expression == 'symbol error':
                return 'Symbol placed incorrectly'
            elif expression == 'empty error':
                return 'Factorial of nothing?'
        
        if expression.count('(')!=expression.count(')'):
            return 'Brackets mismatched!'
        
        if '()' in expression:
            return "There's an empty bracket!"
         
        expression = '('+expression+')'
        for x,y in zip(('^','÷','x'),('**','/','*')):
            expression = expression.replace(x,y)

        if not radians_var:
            cls.unit = ''
            cls.unit_end = ''
        else:
            cls.unit = '(radians'
            cls.unit_end = ')'
            
        for x in range(expression.count('(')):
            solution = cls.solve(cls,expression)
            expression = solution
        
        try:
            return str(round(eval(expression),7))
        except SyntaxError:
            if expression == 'Domain error':
                return ("Domain's not right")
            else:
                return('Wrong Expression')
        except TypeError:
            return("There should be something to operate on!")
        except OverflowError:
            return("Too much for me!")
        
class Convert():

    def time(value,inunit,outunit):
        if inunit == outunit:
            return value

        elif inunit == "hr":
            if outunit == "min":
                return eval(value)*60
            elif outunit == "sec":
                return eval(value)*3600
            elif outunit == "msec":
                return eval(value)*60*60*1000

        elif inunit == "min":
            if outunit == "sec":
                return eval(value)*60
            elif outunit == "msec":
                return eval(value)*60*1000

        elif inunit == "sec":
            if outunit == "msec":
                return eval(value)*1000

    def speed(value,inunit,outunit):
        if inunit == outunit:
            return value

        elif inunit == "m/s":
            if outunit == "km/hr":
                return eval(value)*18/5
            elif outunit == "mph":
                return eval(value)*3600/1609.34

        elif inunit == "km/hr":
            if outunit == "m/s":
                return eval(value)*5/18
            elif outunit == "mph":
                return eval(value)*0.6214

        elif inunit == "mph":
            if outunit == "km/hr":
                return eval(value)*1.60934
            elif outunit == "m/s":
                return eval(value)*0.44704

    def energy(value,inunit,outunit):
        if inunit == outunit:
            return value

        elif inunit == "joule":
            if outunit == "kilojoule":
                return eval(value)*0.001
            elif outunit == "kilocalorie":
                return eval(value)*0.00024

        elif inunit == "kilojoule":
            if outunit == "kilocalorie":
                return eval(value)*0.24
            elif outunit == "joule":
                return eval(value)*1000

        elif inunit == "kilocalorie":
            if outunit == "joule":
                return eval(value)*4184
            elif outuit == "kilojoule":
                return eval(value)*4.184

    def area(value,inunit,outunit):
        if inunit == outunit:
            return value

        elif inunit == "sqkm":
            if outunit == "sqcm":
                return eval(value)*10**(10)
            elif outunit == "sqm":
                return eval(value)*10**(6)
            elif outunit == "sqmm":
                return eval(value)*10**(12)
            elif outunit == "sqft":
                return eval(value)*1.076*10**(7)
            elif outunit == "sqin":
                return eval(value)*1.55*10**(9)

        elif inunit == "sqcm":
            if outunit == "sqkm":
                return eval(value)*10**(-10)
            elif outunit == "sqm":
                return eval(value)*10**(-4)
            elif outunit == "sqmm":
                return eval(value)*100
            elif outunit == "sqft":
                return eval(value)*0.0010764
            elif outunit == "sqin":
                return eval(value)*0.155

        elif inunit == "sqm":
            if outunit == "sqkm":
                return eval(value)*10**(-6)
            elif outunit == "sqcm":
                return eval(value)*10000
            elif outunit == "sqmm":
                return eval(value)*10**(6)
            elif outunit == "sqft":
                return eval(value)*10.764
            elif outunit == "sqin":
                return eval(value)*1550

        elif inunit == "sqmm":
            if outunit == "sqkm":
                return eval(value)*10**(-12)
            elif outunit == "sqcm":
                return eval(value)*0.01
            elif outunit == "sqm":
                return eval(value)*10**(-6)
            elif outunit == "sqft":
                return eval(value)*1.0764*10**(-5)
            elif outunit == "sqin":
                return eval(value)*0.00155

        elif inunit == "sqft":
            if outunit == "sqkm":
                return eval(value)*9.3*10**(-8)
            elif outunit == "sqcm":
                return eval(value)*929.03
            elif outunit == "sqm":
                return eval(value)*0.0924
            elif outunit == "sqmm":
                return eval(value)*92903
            elif outunit == "sqin":
                return eval(value)*144

        elif inunit == "sqin":
            if outunit == "sqkm":
                return eval(value)*6.45*10**(-10)
            elif outunit == "sqcm":
                return eval(value)*6.45
            elif outunit == "sqm":
                return eval(value)*0.000645
            elif outunit == "sqmm":
                return eval(value)*645.16
            elif outunit == "sqft":
                return eval(value)*0.0065
 
    def length(value,inunit,outunit):

        if inunit == 'cm':

            if outunit == 'm':
                return eval(value)*10**(-2)
            if outunit == 'mm':
                return eval(value)*10**(1)
            if outunit == 'km':
                return eval(value)*100000
            if outunit == 'um':
                return eval(value)*10000
            if outunit == 'nm':
                return eval(value)*10000000
            if outunit == 'foot':
                return eval(value)/30.48
            if outunit == 'mile':
                return eval(value)/160934
            elif outunit == 'inch':
                return eval(value)/2.54

        elif inunit == 'm':

            if outunit == 'cm':
                return eval(value)*10**(2)
            if outunit == 'mm':
                return eval(value)*10**(3)
            if outunit == 'km':
                return eval(value)/1000
            if outunit == 'um':
                return eval(value)*1000000
            if outunit == 'nm':
                return eval(value)*1000000000
            if outunit == 'foot':
                return eval(value)*3.281
            if outunit == 'miles':
                return eval(value)/1609
            elif outunit == 'inch':
                return eval(value)*39.37
        
        elif inunit == 'mm':

            if outunit == 'm':
                return eval(value)/1000
            if outunit == 'cm':
                return eval(value)/10
            if ontunit == 'km':
                return eval(value)/1000000
            if outunit == 'um':
                return eval(value)*1000
            if outunit == 'nm':
                return eval(value)*1000000
            if outunit == 'foot':
                return eval(value)/305
            if outunit == 'mile':
                return eval(value)/1.609000
            elif outunit =='inch':
                return eval(value)/25.4

        elif inunit == 'km':

            if outunit == 'm':
                return eval(value)*1000
            if outunit == 'cm':
                return eval(value)*100000
            if outunit == 'um':
                return eval(value)*1000000000
            if outunit == 'mm':
                return eval(value)*1000000
            if outunit == 'nm':
                return eval(value)*1000000000000
            if outunit == 'foot':
                return eval(value)*3281
            if outunit == 'mile':
                return eval(value)/1.609
            elif outunit == 'inch':
                return eval(value)*39370

        elif inunit == 'um':

            if outunit == 'm':
                return eval(value)/1000000
            if outunit == 'cm':
                return eval(value)/10000
            if outunit == 'km':
                return eval(value)/1000000000
            if outunit == 'mm':
                return eval(value)/1000
            if outunit == 'nm':
                return eval(value)*1000
            if outunit == 'foot':
                return eval(value)/304800
            if outunit == 'mile':
                return eval(value)/1609000000
            elif outunit == 'inch':
                 return eval(value)/25400

        elif inunit == 'nm':

            if outunit == 'm':
                return eval(value)/1000000000
            if outunit == 'cm':
                return eval(value)/10000000
            if outunit == 'km':
                return eval(value)/1000000000000
            if outunit == 'mm':
                return eval(value)/1000000
            if outunit == 'um':
                return eval(value)/1000
            if outunit == 'foot':
                return eval (value)/304800000
            if outunit == 'mille':
                return eval(value)/1609344000000
            elif outunit == 'inch':
                 return eval(value)/25400000

        elif inunit == 'inch':

            if outunit == 'm':
                return eval(value)/39.37
            if outunit == 'cm':
                return eval(value)*2.54
            if outunit == 'km':
                return eval(value)/39370
            if outunit == 'nm':
                return eval(value)*25400000
            if outunit =='mm':
                return (value)*25.4
            if outuint == 'foot':
                return eval(value)/12
            if outunit == 'mile':
                return eval(value)/63360
            elif outunit == 'um':
                return eval(value)*25400

        elif inunit == 'foot':

            if outunit == 'm':
                return eval(value)/3.281
            if outunit == 'cm':
                return eval(value)*30.48
            if outunit == 'mm':
                return eval(value)*305
            if outunit == 'km':
                return eval (value)/3281
            if outunit == 'nm':
                return eval(value)*304800000
            if outunit == 'um':
                return eval(value)*304800
            if outunit == 'inch':
                return eval(value)*12
            if outunit == 'mile':
                return eval(value)/5280

        elif inunit == 'mile':

            if outunit == 'm':
                return eval(value)*1609.34
            if outunit == 'cm':
                return eval(value)*1609.34
            if outunit == 'km':
                return eval(value)*1.60934
            if outunit == 'um':
                return eval(value)*1609000000
            if outunit == 'nm':
                return eval(value)*1609344000000
            if outunit == 'inch':
                return eval(value)*63360
            if outunit == 'foot':
                return eval(value)*5280
            if outunit == 'mm':
                return eval(value)*1609000

    def currency(value,inunit,outunit):
        value = Decimal(value)
        if inunit != outunit:
            rate = xmlurl(inunit,outunit)
            try:
                value *= rate
                return str(value).split("'")[0]
            except TypeError:
                return rate
        else:
            return value
    def temperature(value,inunit,outunit):
     if inunit == outunit:
         return value

     elif inunit == 'cel':

         if outunit == 'fhr':
             return eval(value)*9/5+32
         if outunit == 'kel':
             return eval(value)+273.15

     elif inunit == 'fhr':

         if outunit == 'cel':
             return eval(value)-32*5/9
         if outunit == 'kel':
             return eval(value)-32*5/9+273.15

     elif inunit == 'kel':

         if outunit == 'cel':
             return eval(value)-273.15
         if outunit == 'fhr':
             return eval(value)-273.15*9/5+32