from src.tools.calculator import calculator_tool


# 1. 기본 곱셈
def test_basic_multiplication():

    result = calculator_tool("125 * 48")

    assert result["success"] is True
    assert result["result"] == 6000


# 2. 괄호 + 나눗셈
def test_parentheses_and_division():

    result = calculator_tool("(100 + 25) / 5")

    assert result["success"] is True
    assert result["result"] == 25.0


# 3. 거듭제곱
def test_power():

    result = calculator_tool("2 ** 10")

    assert result["success"] is True
    assert result["result"] == 1024


# 4. 문자 입력 거부
def test_reject_text():

    result = calculator_tool("hello * world")

    assert result["success"] is False
    assert "error" in result


# 5. 함수 호출 거부
def test_reject_function_call():

    result = calculator_tool(
        "__import__('os').system('echo hacked')"
    )

    assert result["success"] is False
    assert "error" in result


# 6. 리스트 표현식 거부
def test_reject_list():

    result = calculator_tool("[1, 2, 3]")

    assert result["success"] is False
    assert "error" in result


# 7. 0으로 나누기 안전 처리
def test_division_by_zero():

    result = calculator_tool("100 / 0")

    assert result["success"] is False
    assert "error" in result
