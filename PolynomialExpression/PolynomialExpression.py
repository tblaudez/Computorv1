from __future__ import annotations
from .Exceptions import UnequalPowersException, InvalidExpressionException

import typing
import re


class PolynomialExpression:
    """
    The PolynomialExpression class is used to represent a polynomial expression
    like '-5 * x^2 + 5 * x^1 = 4 * x^0'
    """
    PATTERN = r"(([+\-] ?)?\d+(\.\d+)? ?\* ?x\^([+\-] ?)?\d+(\.\d+)?)"

    def __init__(self, expression: str):
        splited_expression = [units.strip() for units in expression.split('=')]
        if len(splited_expression) != 2 \
                or not re.match(self.PATTERN, splited_expression[0], flags=re.IGNORECASE) \
                or not re.match(self.PATTERN, splited_expression[1], flags=re.IGNORECASE):
            raise InvalidExpressionException(expression)

        self.left_units = [self.PolynomialUnit(match[0])
                           for match in re.findall(self.PATTERN, splited_expression[0], flags=re.IGNORECASE)]
        self.right_units = [self.PolynomialUnit(match[0])
                            for match in re.findall(self.PATTERN, splited_expression[1], flags=re.IGNORECASE)]
        self.side_simplified = False
        self.expression_simplified = False

        if self.get_polynomial_degree() > 2:
            raise InvalidExpressionException(expression, message="Polynomial degree is greater than 2")

    def __str__(self):
        left_units = " + ".join(f"[{unit}]" for unit in self.left_units) or "0"
        right_units = " + ".join(f"[{unit}]" for unit in self.right_units) or "0"
        return left_units + ' = ' + right_units

    def __repr__(self):
        return f"{{left_units: {self.left_units}," \
               f"right_units: {self.right_units}, " \
               f"polynomial_degree: {self.get_polynomial_degree()}" \
               f"simplified: {self.expression_simplified}}}"

    def get_polynomial_degree(self) -> float:
        """Get the degree of the polynomial equation"""
        return max([unit.power for unit in self.left_units + self.right_units])

    def get_left_powers(self) -> typing.List[float]:
        return sorted(list(set([unit.power for unit in self.left_units])))

    def get_right_powers(self) -> typing.List[float]:
        return sorted(list(set([unit.power for unit in self.right_units])))

    def get_all_powers(self) -> typing.List[float]:
        return sorted(list(set(self.get_left_powers() + self.get_right_powers())))

    def _simplify_sides(self):
        """Simplify a side of the expression by merging same-powered units"""
        for unit_list in (self.left_units, self.right_units):
            for power in sorted(list(set([unit.power for unit in unit_list]))):
                simplified_unit = sum([unit for unit in unit_list if unit.power == power])
                unit_list[:] = [unit for unit in unit_list if unit.power != power]
                unit_list.append(simplified_unit)

        self.side_simplified = True

    def get_index_of_unit_of_power(self, power: float, unit_list):
        if self.side_simplified is False:
            self._simplify_sides()
        for index, unit in enumerate(unit_list):
            if unit.power == power:
                return index
        return None

    def simplify_expression(self):
        """Simplify the units of the polynome"""

        # Merging same power polynomes in each sides
        self._simplify_sides()
        # Getting rid of 0-valued polynomes
        self.left_units = [unit for unit in self.left_units if unit != 0]
        self.right_units = [unit for unit in self.right_units if unit != 0]

        for power in self.get_all_powers():
            left_index = self.get_index_of_unit_of_power(power, self.left_units)
            right_index = self.get_index_of_unit_of_power(power, self.right_units)
            if left_index is None or right_index is None:
                continue
            self.left_units[left_index] -= self.right_units[right_index]
            self.right_units.pop(right_index)

        self.expression_simplified = True

    def resolve_polynome(self, verbose=False):
        """Resolve the polynome and display the solutions if there are any"""
        if self.expression_simplified is False:
            self.simplify_expression()

    class PolynomialUnit:
        """The PolynomialUnit class is used to represent a polynomial unit like '-5 * x^2'"""

        def __init__(self, polynome: str = None):
            if polynome is None:
                return
            self.value = float(polynome.split('*')[0].replace(' ', ''))
            self.value = int(self.value) if self.value.is_integer() else self.value
            self.power = float(polynome.split('^')[1].replace(' ', ''))
            self.power = int(self.power) if self.power.is_integer() else self.power

        def __str__(self):
            return f"{self.value} * x^{self.power}"

        def __repr__(self):
            return f'{{value: {self.value}, power: {self.power}}}'

        def __add__(self, other) -> PolynomialExpression.PolynomialUnit:
            if isinstance(other, int) and other == 0:
                return self
            if other.power != self.power:
                raise UnequalPowersException(self.__str__(), other.__str__())
            return self.from_values(self.value + other.value, self.power)

        def __radd__(self, other):
            return self.__add__(other)

        def __sub__(self, other):
            if isinstance(other, int) and other == 0:
                return self
            if other.power != self.power:
                raise UnequalPowersException(self.__str__(), other.__str__())
            return self.from_values(self.value - other.value, self.power)

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

        @classmethod
        def from_values(cls, value: float, power: float) -> PolynomialExpression.PolynomialUnit:
            polynome = cls()
            polynome.value = value
            polynome.power = power
            return polynome
