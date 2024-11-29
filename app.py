from cs50 import *
from flask import Flask,render_template,request

app = Flask(__name__)
#hello
db = SQL("sqlite:///movies.db")

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    search=request.args.get('search','')
    data=db.execute("SELECT * FROM movies,ratings WHERE movie_id = id AND title LIKE ? ORDER BY rating DESC;", (search + '%',))
    return render_template('index.html',search=search,data=data)

@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    data=db.execute("SELECT * FROM movies,ratings WHERE movie_id = id AND id = ?;", (movie_id,))
    data2=db.execute("SELECT name,birth FROM stars,people WHERE movie_id = ? AND person_id = id;",movie_id)
    data3=db.execute("SELECT name,birth FROM directors,people WHERE movie_id =? AND person_id = id;",movie_id)
    if not data:
        return "No such movie found."
    return render_template('movie.html',data=data,data2=data2,data3=data3)

if __name__ == '__main__':
    app.run()



