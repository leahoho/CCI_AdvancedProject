Options of local servers include:

Running npm i -g five-server@latest && five-server --port=8000 in a terminal in the same directory as your HTML file.
Running python -m SimpleHTTPServer (or python -m http.server for Python 3) in a terminal in the same directory as your HTML file.
Once we are running our server, we can open our project in the browser using the local URL and port which the server is running on (e.g., http://localhost:8000). Try not to open the project using the file:// protocol which does not provide a domain; absolute and relative URLs may not work.