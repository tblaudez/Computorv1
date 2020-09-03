#!/usr/local/bin/python3

from PolynomialExpression import PolynomialExpression

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print("Usage: ./computor.py <equation>")
    #     exit(1)

    stdin = "-5 * x^2 + 5 * x^1 + 2 * x^2 = 4 * x^2"
    expression = PolynomialExpression(stdin)
    print(expression)
    expression.simplify_polynome()