#!/usr/local/bin/python3

import PolynomialExpression as Pe
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Simplify and resolve a polynomial equation of maximum degree 2')
    parser.add_argument("expression", help="The expression to be resolved, ex: '5*x^2 + 7 = 0'",
                        type=str, metavar='<expression>')
    parser.add_argument("-v", "--verbose", help="Increase the verbosity of the resolution of the equation",
                        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    try:
        expression = Pe.PolynomialExpression(args.expression)
        expression.resolve_polynomial(args.verbose)
    except Pe.InvalidExpressionException or Pe.UnequalPowersException as e:
        print(f"{type(e).__name__} - {e}")
