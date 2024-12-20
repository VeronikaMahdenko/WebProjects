from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # Додаємо імпорт datetime
from sqlalchemy import UniqueConstraint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nika11@localhost:5432/Excursions'
app.config['SECRET_KEY'] = 'hvlprdrk19'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    excursion_name = db.Column(db.String(100), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='bookings')


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.Text, nullable=True)

    liked_by = db.relationship('User', secondary='feedback_likes', backref='liked_feedbacks')

    def __repr__(self):
        return f'<Feedback {self.username}>'

class FeedbackLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'feedback_id', name='uix_user_feedback'),)


    user = db.relationship('User', backref='feedback_likes')
    feedback = db.relationship('Feedback', backref='feedback_likes')

    def __repr__(self):
        return f'<FeedbackLike user_id={self.user_id} feedback_id={self.feedback_id}>'

class CityRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='ratings')

    __table_args__ = (db.UniqueConstraint('user_id', 'city_name', name='_user_city_uc'),)

    def __repr__(self):
        return f'<CityRating {self.city_name} - {self.rating}>'


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    excursion_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Rating {self.excursion_name} - {self.rating}>'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_average_rating(city_name):
    ratings = CityRating.query.filter_by(city_name=city_name).all()
    if ratings:
        avg_rating = sum([r.rating for r in ratings]) / len(ratings)
        return round(avg_rating, 1)
    return "Немає оцінок"

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/yaremche')
def yaremche():
    avg_rating = get_average_rating('yaremche')
    return render_template('yaremche.html', avg_rating=avg_rating, get_average_rating=get_average_rating)


@app.route('/shipit')
def shipit():
    avg_rating = get_average_rating('shipit')
    return render_template('shipit.html', avg_rating=avg_rating, get_average_rating=get_average_rating)

@app.route('/tram')
def tram():
    avg_rating = get_average_rating('tram')
    return render_template('tram.html', avg_rating=avg_rating, get_average_rating=get_average_rating)


@app.route('/synevir')
def synevir():
    avg_rating = get_average_rating('synevir')
    return render_template('synevir.html', avg_rating=avg_rating, get_average_rating=get_average_rating)


@app.route('/hoshiv')
def hoshiv():
    avg_rating = get_average_rating('hoshiv')
    return render_template('hoshiv.html', avg_rating=avg_rating, get_average_rating=get_average_rating)


@app.route('/dovbush')
def dovbush():
    avg_rating = get_average_rating('dovbush')
    return render_template('dovbush.html', avg_rating=avg_rating, get_average_rating=get_average_rating)


@app.route('/services')
def services():
    excursions = ["yaremche", "shipit", "tram", "synevir", "hoshiv", "dovbush"]
    ratings = {}

    for excursion in excursions:
        excursion_ratings = CityRating.query.filter_by(city_name=excursion).all()
        if excursion_ratings:
            avg_rating = sum(r.rating for r in excursion_ratings) / len(excursion_ratings)
            ratings[excursion] = round(avg_rating, 2)
        else:
            ratings[excursion] = "Немає оцінок"

    return render_template('services.html', ratings=ratings)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Паролі не співпадають. Спробуйте ще раз.', 'danger')
            return redirect(url_for('register'))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Це ім’я вже зайнято. Виберіть інше.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash('Цей номер телефону вже зареєстровано. Використайте інший номер.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, phone=phone, password=hashed_password, role='user')

        db.session.add(new_user)
        db.session.commit()

        flash('Реєстрація пройшла успішно! Ви можете увійти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.role == 'admin':
                flash('Вхід адміністратора', 'success')
                return redirect(url_for('index'))
            return redirect(url_for('index'))
        flash('Неправильний логін або пароль', 'danger')
    return render_template('login.html')

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if current_user.role != 'admin':
        flash('У вас немає доступу до цієї сторінки.', 'danger')
        return redirect(url_for('index'))

    bookings = Booking.query.all()
    users = User.query.all()
    return render_template('admin_bookings.html', bookings=bookings, users=users)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'success')
    return redirect(url_for('login'))

@app.route('/booking/<excursion_name>', methods=['GET', 'POST'])
@login_required
def booking(excursion_name):
    if request.method == 'POST':
        number_of_people = request.form.get('number_of_people')
        booking = Booking(user_id=current_user.id, excursion_name=excursion_name, number_of_people=number_of_people)
        db.session.add(booking)
        db.session.commit()
        flash(f'Екскурсію "{excursion_name}" успішно заброньовано на {number_of_people} осіб.', 'success')
        return redirect(url_for('services'))

    return render_template('booking.html', excursion_name=excursion_name)

@app.route('/delete_booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def delete_booking(booking_id):
    if current_user.role != 'admin':
        flash('У вас немає доступу до цієї сторінки.', 'danger')
        return redirect(url_for('index'))

    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Бронювання успішно видалено.', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/feedbacks', methods=['GET', 'POST'])
def feedbacks():
    if request.method == 'POST':

        username = current_user.username
        content = request.form['content']

        feedback = Feedback(username=username, content=content)
        db.session.add(feedback)
        db.session.commit()

        flash("Ваш відгук було успішно додано!", 'success')
        return redirect(url_for('feedbacks'))

    all_feedbacks = Feedback.query.all()

    return render_template('feedbacks.html', feedbacks=all_feedbacks)

@app.route('/feedbacks/reply/<int:feedback_id>', methods=['POST'])
@login_required
def reply_to_feedback(feedback_id):
    if current_user.role != 'admin':
        flash('У вас немає доступу до цієї сторінки.', 'danger')
        return redirect(url_for('feedbacks'))

    feedback = Feedback.query.get_or_404(feedback_id)

    response = request.form['response']

    feedback.response = response
    db.session.commit()

    flash('Відповідь успішно додана!', 'success')
    return redirect(url_for('feedbacks'))


@app.route('/rate_city/<city_name>', methods=['POST'])
@login_required
def rate_city(city_name):
    if current_user.role == 'admin':
        flash('Адміністратор не може оцінювати місця.', 'danger')
        return redirect(url_for(city_name))

    existing_rating = CityRating.query.filter_by(user_id=current_user.id, city_name=city_name).first()
    if existing_rating:
        flash(f'Ви вже оцінили місце "{city_name}".', 'danger')
        return redirect(url_for(city_name))

    try:
        rating = int(request.form['rating'])
        if 1 <= rating <= 5:
            city_rating = CityRating(city_name=city_name, rating=rating, user_id=current_user.id)
            db.session.add(city_rating)
            db.session.commit()
            flash(f'Дякуємо за оцінку місця "{city_name}"!', 'success')
        else:
            flash('Оцінка повинна бути від 1 до 5.', 'danger')
    except ValueError:
        flash('Невірний формат оцінки.', 'danger')

    return redirect(url_for(city_name))


@app.route('/like_feedback/<int:feedback_id>', methods=['POST'])
@login_required
def like_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        flash('Відгук не знайдено.', 'danger')
        return redirect(url_for('feedbacks'))

    if current_user in feedback.liked_by:
        feedback.liked_by.remove(current_user)
    else:
        feedback.liked_by.append(current_user)

    try:
        db.session.commit()
        flash('Ваше діяння успішно виконано.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Помилка при зміні лайку.', 'danger')
        print(f'Error: {e}')

    return redirect(url_for('feedbacks'))

@app.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Ви не маєте прав на видалення відгуків.', 'error')
        return redirect(url_for('feedbacks'))

    feedback = Feedback.query.get_or_404(feedback_id)

    feedback_likes = FeedbackLikes.query.filter_by(feedback_id=feedback.id).all()
    for like in feedback_likes:
        db.session.delete(like)

    if feedback.response:
        feedback.response = None

    db.session.delete(feedback)
    db.session.commit()

    flash('Відгук успішно видалено разом з лайками.', 'success')
    return redirect(url_for('feedbacks'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

