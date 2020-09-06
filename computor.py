#!/usr/local/bin/python3

import PolynomialExpression as Pe

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print("Usage: ./computor.py <equation>")
    #     exit(1)

    import random

    def get_random_float():
        return round(random.uniform(-99, 99), 3)

    def get_polynomial_side() -> str:
        side = ""
        for i in range(3):
            value = round(random.uniform(-99, 99), 3)
            power = random.randint(0, 2)
            side += f"{' +' if value > 0 else ''} {value}*x^{power}"

        return side


    # stdin = get_polynomial_side() + " = " + get_polynomial_side()
    stdin = "7*x^0 = 14*x^0"
    expression = None

    try:
        expression = Pe.PolynomialExpression(stdin)
        print(expression)
        expression.simplify_expression()
        expression.resolve_polynome(verbose=True)
    except Pe.InvalidExpressionException or Pe.UnequalPowersException as e:
        print(f"{type(e).__name__} - {e}")
        exit(1)
