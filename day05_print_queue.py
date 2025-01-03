import marimo

__generated_with = "0.10.8"
app = marimo.App(width="full", css_file=".git/info/local.css")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Day 5 &mdash; Print Queue

        This problem is about tracking order between objects according to arbitrary precedence rules.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from util import input_editor

    INPUT = input_editor(5)
    mo.accordion({"Input": INPUT})
    return INPUT, input_editor


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part I

        We are given a set of _page ordering rules_, followed with a set of _updates_.
        Each update consists in a set of page numbers that get edited for some reason,
        and whether these updates print in proper order (according to said rules) is in doubt.

        Here's an example:
        """
    )
    return


@app.cell
def _():
    text = """
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """
    return (text,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Rules are separated from updates by an empty line (pair of newlines).
        Then the preceding and following page numbers of a rule are separated by a vertical bar,
        and the page numbers of an update, by commas.
        Parsing this text is a simple string splitting job.

        Let's encode the rules in a dictionary whose values are the set of all pages that the key must precede.
        I will also use a `Page` class to encapsulate integer page numbers.
        This seems like spurious abstraction,
        but integers and page numbers are not strictly the same things.
        Page numbers follow the same ordering rules as integers.
        However, they don't nominally _compose_ in the way integers do.
        """
    )
    return


@app.cell
def _():
    from dataclasses import dataclass
    import functools as ft
    from typing import Any, Self
    return Any, Self, dataclass, ft


@app.cell
def _(Any, Self, dataclass, ft):
    @ft.total_ordering
    @dataclass
    class Page:
        number: int

        @classmethod
        def from_string(cls, s: str) -> Self:
            return cls(number=int(s))

        def __hash__(self) -> int:
            return hash(self.number)

        def __lt__(self, other: Any) -> bool:
            return self.number < int(other)

        def __int__(self) -> int:
            return self.number
    return (Page,)


@app.cell
def _(Page):
    class Update(list[Page]):
        pass
    return (Update,)


@app.cell
def _(Page):
    class RuleSet(dict[Page, set[Page]]):
        pass
    return (RuleSet,)


@app.cell
def _():
    from textwrap import dedent
    return (dedent,)


@app.cell
def _(Page, RuleSet, Update, dedent):
    def parse_rules_updates(text: str) -> tuple[RuleSet, list[Update]]:
        text_rules, text_updates = dedent(text).strip().split("\n\n")

        ruleset = RuleSet()
        for line in text_rules.split("\n"):
            if line.strip():
                p, q = line.split("|")
                ruleset.setdefault(Page.from_string(p), set()).add(Page.from_string(q))

        updates = [
            Update([Page.from_string(p) for p in line.split(",")])
            for line in text_updates.split("\n")
            if line.strip()
        ]

        return ruleset, updates
    return (parse_rules_updates,)


@app.cell
def _(parse_rules_updates, text):
    ruleset, updates = parse_rules_updates(text)
    return ruleset, updates


@app.cell
def _(Page, RuleSet, ruleset):
    _expected = RuleSet(
        {
            Page(29): {Page(13)},
            Page(47): {Page(13), Page(29), Page(53), Page(61)},
            Page(53): {Page(13), Page(29)},
            Page(61): {Page(13), Page(29), Page(53)},
            Page(75): {Page(13), Page(29), Page(47), Page(53), Page(61)},
            Page(97): {Page(13), Page(29), Page(47), Page(53), Page(61), Page(75)},
        }
    )
    _actual = ruleset
    assert _expected == _actual, _actual
    return


@app.cell
def _(Page, Update, updates):
    _expected = [
        Update([Page(75), Page(47), Page(61), Page(53), Page(29)]),
        Update([Page(97), Page(61), Page(53), Page(29), Page(13)]),
        Update([Page(75), Page(29), Page(13)]),
        Update([Page(75), Page(97), Page(47), Page(61), Page(53)]),
        Update([Page(61), Page(13), Page(29)]),
        Update([Page(97), Page(13), Page(75), Page(29), Page(47)]),
    ]
    _actual = updates
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        The first task of this part is to check whether an update is *properly ordered*.
        For that, check each pair $(p, q)$ of page numbers where $q$ comes after $p$ in the sequence.
        If we don't have a direct rule for the pair, it's fine, we ignore it.
        Otherwise, the rules must permit that $q$ be preceded by $p$.
        """
    )
    return


@app.cell
def _():
    from util import add_method
    return (add_method,)


@app.cell
def _(RuleSet, Update, add_method):
    @add_method(Update)
    def is_ordered_properly(self, ruleset: RuleSet) -> bool:
        for i, p in enumerate(self[:-1]):
            for q in self[i + 1 :]:
                if q in ruleset and p in ruleset[q]:
                    return False
        return True
    return (is_ordered_properly,)


@app.cell
def _(ruleset, updates):
    _expected = [True, True, True, False, False, False]
    _actual = [update.is_ordered_properly(ruleset) for update in updates]
    assert _expected == _actual, _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The second task is to get the _middle_ page number of these properly-ordered updates.
        We will assume that each update carries an odd number of pages.
        """
    )
    return


@app.cell
def _(Page, Update, add_method):
    @add_method(Update)
    def page_middle(self) -> Page:
        assert len(self) & 1
        return self[len(self) // 2]
    return (page_middle,)


@app.cell
def _(Page, updates):
    _expected = [Page(61), Page(53), Page(29), Page(47), Page(13), Page(75)]
    _actual = [update.page_middle() for update in updates]
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Putting this all together, we can sum the middle pages of the properly-ordered updates of a given collection.
        Yes, we are now casting pages back as integers for this sum to make sense.
        Sigh.
        """
    )
    return


@app.cell
def _():
    from collections.abc import Iterable
    return (Iterable,)


@app.cell
def _(Iterable, Ruleset, Update):
    def sum_pages_middle_updates_ordered_properly(
        updates: Iterable[Update], ruleset: Ruleset
    ) -> int:
        return sum(
            int(update.page_middle())
            for update in updates
            if update.is_ordered_properly(ruleset)
        )
    return (sum_pages_middle_updates_ordered_properly,)


@app.cell
def _(ruleset, sum_pages_middle_updates_ordered_properly, updates):
    _expected = 143
    _actual = sum_pages_middle_updates_ordered_properly(updates, ruleset)
    assert _expected == _actual
    return


@app.cell
def _(INPUT, parse_rules_updates):
    RULESET, UPDATES = parse_rules_updates(INPUT.value)
    return RULESET, UPDATES


@app.cell
def _(RULESET, UPDATES, mo, sum_pages_middle_updates_ordered_properly):
    mo.md(
        f"Sum of middle pages of properly-ordered updates: **{sum_pages_middle_updates_ordered_properly(UPDATES, RULESET)}**"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part II

        So now we get to fix the misordered updates.
        We can do this by _sorting_ the updates in an order induced from the ruleset.
        So we put together a _comparator_ function based on the ruleset,
        and turn it into a function suitable for the `key` parameter of the [`sorted`](https://docs.python.org/3/library/functions.html#sorted) function with [`functools.cmp_to_key`](https://docs.python.org/3/library/functools.html#functools.cmp_to_key).
        """
    )
    return


@app.cell
def _(Page, Ruleset, Self, Update, add_method, ft):
    @add_method(Update)
    def fix(self, ruleset: Ruleset) -> Self:
        def cmp(left: Page, right: Page) -> int:
            if left in ruleset and right in ruleset[left]:
                return -1
            elif right in ruleset and left in ruleset[right]:
                return 1
            else:
                return 0

        return Update(sorted(self, key=ft.cmp_to_key(cmp)))
    return (fix,)


@app.cell
def _(Page, Update, ruleset, updates):
    _expected = [
        Update([Page(75), Page(47), Page(61), Page(53), Page(29)]),
        Update([Page(97), Page(61), Page(53), Page(29), Page(13)]),
        Update([Page(75), Page(29), Page(13)]),
        Update([Page(97), Page(75), Page(47), Page(61), Page(53)]),
        Update([Page(61), Page(29), Page(13)]),
        Update([Page(97), Page(75), Page(47), Page(29), Page(13)]),
    ]
    _actual = [update.fix(ruleset) for update in updates]
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        So the task here is to sum, once again, the middle page numbers,
        but only for the improperly-ordered updates,
        which should get fixed.
        """
    )
    return


@app.cell
def _(Iterable, RuleSet, Update):
    def sum_pages_middle_updates_fixed(updates: Iterable[Update], ruleset: RuleSet) -> int:
        return sum(
            int(update.fix(ruleset).page_middle())
            for update in updates
            if not update.is_ordered_properly(ruleset)
        )
    return (sum_pages_middle_updates_fixed,)


@app.cell
def _(ruleset, sum_pages_middle_updates_fixed, updates):
    _expected = 123
    _actual = sum_pages_middle_updates_fixed(updates, ruleset)
    assert _expected == _actual, _actual
    return


@app.cell
def _(RULESET, UPDATES, mo, sum_pages_middle_updates_fixed):
    mo.md(
        f"Sum of the middle pages of fixed updates: **{sum_pages_middle_updates_fixed(UPDATES, RULESET)}**"
    )
    return


if __name__ == "__main__":
    app.run()
