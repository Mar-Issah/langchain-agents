from langchain_core.tools import tool


# 	TOOLS FOR BASIC CALCULATOR BELOW
@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' and 'y'."""
    return x * y


@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the power of 'y'."""
    return x**y


@tool
def subtract(x: float, y: float) -> float:
    """Subtract 'x' from 'y'."""
    return y - x


@tool
def divide(x: float, y: float) -> float:
    """Divide 'y' by 'x'."""
    if x == 0:
        raise ValueError("Cannot divide by zero.")
    return y / x


# END OF TOOLS FOR BASIC CALCULATOR BELOW
