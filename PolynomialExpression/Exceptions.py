class UnequalPowersException(Exception):
    """Custom error class for raised when to PolynomialUnit of different powers are simplified"""

    def __init__(self, unit1: str, unit2: str, message="Units of different powers cannot be simplified"):
        self.unit1 = unit1
        self.unit2 = unit2
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.unit1}] | [{self.unit2}] -> {self.message}"


class InvalidExpressionException(Exception):
    def __init__(self, expression, message="Given expression is invalid"):
        self.expression = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[[ {self.expression} ]] -> {self.message}"
