from collections import Counter
import sys
from tabulate import tabulate

# Could be replaced by automatic parsing if we 100% sure that log format stays the same
# Pagination of output for big files is skiped intentionally to not overload the code 

"""Supported log levels, in display order."""
LOG_LEVELS = ("INFO", "ERROR", "WARNING", "DEBUG")


def row_generator(path):
    """Yield stripped lines from a file one at a time.

    Args:
        path: Path to the log file.

    Yields:
        str: Each line with leading/trailing whitespace removed.
    """
    try:
        with open(path, "r") as file:
            for line in file:
                yield line.strip()
    except IsADirectoryError:
        print(f"Path {path} is a directory not a file")
    except FileNotFoundError:
        print(f"File not found: {path}")


def count_logs(argv, level_filter=None):
    """Parse the log file and count entries per level.

    Reads the file lazily via row_generator. Only stores full lines
    for the requested level_filter to minimise memory usage.

    Args:
        argv: Argument list where argv[1] is the path to the log file.
        level_filter: Optional uppercase log level (e.g. "ERROR") whose
            lines should be collected. If None, no lines are stored.

    Returns:
        tuple[Counter, list[str]]: A counter of occurrences per level
            and a list of lines matching level_filter (empty if None).
    """
    counts = Counter()
    filtered_lines = []

    for line in row_generator(argv[1]):
        level = next((lvl for lvl in LOG_LEVELS if lvl in line.upper()), None)
        if level:
            counts[level] += 1
            if level == level_filter:
                filtered_lines.append(line)

    return counts, filtered_lines


def main(argv):
    """Entry point: validate arguments, parse the log file, and print results.

    Usage:
        python task_3.py <path_to_log_file> [log_level]

    Args:
        argv: Command-line arguments (sys.argv).
    """
    if len(argv) < 2:
        print("Path to log file is not specified.")
        return

    level_filter = None
    if len(argv) > 2:
        level_filter = argv[2].upper()
        if level_filter not in LOG_LEVELS:
            print(f"Unknown log level: {level_filter}. Valid levels: {', '.join(LOG_LEVELS)}")

    counts, filtered_lines = count_logs(argv, level_filter)
    if counts:
        table = [[lvl, counts[lvl]] for lvl in LOG_LEVELS if lvl in counts]
        print("\n")
        print(tabulate(table, headers=["LOG LEVEL", "RECORDS COUNT"], tablefmt="grid"), "\n")
    if level_filter:
        if filtered_lines:
            print(f"\nRecords with log level {level_filter}:\n")
            print("\n".join(filtered_lines))
        else:
            print(f"\nThere is no records with {level_filter} log level\n")


if __name__ == "__main__":
    main(sys.argv)
