import typing
import re

PolynomialUnitType = typing.List['PolynomialUnit']


class PolynomialExpression:
    """
    The PolynomialExpression class is used to represent a polynomial expression like '-5 * x^2 + 5 * x^1 = 4 * x^0'
    """
    PATTERN = r"(([+\-] ?)?\d+(\.\d+)? ?\* ?x\^([+\-] ?)?\d+(\.\d+)?)"

    def __init__(self, expression: str):
        self.left_units = self.get_units_from_expression(expression.split('=')[0])
        self.right_units = self.get_units_from_expression(expression.split('=')[1])

    def get_units_from_expression(self, expression: str) -> typing.List['PolynomialUnit']:
        """
        Parse the equation using regex and returns a list of PolynomialUnits
        """
        matches = re.findall(self.PATTERN, expression, flags=re.IGNORECASE)
        return [self.PolynomialUnit(match[0]) for match in matches]

    def __str__(self):
        return " ".join(f"[{unit.__str__()}]" for unit in self.left_units) \
               + " = " \
               + " ".join(f"[{unit.__str__()}]" for unit in self.right_units)

    def __repr__(self):
        return f"{{" \
            f"left_units: {self.left_units}, " \
            f"right_units: {self.right_units}, " \
            f"polynomial_degree: {self.get_polynomial_degree()}" \
            f"}}"

    def get_polynomial_degree(self) -> int:
        """Get the degree of the polynomial equation"""
        return max([unit.power for unit in self.left_units + self.right_units])

    @staticmethod
    def get_unit_by_degree(degree: int, units: PolynomialUnitType) -> PolynomialUnitType:
        """Get the units that are of degree `degree` in the unit list `units`"""
        return [unit for unit in units if unit.power == degree]

    def simplify_polynome(self):
       pass

    class PolynomialUnit:
        """
        The PolynomialUnit class is used to represent a polynomial unit like '-5 * x^2'
        """

        def __init__(self, polynome: str):
            self.value = float(polynome.split('*')[0].replace(' ', ''))
            self.power = float(polynome.split('^')[1].replace(' ', ''))

            if self.value.is_integer():
                self.value = int(self.value)
            if self.power.is_integer():
                self.power = int(self.power)

        def __str__(self):
            return f"{self.value} * x^{self.power}"

        def __repr__(self):
            return f'{{value: {self.value}, power: {self.power}}}'
