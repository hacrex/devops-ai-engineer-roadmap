# Contributing to 12 Days of AI Infrastructure

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Content Guidelines](#content-guidelines)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

---

## Code of Conduct

Please be respectful and inclusive. We welcome contributors of all backgrounds and skill levels.

### Our Pledge
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Gracefully accept constructive criticism
- Focus on what's best for the community

---

## How to Contribute

### Types of Contributions

**1. Content Improvements**
- Fix typos or clarify explanations
- Add code examples
- Update outdated information
- Create new labs or exercises

**2. Bug Fixes**
- Report issues via GitHub Issues
- Fix broken code examples
- Correct configuration files

**3. New Features**
- Add new days/topics (coordinate with maintainers first)
- Create additional lab exercises
- Add support for new tools/frameworks

**4. Documentation**
- Improve README files
- Add troubleshooting guides
- Translate content to other languages

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating an issue, include:

- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots/logs if applicable

**Example:**
```markdown
**Issue:** Day 03 example script fails with ImportError

**Steps to Reproduce:**
1. cd day03-python-automation/examples
2. python automation_examples.py

**Expected:** Script runs successfully
**Actual:** ModuleNotFoundError: No module named 'requests'

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.12
- venv activated: Yes
```

### Suggesting Enhancements

Enhancement suggestions should include:
- Clear description of the proposed change
- Rationale (why this improvement is needed)
- Examples or mockups if applicable
- Potential impact on existing content

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/12-days-series.git
cd 12-days-series
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks (optional but recommended)
pre-commit install
```

### 3. Create a Branch

```bash
# Always create a new branch for your changes
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 4. Make Your Changes

- Follow the [Content Guidelines](#content-guidelines)
- Test your changes locally
- Ensure all examples run correctly

### 5. Run Tests (if applicable)

```bash
# Run any available tests
pytest tests/

# Validate markdown links
markdown-link-check README.md
```

---

## Content Guidelines

### README Structure

Each day's README should follow this structure:

```markdown
# Day XX: Topic Title

## Overview
[Brief description of what will be covered]

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Prerequisites
- Required knowledge
- Required tools/software

## Core Concepts
[Detailed explanation of key concepts]

## Hands-On Examples
[Working code examples with explanations]

## Lab Exercises
[Exercises for learners to complete]

## Knowledge Check
[Questions to verify understanding]

## Additional Resources
[Links to documentation, articles, videos]
```

### Code Example Standards

**Good Example:**
```python
"""
Example: Basic Container Operations
Demonstrates pulling, running, and managing containers
"""

import docker

def main():
    # Initialize Docker client
    client = docker.from_env()
    
    # Pull image
    print("Pulling alpine:latest...")
    client.images.pull('alpine', tag='latest')
    
    # Run container
    container = client.containers.run(
        'alpine:latest',
        command='echo "Hello from container!"',
        detach=False
    )
    print(container.decode())

if __name__ == '__main__':
    main()
```

**Guidelines:**
- Include docstrings explaining purpose
- Use meaningful variable names
- Add comments for complex logic
- Handle errors appropriately
- Include `if __name__ == '__main__':` blocks
- Test all examples before submitting

### Lab Exercise Format

```markdown
## Lab 1: [Lab Title]

### Objective
[What learners will accomplish]

### Duration
[Estimated time: 15-30 minutes]

### Instructions
1. Step one
2. Step two
3. Step three

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Starter Code
[Provide starting point if needed]

### Hints
- Hint 1
- Hint 2

### Solution
[Link to solution file or section]
```

---

## Pull Request Process

### Before Submitting

1. **Test your changes**
   - Run all code examples
   - Verify links work
   - Check for typos

2. **Update documentation**
   - Update README if adding features
   - Add/update CHANGELOG entries

3. **Ensure consistency**
   - Follow existing style
   - Match folder structure
   - Use consistent formatting

### Creating a PR

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "type: descriptive message"
   
   # Commit message types:
   # feat: New feature
   # fix: Bug fix
   # docs: Documentation only
   # style: Formatting changes
   # refactor: Code restructuring
   # test: Adding tests
   # chore: Maintenance tasks
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template

### PR Template

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Content improvement
- [ ] Other (please describe)

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have tested my changes
- [ ] I have updated documentation accordingly
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works

## Related Issues
Closes #XXX (if applicable)

## Screenshots/Examples
[If applicable]
```

### Review Process

1. Maintainers will review your PR
2. Feedback may be provided
3. Make requested changes
4. Once approved, PR will be merged

**Response Time:** We aim to review PRs within 1 week

---

## Style Guide

### Markdown Style

- Use ATX-style headers (`#` not `<h1>`)
- Use backticks for inline code: `code`
- Use fenced code blocks with language specification
- Keep lines under 80 characters when possible
- Use hyphens for unordered lists
- Use numbers for ordered lists

**Good:**
```markdown
## Section Title

This is a paragraph with `inline code`.

```python
def example():
    return "code block"
```

- List item 1
- List item 2
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 88 characters
- Use f-strings for string formatting

**Bash:**
- Use `shellcheck` for validation
- Quote variables: `"$var"`
- Use functions for reusable code

**YAML:**
- Use 2-space indentation
- Quote strings when necessary
- Keep structure flat when possible

### File Naming

- Use lowercase with hyphens: `my-file.py`
- Descriptive names: `basic_agent.py` not `agent1.py`
- Prefix lab files: `lab1_topic.py`
- Prefix solution files: `solution_lab1.py`

### Folder Structure

```
dayXX-topic/
├── README.md           # Main content
├── CHECKLIST.md        # Learning checklist
├── examples/           # Working examples
│   └── example_name.py
├── labs/               # Lab exercises
│   └── lab1_name/
│       └── starter.py
├── solutions/          # Solutions
│   └── lab1_solution.py
└── resources/          # Additional resources
    └── README.md
```

---

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Repository README (for significant contributions)

### Top Contribution Areas
1. Content quality improvements
2. New lab exercises
3. Bug fixes
4. Documentation enhancements
5. Community support

---

## Questions?

Need help? Reach out via:
- GitHub Discussions
- Open an issue
- Contact maintainers

Thank you for contributing to make AI infrastructure education better for everyone! 🚀
