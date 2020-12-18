import sys


################
# AST building #
################


def to_ast_item(expression):
    if expression.isdigit():
        return {'type': 'number', 'value': int(expression)}
    elif expression in ['+', '*']:
        return {'type': 'operator', 'value': 'add' if expression == '+' else 'mul'}


def find_end_parenthesis_index(expression, start_index):
    index = start_index
    stack = 0

    while index < len(expression):
        if expression[index] in ['(', ')']:
            stack += 1 if expression[index] == '(' else -1

        if stack == 0:
            break

        index += 1

    return index


def parse_ast_value(expression):
    start_index = 0
    end_index = 0

    while end_index < len(expression):
        char = expression[end_index]

        if char == ' ':
            yield to_ast_item(expression[start_index:end_index])
            start_index = end_index + 1
        elif char == '(':
            start_parenthesis_index = end_index
            end_parenthesis_index = find_end_parenthesis_index(
                expression, end_index)
            yield to_ast(expression[start_parenthesis_index + 1:end_parenthesis_index])
            start_index = end_parenthesis_index + 2
            end_index = end_parenthesis_index + 1

        end_index += 1

    if start_index < len(expression):
        yield to_ast_item(expression[start_index:end_index])


def to_ast(expression):
    return {'type': 'ast', 'value': parse_ast_value(expression)}


#########
# Debug #
#########

def print_ast(ast, indent=0):
    for item in ast['value']:
        if item['type'] == 'ast':
            print('{}ast:'.format(''.rjust(indent)))
            print_ast(item, indent + 2)
        else:
            print('{}{}: {}'.format(''.rjust(indent),
                                    item['type'], item['value']))


##############
# Assertions #
##############


def assert_value(item):
    assertion = item['type'] in ['number', 'ast']
    message = 'Expected number or AST, got {}'.format(item['type'])
    assert assertion, message


def assert_operator(item):
    assertion = item['type'] == 'operator'
    message = 'Expected operator, got {}'.format(item['type'])
    assert assertion, message


def assert_ast(item):
    assertion = item['type'] == 'ast'
    message = 'Can\'t compute non AST type: {}'.format(item['type'])
    assert assertion, message


###############
# Compute AST #
###############


def get_value(item, add_first=False):
    assert_value(item)
    return item['value'] if item['type'] == 'number' else compute_ast(item, add_first)


def get_operator(item):
    assert_operator(item)
    return item['value']


def apply_operator(left_value, operator, item, add_first=False):
    right_value = get_value(item, add_first)
    return left_value + right_value if operator == 'add' else left_value * right_value


def rewrite_ast_value_without_add(ast_value):
    operator = None
    left_value = None

    for item in ast_value:
        if left_value is None:
            left_value = get_value(item, add_first=True)
        elif operator is None:
            operator = get_operator(item)

            if operator == 'mul':
                yield {'type': 'number', 'value': left_value}
                yield item
                left_value = None
                operator = None
        else:
            left_value = apply_operator(
                left_value, operator, item, add_first=True)
            operator = None

    yield {'type': 'number', 'value': left_value}


def rewrite_ast_without_add(ast):
    return {'type': 'ast', 'value': rewrite_ast_value_without_add(ast['value'])}


def compute_ast(ast, add_first=False):
    assert_ast(ast)

    operator = None
    left_value = None

    for item in (rewrite_ast_without_add(ast) if add_first else ast)['value']:
        if left_value is None:
            left_value = get_value(item, add_first)
        elif operator is None:
            operator = get_operator(item)
        else:
            left_value = apply_operator(left_value, operator, item, add_first)
            operator = None

    return left_value


def compute(expression, add_first=False):
    return compute_ast(to_ast(expression), add_first)


def compute_sum(expressions, add_first=False):
    return sum([
        compute(expression, add_first)
        for expression in expressions
    ])


if __name__ == '__main__':
    expressions = sys.stdin.read().replace('\r', '').split('\n')

    print('solution 1:', compute_sum(expressions))
    print('solution 2:', compute_sum(expressions, add_first=True))
