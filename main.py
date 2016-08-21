#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
from caesar import encrypt

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Caesar</a>
    </h1>
"""
# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
edit_header = "<h2>Encrypt this text for me:</h2>"

cipher_form ="""
<form action="/cipher" method="post">
    <textarea type="text" name="cipher-me" style = "height:100px; width:350px;">
    </textarea>
    <br>
    <h4><label>Rotate the characters by this amount:<br>
    <input type="text" name="rot"/>
    </label></h4>

    <input type="submit"/>
</form>"""


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the main page)"""

    def get(self):

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        response = page_header + edit_header + cipher_form + error_element + page_footer
        self.response.write(response)


class Cipher(webapp2.RequestHandler):
    """Handles request to encrypt user text"""

    def post(self):
        #look inside the request
        cipher_me = self.request.get("cipher-me")
        rotate = self.request.get("rot")


        # if no text was entered return the form with an error message
        if cipher_me != "" and rotate > 0:
            # if text was entered, escape it and send it to the encryption function
            cipher_me = cgi.escape(cipher_me, quote = True)

            #rotate = cgi.escape(rotate, quote = True)
        else:
            error = "missing values"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        ciphered = encrypt(cipher_me, int(rotate))

        answer = """
        <form action="/cipher" method="post">
            <textarea type="text" name="cipher-me" style = "height:100px;
            width:350px;">{0}</textarea>
            <br>
            <h4><label>Rotate the characters by this amount:<br>
            <input type="text" name="rot"/>
            </label></h4>

            <input type="submit"/>
        </form>""".format(ciphered)


        response = page_header + edit_header + answer + page_footer
        self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/cipher', Cipher)
], debug=True)
