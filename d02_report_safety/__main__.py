from . import (
    count_reports_safe,
    count_reports_safe_with_pd,
    reports_input
)


if __name__ == "__main__":
    print("Number of safe reports:", count_reports_safe(reports_input))
    print(
        "Number of safe reports with Problem Dampener:",
        count_reports_safe_with_pd(reports_input)
    )
