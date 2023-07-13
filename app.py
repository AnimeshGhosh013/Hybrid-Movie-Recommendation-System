from flask import Flask, render_template,request,redirect,url_for
from Collaborative import get_recommended_movies
from content import content_based_filtering

app = Flask(__name__)

data = {}
error_message = "No more movies to display!!!"
error_user = "Enter valid User Id!!!"

@app.route('/',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        data['user'] = request.form["userId"]
        if(data['user'].isdigit()):
            if (int(data['user'])>0 and int(data['user'])<=620):
                data['point'] = 0
                return redirect(url_for('home'))
        return render_template('login.html',error = error_user)
    return render_template('login.html')

@app.route('/recommend', methods=['GET', 'POST'])
def home():  
    if "moreMovies" in request.form:
        if data['point']<10:
            movie_name = (data['movie'])[data['point']]
            data['point']+=1
            movies = content_based_filtering(movie_name)
            return render_template('index.html', userId = data['user'], movies = movies)
        else:
            return render_template('index.html', error = error_message)
    elif "back" in request.form:
        return redirect(url_for('login'))
    movies = get_recommended_movies(int(data['user']))
    data['movie'] = movies
    return render_template('index.html', userId = data['user'], movies = movies)

if __name__ == '__main__':
    app.run()