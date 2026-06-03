# Contributing to DevOps AI Engineer Roadmap

Thank you for your interest in contributing! This guide will help you get started.

## 🎯 How to Contribute

### 1. Report Bugs
- Check existing issues first
- Use the bug report template
- Include: Python version, OS, steps to reproduce, expected vs actual behavior

### 2. Suggest Features
- Open a feature request issue
- Describe the use case and benefits
- Wait for maintainer feedback before implementing

### 3. Submit Code Changes

#### For Small Fixes (typos, documentation):
1. Fork the repository
2. Create a branch: `git checkout -b fix/typo-readme`
3. Make changes
4. Commit with clear message: `docs: fix typo in QUICKSTART.md`
5. Push and open a PR

#### For Larger Changes:
1. Open an issue to discuss the change
2. Fork and create feature branch: `git checkout -b feature/add-new-module`
3. Follow coding standards below
4. Add/update tests
5. Update documentation
6. Submit PR with detailed description

## 📝 Coding Standards

### Python Code
- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where possible
- Keep functions under 50 lines
- Add docstrings to public functions
- Maximum line length: 100 characters

```python
def check_port_open(host: str, port: int) -> bool:
    """Check if a specific port is open on the given host.
    
    Args:
        host: The hostname or IP address
        port: The port number to check
        
    Returns:
        True if port is open, False otherwise
    """
    # Implementation here
    pass
```

### Documentation
- Use Markdown for all `.md` files
- Include code examples with expected output
- Add screenshots for UI components (as SVG/PNG)
- Keep README files under 500 lines (split into separate docs if larger)

### Project Structure
Each project should have:
```
project-name/
├── README.md          # Project overview with usage examples
├── requirements.txt   # Python dependencies
├── Makefile          # Common commands (test, run, clean)
├── src/              # Source code (if complex)
├── tests/            # Test suite
├── examples/         # Usage examples
└── docker-compose.yml # If containerized
```

## 🧪 Testing Requirements

### Before Submitting PR:
- [ ] All existing tests pass: `make test`
- [ ] New code has test coverage (>80%)
- [ ] No linting errors: `make lint`
- [ ] Documentation updated
- [ ] Examples tested end-to-end

### Running Tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v --cov=src

# Run specific test file
pytest tests/test_copilot.py -v

# Check code coverage
coverage report -m
```

## 📚 Adding New Learning Modules

When adding to `12-days-series/`:

1. Create directory: `dayXX-topic-name/`
2. Include:
   - `README.md` with learning objectives
   - `CHECKLIST.md` with interactive tasks
   - `lab/` directory with hands-on exercises
   - `solutions/` directory with answers
3. Update main series README
4. Add to learning path diagram

## 🎨 Adding Diagrams

- Use draw.io, Excalidraw, or Mermaid
- Export as both `.svg` (for web) and `.png` (for GitHub preview)
- Store in `diagrams/` directory at project root
- Reference in documentation with relative paths
- Include source files for future edits

Example:
```markdown
![Architecture](./diagrams/rag-architecture.mmd)
```

## 🔀 Pull Request Process

1. **Title Format:** `[TYPE] Brief description`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   
2. **Description Template:**
```markdown
## What does this PR do?
Brief description

## Why is this needed?
Problem statement

## How was it tested?
Testing approach and results

## Screenshots (if applicable)
Add images for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

3. **Review Process:**
   - Maintainer reviews within 48 hours
   - Address feedback promptly
   - CI/CD checks must pass
   - Minimum 1 approval required

## 🌟 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Tagged in related announcements

## ❓ Questions?

- Open a discussion in GitHub Discussions
- Check existing issues for similar questions
- Join our community chat (link TBD)

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We welcome contributors of all backgrounds and skill levels. Harassment, discrimination, or hostile behavior will not be tolerated.

---

**Thank you for making this roadmap better for everyone!** 🙏

Every contribution matters, whether it's fixing a typo, adding a test, or creating a new module.
