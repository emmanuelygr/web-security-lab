# Web Security Testing Lab

**Author:** Emmanuel (@emmanuelygr)

## Overview
The Web Security Testing Lab is a deliberately vulnerable Python Flask web application designed for educational purposes. It serves as a practical, hands-on environment to understand foundational web security concepts, common vulnerabilities (like Cross-Site Scripting), and how to secure against them.

## Why I Built This
I created this project to solidify my understanding of web application security. Reading about vulnerabilities is important, but seeing them in action and building the fixes yourself provides a much deeper level of comprehension. I wanted a lightweight, contained sandbox where I could safely experiment with HTTP concepts, test payloads, and practice secure coding paradigms without the overhead of massive vulnerability platforms.

## Learning Objectives
By using and studying this project, you will:
- Understand the stateless nature of HTTP and how state is maintained using cookies and sessions.
- Differentiate between secure and insecure coding practices for handling user input.
- Practically exploit and then mitigate Reflected Cross-Site Scripting (XSS).
- Observe how HTTP headers operate (e.g., User-Agent, WWW-Authenticate).
- Learn how to intercept and manipulate web traffic using proxy tools.

## Features
- **Intentional XSS Vulnerability:** A search route that reflects unsanitized user input.
- **Secure Counterpart Route:** The identical search functionality implemented safely using HTML output encoding.
- **Insecure Cookie Generation:** Demonstrates how misconfigured cookies (missing `HttpOnly`) can be stolen via JavaScript.
- **HTTP Basic Authentication:** A protected route showing how 401 Unauthorized status codes and WWW-Authenticate headers function.
- **Header Inspection:** Displays request headers (User-Agent) to demonstrate client-server data exchange.

## Technologies
- **Python 3.x:** Core programming language.
- **Flask (Werkzeug/Jinja2):** Lightweight web framework used to handle routing, requests, and HTML templates.
- **HTML5/CSS3:** Frontend structure and basic styling.

## Cybersecurity Concepts Explored

### HTTP Lifecycle & Methods
The web operates on a request-response cycle. A client (browser) sends an HTTP Request (e.g., `GET /search?q=test`), and the server returns an HTTP Response containing HTML. This lab uses `GET` requests to demonstrate how data is passed in the URL string.

### HTTP Status Codes
- **200 OK:** The request succeeded (standard page loads).
- **401 Unauthorized:** The client must authenticate itself to get the requested response (used in the `/admin` route).

### HTTP Headers
Headers are key-value pairs sent in requests and responses. 
- **Request Headers:** E.g., `User-Agent` tells the server what browser the client is using.
- **Response Headers:** E.g., `Set-Cookie` instructs the browser to store a cookie.

### Cookies & Sessions
Because HTTP is stateless, cookies are used to remember users. If a cookie lacks the `HttpOnly` flag, client-side scripts (JavaScript) can read it (`document.cookie`). This lab deliberately sets a cookie without this flag to demonstrate the risk of session hijacking via XSS.

### OWASP Basics: Secure vs Insecure
The Open Web Application Security Project (OWASP) lists Injection and XSS as top risks. 
- **Insecure:** Trusting user input implicitly. In `/search_vulnerable`, user data is directly concatenated into the HTML DOM.
- **Secure:** "Never trust user input." In `/search_secure`, input is contextually encoded (`html.escape`), turning `<script>` into `&lt;script&gt;`, rendering it harmless text.

## How It Works
The backend is a single file (`app.py`) running a Flask development server. It listens on `localhost:5000` and defines multiple URL routes (`/`, `/search_vulnerable`, `/search_secure`, etc.). When you navigate to these URLs, Flask executes the corresponding Python function and returns HTML rendered from the `templates/` folder.

## Project Structure
```text
web-security-lab/
├── app.py                # Main Flask application and routes
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
├── README.md             # Project documentation (You are here)
└── templates/
    └── index.html        # Frontend HTML view
```

## Installation

1. **Clone the repository** (or download the files):
   ```bash
   git clone https://github.com/emmanuelygr/web-security-lab.git
   cd web-security-lab
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```
2. **Access the lab**: Open your web browser and navigate to `http://127.0.0.1:5000`

## Examples & Learning Exercises

### Exercise 1: Execute Reflected XSS
1. Go to the home page.
2. Under "Vulnerable Search", enter: `<script>alert('XSS Successful!');</script>`
3. Click Search. You should see a JavaScript pop-up alert box.

### Exercise 2: Steal a Cookie via XSS
1. Click the link to "Set a test cookie".
2. Go back to the "Vulnerable Search" box.
3. Enter: `<script>alert(document.cookie);</script>`
4. Click Search. The pop-up will now display your session ID, proving that an attacker could exfiltrate this data.

### Exercise 3: Verify the Mitigation
1. Try the exact same payloads from Exercises 1 & 2 in the **Secure Search** box.
2. Notice that the payload is printed harmlessly on the screen. If you inspect the page source, you will see the brackets were converted to HTML entities.

### Exercise 4: Intercept with Burp Suite (Advanced)
1. Download and open [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload).
2. Configure your browser to proxy traffic through Burp (usually `127.0.0.1:8080`).
3. Intercept the request to `/admin`. Notice there is no Authorization header.
4. Forward the request, observe the `401 Unauthorized` response with the `WWW-Authenticate` header.
5. Enter the credentials (`admin` / `secret`) in your browser.
6. Intercept the request again. You will now see the `Authorization: Basic YWRtaW46c2VjcmV0` header added by the browser.

## Security Considerations (LOCALHOST ONLY)
⚠️ **WARNING:** This application is intentionally vulnerable. **Do not deploy this application to a public server, cloud provider, or bind it to `0.0.0.0`.** It is designed to be run locally (`127.0.0.1`) for educational purposes only. Exposing it to a network poses a significant security risk.

## Ethical / Legal Use
This repository is provided for educational and research purposes only. The concepts and techniques demonstrated here must only be used on systems you own or have explicit permission to test. The author (@emmanuelygr) is not responsible for any misuse of the information or code contained in this project.

## Limitations
- This is not a comprehensive security suite. It currently only demonstrates basic XSS, Authentication, and Cookie concepts.
- It uses Flask's built-in development server, which is not suitable for production.
- Does not utilize a database; state is entirely stateless or reliant on basic HTTP mechanisms.

## Troubleshooting
- **`Address already in use` error:** Another service is running on port 5000. Run the app on a different port: `flask run --port 8080` (requires setting `FLASK_APP=app.py`).
- **`ModuleNotFoundError: No module named 'flask'`:** Ensure your virtual environment is activated and you ran `pip install -r requirements.txt`.

## FAQ
**Q: Why doesn't the XSS payload work in some browsers?**
A: Some modern browsers have built-in XSS auditors (though many have deprecated them recently). If it doesn't work, ensure you are testing against the explicitly vulnerable route, or try a different browser like Firefox.

**Q: Is Basic Authentication secure?**
A: No, not by itself. Basic Auth encodes credentials in Base64 (which is easily decoded, not encrypted). It should *only* ever be used over a secure HTTPS (TLS/SSL) connection.

## What I Learned
Through building this project, I gained a much firmer grasp of the Request/Response lifecycle. I learned how easy it is to introduce an XSS vulnerability by simply trusting an input string, and how vital output encoding is. I also realized the importance of security flags like `HttpOnly` and `Secure` when setting HTTP Cookies.

## Future Improvements
1. **Implement SQL Injection (SQLi):** Add an SQLite database and a vulnerable login or product search feature.
2. **Cross-Site Request Forgery (CSRF):** Add a state-changing action (like changing a password) without CSRF tokens.
3. **Command Injection:** Add a feature that supposedly pings an IP address but allows arbitrary OS command execution.
4. **Insecure Direct Object Reference (IDOR):** Create user profiles where changing a URL parameter accesses someone else's data.
5. **Dockerization:** Package the application in a Docker container for even easier and safer sandboxing.
6. **Logging and Monitoring:** Add detailed console logging so users can see the raw HTTP requests as they hit the server in real-time.
