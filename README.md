# Personal CV Site - Python Static Generator

This project is a simple, file-based static site generator for a personal CV or portfolio website. It uses Python with Flask and Flask-Frozen to read content from text files and generate a static HTML site.

## How it Works

The site is built around a "widget" concept. Each section of the homepage (like "Hero", "Experience", "Publications") is a separate content file in the `content/home/` directory.

The build process is as follows:

1.  The `python build.py` script is executed.
2.  It uses `Flask-Frozen` to crawl the Flask application defined in `app.py`.
3.  The main `/` route in `app.py` scans the `content/home/` directory for `.txt` files.
4.  For each file, it parses the frontmatter (the metadata at the top) and the Markdown content.
5.  It filters for widgets marked as `active = true` and sorts them by their `weight`.
6.  The sorted list of widgets is passed to the `templates/index.html` template.
7.  The `index.html` template loops through the widgets and dynamically includes a corresponding partial template from `templates/widgets/` based on the `widget` key in the frontmatter (e.g., `widget = "hero"` will look for `hero.html`).
8.  The final rendered HTML is saved to the `build/` directory, which can then be deployed to any static web host.

## Directory Structure

The project is organized as follows:

```
stevewil.link-python/
├── app.py                # Main Flask application logic
├── build.py              # Static site generator script
├── requirements.txt      # Project dependencies
├── README.md             # This file
│
├── content/
│   └── home/
│       ├── hero.txt      # Content for the hero widget
│       ├── experience.txt# Content for the experience widget
│       └── ...           # Other content widget files
│
├── templates/
│   ├── base.html         # Base HTML template (layout, head, etc.)
│   ├── index.html        # Main homepage template (loops through widgets)
│   └── widgets/
│       ├── hero.html     # Template for the hero widget
│       ├── experience.html # Template for the experience widget
│       └── _default.html # Fallback template for simple widgets
│
├── static/
│   └── css/
│       └── style.css     # (Optional) CSS styles
│
├── build/                # Output directory for the generated static site
│
└── log/
    └── debug.log         # Log file for debugging application runs
```

## Content Management

To add or edit a section on the homepage, simply create or modify a `.txt` file in the `content/home/` directory.

Each file must contain a frontmatter section at the top, enclosed by `---`. The frontmatter must include:

- `widget`: The name of the widget, which corresponds to a template in `templates/widgets/`.
- `active`: Set to `true` to display the widget.
- `weight`: A number to control the order of the widgets on the page (lower numbers appear first).
- `title`: The title of the section.

Any content below the frontmatter will be rendered as Markdown.

### Example (`quote.txt`):

```text
---
widget: "quote"
active: true
weight: 90
title: "Quote"
---

*"The future is already here – it's just not evenly distributed."* - William Gibson
```

## How to Build

To generate the static site, ensure you have the dependencies installed (`pip install -r requirements.txt`) and then run the build script:

```bash
python build.py
```

The complete static site will be available in the `build/` directory.