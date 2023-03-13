#define _USE_MATH_DEFINES
#include <iostream>
#include <windows.h>
#include <string>
#include <cmath>
#include <iomanip>

using namespace std;
int main()
{
	double a, b, c, d, x1, x2, _4 = 4, _2 = 2, _1 = 1;
	cout << "Lab 7:\n";
	cout << "a = "; cin >> a;
	cout << "b = "; cin >> b;
	cout << "c = "; cin >> c;
	if (a == 0) {
		cout << "a==0";
	}
	else {
		// Нахождение D
		__asm {
			FLD b	// Загрузка в стек b
			FLD b	// Загрузка в стек b
			FMUL	// Умножение ST(0) и ST(1)
			FLD _4	// Загрузка в стек 4
			FLD a	// Загрузка в стек a
			FLD c	// Загрузка в стек c
			FMUL	// Умножение ST(0) и ST(1)
			FMUL	// Умножение ST(0) и ST(1)
			FSUB	// Вычитание ST(0) и ST(1)
			FSTP d	// Запись ST(0) в d
		}
		if (d <= 0) {
			cout << "D <= 0";
		}
		else {

			// Вычисление x1, x2
			__asm {
				FLD b	// Загрузка в стек b
				FCHS	// Инверсия знака ST(0)
				FLD d	// Загрузка в стек d
				FSQRT	// Квадратный корень ST(0)
				FADD	// Сумма ST(0) из ST(1)
				FLD _2  // Загрузка в стек 2
				FLD a	// Загрузка в стек a
				FMUL	// Умножение ST(0) и ST(1)
				FDIV	// Деление ST(0) и ST(1)
				FSTP x1 // Запись ST(0) в x1
			}
			__asm {
				FLD b	// Загрузка в стек b
				FCHS	// Инверсия знака ST(0)
				FLD d	// Загрузка в стек d
				FSQRT	// Квадратный корень ST(0)
				FSUB	// Вычитание ST(0) из ST(1)
				FLD _2  // Загрузка в стек 2
				FLD a	// Загрузка в стек a
				FMUL	// Умножение ST(0) и ST(1)
				FDIV	// Деление ST(0) и ST(1)
				FSTP x2 // Запись ST(0) в x2
			}

			cout << "x1 = " << x1 << ", x2 = " << x2;
		}
	}

	double h, e, pi = M_PI;
	bool fail = false;
	cout << "\n\nLab 8:\n";
	cout << "a = "; cin >> a;
	cout << "b = "; cin >> b;
	cout << "h = "; cin >> h;
	cout << "e = "; cin >> e;

	// Вариант 5
	cout << "\n_______________________________________________________________________\n";
	cout << "X                S(X)             Y(X)             |Y(x)-S(x)|      n\n";
	cout << "-----------------------------------------------------------------------\n";
	for (double x = a; x < b + h;x += h) {
		double y;
		__asm {
			FLD x	// Загрузка в стек x
			FLD pi	// Загрузка в стек pi
			FLD _4	// Загрузка в стек 4
			FDIV	// Деление ST(0) и ST(1)
			FSIN	// Синус ST(0)
			FMUL	// Умножение ST(0) и ST(1)
			FLD _1	// Загрузка в стек 1
			FLD x	// Загрузка в стек x
			FLD x	// Загрузка в стек x
			FMUL	// Умножение ST(0) и ST(1)
			FLD _2	// Загрузка в стек 2
			FLD x	// Загрузка в стек x
			FLD pi	// Загрузка в стек pi
			FLD _4	// Загрузка в стек 4
			FDIV	// Деление ST(0) и ST(1)
			FCOS	// Косинус ST(0)
			FMUL	// Умножение ST(0) и ST(1)
			FMUL	// Умножение ST(0) и ST(1)
			FSUB	// Вычитание ST(0) и ST(1)
			FADD	// Сумма ST(0) и ST(1)
			FDIV	// Деление ST(0) и ST(1)
			FSTP y	// Запись ST(0) в у
		}
		double n = 1;
		double s = 0;
		double power = x;
		do {
			for (double o = 1;o < n;o++) {
				__asm {
					FLD x		// Загрузка в стек x
					FLD power	// Загрузка в стек power
					FMUL		// Умножение ST(0) и ST(1)
					FSTP power	// Запись ST(0) в power
				}
			}
			__asm {
				FLD s		// Загрузка в стек s
				FLD power	// Загрузка в стек power
				FLD pi		// Загрузка в стек pi
				FLD n		// Загрузка в стек n
				FMUL		// Умножение ST(0) и ST(1)
				FLD _4		// Загрузка в стек 4
				FDIV		// Деление ST(0) и ST(1)
				FSIN		// Синус ST(0) и ST(1)
				FMUL		// Умножение ST(0) и ST(1)
				FADD		// Сумма ST(0) и ST(1)
				FSTP s		// Запись ST(0) в s
			}
			n++;
			if (n == 1000) {
				fail = true;
				break;
			}
		} while (abs(y - s) > e);
		if (!fail)
			cout << setiosflags(ios::left) << setw(17) << x << setw(17) << s << setw(17) << y <<
			setw(17) << abs(y - s) << setw(5) << n-1 << '\n';
		else
			cout << "--------------------------------ERROR----------------------------------\n";
	}
	return 0;
}
