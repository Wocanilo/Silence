'''
 This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.
from flask import Flask, request
from flask_session import Session
from flask_cors import CORS

# The main initializer for the Flask application
app = Flask(__name__)

# The app's secret key, which is used for encoding sensitive data such as cookies
app.secret_key = "8]c(G#*!u--hqdl[gi~RW;Z*S5Fwe-"  # You should change this to something random
app.config["SESSION_TYPE"] = "filesystem"

# Initialize the session manager and the CORS manager for the app
Session(app)
CORS(app, supports_credentials=True)

################################################
### ↓↓↓↓↓ Register your API endpoints here ↓↓↓↓↓

from api.subject import subject_api
app.register_blueprint(subject_api, url_prefix="/v1")

### ↑↑↑↑↑ Register your API endpoints here ↑↑↑↑↑
################################################

# Finally, if we're running this file, start the app
if __name__ == "__main__":
	app.run(port=8080, debug=True)