import ast
import operator


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculator_tool(expression):
    """Safely evaluate a basic mathematical expression."""

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )

        if isinstance(node, ast.BinOp):

            operator_type = type(node.op)

            if operator_type not in ALLOWED_OPERATORS:
                raise ValueError(
                    "Operator is not allowed."
                )

            left = evaluate(node.left)
            right = evaluate(node.right)

            return ALLOWED_OPERATORS[
                operator_type
            ](
                left,
                right
            )

        if isinstance(node, ast.UnaryOp):

            operator_type = type(node.op)

            if operator_type not in ALLOWED_OPERATORS:
                raise ValueError(
                    "Operator is not allowed."
                )

            return ALLOWED_OPERATORS[
                operator_type
            ](
                evaluate(node.operand)
            )

        raise ValueError(
            "Expression is not allowed."
        )

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = evaluate(tree)

        return {
            "success": True,
            "expression": expression,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "expression": expression,
            "error": str(e)
        }
