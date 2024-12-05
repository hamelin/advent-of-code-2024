from . import (
    INPUT,
    iter_middle_page_updates_fixed,
    iter_middle_page_updates_valid,
    parse_full_text
)


if __name__ == "__main__":
    rules, updates = parse_full_text(INPUT)
    print(
        "Sum of middle pages of valid updates:",
        sum(iter_middle_page_updates_valid(rules, updates))
    )
    print(
        "Sum of middle pages of fixed updates:",
        sum(iter_middle_page_updates_fixed(rules, updates))
    )
