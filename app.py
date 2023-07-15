from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
comments = SQLAlchemy(app)


class Text(comments.Model):
    id = comments.Column(comments.Integer, primary_key=True)
    comment = comments.Column(comments.Text, nullable=False)
    date = comments.Column(comments.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Text %r>' % self.id


@app.route('/', methods=["POST", "GET"])
def index():
    text2 = Text.query.order_by(Text.date.desc()).all()

    if request.method == "POST":
        comment = request.form['comment']
        text = Text(comment=comment)

        try:
            comments.session.add(text)
            comments.session.commit()
            return redirect('/')
        except:
            return "Упс..."
    else:
        return render_template('Блог юного робототехника Главная.html', comments=text2)


@app.route('/comment/<int:id>', methods=["POST", "GET"])
def commentation(id):
    text3 = Text.query.get(id)
    return render_template('comment.html', comment=text3)


@app.route('/comment/<int:id>/delete', methods=["POST", "GET"])
def commentation_delete(id):
    text3 = Text.query.get_or_404(id)

    try:
        comments.session.delete(text3)
        comments.session.commit()
        return redirect('/')
    except:
        return "Упс..."

    return render_template('comment.html', comment=text3)


@app.route('/comment/<int:id>/update', methods=["POST", "GET"])
def commentation_update(id):
    text3 = Text.query.get(id)

    if request.method == "POST":
        text3.comment = request.form['comment']

        try:
            comments.session.commit()
            return redirect('/')
        except:
            return "Упс..."
    else:
        return render_template('update.html', comment=text3)


if __name__ == "__main__":
    app.run(debug=False)