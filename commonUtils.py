# Class to model bounding box rectangle
class Rectangle:
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

# Class to store prediction result
class Result:
    def __init__(self, name, score, ms):
        self.Name = name
        self.Score = score
        self.Time = ms

    def display(self):
        print("Recognized Gesture: {}, Confidence Score:{}, Time:{}".format(self.Name, self.Score, self.Time))

    def getResult(self):
        return self.Name, self.Score, self.Time
    
def evaluate_math_expression(expression):
    """
    Evaluates a given mathematical expression represented as a list of strings.

    Args:
        expression (list): List of strings representing a mathematical expression.

    Returns:
        float: The result of evaluating the mathematical expression.
    """
    stack = []
    operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def apply_operator(operators_stack, values_stack):
        """Applies an operator on top of the operator stack to the values stack."""
        operator = operators_stack.pop()
        right = values_stack.pop()
        left = values_stack.pop()

        if operator == '+':
            result = left + right
        elif operator == '-':
            result = left - right
        elif operator == '*':
            result = left * right
        elif operator == '/':
            result = left / right
        elif operator == '^':
            result = left ** right

        values_stack.append(result)

    for token in expression:
        if token.isdigit() or token.replace('.', '').isdigit():
            stack.append(float(token))
        elif token in operators:
            while (stack and stack[-1] != '(' and
                   operators.get(token, 0) <= operators.get(stack[-1], 0)):
                apply_operator(stack, stack)
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack[-1] != '(':
                apply_operator(stack, stack)
            stack.pop()

    while stack:
        apply_operator(stack, stack)

    return stack[0] if stack else 0.0  # Return 0.0 if the stack is empty
