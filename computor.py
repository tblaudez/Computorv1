#!/usr/local/bin/python3

import PolynomialExpression as Pe

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print("Usage: ./computor.py <equation>")
    #     exit(1)

    stdin = "-2 * x^0 + 7 * x^1 -6 * x^2 = 0*x^0 + 1 *x^1 + 2 * x^2"
    expression = None
    try:
        expression = Pe.PolynomialExpression(stdin)
        print(expression)
        expression.simplify_expression()
    except Pe.InvalidExpressionException or Pe.UnequalPowersException as e:
        print(f"{type(e).__name__} - {e}")
        exit(1)
    print(expression)
