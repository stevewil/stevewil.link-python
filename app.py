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
    # In the Hugo site, the homepage is built from `content/home/*.md` files.
    # We will replicate that logic here eventually.
    # For now, let's just render a basic homepage.
    
    # Example: Load the 'hero' widget data
    hero_widget = get_page_data('home/hero.md')
    
    return render_template("index.html", hero=hero_widget)

if __name__ == "__main__":
    app.run(debug=True)