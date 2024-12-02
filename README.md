# Advent of Code 2024

This repository presents my solutions for some of the [Advent of Code 2024](https://adventofcode.com/2024) problems.
I focus in particular on leveraging [NumPy](https://numpy.org/) as the primary tool in my box to formulate these solutions.

## Setup

I use [Conda](https://docs.conda.io/en/latest/) to manage my computing environment.
Once one has [Miniconda](https://docs.anaconda.com/miniconda/)
[installed](https://docs.anaconda.com/miniconda/install/#quick-command-line-install),
just run

```sh
conda env create
conda activate advent-of-code-2024
```

## Development process

I use the [Helix](https://helix-editor.com/) text editor with terminal multiplexing from [Tmux](https://github.com/tmux/tmux/wiki).
Most of my code writing is done by writing unit and integration tests that I then run on a side terminal with
[pytest](https://docs.pytest.org/en/stable/#).

```sh
pytest
```

My text editor is configured to leverage [Flake8](https://flake8.pycqa.org/en/latest/) for code styling,
as well as the [Python LSP](https://github.com/python-lsp/python-lsp-server) for code hinting.
These development support tools are deployed as part of the Conda environment.
