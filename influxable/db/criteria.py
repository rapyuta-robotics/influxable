import re
from enum import Enum


class WhereOperatorEnum(Enum):
    LT = 'lt'
    LTE = 'lte'
    GT = 'gt'
    GTE = 'gte'
    EQ = 'eq'
    NE = 'ne'
    REGEQ = 'regeq'
    REGNEQ = 'regneq'


EVALUATED_OPERATORS = {
    WhereOperatorEnum.LT: '<',
    WhereOperatorEnum.LTE: '<=',
    WhereOperatorEnum.GT: '>',
    WhereOperatorEnum.GTE: '>=',
    WhereOperatorEnum.EQ: '=',
    WhereOperatorEnum.NE: '!=',
    WhereOperatorEnum.REGEQ: '=~',
    WhereOperatorEnum.REGNEQ: '!~'
}

INVERTED_OPERATORS = {
    WhereOperatorEnum.LT: WhereOperatorEnum.GTE,
    WhereOperatorEnum.LTE: WhereOperatorEnum.GT,
    WhereOperatorEnum.GT: WhereOperatorEnum.LTE,
    WhereOperatorEnum.GTE: WhereOperatorEnum.LT,
    WhereOperatorEnum.EQ: WhereOperatorEnum.NE,
    WhereOperatorEnum.NE: WhereOperatorEnum.EQ,
    WhereOperatorEnum.REGEQ: WhereOperatorEnum.REGNEQ,
    WhereOperatorEnum.REGNEQ: WhereOperatorEnum.REGEQ
}


class Field:
    def __init__(self, field_name):
        self.field_name = field_name

    def __lt__(self, value):
        return Criteria(self, value, WhereOperatorEnum.LT)

    def __le__(self, value):
        return Criteria(self, value, WhereOperatorEnum.LTE)

    def __eq__(self, value):
        return Criteria(self, value, WhereOperatorEnum.EQ)

    def __ne__(self, value):
        return Criteria(self, value, WhereOperatorEnum.NE)

    def __ge__(self, value):
        return Criteria(self, value, WhereOperatorEnum.GTE)

    def __gt__(self, value):
        return Criteria(self, value, WhereOperatorEnum.GT)

    def __regeq__(self, value):
        return Criteria(self, value, WhereOperatorEnum.REGEQ)

    def __regneq__(self, value):
        return Criteria(self, value, WhereOperatorEnum.REGNEQ)

    def __str__(self):
        return self.field_name


class Criteria:
    def __init__(self, left_operand, right_operand, operator):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator

    def __invert__(self):
        inverted_operator = INVERTED_OPERATORS[self.operator]
        return Criteria(
            self.left_operand,
            self.right_operand,
            inverted_operator,
        )

    def __or__(self, criteria):
        return DisjunctionCriteria(self, criteria)

    def evaluate(self):
        left_operand = '"{}"'.format(self.left_operand)
        operator = EVALUATED_OPERATORS[self.operator]
        right_operand = self.right_operand
        if isinstance(right_operand, str):
            if operator in [EVALUATED_OPERATORS[WhereOperatorEnum.REGEQ],
                            EVALUATED_OPERATORS[WhereOperatorEnum.REGNEQ]]:
                right_operand = '/{}/'.format(re.sub('/', '\\/', self.right_operand))
            else:
                right_operand = '\'{}\''.format(self.right_operand)
        return '{} {} {}'.format(left_operand, operator, right_operand)

    def __str__(self):
        return 'CRITERIA: {} {} {}'.format(
            self.left_operand,
            EVALUATED_OPERATORS[self.operator],
            self.right_operand,
        )


class DisjunctionCriteria:
    def __init__(self, left_criteria, right_criteria):
        self.left_criteria = left_criteria
        self.right_criteria = right_criteria

    def __or__(self, criteria):
        return DisjunctionCriteria(self, criteria)

    def evaluate(self):
        left_criteria = '({}'.format(self.left_criteria.evaluate())
        right_criteria = '{})'.format(self.right_criteria.evaluate())
        return ' OR '.join([left_criteria, right_criteria])
