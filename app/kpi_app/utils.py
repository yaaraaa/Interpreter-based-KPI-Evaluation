from .models import EvaluationResult
from .interpreter.lexer import Lexer
from .interpreter.parser import Parser
from .interpreter.interpreter import Interpreter
from datetime import datetime
from django.utils import timezone


def evaluate_expression(equation, value):
    equation_with_value = equation.replace("ATTR", str(value))
    lexer = Lexer(equation_with_value)
    parser = Parser(lexer)
    interpreter = Interpreter()
    tree = parser.parse()
    return interpreter.interpret(tree)


def parse_timestamp(timestamp_str):
    """Parse the timestamp from the received format to a valid datetime object."""
    # Remove "[UTC]" and parse with the format Django expects
    cleaned_timestamp = timestamp_str.replace("[UTC]", "").replace("T", " ").replace("Z", "")
    date_time = datetime.strptime(cleaned_timestamp, "%Y-%m-%d %H:%M:%S")
    return timezone.make_aware(date_time)


def evaluate_and_store_result(message, kpi_expression):
    asset_id = message.get("asset_id")
    attribute_id = f"output_{message['attribute_id']}"
    timestamp = parse_timestamp(message["timestamp"])
    value = message["value"]

    result_value = evaluate_expression(kpi_expression, value)

    EvaluationResult.objects.create(
        asset_id=asset_id,
        attribute_id=attribute_id,
        timestamp=timestamp,
        value=result_value
    )
