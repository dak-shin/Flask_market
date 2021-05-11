
# TODO: set FLASK_APP=nameofthefile.py
# TODO: set FLASK_ENV=development
# FLASK RUN

from market.app import app
from market import routes


if __name__ == "__main__":
    app.run(debug=True)
