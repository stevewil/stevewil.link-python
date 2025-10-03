import os
import frontmatter
import logging
from frontmatter import TOMLHandler
from flask import Flask, render_template
from datetime import datetime
from markdown import markdown

app = Flask(__name__)

# --- Logging Setup ---
if not os.path.exists('log'):
    os.makedirs('log')
logging.basicConfig(
    filename='log/debug.log', 
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)
# Configuration

@app.template_filter('date_format')
def date_format_filter(s, format_str):
    """Jinja2 filter to format a date string."""
    if not s:
        return ""
    # The date might be a string or already a date object
    date_obj = s if isinstance(s, datetime) else datetime.fromisoformat(s.rstrip('Z'))
    return date_obj.strftime(format_str)

@app.template_filter('markdown')
def markdown_filter(s):
    """Jinja2 filter to apply markdown conversion."""
    return markdown(s)

CONTENT_DIR = 'content'

def get_page_data(path):
    """Loads and parses a Markdown file with front matter."""
    full_path = os.path.join(CONTENT_DIR, path)
    if not os.path.exists(full_path):
        return None

    try:
        with open(full_path, 'r', encoding='utf-8') as f_in:
            content = f_in.read()

        # Standardize non-standard delimiters before parsing.
        # Replace '+' and '+++' with '---' which is the default for the library.
        if content.startswith('+++\n'):
            content = content.replace('+++', '---', 2)
        elif content.startswith('+\n'):
            content = content.replace('+', '---', 2)

        post = frontmatter.loads(content)
        post.content = markdown(post.content)
        return post
    except Exception as e:
        app.logger.error(f"Error parsing file {full_path}: {e}")
        return None

@app.route("/")
def index():
    """Renders the home page by assembling widgets."""
    app.logger.info("--- Rendering homepage ---")
    home_dir = os.path.join(CONTENT_DIR, 'home')
    widgets = []
    if os.path.exists(home_dir):
        filenames = sorted(os.listdir(home_dir))
        app.logger.debug(f"Found files in content/home: {filenames}")
        for filename in filenames:
            if filename.endswith('.txt'):
                app.logger.debug(f"Processing widget file: {filename}")
                widget_data = get_page_data(os.path.join('home', filename))
                if widget_data and widget_data.metadata.get('active', False):
                    app.logger.debug(f"'{filename}' is active. Adding to widgets.")
                    widgets.append(widget_data)
                elif widget_data:
                    app.logger.debug(f"'{filename}' is inactive. Skipping.")
    
    # Sort widgets by weight
    widgets.sort(key=lambda w: w.metadata.get('weight', 0))
    app.logger.debug(f"Final sorted widget order: {[w.metadata.get('widget') for w in widgets]}")
    
    # For now, we can assume the first widget is the hero for the title
    if not widgets:
        app.logger.warning("No active widgets found. The page will be blank.")
        return "No active widgets found. Please check your content files.", 200
    page_title = widgets[0].metadata.get('title', "Home")
    
    return render_template("index.html", widgets=widgets, title=page_title)

if __name__ == "__main__":
    app.run(debug=True)