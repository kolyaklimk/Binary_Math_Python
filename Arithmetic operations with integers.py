import re


# двоичное в десятичное
def decimal(a):
    buf = 0
    minus = 1
    if a[0] == '1':
        minus = -1
        a = '0' + a[1:]
    for i in range(len(a)):
        buf += int(a[len(a) - 1 - i]) * int(pow(2, i))
    return buf * minus


# ввод
def input_num(num):
    while True:
        a = str(input('x' + str(num) + ': '))
        try:
            if (-32768 < int(a) < 32768) and re.search("^[0-9,-]+$", a):
                break
            else:
                print('Error')
        except:
            print('Error')
    if int(a) >= 0:
        code = bin(int(a))[2:]
        code = '0' * (16 - (len(code))) + code
    else:
        code = bin(int(a))[3:]
        code = '1' + '0' * (15 - (len(code))) + code
    return code


# сумма
def sum(a, b, of):
    buf = 0
    rez = ""
    for i in range(len(a) - 1, -1, -1):
        if int(a[i]) + int(b[i]) + buf > 1:
            rez += str((int(a[i]) + int(b[i]) + buf) % 2)
            buf = 1
        else:
            rez += str(int(a[i]) + int(b[i]) + buf)
            buf = 0
    rez = rez[::-1]
    if (a[0] == b[0]) and (a[0] != rez[0]):
        if of:
            return 'OverFlow'
    return rez


# Отрицание
def negation(x):
    buf = ""
    for i in range(len(x)):
        if x[i] == '1':
            buf += '0'
        else:
            buf += '1'

    return sum(buf, '0' * (len(buf) - 1) + '1', True)


# дополнительный код
def additional_code(x):
    if x[0] == '0':
        return x
    buf = "1"
    for i in range(1, len(x)):
        if x[i] == '1':
            buf += '0'
        else:
            buf += '1'

    return sum(buf, '0' * (len(buf) - 1) + '1', True)


# отрицание
def subtraction(a, b, of):
    b = negation(b)
    if of:
        print('Отрицание x2:', b, '\n')
        print('Вычитание:')
        print('+', a)
        print(' ', b)
        print('-' * 18)
    return sum(a, b, of)


# перевод из 16 в 32 разряда доп код
def _16_to_32_additional_code(x):
    if x[0] == '1':
        return '1' * 16 + x
    return '0' * 16 + x


# умножение
def multiplication(x1_, x2_):
    print('16 бит в 32:')
    m = _16_to_32_additional_code(x1_)
    a = '0' * 32
    q = _16_to_32_additional_code(x2_)
    q_1 = '0'
    print('x1:', m)
    print('x2:', q, '\n')
    print('Исходное состояние:')
    print('A:', a)
    print('Q:', q)
    print('Q-1:', q_1)
    print('M:', m, '\n')
    print('      A                                Q                                Q-1')
    for i in range(32):
        if q[-1] + q_1 == '01':
            a = sum(a, m, False)
            print('А=А+М', a, q, q_1)
        elif q[-1] + q_1 == '10':
            a = subtraction(a, m, False)
            print('А=А-М', a, q, q_1)
        q_1 = q[-1]
        q = a[-1] + q[:-1]
        a = a[0] + a[:-1]
        print('Сдвиг', a, q, q_1)
    return q


# деление
def division(x1_, x2_):
    m = _16_to_32_additional_code(x2_)
    q = _16_to_32_additional_code(x1_)

    if q[0] == '1':
        a = '1' * 32
    else:
        a = '0' * 32

    print('16 бит в 32:')
    print('x1:', q)
    print('x2:', m, '\n')
    print('Исходное состояние:')
    print('A:', a)
    print('Q:', q)
    print('M:', m, '\n')
    print('               A                                Q')

    for i in range(32):
        a = a[1:] + q[0]
        q = q[1:] + '0'
        print('сдвиг         ', a, q)

        buf_a = a
        if m[0] == a[0]:
            a = subtraction(a, m, False)
            print('вычитание     ', a, q)
        else:
            a = sum(a, m, False)
            print('сложение      ', a, q)

        if (a[0] == buf_a[0]) or (a == '0' * 32 == q):
            q = q[:-1] + '1'
            print('q0            ', a, q)
        else:
            a = buf_a
            q = q[:-1] + '0'
            print('восстановление', a, q)

    if x1_[0] == x2_[0]:
        return q, negation(a) if x1_[0] == '1' else a
    return negation(q), negation(a) if x1_[0] == '1' else a


x1 = input_num(1)
x2 = input_num(2)
print('=' * 85, '\n')
print('Прямой код:')
print('x1:', x1)
print('x2:', x2)

x1_additional = additional_code(x1)
x2_additional = additional_code(x2)
print('=' * 85, '\n')
print('Дополнительный код:')
print('x1:', x1_additional)
print('x2:', x2_additional)

# Сложение
summa = sum(x1_additional, x2_additional, True)
print('=' * 85, '\n')
print('Сумма:')
print('+', x1_additional)
print(' ', x2_additional)
print('-' * 18)
print(' ', summa)
if summa != 'OverFlow':
    print('\nПрямой код:', additional_code(summa))
    print('Ответ:', decimal(additional_code(summa)))

# вычитание
print('=' * 85, '\n')
sub = subtraction(x1_additional, x2_additional, True)
print(' ', sub)
if sub != 'OverFlow':
    print('\nПрямой код:', additional_code(sub))
    print('Ответ:', decimal(additional_code(sub)))

# Умножение
print('=' * 85, '\n')
print('Умножение:')
if int(x1) == 0 or int(x2) == 0:
    print('Ответ: 0')
else:
    mult = multiplication(x1_additional, x2_additional)
    print('\nПрямой код:', additional_code(mult))
    print('Ответ:', decimal(additional_code(mult)))

# Деление
print('=' * 85, '\n')
print('Деление:')
if int(x2) == 0:
    print('Ответ: OverFlow')
else:
    div, remainder = division(x1_additional, x2_additional)
    print('\nПрямой код:', additional_code(div), 'остаток', additional_code(remainder))
    print('Ответ:', decimal(additional_code(div)), 'остаток', decimal(additional_code(remainder)))
