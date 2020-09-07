from __future__ import annotations
from .Exceptions import UnequalPowersException, InvalidExpressionException

import re
import math


class PolynomialExpression:
    """
    The PolynomialExpression class is used to represent a polynomial expression
    like '-5 * x^2 + 5 * x^1 = 4 * x^0'
    """
    PATTERN = r"(\d+(\.\d+)?( ?\* ?))?x(\^\d)?|\d+"

    def __init__(self, expression: str):
        if expression.count('=') != 1:
            raise InvalidExpressionException(expression, message="Invalid number of equal signs")

        self.left_units, self.right_units = self.parse_expression(expression)
        self.simplified = False

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
        """Simplify the units of the polynome"""

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

    def resolve_polynome(self, verbose=False):
        """Resolve the polynome and display the solutions if there are any"""
        if self.simplified is not True:
            self.simplify_expression()

        degree = self.get_polynomial_degree()
        if degree == 0:
            print("Polynonial degree: 0", "This equation is trivial", sep='\n')
            if len(self.left_units) == 0:
                print("Every real number 'ℝ' could be a solution of this equation")
            else:
                print("The equation cannot be solved for there is nothing to solve. It's just wrong.")
            return

        a, b, c = self.get_equation_members()
        print(f"Reduced form : {self}", "", sep='\n')

        if verbose is True:
            print("A polynomial equation has the form 'ax² + bx + c = 0'",
                  f"Here a is '{a}', b is '{b}' and c is '{c}'", "", sep='\n')

        if degree == 1:
            print("Polynonial degree: 1")
            if verbose is True:
                print("When polynomial degree is 1 the equation can simply be hand-resolved",
                      "In this case 'x = -c/b'", sep='\n')
            x = round(-c / b, 3)
            x = int(x) if x.is_integer() else x
            print(f"The solution is : {x}")

        elif degree == 2:
            print("Polynonial degree: 2")
            discriminant = round(math.pow(b, 2) - (4 * a * c), 3)
            discriminant = int(discriminant) if discriminant.is_integer() else discriminant

            if verbose is True:
                print("When polynonial degree is 2 the potential solutions are solved using "
                      "something called the 'discriminant', written 'Δ'",
                      "The discriminant formula is 'Δ = b² - 4ac'",
                      f"In our situation, Δ is equal to '{discriminant}'", "", sep='\n')

            if discriminant < 0:
                print("The discriminant is strictly negative.")
                if verbose is True:
                    print("When the discriminant is strictly negative "
                          "no solutions can be found on the real numbers realm 'ℝ'",
                          "We need to use complex numbers (involving 'i') to find a solution to this equation",
                          sep='\n')
                import cmath
                x1 = f"{complex(-b, round(math.sqrt(-discriminant), 3))} / {2 * a}".replace('j', 'i')
                x2 = f"{complex(-b, -round(math.sqrt(-discriminant), 3))} / {2 * a}".replace('j', 'i')
                print("There two solutions are :", x1, x2, sep='\n')

            elif discriminant == 0:
                x1 = round(-b / (2 * a), 3)
                x1 = int(x1) if x1.is_integer() else x1
                print("The discriminant is equal to 0")
                if verbose is True:
                    print("When the discriminant is equal to 0 there is one and only one solution to the equation",
                          "In this case, the solution formula is 'x1 = -b/2a'", sep='\n')
                print(f"The solution is : {x1}")

            elif discriminant > 0:
                x1 = round((-b - math.sqrt(discriminant)) / (2 * a), 3)
                x1 = int(x1) if x1.is_integer() else x1
                x2 = round((-b + math.sqrt(discriminant)) / (2 * a), 3)
                x2 = int(x2) if x2.is_integer() else x2
                print("The discriminant is strictly positive.")
                if verbose is True:
                    print("When the discriminant is strictly positive "
                          "two solutions can be found using the discriminant itself",
                          f"The solutions formulas are 'x1 = (-b - √Δ)/2a' and 'x2 = (-b + √Δ)/2a'", "", sep='\n')
                print(f"The two solutions are :", x1, x2, sep='\n')

        else:
            print(f"Polynonial degree: {degree}")
            if verbose is True:
                print("When the polynonial degree is greater than 2 "
                      "the equation cannot be solved using the discriminant only",
                      "We would need to derivate the equation to the power of 2 to find its solutions", sep='\n')
            else:
                print("The polynomial degree is strictly greater than 2, I can't solve.")

    class PolynomialUnit:
        """The PolynomialUnit class is used to represent a polynomial unit like '-5 * x^2'"""

        def __init__(self, polynome: str = None):
            if polynome is None:
                return

            self.value = round(float(polynome.split('*')[0].replace(' ', '')), 3)
            if self.value.is_integer():
                self.value = int(self.value)

            self.power = int(polynome.split('^')[1].replace(' ', ''))

        def __str__(self):
            return f"{self.value} * x^{self.power}"

        def __repr__(self):
            return f'{{value: {self.value}, power: {self.power}}}'

        def __add__(self, other) -> PolynomialExpression.PolynomialUnit:
            if isinstance(other, int) and other == 0:
                return self
            if other.power != self.power:
                raise UnequalPowersException(self.__str__(), other.__str__())
            return self.from_values(round(self.value + other.value, 3), self.power)

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            if isinstance(other, int) and other == 0:
                return self
            if other.power != self.power:
                raise UnequalPowersException(self.__str__(), other.__str__())
            return self.from_values(round(self.value - other.value, 3), self.power)

        def __rsub__(self, other):
            return other.__sub__(self)

        def __eq__(self, other):
            if isinstance(other, int):
                if other == 0:
                    return self.value == 0
                return self.power == 0 and self.value == other
            return self.value == other.value and self.power == other.power

        def __ne__(self, other):
            return not self.__eq__(other)

        def __neg__(self):
            return PolynomialExpression.PolynomialUnit.from_values(-self.value, self.power)

        @classmethod
        def from_values(cls, value: float, power: float) -> PolynomialExpression.PolynomialUnit:
            polynome = cls()
            polynome.value = value
            polynome.power = power
            return polynome
