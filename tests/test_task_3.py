import pytest
from collections import Counter

from tasks.task_3 import row_generator, count_logs

SAMPLE_LINES = [
    "2024-01-22 08:30:01 INFO User logged in successfully.",
    "2024-01-22 09:00:45 ERROR Database connection failed.",
    "2024-01-22 10:30:55 WARNING Disk usage above 80%.",
    "2024-01-22 11:05:00 DEBUG Starting data backup process.",
    "2024-01-22 11:30:15 ERROR Backup process failed.",
]


@pytest.fixture
def log_file(tmp_path):
    f = tmp_path / "test.log"
    f.write_text("\n".join(SAMPLE_LINES))
    return f


# --- row_generator ---


def test_row_generator_yields_all_lines(log_file):
    assert list(row_generator(str(log_file))) == SAMPLE_LINES


def test_row_generator_strips_whitespace(tmp_path):
    f = tmp_path / "test.log"
    f.write_text("  padded line  \n")
    assert list(row_generator(str(f))) == ["padded line"]


def test_row_generator_file_not_found(capsys):
    list(row_generator("nonexistent_file.log"))
    assert "File not found" in capsys.readouterr().out


def test_row_generator_path_is_directory(tmp_path, capsys):
    list(row_generator(str(tmp_path)))
    assert "is a directory" in capsys.readouterr().out


def test_row_generator_empty_file(tmp_path):
    f = tmp_path / "empty.log"
    f.write_text("")
    assert list(row_generator(str(f))) == []


# --- count_logs ---


def test_count_logs_counts_all_levels(log_file):
    counts, _ = count_logs(["script", str(log_file)])
    assert counts["INFO"] == 1
    assert counts["ERROR"] == 2
    assert counts["WARNING"] == 1
    assert counts["DEBUG"] == 1


def test_count_logs_total_equals_line_count(log_file):
    counts, _ = count_logs(["script", str(log_file)])
    assert sum(counts.values()) == len(SAMPLE_LINES)


def test_count_logs_no_filter_returns_empty_list(log_file):
    _, filtered = count_logs(["script", str(log_file)])
    assert filtered == []


def test_count_logs_filter_returns_correct_count(log_file):
    _, filtered = count_logs(["script", str(log_file)], level_filter="ERROR")
    assert len(filtered) == 2


def test_count_logs_filter_unknown_level_returns_empty(log_file):
    _, filtered = count_logs(["script", str(log_file)], level_filter="CRITICAL")
    assert filtered == []


def test_count_logs_lines_without_level_are_skipped(tmp_path):
    f = tmp_path / "mixed.log"
    f.write_text(
        "2024-01-22 08:30:01 INFO Valid line.\n"
        "This line has no recognisable log level.\n"
    )
    counts, _ = count_logs(["script", str(f)])
    assert sum(counts.values()) == 1
