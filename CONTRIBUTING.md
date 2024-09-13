## Contributing

Any contributions to the framework are warmly welcome! Your help will make it a better resource for the community. If you're ready to contribute, here's how to get started.

### Set Up Pre-Commit Hooks

Before submitting code, set up pre-commit hooks to ensure code quality and consistency. Instructions on how to do this should be included in your project's setup documentation.

```bash
python -m pip install pre-commit
pre-commit install --install-hooks
```

### Code Changes

If you're adding new features or fixing bugs, please include tests that cover your changes. Run `pytest` to execute the test suite.

You need to install test dependencies to be able to run `pytest`:

```bash
python -m pip install -e ".[full,test]"
```

You can also use `hatch` which automatically creates virtual environment with all the optional dependencies:

```bash
hatch shell
```

### Documentation Updates

We use MkDocs for documentation. To make changes to the documentation:

- Install MkDocs if you don't already have it with `pip install mkdocs-material`.
- Make your edits to the Markdown files within the documentation directory.
- Run `mkdocs serve` to preview your changes.

### Create a Pull Request

- Fork the repository and create a new branch for your feature or bug fix.
- Push your changes to your branch.
- Create a pull request, providing a brief description of your changes and why they are important if needed.
