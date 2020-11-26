
import requests
import json

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

clientID = "Cbbb54d9e35aa736ef45c2e21b3cef7d5d44f0dbf86535732768540c456e13b63"
secretID = "052ac0a80718fc4471128a5db6185a03c3786c2ec631ee1efd73909f528a20d1"
redirectURI = "http://localhost:10060/oauth"  # This could be different if you publicly expose this endpoint.


def get_tokens(code):
    """Gets access token and refresh token"""
    print("code:", code)
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
               "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    print(results)
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]
    return access_token, refresh_token


def get_oauthuser_info(access_token):
    """Retreives OAuth user's details."""
    url = "https://webexapis.com/v1/people/me"
    headers = {'accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + access_token}
    req = requests.get(url=url, headers=headers)
    results = json.loads(req.text)
    personID = results["id"]
    emailID = results["emails"][0]
    displayName = results["displayName"]
    return personID, emailID, displayName


@app.route("/")
def main_page():
    """Main Grant page"""
    return render_template("index.htmlcss")


@app.route("/oauth")  # Endpoint acting as Redirect URI.
def oauth():
    """Retrieves oauth code to generate tokens for users"""

    if "code" in request.args and request.args.get("state") == "geht":
        state = request.args.get("state")  # Captures value of the state.
        code = request.args.get("code")  # Captures value of the code.
        print("OAuth code:", code)
        print("OAuth state:", state)
        access_token, refresh_token = get_tokens(code)  # As you can see, get_tokens() uses the code and returns access and refresh tokens.

        # Now, let's do something with the generated token: Get the user's info: PersonId, Email Address and DisplayName.
        personID, emailID, displayName = get_oauthuser_info(access_token)
        print
        "personID:", personID
        print
        "email ID:", emailID
        print
        "display Name", displayName
        return render_template("granted.htmlcss")
    else:
        return render_template("index.htmlcss")


if __name__ == '__main__':
    app.run("0.0.0.0", port=10060, debug=False)