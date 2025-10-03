import os
import frontmatter
import logging
import time
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

@app.context_processor
def inject_cache_buster():
    """Injects a cache-busting query string into templates."""
    return dict(cache_buster=int(time.time()))

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
        return None, f"File not found at '{full_path}'"

    try:
        with open(full_path, 'r', encoding='utf-8') as f_in:
            content = f_in.read()

        # The python-frontmatter library's default handler is YAML, which is
        # what our content files are formatted in. By calling .loads() without
        # any extra handlers, we use the most stable parsing path.
        post = frontmatter.loads(content)
        
        # The content body of the post is markdown, so we convert it to HTML.
        post.content = markdown(post.content)
        return post, None
    except Exception as e:
        app.logger.error(f"Error parsing file '{full_path}': {e}")
        return None, str(e)

@app.route("/")
def index():
    """Renders the home page by assembling widgets."""
    app.logger.info("--- Rendering homepage ---")
    home_dir = os.path.join(CONTENT_DIR, 'home')
    widgets = []
    errors = []
    if os.path.exists(home_dir):
        filenames = sorted(os.listdir(home_dir))
        app.logger.debug(f"Found files in content/home: {filenames}")
        for filename in filenames:
            if filename.endswith('.txt'):
                filepath = os.path.join('home', filename)
                app.logger.debug(f"Processing widget file: {filepath}")
                widget_data, error = get_page_data(filepath)
                if widget_data and widget_data.metadata.get('active', False):
                    app.logger.debug(f"'{filename}' is active. Adding to widgets.")
                    widgets.append(widget_data)
                elif error:
                    # Capture the specific error message for display.
                    errors.append(f"<strong>{filepath}:</strong> {error}")
    
    # Sort widgets by weight
    widgets.sort(key=lambda w: w.metadata.get('weight', 0))
    app.logger.debug(f"Final sorted widget order: {[w.metadata.get('widget') for w in widgets]}")
    
    if not widgets:
        app.logger.warning("No active widgets found. The page will be blank.")
        error_message = f"No active widgets found in the '{home_dir}' directory."
        if errors:
            error_html = f"<h1>{error_message}</h1>"
            error_html += "<h2>The following files could not be parsed:</h2><ul>"
            error_html += "".join([f"<li style='margin-bottom: 0.5em;'>{e}</li>" for e in errors])
            error_html += "</ul><p>This is often due to incorrect frontmatter syntax (e.g., using YAML format for a TOML file).</p>"
            return error_html, 200
        return error_message, 200

    page_title = widgets[0].metadata.get('title', "Home")
    
    return render_template("index.html", widgets=widgets, title=page_title)

if __name__ == "__main__":
    app.run(debug=True)

# This helps Flask-Frozen find the static files correctly.
@app.route('/static/<path:path>')
def static_files(path):
    return app.send_static_file(path)