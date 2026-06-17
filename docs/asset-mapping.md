# E13 Asset Mapping

## Overview

This document describes the mapping from legacy Enlightenment 0.13 (E13) pixmap
filenames (the `win_*` corpus) to semantic decoration roles and state variants.

**Sources:**

- Original E13 source: [mathieujobin/enlightenment-13](https://github.com/mathieujobin/enlightenment-13)
- Authoritative raster pixmaps: [mathieujobin/kwin_e13 @ bd9908ec](https://github.com/mathieujobin/kwin_e13/tree/bd9908ec2720e3285302388084822ef92b7ef733/contents/imgs)
- Machine-readable mapping: [`asset_map.json`](../asset_map.json) in the repository root

---

## State Suffix Convention

E13 uses three visual states for every subwindow asset.  The number suffix in
the legacy filenames maps as follows:

| Suffix | E13 keyword   | Semantic tag | Meaning                              |
|--------|---------------|--------------|--------------------------------------|
| `_1`   | `unselected`  | `uns`        | Normal / unfocused window            |
| `_2`   | `selected`    | `sel`        | Focused / active window              |
| `_3`   | `clicked`     | `clk`        | Button/area is being pressed         |

---

## Legacy-to-Semantic Mapping Table

The mapping was derived directly from the `windowstyles` configuration files
embedded in the **DEFAULT** and **DEFAULT_small** theme tarballs shipped with
the E13 source code.  Each row corresponds to one *role group* (letter).

| Legacy pattern | Semantic role            | Type        | Position / description                                             |
|----------------|--------------------------|-------------|---------------------------------------------------------------------|
| `win_a_*.{ppm,png}` | `button_iconify`    | button      | Iconify button — top of the left sidebar panel                      |
| `win_b_*.{ppm,png}` | `button_raise_lower`| button      | Raise/lower button — second on the left sidebar                     |
| `win_c_*.{ppm,png}` | `button_drag_sticky`| button      | Drag/sticky-toggle button — third on the left sidebar               |
| `win_d_*.{ppm,png}` | `button_resize`     | button      | Resize/move button — bottom of the left sidebar                     |
| `win_e_*.{ppm,png}` | `border_left`       | decoration  | Left border strip (scalable, below the sidebar buttons)             |
| `win_f_*.{ppm,png}` | `corner_bottomleft` | decoration  | Bottom-left corner piece                                            |
| `win_g_*.{ppm,png}` | `border_bottom`     | decoration  | Bottom border strip (scalable)                                      |
| `win_h_*.{ppm,png}` | `corner_bottomright`| decoration  | Bottom-right corner piece                                           |
| `win_i_*.{ppm,png}` | `border_right`      | decoration  | Right border strip (scalable)                                       |
| `win_j_*.{ppm,png}` | `titlebar_right_cap`| decoration  | Right cap of the top header bar (above right border)                |
| `win_k_*.{ppm,png}` | `titlebar_mid_strip`| decoration  | Middle strip of top header bar (scalable, between sidebar and cap)  |
| `win_l_*.{ppm,png}` | `button_close`      | button      | Close/kill button — top-left corner; right-click iconifies          |
| `win_m_*.{ppm,png}` | `titlebar_bg`       | button      | Full titlebar background (behind title text and right buttons)      |
| `win_n_*.{ppm,png}` | `button_maximize`   | button      | Maximize/restore button — right side of titlebar                    |
| `win_o_*.{ppm,png}` | `titlebar_title`    | title       | Title text region — **DEFAULT** (full-size) theme only              |
| `win_p_*.{ppm,png}` | `titlebar_title_small` | title    | Title text region — **DEFAULT_small** (compact) theme only          |

### Semantic filename examples

```
win_a_1.ppm  →  button_iconify_uns.png
win_a_2.ppm  →  button_iconify_sel.png
win_a_3.ppm  →  button_iconify_clk.png
win_l_1.ppm  →  button_close_uns.png
win_m_2.ppm  →  titlebar_bg_sel.png
win_o_3.ppm  →  titlebar_title_clk.png
```

---

## Window Decoration Layout (DEFAULT theme)

```
Border dimensions: left=38 px, top=47 px, right=6 px, bottom=6 px

┌──────┬────────────────────────────────────────────┬──────────┐
│  win_l │  win_m (titlebar_bg)                       │  win_j   │
│(close) │  ┌──────────────────────────────┐          │ (right   │
│        │  │  win_o (titlebar_title text) │  win_n   │  cap)    │
│        │  └──────────────────────────────┘(maximize)│          │
├────────┴────────────────────────────────────────────┴──────────┤
│ win_k (titlebar_mid_strip)                                      │
├────────┬──────────────────────────────────────────────────┬─────┤
│ win_a  │                                                  │     │
│(iconif)│                                                  │ w   │
├────────┤             client window area                   │ i   │
│ win_b  │                                                  │ n   │
│(raise) │                                                  │ _   │
├────────┤                                                  │ i   │
│ win_c  │                                                  │     │
│(sticky)│                                                  │(bor)│
├────────┤                                                  │ d   │
│ win_d  │                                                  │ e   │
│(resize)│                                                  │ r   │
├────────┤                                                  │ _   │
│ win_e  │                                                  │ r   │
│(border │                                                  │ i   │
│  left) │                                                  │ g   │
│(scale) │                                                  │ h   │
│        │                                                  │ t)  │
├────────┴──────────────────────────────────────────────────┴─────┤
│ win_f  │     win_g  (border_bottom, scalable)          │ win_h  │
│(corner)│                                               │(corner)│
└────────┴──────────────────────────────────────────────┴─────────┘
```

---

## SVG Button Icons (Experimental)

The `kwin_e13` repository also contains SVG versions of button icons.  These
are **experimental** and do not correspond directly to original E13 raster
assets.  They are used by the KWin QML decoration only.

| SVG file              | Semantic role                       |
|-----------------------|-------------------------------------|
| `close.svg`           | `button_close_icon`                 |
| `maximize.svg`        | `button_maximize_icon`              |
| `maximize_hover.svg`  | `button_maximize_icon_hover`        |
| `maximize_disable.svg`| `button_maximize_icon_disabled`     |
| `minimize.svg`        | `button_minimize_icon`              |
| `minimize_hover.svg`  | `button_minimize_icon_hover`        |
| `minimize_disable.svg`| `button_minimize_icon_disabled`     |
| `restore.svg`         | `button_restore_icon`               |
| `restore_hover.svg`   | `button_restore_icon_hover`         |
| `restore_disable.svg` | `button_restore_icon_disabled`      |

---

## Rationale

- The letter assignment (`win_a` … `win_p`) comes from the *declaration order*
  of `begin subwin` blocks in the `windowstyles` config embedded in each E13
  theme tarball.  The letters themselves are arbitrary names chosen by the
  DEFAULT theme author (Carsten "Rasterman" Haitzler).
- `win_o` and `win_p` both map to a `type title` subwindow (the region that
  renders the window caption text), but they originate from different theme
  variants (DEFAULT vs DEFAULT_small) and therefore have slightly different
  pixel content.
- Raster `.ppm` and `.png` files are considered *authoritative*; SVG files in
  `kwin_e13` are experimental re-implementations.

---

## Extractor `--semantic-names` mode

When `tools/extract_theme.py` is invoked with `--semantic-names`, extracted
image files are written using the semantic filenames defined here instead of
the original `win_*` names.  For example:

```sh
python tools/extract_theme.py -i theme.db -o ./out/ --semantic-names
# Produces: out/images/button_close_uns.png  (instead of win_l_1.png)
```

See [`tools/semantic_names.py`](../tools/semantic_names.py) for the
implementation of the name-translation helper.
