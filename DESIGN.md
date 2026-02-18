# E13 Revival Window Decoration - Visual Design

## Window Structure

```
┌─────────────────────────────────────────────────────────────┐
│ [☰] Window Title                              [_] [□] [×]   │ ← Title Bar (24px)
├─────────────────────────────────────────────────────────────┤ ← Separator Line
│                                                               │
│                                                               │
│                    Window Content Area                        │
│                                                               │
│                                                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
   ↑                                                           ↑
   Border (4px)                                       Border (4px)
```

## Component Breakdown

### Title Bar
- **Height**: 24px (configurable)
- **Background**: Gradient-style solid color
- **Layout**: Menu button (left) | Window title (center) | Control buttons (right)
- **Font**: 10pt, regular weight (configurable)

### Buttons

#### Menu Button [☰]
- Application icon or menu symbol
- Position: Left side of title bar
- Size: 24x24px (configurable)

#### Minimize Button [_]
- Horizontal line icon
- Action: Minimize window to taskbar

#### Maximize/Restore Button [□]
- Single square for maximize
- Double overlapping squares for restore
- Action: Toggle between maximized and normal state

#### Close Button [×]
- X symbol
- Special color: Red tint (#dc5050)
- Action: Close window

### Borders
- **Width**: 4px (configurable, 0-oversized)
- **Style**: Solid color frame
- **Behavior**: Hidden when window is maximized
- **Resize**: Clickable/draggable for window resizing

### Separator Line
- **Position**: Between title bar and content
- **Height**: 1px
- **Color**: Subtle darker shade (configurable)
- **Purpose**: Visual separation

## Color Scheme (Default Theme)

### Active Window (Focused)
```
Frame:      #28282d  ████  Dark charcoal
Title Bar:  #32323a  ████  Slightly lighter
Text:       #ffffff  ████  White
Separator:  #46464b  ████  Medium gray
```

### Inactive Window (Unfocused)
```
Frame:      #3c3c41  ████  Medium gray
Title Bar:  #464649  ████  Lighter gray
Text:       #a0a0a5  ████  Light gray
Separator:  #46464b  ████  Medium gray
```

### Button States
```
Normal:     Transparent
Hover:      #464649  ████  Gray overlay
Press:      #1e1e23  ████  Dark overlay
Close:      #dc5050  ████  Red icon
```

## Visual States

### Normal Window
```
┌────────────────────────────────────┐
│ [☰] Document.txt      [_] [□] [×] │
├────────────────────────────────────┤
│                                    │
│  File content here...              │
│                                    │
└────────────────────────────────────┘
```

### Maximized Window
```
[☰] Large Document.txt              [_] [□] [×]
────────────────────────────────────────────────
│                                              │
│  File content fills entire screen...         │
│                                              │
```
Note: No side/bottom borders when maximized

### Inactive Window
```
┌────────────────────────────────────┐
│ [☰] Background.txt    [_] [□] [×] │  (Dimmed colors)
├────────────────────────────────────┤
│                                    │
│  Inactive window content...        │
│                                    │
└────────────────────────────────────┘
```

## Button Interaction States

### Hover State
```
[☰] Window Title                    [_] [▓] [×]
                                          ↑
                                    Highlighted
```

### Press State
```
[☰] Window Title                    [_] [█] [×]
                                          ↑
                                       Pressed
```

### Close Button Special Behavior
```
Normal:  [×]  (Red icon)
Hover:   [▓]  (Red icon on gray background)
Press:   [█]  (White icon on dark background)
```

## Responsive Design

### Small Windows (< 200px width)
- Title text elides with "..."
- All buttons remain visible
- Maintains minimum size

### Large Windows (> 1000px width)
- Full title text displayed
- Buttons aligned to edges
- Consistent spacing maintained

### Multi-Monitor
- Decoration adapts to screen DPI
- Consistent appearance across displays
- Proper scaling support

## Theme Variants

### Dark Blue Theme
```
Active:     #243447  ████  Deep blue
Text:       #e8f0ff  ████  Light blue-white
```

### Light Theme
```
Active:     #e8e8ec  ████  Light gray
Text:       #202020  ████  Dark text
```

### Minimal Theme
```
Borders:    2px (thinner)
Height:     22px (shorter)
Shadows:    Disabled
```

### Classic Green Theme
```
Active:     #243830  ████  Dark green
Text:       #d0f0d8  ████  Light green
Borders:    5px (thicker)
```

## E13 Heritage

This design faithfully recreates the classic E13 aesthetic:

- **Clean Lines**: Simple, uncluttered design
- **Functional**: Focus on usability over decoration
- **Customizable**: User control over every aspect
- **Efficient**: Minimal resource usage
- **Classic**: Timeless design that doesn't date

## Technical Features

### Dynamic Rendering
- Real-time updates on window state changes
- Smooth color transitions
- Efficient repainting

### Integration
- Native KWin API usage
- KDecoration2 framework
- Qt5 painting system

### Performance
- Hardware-accelerated rendering
- Minimal CPU usage
- No animation overhead (by design)

## Accessibility

- **High Contrast**: Strong contrast ratios
- **Clear Icons**: Recognizable button symbols
- **Configurable**: Adjustable sizes and colors
- **Keyboard**: Full keyboard navigation support

## Future Enhancements

Potential additions while maintaining E13 style:

- [ ] Custom application icon display
- [ ] Optional rounded corners
- [ ] Configurable button order
- [ ] Theme import/export
- [ ] Visual theme editor
- [ ] Animation effects (optional)

---

For implementation details, see the source code in `src/` directory.
For theme customization, see `theme/README.md`.
