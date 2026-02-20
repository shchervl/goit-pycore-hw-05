from decimal import Decimal

from tasks.task_2 import generator_numbers, sum_profit


# --- generator_numbers ---


def test_generator_yields_all_floats():
    text = "Values: 1000.01 and 27.45 and 324.00"
    result = list(generator_numbers(text))
    assert result == [Decimal("1000.01"), Decimal("27.45"), Decimal("324.00")]


def test_generator_yields_decimal_type():
    text = "Amount: 42.50"
    values = list(generator_numbers(text))
    assert len(values) == 1
    assert isinstance(values[0], Decimal)


def test_generator_empty_text():
    assert list(generator_numbers("")) == []


def test_generator_no_floats_integers_only():
    text = "There are 3 items and 10 boxes"
    assert list(generator_numbers(text)) == []


def test_generator_ignores_numbers_embedded_in_words():
    # word boundary (\b) prevents matching numbers glued to letters
    text = "abc123.45xyz and normal 6.78 value"
    assert list(generator_numbers(text)) == [Decimal("6.78")]


def test_generator_single_float():
    text = "Only 99.99 here"
    assert list(generator_numbers(text)) == [Decimal("99.99")]


# --- sum_profit ---


def test_sum_profit_example_text():
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    assert sum_profit(text, generator_numbers) == Decimal("1351.46")


def test_sum_profit_empty_text():
    assert sum_profit("", generator_numbers) == Decimal("0.00")


def test_sum_profit_no_floats():
    assert sum_profit("no numbers here at all", generator_numbers) == Decimal("0.00")


def test_sum_profit_single_number():
    assert sum_profit("Profit: 500.75", generator_numbers) == Decimal("500.75")


def test_sum_profit_rounds_half_up():
    # 0.005 rounded to 2 decimal places:
    #   ROUND_HALF_UP  → 0.01
    #   ROUND_HALF_EVEN → 0.00 (0 is even)
    assert sum_profit("0.005", generator_numbers) == Decimal("0.01")


def test_sum_profit_custom_generator():
    def fixed_generator(_text):
        yield Decimal("10.00")
        yield Decimal("20.00")
        yield Decimal("30.00")

    assert sum_profit("ignored", fixed_generator) == Decimal("60.00")
