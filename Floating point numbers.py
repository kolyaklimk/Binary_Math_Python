import re
import math

P = 11
M = 52
A = 20


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

    return sum_fix(buf, '0' * (len(buf) - 1) + '1', True)


# двоичное в десятичное
def decimal(a):
    buf = 0
    minus = 1
    if a[0] == '1':
        minus = -1
        a = '0' + a[1:]
    for i in range(len(a)):
        buf += float(a[len(a) - 1 - i]) * float(pow(2, i))
    return buf * minus


# сумма
def sum_fix(a, b, of):
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
    return sum_fix(buf, '0' * (len(buf) - 1) + '1', False)


# вычитание
def subtraction(a, b, of):
    b = negation(b)
    return sum_fix(a, b, of)


# значение после запятой в двоичную систему
def afterdot_to_bun(a):
    buf = ""
    a = '0.' + a
    for i in range(A):
        a = float(a) * 2.0
        if float(a) < 1.0:
            buf += '0'
        else:
            buf += '1'
            a = '0' + str(a)[1:]
    if int(buf) != 0:
        for i in range(A - 1, -1, -1):
            if buf[i] == '0':
                buf = buf[:i]
            else:
                break
    return buf


# ввод
def input_num(num):
    while True:
        a = str(input('x' + str(num) + ': '))
        x1_inp = a
        try:
            if -pow(2, M - A) + 1 < float(a) < pow(2, M - A) - 1:
                break
            else:
                print('Error')
        except Exception as e:
            print(e)

    minus = '0'

    if a[0] == '-':
        minus = '1'
        a = a[1:]

    befordot = bin(math.floor(float(a)))[2:]
    afterdot = afterdot_to_bun(a[len(str(math.floor(float(a)))) + 1:])
    print('x' + num + ': 10-е в 2-е:', a, '=', befordot + '.' + afterdot)

    # если меньше 1
    buf_p = 0
    new_p = bin(0)[2:]
    if int(befordot) == 0 and int(afterdot) != 0:
        for i in range(len(afterdot)):
            if afterdot[0] == '0':
                afterdot = afterdot[1:]
                buf_p += 1
            else:
                break
        afterdot = afterdot[1:]
    else:
        if int(befordot) != 0:
            new_p = bin(len(befordot))[2:]

    offset = bin(pow(2, P - 1) - 1 - buf_p)[2:]
    return x1_inp, minus + \
                   sum_fix('0' * (P - len(offset)) + offset, '0' * (P - len(new_p)) + new_p, False) + \
                   befordot[1:] + afterdot + '0' * (M - len(befordot[1:] + afterdot))


# сумма и вычитание
def sum_or_sub(sum, x1, x2, x1_inp, x2_inp):
    print('=' * 50)
    if sum:
        print("Сложение:")
    else:
        print("Вычитание:")
        print('Изменение знака x2.', end=' ')
        if x2[0] == '0':
            x2 = '1' + x2[1:]
        else:
            x2 = '0' + x2[1:]
        print('Результат x2:', x2)

    x1_znak = x1[0]
    x1_paradok = x1[1:P + 1]
    x1_mantisa = '1' + x1[P + 1:]
    x2_znak = x2[0]
    x2_paradok = x2[1:P + 1]
    x2_mantisa = '1' + x2[P + 1:]
    print('x1=0?', end=' ')
    if float(x1_inp) == 0.0:
        print('Да. Результат: x2')
        return x2

    print('Нет.')
    print('x2=0?', end=' ')
    if float(x2_inp) == 0.0:
        print('Да. Результат: x1')
        return x1

    print('Нет.')
    while True:
        print('Порядки равны?', end=' ')
        if x1_paradok == x2_paradok:
            print('Да.')
            print('Сложение мантисс с учётом знака.', end=' ')
            rez_sum = sum_fix(additional_code(x1_znak + x1_mantisa), additional_code(x2_znak + x2_mantisa), True)
            if rez_sum != 'OverFlow':
                rez_sum = additional_code(rez_sum)
            print('Результат:', rez_sum)
            print('Мантисса=0?', end=' ')
            if rez_sum != 'OverFlow':
                if int(rez_sum[1:]) == 0:
                    print('Да. Результат: 0')
                    return '0' + '0' * P + '0' * M
            print('Нет.')
            print('Переполнение мантиссы?', end=' ')
            if rez_sum == 'OverFlow':
                print('Да.')
                print('Сдвиг мантиссы меньшего слагаемого вправо.', end=' ')
                if int(decimal(x1_mantisa)) > int(decimal(x2_mantisa)):
                    x2_mantisa = '0' + x2_mantisa[:-1]
                    print('Результат, сдвиг x2:', x2_mantisa)
                    print('Приращение порядка.', end=' ')
                    x2_paradok = sum_fix(x2_paradok, '0' * (P - 1) + '1', True)
                    print('Результат, порядок x2:', x2_paradok)
                else:
                    x1_mantisa = '0' + x1_mantisa[:-1]
                    print('Результат, сдвиг x1:', x1_mantisa)
                    print('Приращение порядка.', end=' ')
                    x1_paradok = sum_fix(x1_paradok, '0' * (P - 1) + '1', True)
                    print('Результат, порядок x1:', x1_mantisa)
                print('Переполнение порядка?', end=' ')
                if x1_paradok == 'OverFlow' or x2_paradok == 'OverFlow':
                    print('Да.', end=' ')
                    print('Сигнал о переполнении.')
                    return 'OverFlow'
                print('Нет.')
            print('Нет.')
            while True:
                print('Результат нормализован?', end=' ')
                if rez_sum[1] == '1':
                    print('Да.')
                    return rez_sum[0] + x1_paradok + rez_sum[2:]
                print('Нет.')
                print('Сдвиг мантиссы влево.', end=' ')
                rez_sum = rez_sum[0] + rez_sum[2:] + '0'
                print('Результат матиссы:', rez_sum[1:])
                print('Уменьшение порядка.', end=' ')
                # x1_paradok = subtraction(x1_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False)
                x1_paradok = subtraction((x1_paradok), '0' * (P - 1) + '1', True)
                # x1_paradok = sum_fix(x1_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False)
                print('Результат порядка:', x1_paradok)
                print('Потеря значимости порядка?', end=' ')
                if x1_paradok == 'OverFlow':
                    print('Да.', end=' ')
                    print('Сигнал о потере значимости.')
                    return 'OverFlow'
                print('Да')
        print('Нет.')
        print('Приращение порядка меньшего слагаемого.', end=' ')

        if int(decimal(subtraction(x1_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False))) > int(
                decimal(subtraction(x2_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False))):
            x2_paradok = sum_fix(x2_paradok, '0' * (P - 1) + '1', False)
            print('Результат порядка x2:', x2_paradok)
            print('Сдвиг мантиссы меньшего слагаемого вправо.', end=' ')
            x2_mantisa = '0' + x2_mantisa[:-1]
            print('Результат мантиссы x2:', x2_mantisa)
        else:
            x1_paradok = sum_fix(x1_paradok, '0' * (P - 1) + '1', False)
            print('Результат порядка x1:', x1_paradok)
            print('Сдвиг мантиссы меньшего слагаемого вправо.', end=' ')
            x1_mantisa = '0' + x1_mantisa[:-1]
            print('Результат мантиссы x1:', x1_mantisa)
        print('Мантисса=0?', end=' ')
        if int(x1_mantisa) == 0 or int(x2_mantisa) == 0:
            print('Да.', end=' ')
            print('Переслать другое слагаемое в ответ.')
            if int(x1_mantisa) == 0:
                return x2_znak + x2_paradok + x2_mantisa[1:]
            return x1_znak + x1_paradok + x1_mantisa[1:]
        print('Нет.')


# перевод из M в M*2 разряда доп код
def _M_to_M2_additional_code(x):
    if x[0] == '1':
        return '1' * (M + 2) + x
    return '0' * (M + 2) + x


# умножение
def multiplication_fix(x1_, x2_):
    m = _M_to_M2_additional_code(x1_)
    a = '0' * ((M + 2) * 2)
    q = _M_to_M2_additional_code(x2_)
    q_1 = '0'
    for i in range((M + 2) * 2):
        if q[-1] + q_1 == '01':
            a = sum_fix(a, m, False)
        elif q[-1] + q_1 == '10':
            a = subtraction(a, m, False)
        q_1 = q[-1]
        q = a[-1] + q[:-1]
        a = a[0] + a[:-1]
    return q


# умножение с плавающей точкой
def mult(x1, x2, x1_inp, x2_inp):
    print('=' * 50)
    print('Умножение:')
    print('x1=0?', end=' ')
    if float(x1_inp) == 0:
        print('Да.')
        return ' 0'
    print('Нет.')
    print('x2=0?', end=' ')
    if float(x2_inp) == 0:
        print('Да.')
        return ' 0'
    print('Нет.')
    x1_znak = x1[0]
    x1_paradok = x1[1:P + 1]
    x1_mantisa = '1' + x1[P + 1:]
    x2_znak = x2[0]
    x2_paradok = x2[1:P + 1]
    x2_mantisa = '1' + x2[P + 1:]
    print('Суммирование порядков.', end=' ')
    rez_paradok = sum_fix(x1_paradok, x2_paradok, False)
    print('Результат:', rez_paradok)
    print('Вычитанием смещения.', end='')
    rez_paradok = subtraction(rez_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False)
    print('Результат:', rez_paradok)
    print('Переполнение порядка?', end=' ')
    if rez_paradok == 'OverFlow':
        print('Да.')
        print('Сигнал о переполнениию')
        return 'OverFlow'
    print('Нет.')
    print('Потеря значимости поядка?', end=' ')
    if rez_paradok == 'OverFlow':
        print('Да.')
        print('Сигнал о потере значимости.')
        return 'OverFlow'
    print('Нет.')
    print('Умножение мантисс', end=' ')
    rez_mult_2 = additional_code(
        multiplication_fix(additional_code(x1_znak + x1_mantisa), additional_code(x2_znak + x2_mantisa)))
    rez_mult_2 = rez_mult_2[0] + rez_mult_2[2:]
    print('Результат:', rez_mult_2)
    print('Нормализация.', end=' ')
    while True:
        if rez_mult_2[1] == '1':
            break
        rez_mult_2 = rez_mult_2[0] + rez_mult_2[2:] + '0'
        rez_paradok = subtraction(rez_paradok, '0' * (P - 1) + '1', True)
        if x1_paradok == 'OverFlow':
            print('Сигнал о потере значимости.')
            return 'OverFlow'
    print('Результат:', rez_mult_2[0], rez_paradok, rez_mult_2[2:])
    print('Округление.', end=' ')
    print('Результат:', rez_mult_2[0], rez_paradok, rez_mult_2[2:M + 2])
    return rez_mult_2[0] + rez_paradok + rez_mult_2[2:M + 2]


# деление фикс
def division_fix(a, b):
    znak1 = a[0]
    znak2 = b[0]
    a = decimal('0' + a[1:])
    b = decimal('0' + b[1:])
    buf = str(a / b)
    befordot = bin(math.floor(float(buf)))[2:]
    afterdot = afterdot_to_bun(buf[len(str(math.floor(float(buf)))) + 1:])
    buf = befordot + afterdot
    buf = buf + '0' * (M - len(buf))
    if znak1 == znak2:
        return '0' + buf
    return '1' + buf


# деление с плавающей точкой
def div(x1, x2, x1_inp, x2_inp):
    print('Деление:')
    print('x1=0?', end=' ')
    if float(x1_inp) == 0:
        print('Да.')
        return ' 0'
    print('Нет.')
    print('x2=0?', end=' ')
    if float(x2_inp) == 0:
        print('Да.')
        return 'infinity'
    print('Нет.')
    x1_znak = x1[0]
    x1_paradok = x1[1:P + 1]
    x1_mantisa = '1' + x1[P + 1:]
    x2_znak = x2[0]
    x2_paradok = x2[1:P + 1]
    x2_mantisa = '1' + x2[P + 1:]
    print('Вычитание порядков.', end=' ')
    rez_paradok = subtraction(x1_paradok, x2_paradok, False)
    print('Результат:', rez_paradok)
    print('Сложение смещения.', end='')
    rez_paradok = sum_fix(rez_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False)
    rez_paradok = sum_fix(rez_paradok, '0' * (P - 1) + '1', False)
    print('Результат:', rez_paradok)
    print('Переполнение порядка?', end=' ')
    if rez_paradok == 'OverFlow':
        print('Да.')
        print('Сигнал о переполнениию')
        return 'OverFlow'
    print('Нет.')
    print('Потеря значимости порядка?', end=' ')
    if rez_paradok == 'OverFlow':
        print('Да.')
        print('Сигнал о потере значимости.')
        return 'OverFlow'
    print('Нет.')
    print('Деление мантисс.', end=' ')
    rez_div_2 = division_fix((x1_znak + x1_mantisa), (x2_znak + x2_mantisa))
    print('Результат:', rez_div_2)
    print('Нормализация.', end=' ')
    while True:
        if rez_div_2[1] == '1':
            break
        rez_div_2 = rez_div_2[0] + rez_div_2[2:] + '0'
        rez_paradok = subtraction(rez_paradok, '0' * (P - 1) + '1', True)
        if x1_paradok == 'OverFlow':
            print('Сигнал о потере значимости.')
            return 'OverFlow'
    print('Результат:', rez_div_2[0], rez_paradok, rez_div_2[2:])
    print('Округление.', end=' ')
    print('Результат:', rez_div_2[0], rez_paradok, rez_div_2[2:M + 2])
    return rez_div_2[0] + rez_paradok + rez_div_2[2:M + 2]


# перевод с 2 в 10
def _2_to_10(x):
    x_paradok = x[1:P + 1]
    x_mantisa = '1' + x[P + 1:]
    count = 0
    minus = 1
    if x_paradok[0] == '1':
        x_paradok = subtraction(x_paradok, '0' + bin(pow(2, P - 1) - 1)[2:], False)
    else:
        x_paradok = subtraction('0' + bin(pow(2, P - 1) - 1)[2:], x_paradok, False)
        minus = 0
    while True:
        if int(x_paradok) == 0:
            break
        x_paradok = subtraction(x_paradok, '0' * (P - 1) + '1', False)
        count += 1
    buf = 0.0
    count -= minus
    if minus == 0:
        x_mantisa = '0' * (count + 1) + x_mantisa
    count *= minus
    for i in range(M):
        # print(x_mantisa[i] + '*2^' + str(count - i), buf)
        buf += int(x_mantisa[i]) * pow(2, count - i)
    print('Ответ:', '-' + str(buf) if x[0] == '1' else '+' + str(buf))


x1_inp, x1 = input_num('1')
x2_inp, x2 = input_num('2')

print('\nПредставление x1:', x1[0], x1[1:P + 1], x1[P + 1:])
print('Представление x2:', x2[0], x2[1:P + 1], x2[P + 1:])

summ = sum_or_sub(True, x1, x2, x1_inp, x2_inp)
if summ == 'OverFlow':
    print('Ответ: OverFlow')
else:
    print('Ответ:', summ[0], summ[1:P + 1], summ[P + 1:])
    _2_to_10(summ)

sub = sum_or_sub(False, x1, x2, x1_inp, x2_inp)
if sub == 'OverFlow':
    print('Ответ: OverFlow')
else:
    print('Ответ:', sub[0], sub[1:P + 1], sub[P + 1:])
    _2_to_10(sub)

multi = mult(x1, x2, x1_inp, x2_inp)
if multi[0] != '0' and multi[0] != '1':
    print('Ответ:', multi)
else:
    print('Ответ:', multi[0], multi[1:P + 1], multi[P + 1:])
    _2_to_10(multi)
print('=' * 50)

divv = div(x1, x2, x1_inp, x2_inp)
if divv[0] != '0' and divv[0] != '1':
    print('Ответ:', divv)
else:
    print('Ответ:', divv[0], divv[1:P + 1], divv[P + 1:])
    _2_to_10(divv)
print('=' * 50)
