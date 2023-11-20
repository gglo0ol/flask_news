from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    with app.app_context():
        news_list = News.query.all()
    return render_template('index.html', news=news_list)

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    with app.app_context():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_news = News(title=title, content=content)
            db.session.add(new_news)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add_news.html')

@app.route('/delete_news/<int:news_id>')
def delete_news(news_id):
    with app.app_context():
        news_to_delete = News.query.get_or_404(news_id)
        db.session.delete(news_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    with app.app_context():
        news_to_edit = News.query.get_or_404(news_id)

        if request.method == 'POST':
            news_to_edit.title = request.form['title']
            news_to_edit.content = request.form['content']
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('edit_news.html', news=news_to_edit)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
