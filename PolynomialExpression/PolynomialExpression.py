from .Exceptions import UnequalPowersException, InvalidExpressionException

import re
import math
from fractions import Fraction


class PolynomialExpression:
    """
    The PolynomialExpression class is used to represent a polynomial expression
    like '-5 * x^2 + 5 * x^1 = 4 * x^0'
    """
    SIGNS = r"([+-] ?)?"
    X = SIGNS + r"x"
    VALUE = SIGNS + r"\d+(\.\d+)?"
    X_POWER = SIGNS + r"x\^\d+"
    VALUE_TIMES_X = SIGNS + r"\d+(\.\d+)? ?\* ?x"
    VALUE_TIMES_X_POWER = SIGNS + r"\d+(\.\d+)? ?\* ?x\^\d+"
    PATTERN = f"({VALUE_TIMES_X_POWER}|{VALUE_TIMES_X}|{X_POWER}|{VALUE}|{X})"

    def __init__(self, expression: str):
        if expression.count('=') != 1:
            raise InvalidExpressionException(expression, message="Invalid number of equal signs")

        self.left_units = self._parse_side(expression.split('=')[0])
        self.right_units = self._parse_side(expression.split('=')[1])

        self.simplified = False

    def _parse_side(self, side: str):
        tokens = [match[0] for match in re.findall(self.PATTERN, side, flags=re.IGNORECASE)]
        return [PolynomialExpression.PolynomialUnit(token.replace(' ', '')) for token in tokens]

    def __str__(self):
        left_units = " + ".join(f"[{unit}]" for unit in self.left_units) or "0"
        right_units = " + ".join(f"[{unit}]" for unit in self.right_units) or "0"
        return left_units + ' = ' + right_units

    def __repr__(self):
        return f"{{left_units: {self.left_units}," \
               f"right_units: {self.right_units}, " \
               f"polynomial_degree: {self.get_polynomial_degree()}" \
               f"simplified: {self.simplified}}}"

    def get_polynomial_degree(self) -> float:
        """Get the degree of the polynomial equation"""
        return max([unit.power for unit in self.left_units + self.right_units] or [0])

    def simplify_expression(self):
        """Simplify the units of the polynomial"""

        # Pass all units on the left side for simplification
        self.left_units.extend([-unit for unit in self.right_units])
        self.right_units = []

        # Simplify the units by merging same-powered units
        for power in sorted(list(set([unit.power for unit in self.left_units]))):
            unit_of_power = [unit for unit in self.left_units if unit.power == power]
            self.left_units = [unit for unit in self.left_units if unit not in unit_of_power]
            self.left_units.append(sum(unit_of_power))

        # Remove 0-valued units
        self.left_units = [unit for unit in self.left_units if unit != 0]

        # Sort the units to have lowest power on the leftmost part of the expression
        self.left_units.sort(key=lambda unit: unit.power, reverse=True)

        self.simplified = True

    def get_equation_members(self):
        if self.simplified is not True:
            self.simplify_expression()

        a = next((unit.value for unit in self.left_units if unit.power == 2), 0)
        b = next((unit.value for unit in self.left_units if unit.power == 1), 0)
        c = next((unit.value for unit in self.left_units if unit.power == 0), 0)

        return a, b, c

    def _resolve_degree_zero(self):
        print("Polynomial degree: 0", "This equation is trivial", sep='\n')
        if len(self.left_units) == 0:
            print("Every real number 'ℝ' could be a solution of this equation")
        else:
            print("The equation cannot be solved for there is nothing to solve. It's just wrong.")

    def _resolve_degree_one(self, b, c, verbose):
        print("Polynomial degree: 1")
        if verbose is True:
            print("When polynomial degree is 1 the equation can simply be hand-resolved",
                  "In this case 'x = -c/b'", sep='\n')
        x = self.get_closest_fraction(-c/b)
        if x.denominator != 1:
            x = f"{x} ({round(-c/b, 3)})"
        print(f"The solution is : {x}")

    def get_closest_fraction(self, value: float):
        return Fraction(round(value, 8)).limit_denominator(128)

    def _resolve_degree_two(self, a, b, c, verbose):
        discriminant = self.get_closest_fraction(b**2 - 4*a*c)
        discriminant_sqrt = self.get_closest_fraction(math.sqrt(abs(discriminant)))

        print("Polynomial degree: 2", f"Discriminant: {discriminant}", "", sep='\n')
        if verbose is True:
            print("When the polynomial degree is 2 the potential solutions are solved using "
                  "something called the 'discriminant', written 'Δ'",
                  "The discriminant formula is 'Δ = b² - 4ac'",
                  f"In our situation, Δ is equal to '{discriminant}'", "", sep='\n')

        if discriminant > 0:
            x1 = Fraction(self.get_closest_fraction(-b) - discriminant_sqrt, self.get_closest_fraction(2*a))\
                .limit_denominator(1024)
            x2 = Fraction(self.get_closest_fraction(-b) + discriminant_sqrt, self.get_closest_fraction(2*a))\
                .limit_denominator(1024)
            if x1.denominator != 1:
                x1 = f"{x1} ({round((-b-math.sqrt((b**2)-(4*a*c)))/(2*a), 3)})"
            if x2.denominator != 1:
                x2 = f"{x2} ({round((-b+math.sqrt((b**2)-(4*a*c)))/(2*a), 3)})"
            print("The discriminant is strictly positive.")
            if verbose is True:
                print("When the discriminant is strictly positive "
                      "two solutions can be found using the discriminant itself",
                      f"The solutions formulas are 'x1 = (-b-√Δ)/2a' and 'x2 = (-b+√Δ)/2a'", "", sep='\n')
            print(f"The two solutions are :", x1, x2, sep='\n')

        if discriminant < 0:
            x1 = f"(({self.get_closest_fraction(-b) if b != -0 else ''})-√({-discriminant})i)" \
                 f"/({self.get_closest_fraction(2*a)})"
            x2 = f"(({self.get_closest_fraction(-b) if b != -0 else ''})+√({-discriminant})i)" \
                 f"/({self.get_closest_fraction(2*a)})"
            print("The discriminant is strictly negative.")
            if verbose is True:
                print("When the discriminant is strictly negative "
                      "no solutions can be found on the real numbers realm 'ℝ'",
                      "We need to use complex numbers (involving 'i') to find a solution to this equation",
                      "The solutions formulas are 'x1 = (-b - i√(-Δ))/2a' and 'x2 = (-b + i√(-Δ))/2a'",
                      sep='\n')
            print("There two solutions are :", x1, x2, sep='\n')

        elif discriminant == 0:
            x1 = self.get_closest_fraction((-b)/(2*a))
            if x1.denominator != 1:
                x1 = f"{x1} ({round((-b)/(2*a), 3)})"
            print("The discriminant is equal to 0")
            if verbose is True:
                print("When the discriminant is equal to 0 there is one and only one solution to the equation",
                      "In this case, the solution formula is 'x1 = -b/2a'", sep='\n')
            print(f"The solution is : {x1}")

    def resolve_polynomial(self, verbose=False):
        """Resolve the polynomial and display the solutions if there are any"""
        if self.simplified is not True:
            self.simplify_expression()

        degree = self.get_polynomial_degree()
        a, b, c = self.get_equation_members()

        print(f"Reduced form : {self}", "", sep='\n')
        if verbose is True:
            print("A polynomial equation has the form 'ax² + bx + c = 0'",
                  f"Here a is '{a}', b is '{b}' and c is '{c}'", "", sep='\n')

        if degree == 0:
            self._resolve_degree_zero()
        elif degree == 1:
            self._resolve_degree_one(b, c, verbose)
        elif degree == 2:
            self._resolve_degree_two(a, b, c, verbose)

        else:
            print(f"Polynomial degree: {degree}")
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            if verbose is True:
                print("When the polynomial degree is greater than 2 "
                      "the equation cannot be solved using the discriminant only",
                      "We would need to derivate the equation to the power of 2 to find its solutions", sep='\n')

    class PolynomialUnit:
        """The PolynomialUnit class is used to represent a polynomial unit like '-5 * x^2'"""

        def __init__(self, polynomial: str):
            self.value = 0
            self.power = 0

            # -2.43*x^2
            if re.fullmatch(PolynomialExpression.VALUE_TIMES_X_POWER, polynomial, flags=re.IGNORECASE):
                self.value = float(polynomial.split('*')[0])
                self.power = int(polynomial.split('^')[1])

            # -2.43*x
            elif re.fullmatch(PolynomialExpression.VALUE_TIMES_X, polynomial, flags=re.IGNORECASE):
                self.value = float(polynomial.split('*')[0])
                self.power = 1

            # -x^2
            elif re.fullmatch(PolynomialExpression.X_POWER, polynomial, flags=re.IGNORECASE):
                self.value = -1.0 if polynomial[0] == '-' else 1.0
                self.power = int(polynomial.split('^')[1])

            # -2.43
            elif re.fullmatch(PolynomialExpression.VALUE, polynomial, flags=re.IGNORECASE):
                self.value = float(polynomial.split('*')[0])
                self.power = 0

            # -x
            elif re.fullmatch(PolynomialExpression.X, polynomial, flags=re.IGNORECASE):
                self.value = -1.0 if polynomial[0] == '-' else 1.0
                self.power = 1

            else:
                raise InvalidExpressionException(polynomial)

            self.value = int(self.value) if self.value.is_integer() else self.value

        def __str__(self):
            return f"{self.value} * x^{self.power}"

        def __repr__(self):
            return f'{{value: {self.value}, power: {self.power}}}'

        def __add__(self, other):
            # 3*x^0 + 7 -> 10*x^0
            if isinstance(other, int) or isinstance(other, float):
                if other == 0:
                    return self
                if self.power != 0:
                    raise UnequalPowersException(self.__str__(), other.__str__())
                return self.from_values(self.value + other, 0)

            if isinstance(other, PolynomialExpression.PolynomialUnit):
                # 3*x^2 + 2*x^1 -> Error
                if other.power != self.power:
                    raise UnequalPowersException(self.__str__(), other.__str__())

                # 3*x^1 + 4*x^1 -> 7*x^1
                return self.from_values(self.value + other.value, self.power)

            return self

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            return self.__add__(-other)

        def __eq__(self, other):
            # 0*x^2 == 0 OR 4*x^0 == 4
            if isinstance(other, int) or isinstance(other, float):
                if other == 0:
                    return self.value == 0
                return self.power == 0 and self.value == other
            # 3*x^2 == 3*x^2
            return self.value == other.value and self.power == other.power

        def __neg__(self):
            return PolynomialExpression.PolynomialUnit.from_values(-self.value, self.power)

        @classmethod
        def from_values(cls, value: float, power: int):
            return cls(f"{value}*x^{power}")
