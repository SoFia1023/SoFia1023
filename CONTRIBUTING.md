# Contributing to Inspire AI

![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

First off, thank you for considering contributing to Inspire AI! It's people like you that make this project such a great tool for students and educators.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment Setup](#development-environment-setup)
  - [Project Structure](#project-structure)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
  - [JavaScript Styleguide](#javascript-styleguide)
  - [HTML/CSS Styleguide](#htmlcss-styleguide)
  - [Documentation Styleguide](#documentation-styleguide)
- [Testing](#testing)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by the Inspire AI Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project team.

## Getting Started

### Development Environment Setup

1. **Fork the repository**:
   Visit the [Inspire AI repository](https://github.com/yourusername/inspireai) and click the "Fork" button.

2. **Clone your fork**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/inspireai.git
   cd inspireai
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - Windows:

     ```bash
     venv\Scripts\activate
     ```

   - Unix/MacOS:

     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

6. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration settings
   ```

7. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

8. **Populate with sample data (optional)**:

   ```bash
   python manage.py populate_ai_tools
   ```

9. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

10. **Install pre-commit hooks**:

    ```bash
    pre-commit install
    ```

### Project Structure

For an overview of the project structure, refer to the [README.md](README.md) file.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report**:

- Check the [existing issues](https://github.com/yourusername/inspireai/issues) to see if the problem has already been reported.
- Perform a quick search to see if the problem has been reported recently.

**How Do I Submit A Good Bug Report?**:
Bug reports should include:

1. **Use a clear and descriptive title** for the issue.
2. **Describe the exact steps to reproduce the problem** with as much detail as possible.
3. **Provide specific examples** to demonstrate the steps.
4. **Describe the behavior you observed** after following the steps.
5. **Explain which behavior you expected to see instead** and why.
6. **Include screenshots or animated GIFs** if possible.
7. **Include your environment information**: Django version, Python version, browser type and version, OS, etc.
8. **Include any relevant log outputs** (with sensitive information removed).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion**:

- Check the [existing issues](https://github.com/yourusername/inspireai/issues) to see if the enhancement has already been suggested.
- Briefly search to see if the enhancement has already been suggested.

**How Do I Submit A Good Enhancement Suggestion?**:
Enhancement suggestions should include:

1. **Use a clear and descriptive title** for the issue.
2. **Provide a step-by-step description of the suggested enhancement** in as much detail as possible.
3. **Provide specific examples to demonstrate the steps** or point to similar features in other apps.
4. **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
5. **Include screenshots or animated GIFs** if relevant.
6. **Explain why this enhancement would be useful** to most Inspire AI users.
7. **List some other applications where this enhancement exists**, if applicable.

### Your First Code Contribution

Unsure where to begin contributing to Inspire AI? You can start by looking through these `good-first-issue` and `help-wanted` issues:

- [Good First Issues](https://github.com/yourusername/inspireai/labels/good%20first%20issue) - issues that should only require a few lines of code and limited understanding of the system.
- [Help Wanted Issues](https://github.com/yourusername/inspireai/labels/help%20wanted) - issues that are more involved than `good-first-issue`.

### Pull Requests

Follow these steps to have your contribution considered by the maintainers:

1. **Create a branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they adhere to the styleguides.

3. **Write or update tests** as needed.

4. **Run tests** to ensure they pass:

   ```bash
   python manage.py test
   ```

5. **Run linting and formatting checks**:

   ```bash
   pre-commit run --all-files
   ```

6. **Commit your changes** with a descriptive commit message:

   ```bash
   git commit -m "Add feature: brief description of your changes"
   ```

7. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a pull request** from your fork to the main repository.

9. **Title your pull request** clearly and concisely, describing the purpose of your changes.

10. **Fill in the pull request template** with all required information.

11. **Reference any related issues** using the GitHub issue linking (e.g., "Fixes #123").

12. The team will review your pull request as soon as possible.

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 🔒 `:lock:` when dealing with security
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - 💚 `:green_heart:` when fixing CI build
  - ✅ `:white_check_mark:` when adding tests
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies
  - 🔧 `:wrench:` when modifying configuration files

### Python Styleguide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use [Black](https://github.com/psf/black) for code formatting.
- Use [isort](https://github.com/PyCQA/isort) to sort imports.
- Use [flake8](https://flake8.pycqa.org/en/latest/) for linting.
- Write docstrings for all functions, classes, and modules.
- Use type hints where appropriate.

Example:

```python
from typing import List, Optional

def get_ai_tools(category: Optional[str] = None) -> List[dict]:
    """
    Retrieve AI tools, optionally filtered by category.
    
    Args:
        category: Optional category name to filter tools
        
    Returns:
        List of AI tool dictionaries
    """
    # Implementation goes here
    pass
```

### JavaScript Styleguide

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Use ESLint with the provided configuration.
- Prefer ES6+ features where appropriate.
- Comment complex code sections.

### HTML/CSS Styleguide

- Use Bootstrap 5 classes where possible.
- Write semantic HTML.
- Use CSS variables for theme colors and dimensions.
- Follow BEM (Block Element Modifier) naming convention for custom CSS classes.

### Documentation Styleguide

- Use Markdown for documentation.
- Include code examples where appropriate.
- Keep documentation up-to-date with code changes.
- Document both the "what" and the "why".

## Testing

- Write tests for all new features and bug fixes.
- Ensure all tests pass before submitting a pull request.
- Aim for high test coverage.

**Running Tests**:

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test catalog

# Run a specific test class
python manage.py test catalog.tests.TestAIToolModel

# Generate coverage report
coverage run --source='.' manage.py test
coverage report
```

---

Thank you for contributing to Inspire AI! Together, we can create an amazing platform for AI tool discovery and education.
