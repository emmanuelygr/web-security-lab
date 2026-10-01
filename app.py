from flask import Flask, request, render_template, make_response, redirect, url_for, session, abort
from functools import wraps
import html

app = Flask(__name__)
# In a real app, this should be a random, secret string. 
# It's used to cryptographically sign session cookies.
app.secret_key = 'super_secret_key_for_testing_only'

# =====================================================================
# 1. BASIC AUTHENTICATION
# =====================================================================

def check_auth(username, password):
    """This function is called to check if a username / password combination is valid."""
    # In a real app, credentials would be hashed and checked against a database.
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return make_response(
        "Could not verify your access level for that URL.\nYou have to login with proper credentials", 
        401, 
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    """Decorator to require basic authentication for specific routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # Check if auth headers exist and if credentials match
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# =====================================================================
# ROUTES
# =====================================================================

@app.route('/')
def index():
    """
    The main landing page.
    Demonstrates reading HTTP Request Headers.
    """
    # Reading the User-Agent header sent by the client's browser
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user_agent=user_agent)

# --- A. COOKIES ---
@app.route('/set_cookie')
def set_cookie():
    """
    Demonstrates setting an HTTP Cookie.
    Notice httponly=False. This means JavaScript CAN access this cookie,
    which makes it vulnerable to Cross-Site Scripting (XSS) cookie theft!
    In production, session cookies should have HttpOnly=True and Secure=True.
    """
    resp = make_response(redirect(url_for('index')))
    # Setting a dummy session ID
    resp.set_cookie('session_id', '12345ABCDE_VULNERABLE', httponly=False) 
    return resp

# --- B. VULNERABLE ROUTE (Reflected XSS) ---
@app.route('/search_vulnerable')
def search_vulnerable():
    """
    INTENTIONALLY VULNERABLE ROUTE: Reflected Cross-Site Scripting (XSS)
    The user input ('q' parameter from the GET request) is taken and 
    immediately rendered in the HTML response WITHOUT any sanitization or escaping.
    
    If a user submits <script>alert(1)</script>, the browser will execute it.
    """
    query = request.args.get('q', '')
    
    # DANGEROUS: Rendering raw input directly into the HTML stream.
    return f"<h1>Search Results (Vulnerable)</h1><p>You searched for: {query}</p><br><a href='/'>Back</a>"

# --- C. SECURE ROUTE (Mitigated XSS) ---
@app.route('/search_secure')
def search_secure():
    """
    SECURE ROUTE: Mitigated XSS
    This route performs the exact same function as above, but securely.
    It uses input validation / output encoding (html.escape) to neutralize 
    any potentially malicious characters (like <, >, &, etc.).
    """
    query = request.args.get('q', '')
    
    # SECURE: Output encoding. Converts < to &lt;, > to &gt;, etc.
    # The browser will display the script tags as text, rather than executing them.
    safe_query = html.escape(query)
    
    return f"<h1>Search Results (Secure)</h1><p>You searched for: {safe_query}</p><br><a href='/'>Back</a>"

# --- D. AUTHENTICATED ROUTE ---
@app.route('/admin')
@requires_auth
def admin():
    """
    This route requires Basic Authentication to access.
    It demonstrates how access controls and status codes (401 Unauthorized) work.
    """
    return "<h1>Admin Panel</h1><p>Welcome! You are successfully authenticated.</p><br><a href='/'>Back</a>"

if __name__ == '__main__':
    # Binds to 127.0.0.1 (localhost) ONLY.
    # Exposing this to 0.0.0.0 on a public network would be highly dangerous 
    # because of the intentional vulnerabilities.
    app.run(host='127.0.0.1', port=5000, debug=True)
