import os
import frontmatter
from frontmatter.default_handlers import TOMLHandler
from flask import Flask, render_template
from markdown import markdown

app = Flask(__name__)

# Configuration
CONTENT_DIR = 'content'

def get_page_data(path):
    """Loads and parses a Markdown file with front matter."""
    full_path = os.path.join(CONTENT_DIR, path)
    if not os.path.exists(full_path):
        return None
    
    post = frontmatter.load(full_path, handler=TOMLHandler())
    post.content = markdown(post.content)
    return post

@app.route("/")
def index():
    """Renders the home page by assembling widgets."""
    home_dir = os.path.join(CONTENT_DIR, 'home')
    widgets = []
    if os.path.exists(home_dir):
        for filename in os.listdir(home_dir):
            if filename.endswith('.md'):
                widget_data = get_page_data(os.path.join('home', filename))
                if widget_data and widget_data.metadata.get('active', False):
                    widgets.append(widget_data)
    
    # Sort widgets by weight
    widgets.sort(key=lambda w: w.metadata.get('weight', 0))
    
    # For now, we can assume the first widget is the hero for the title
    page_title = widgets[0].metadata.get('title') if widgets else "Home"
    
    return render_template("index.html", widgets=widgets, title=page_title)

if __name__ == "__main__":
    app.run(debug=True)