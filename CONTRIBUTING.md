# Contributing to E13 Revival

Thank you for your interest in contributing to the E13 Revival project! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch for your changes
4. Make your changes following our coding standards
5. Test your changes thoroughly
6. Submit a pull request

## Development Environment Setup

### Required Tools

- CMake 3.16+
- C++ compiler with C++17 support (GCC 7+, Clang 5+, MSVC 2017+)
- Git

### Required Libraries

- Qt5 (Core, Gui, Widgets)
- KDE Frameworks 5:
  - KConfig
  - KCoreAddons
  - KGuiAddons
  - KI18n
- KDecoration2
- KWin

### Building for Development

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install cmake extra-cmake-modules qtbase5-dev \
    libkf5config-dev libkf5coreaddons-dev libkf5guiaddons-dev \
    libkf5i18n-dev kdecoration-dev kwin-dev git

# Clone and build
git clone https://github.com/mathieujobin/e13-revival.git
cd e13-revival
./build.sh
```

## Code Style

### C++ Guidelines

- Follow the existing code style in the project
- Use 4 spaces for indentation (no tabs)
- Use `camelCase` for variable and function names
- Use `PascalCase` for class names
- Keep line length under 120 characters when reasonable
- Use modern C++17 features appropriately

### File Organization

- Header files (`.h`) should include include guards
- Implementation files (`.cpp`) should include their header first
- Group includes: system headers, then Qt headers, then KDE headers, then local headers
- Use forward declarations when possible to reduce compile times

### Example Code Style

```cpp
#include "myclass.h"

#include <KDecoration2/Decoration>

#include <QPainter>
#include <QString>

namespace E13
{

MyClass::MyClass(QObject *parent)
    : QObject(parent)
    , m_someVariable(0)
{
}

void MyClass::someMethod()
{
    if (condition) {
        // do something
    }
    
    for (const auto &item : collection) {
        processItem(item);
    }
}

} // namespace E13
```

## Testing Changes

### Manual Testing

1. Build and install the decoration
2. Activate it in KWin
3. Test the following scenarios:
   - Window creation and destruction
   - Window activation/deactivation
   - Maximize/restore operations
   - Minimize operations
   - Window moving and resizing
   - Theme switching
   - Different button layouts
   - Multiple monitor setups

### Checklist

Before submitting a pull request, ensure:

- [ ] Code compiles without warnings
- [ ] Changes follow the existing code style
- [ ] Manual testing completed successfully
- [ ] Documentation updated if needed
- [ ] No unnecessary files committed (build artifacts, etc.)

## Areas for Contribution

### High Priority

- Additional theme presets
- Configuration UI (KCM module)
- Performance optimizations
- Better support for HiDPI displays
- Wayland-specific improvements

### Medium Priority

- Animated transitions
- Custom button icon support
- Advanced shadow rendering
- Window blur effects
- Accessibility improvements

### Low Priority

- Additional color schemes
- Documentation translations
- Example configurations
- Video tutorials

## Submitting Changes

### Pull Request Process

1. Update documentation for any user-facing changes
2. Add a clear description of the changes in the PR
3. Reference any related issues
4. Be prepared to address review feedback

### PR Description Template

```markdown
## Description
Brief description of what this PR does

## Motivation
Why is this change needed?

## Changes Made
- List of changes
- Another change

## Testing
How was this tested?

## Screenshots (if applicable)
Add screenshots for visual changes
```

## Bug Reports

### Before Reporting

1. Check if the bug is already reported
2. Try to reproduce with the latest version
3. Check if it's a KWin issue vs. decoration issue

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- KDE Plasma version:
- KWin version:
- Qt version:
- Distribution:
- E13 decoration version:

**Logs**
Relevant log output from `journalctl -xe | grep kwin`
```

## Feature Requests

We welcome feature suggestions! Please:

1. Check if the feature is already requested
2. Explain the use case
3. Describe the expected behavior
4. Provide mockups if applicable

## Code Review

All submissions require review. We aim to:

- Review PRs within 1 week
- Provide constructive feedback
- Help contributors improve their changes

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.

## Questions?

- Open an issue for general questions
- Join discussions in existing issues
- Check the README for common questions

## Recognition

Contributors will be recognized in:

- Git commit history
- Release notes for significant contributions
- Project documentation

Thank you for contributing to E13 Revival!
