from cs50 import *
from flask import Flask,render_template,request

app = Flask(__name__)

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


# if not data:
#     print("No such movie found.")
#     exit(1)



# if len(data) > 0:

#     for i in range(len(data)):
#         print(f"{i+1}.{data[i]['title']} ({data[i]['year']}) rating:{data[i]['rating']}")
#     print()
#     movie_choice = get_int("Choose movie index: ")
#     print()
#     print("="*20)
#     print(f"movie title: {data[movie_choice-1]['title']}")
#     print(f"movie year:  {data[movie_choice-1]['year']}")
#     print(f"movie rating:  {data[movie_choice-1]['rating']}")
#     print(f"movie votes:  {data[movie_choice-1]['votes']}\n")
#     print("stars\n")

    
#     data2=db.execute("SELECT name,birth FROM stars,people WHERE movie_id = ? AND person_id = id;",data[movie_choice-1]['id'])
#     if not data2:
#         print("No star name mentioned")
#     else:
#         for i in data2:
#             print(f"{i['name']} birth({i['birth']})")
    
#     print("\nDirector\n")
#     data3=db.execute("SELECT name,birth FROM directors,people WHERE movie_id =? AND person_id = id;",data[movie_choice-1]['id'])
#     if not data3:
#         print("No director name mentioned")
#     else:     
#         for i in data3:
#             print(f"{i['name']} birth({i['birth']})")
#     print()
#     print("="*20)

