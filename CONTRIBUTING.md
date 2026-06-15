# Contributing to E13 Revival

Thank you for your interest in contributing to the E13 Revival project! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [issue tracker](https://github.com/mathieujobin/e13-revival/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Sample theme files (if applicable)
   - System information (OS, Python version)

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the code style (see below)
   - Add tests for new functionality
   - Update documentation as needed
4. **Test your changes**:
   ```bash
   python3 -m unittest discover tests
   ```
5. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Code Style

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small

Example:
```python
def parse_entry(data: bytes) -> Optional[Dict[str, Any]]:
    """
    Parse a DB entry.
    
    Args:
        data: Raw entry data
        
    Returns:
        Parsed entry dictionary, or None if invalid
    """
    # Implementation
    pass
```

### Documentation

- Use Markdown for documentation files
- Keep lines under 80 characters when possible
- Use clear, concise language
- Include code examples

## Testing

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests.test_parser

# Run with verbose output
python3 -m unittest discover tests -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use unittest framework
- Aim for high code coverage

Example:
```python
import unittest
from pathlib import Path
from imlib_db_parser import ImlibDBParser

class TestFeature(unittest.TestCase):
    def test_something(self):
        # Arrange
        parser = ImlibDBParser(Path('test.db'))
        
        # Act
        result = parser.parse()
        
        # Assert
        self.assertTrue(result)
```

## Project Structure

```
e13-revival/
├── tools/              # Core utilities
│   ├── imlib_db_parser.py    # DB parser library
│   ├── extract_theme.py      # Theme extraction tool
│   └── batch_extract.py      # Batch processing tool
├── tests/              # Unit tests
│   ├── test_parser.py
│   └── create_test_db.py
├── examples/           # Example scripts and sample data
│   ├── analyze_theme.py
│   └── themes/         # Sample theme files
├── README.md           # Main documentation
├── API.md              # API reference
├── INTEGRATION.md      # Integration guide
└── CONTRIBUTING.md     # This file
```

## Adding New Features

### Adding DB Format Support

To add support for a new DB format variant:

1. Add magic number constant in `ImlibDBParser`
2. Implement parser method (e.g., `_parse_v3()`)
3. Add detection in `parse()` method
4. Add tests in `tests/test_parser.py`
5. Update documentation

### Adding Image Format Support

To support a new image format:

1. Add format signature to `_is_image_data()` method
2. Update `_parse_generic()` for format-specific parsing
3. Add extraction logic in `_extract_image()` if needed
4. Add tests with sample images
5. Update documentation

### Adding Extraction Features

To add new extraction features:

1. Extend `ThemeExtractor` class
2. Add command-line arguments if needed
3. Update output format documentation
4. Add tests
5. Update README and INTEGRATION.md

## Documentation

When adding or changing features:

1. **Update README.md** with usage examples
2. **Update API.md** with API changes
3. **Update INTEGRATION.md** if integration changes
4. **Add docstrings** to all new functions/classes
5. **Include examples** in documentation

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check for:
- Code quality and style
- Test coverage
- Documentation completeness
- Backwards compatibility
- Performance impact

## Community

- Be respectful and inclusive
- Help others learn
- Share your use cases
- Contribute documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the GPL-2.0 License.

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Contact the maintainers

Thank you for contributing to E13 Revival!
