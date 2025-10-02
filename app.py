import os
import frontmatter
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
    
    post = frontmatter.load(full_path)
    post.content = markdown(post.content)
    return post

@app.route("/")
def index():
    """Renders the home page by assembling widgets."""
    # Example: Load the 'hero' widget data
    hero_widget = get_page_data('home/hero.md')
    
    # Provide a default title if the widget doesn't exist
    page_title = "Home"
    if hero_widget and 'title' in hero_widget.metadata:
        page_title = hero_widget.metadata['title']
    
    return render_template("index.html", hero=hero_widget, title=page_title)

if __name__ == "__main__":
    app.run(debug=True)