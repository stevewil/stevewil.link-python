from flask_frozen import Freezer # The package is Frozen-Flask, but the import is flask_frozen
from app import app

app.config['FREEZER_DESTINATION'] = 'build'
freezer = Freezer(app)

if __name__ == '__main__':
    print("Freezing site...")
    freezer.freeze()
    print("Done. Static site is in the 'build' directory.")