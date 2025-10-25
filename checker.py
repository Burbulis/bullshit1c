import re


def readfile(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()
    return lines


def quantification(text):
    ret = re.search('(?i)([а-яА-Я])', text, 0)
    return ret


def argquantification(regex,text):
    ret = re.search(regex, text, 0)
    # '\((.*)\)', text, 0)
    return ret

def procAndFuncDetector(lines,token_start,token_end):
    ret = {}
    issignature = False
    isbody = False
    body = []
    _name = ""
    args_list = []
    for line in lines:
        qq = quantification(line)
        if qq is not None:
            line = qq.string
            if -1 != line.find(token_start):
                issignature = True
            if -1 != line.find(token_end):
#                print("************************************")
#                print("Имя: :" + _name);
                ret[_name] = (args_list,body)
                isbody = False

            #Нормальное форматирование кода
            g = argquantification('([А-Яа-я]+)\\s+([А-Яа-я]+)\\s*\\((.*)\\)',line)
            if g is not None and issignature:
                pos = g.group(1).find(token_start);
                if -1 != pos:
                    _name = g.group(2)
                    args_list = g.group(3).split(',')
#                    print("Вывод[имя]:"+ _name)
                    issignature = False
                    isbody= True
                    continue
            #к нам пришли киберпанки и кибергопники?
            g = argquantification('([А-Яа-я]+)\\s*\\((.*)\\)', line)
            if g is not None and issignature:
                _name = g.group(1)
                args_list = g.group(2).split(',')
                issignature = False
                isbody = True
                continue
            if isbody:
                 body.append(line)
    return ret

def ShowData(vals):
   for val in vals:
       print(val)


lines = readfile("dumbcode.1c")
ret = procAndFuncDetector(lines,"Функция","КонецФункции")
ARG_NAMES = 0;
BODY = 1;
desc = ret["Фуфлограмма"]
print("**Аргументы**")
ShowData( desc[ARG_NAMES] )
print("**Тело функции**:")
ShowData( desc[BODY] )
print("************************************************************************")
print("* Следующая функция")
print("************************************************************************")
desc = ret["ПредварительнаяПроверкаНомера"]
print("**Аргументы**")
ShowData( desc[ARG_NAMES] )
print("**Тело функции**:")
ShowData( desc[BODY] )

ret = procAndFuncDetector(lines,"Процедура","КонецПроцедуры")
desc = ret["ПриСозданииНаСервере"]
print("**Аргументы**")
ShowData( desc[ARG_NAMES] )
print("**Тело процедуры**:")
ShowData( desc[BODY] )

