# Evals for the agent skills

These cases check that an agent writes correct Ludic code with the skills in
`skills/`, and how much the skills help compared to an agent without them. They
run with [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals).

Each case is a directory with a `case.yaml` (the prompt and the graders) and a
`setup.sh` that writes the starting project into the empty workspace: a
`pyproject.toml` that pins the Ludic version, and for some cases an existing
`app.py` or `components.py` to change.

- `components/` – the `ludic-components` skill: t-strings, escaping, the
  catalog, themes and the Ludic 0.5 version check.
- `web/` – the `ludic-web` skill: `LudicApp`, `Endpoint`, `Parser`, htmx and
  FastAPI.

## Run

From the root of the repository:

```bash
claude plugin eval . --scaffold --allow-tools Write Edit
```

- `--scaffold` runs the `setup.sh` scripts. They only write files.
- `--allow-tools Write Edit` lets the agent write code. The agent has no Bash, so
  it cannot install Ludic or run mypy; the graders read the files it writes.
- Every case runs 3 times with the plugin and 3 times without it, so the report
  shows the difference the skills make. For a quick check, add `--runs 1`, or
  run one case with `--case inline-markup`. `--max-cost-usd` sets a budget.

Results go to `evals/results/`, which is not tracked.

## Graders

There are no graders that run code, so most graders are regular expressions
(JavaScript syntax) on the files the agent writes. They look for the mistakes
the skills warn about:

- elements put into f-strings or `str()`, which renders them as escaped text;
- `Safe`, `Markup` or `mark_safe` around user input;
- absolute URLs from `url_for` in htmx attributes (host header poisoning);
- hand-written HTML documents, layout CSS, button CSS or dark mode scripts
  where the catalog and the theme have a component or an option;
- t-strings in a project on Ludic 0.5.

The checks for the first two mistakes have weight 3. `user-comments` also has
an LLM grader, because line breaks can be kept safely in more than one way.

The `skill-fired` graders show whether the agent loaded the skill. They are not
part of the score.

When you add a case, check its graders on a correct and on a wrong solution
before running it: a pattern that never matches makes both arms pass.
