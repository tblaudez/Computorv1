#!/usr/local/bin/python3

import PolynomialExpression as Pe

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print("Usage: ./computor.py <equation>")
    #     exit(1)


    def get_polynomial_side() -> str:
        import random

        side = ""
        for _ in range(6):
            value = round(random.uniform(-999, 999), 3)
            power = random.randint(0, 2)
            side += f"{'+' if value > 0 else ''}{value}*x^{power} "

        return side


    # stdin = get_polynomial_side() + "= " + get_polynomial_side()
    stdin = "+5 + x -x^2 +4*x = 0"
    try:
        expression = Pe.PolynomialExpression(stdin)
        #expression.resolve_polynome(verbose=True)
    except Pe.InvalidExpressionException or Pe.UnequalPowersException as e:
        print(f"{type(e).__name__} - {e}")
