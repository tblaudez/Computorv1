from __future__ import annotations
from .Exceptions import UnequalPowersException, InvalidExpressionException

import typing
import re


class PolynomialExpression:
    """
    The PolynomialExpression class is used to represent a polynomial expression like '-5 * x^2 + 5 * x^1 = 4 * x^0'
    """
    PATTERN = r"(([+\-] ?)?\d+(\.\d+)? ?\* ?x\^([+\-] ?)?\d+(\.\d+)?)"

    def __init__(self, expression: str, simplified=False):
        splited_expression = [units.strip() for units in expression.split('=')]
        if len(splited_expression) != 2 \
                or not re.match(self.PATTERN, splited_expression[0], flags=re.IGNORECASE) \
                or not re.match(self.PATTERN, splited_expression[1], flags=re.IGNORECASE):
            raise InvalidExpressionException(expression)

        self.left_units = [self.PolynomialUnit(match[0])
                           for match in re.findall(self.PATTERN, splited_expression[0], flags=re.IGNORECASE)]
        self.right_units = [self.PolynomialUnit(match[0])
                            for match in re.findall(self.PATTERN, splited_expression[1], flags=re.IGNORECASE)]
        self.simplified = simplified

        if self.get_polynomial_degree() > 2:
            raise InvalidExpressionException(expression, message="Polynomial degree is greater than 2")

    def __str__(self):
        left_units = " + ".join(f"[{unit}]" for unit in self.left_units) or "0"
        right_units = " + ".join(f"[{unit}]" for unit in self.right_units) or "0"
        return left_units + ' = ' + right_units

    def __repr__(self):
        return f"{{left_units: {self.left_units}, right_units: {self.right_units}, " \
               f"polynomial_degree: {self.get_polynomial_degree()}}}"

    def get_polynomial_degree(self) -> float:
        """Get the degree of the polynomial equation"""
        return max([unit.power for unit in self.left_units + self.right_units])

    def simplify_polynome(self):
        """Simplify the units of the polynome"""

        def _simplify_units_on_side(side: typing.List[PolynomialExpression.PolynomialUnit]):
            """Simplify the units in a side of the polynome"""

            def _get_unit_index_by_power(unit_list: typing.List[PolynomialExpression.PolynomialUnit],
                                         power: float) -> typing.List[int]:
                """Get the index of the units that are of power <power> in <unit_list>"""
                return [unit_index for unit_index, unit in enumerate(unit_list) if unit.power == power]

            for i in [unit.power for unit in side]:
                simplifiable_units_index = _get_unit_index_by_power(side, i)
                if len(simplifiable_units_index) <= 1:
                    continue
                simplifiable_units_index.reverse()
                for index in simplifiable_units_index[1:]:
                    side[simplifiable_units_index[0]] += side[index]
                    side.pop(index)

        # Getting rid of 0-valued polynomes
        self.left_units = [unit for unit in self.left_units if unit.power != 0 and unit.value != 0]
        self.right_units = [unit for unit in self.right_units if unit.power != 0 and unit.value != 0]

        # Merging same power polynomes in each sides
        _simplify_units_on_side(self.left_units)
        _simplify_units_on_side(self.right_units)

        self.simplified = True

    def resolve_polynome(self):
        """Resolve the polynome and display the solutions if there are any"""
        if self.simplified is False:
            self.resolve_polynome()

    class PolynomialUnit:
        """The PolynomialUnit class is used to represent a polynomial unit like '-5 * x^2'"""

        def __init__(self, polynome: str = None):
            if polynome is None:
                self.value = 0
                self.power = 0
            else:
                self.value = float(polynome.split('*')[0].replace(' ', ''))
                self.value = int(self.value) if self.value.is_integer() else self.value
                self.power = float(polynome.split('^')[1].replace(' ', ''))
                self.power = int(self.power) if self.power.is_integer() else self.power

        def __str__(self):
            return f"{self.value} * x^{self.power}"

        def __repr__(self):
            return f'{{value: {self.value}, power: {self.power}}}'

        def __add__(self, other) -> PolynomialExpression.PolynomialUnit:
            if isinstance(other, int):
                return self.from_values(self.value + other, self.power)
            if other.power != self.power:
                raise UnequalPowersException(self.__str__(), other.__str__())
            return self.from_values(self.value + other.value, self.power)

        @classmethod
        def from_values(cls, value: float, power: float) -> PolynomialExpression.PolynomialUnit:
            polynome = cls()
            polynome.value = value
            polynome.power = power
            return polynome
