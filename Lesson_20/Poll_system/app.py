from datetime import timedelta, datetime

from flask import Flask, render_template, request, session, url_for, redirect, flash
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from Poll_system.secretKey import APP_SECRET_KEY
from models import db, Users, Polls, Questions, Answers, Responses, Response_answers
from config import Config
import hashlib

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.secret_key = APP_SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=1)

def setup():
    inspector = inspect(db.engine)
    if not inspector.has_table('users'):
        db.create_all()
    anonymous_user = Users.query.filter_by(username="Anonymous", id=1).first()

    if anonymous_user:
        print('The app is finally set up and ready to go!')

    else:
        print('Firstly we need to create an Anonymous user.')
        anonymous_user = Users(username="Anonymous", password_hash='1234567890qwertyuiop', email='none@gmail.com')
        db.session.add(anonymous_user)
        db.session.commit()
        db.session.close()
        print('Anonymous user created. We can start!')

@app.route('/')
def home():
    polls = Polls.query.order_by(Polls.id.desc()).all()
    for poll in polls:
        poll = poll.__dict__
        creator_id = poll['created_by']
        poll_creator_tuple = Users.query.with_entities(Users.username).filter_by(
            id=creator_id).first()
        poll['created_by'] = poll_creator_tuple[0]


    return render_template('home.html', polls = polls)


@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        poll_title = request.form['poll_title']
        poll_description = request.form['poll_desc']
        polls = []
        questions = []

        for i in range(len(request.form.getlist('questions[]'))):
            question_text = request.form.getlist('questions[]')[i]
            answers = request.form.getlist(f'answers[{i}][]')
            questions.append({
                'question': question_text,
                'answers': [answer for answer in answers[0].strip().split(';') if answer.strip()],
            })

        polls.append({
            'title': poll_title,
            'description': poll_description,
            'questions': questions
        })

        user_id = session.get('user_id')

        if user_id is None:
            user_id = 1


        try:
            new_poll = Polls(title=poll_title, description=poll_description, created_by=user_id)
            db.session.add(new_poll)
            db.session.flush()
            poll_id = new_poll.id


            for poll in polls:
                list_of_questions = poll['questions']
                for question in list_of_questions:
                    text = question['question']
                    new_question = Questions(poll_id=poll_id, question_text=text)
                    db.session.add(new_question)
                    db.session.flush()
                    question_id = new_question.id


                    list_of_answers = question['answers']
                    for answer in list_of_answers:
                        answer = Answers(question_id=question_id, answer_text=answer)
                        db.session.add(answer)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

        return redirect(url_for('home'))

    return render_template('create_poll.html')


@app.route('/poll/<int:poll_id>/delete', methods=('POST',))
def delete_poll(poll_id):
    try:
        poll = Polls.query.get(poll_id)

        response_ids = Responses.query.with_entities(Responses.id).filter_by(poll_id=poll_id).all()
        response_ids_list = [r[0] for r in response_ids]

        if response_ids_list:
            Response_answers.query.filter(Response_answers.response_id.in_(response_ids_list)).delete(
                synchronize_session=False)

        Responses.query.filter_by(poll_id=poll_id).delete()

        questions = Questions.query.filter_by(poll_id=poll_id).all()

        for question in questions:
            Answers.query.filter_by(question_id=question.id).delete()

        Questions.query.filter_by(poll_id=poll_id).delete()


        db.session.delete(poll)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()

    finally:
        db.session.close()

    return redirect(url_for('home'))


@app.route('/poll/<int:poll_id>', methods=['GET'])
def view_poll(poll_id):
    user_id = session.get('user_id')

    if user_id:
        skip_database_requests = False
        is_done = is_chosen_poll_done_by_user(user_id, poll_id)
    else:
        skip_database_requests = True
        temp_response = session.get('temporary_response')
        if temp_response and int(temp_response.get('poll_id')) == poll_id:
            is_done = True
        else:
            is_done = False


    poll_information = Polls.query.filter_by(id=poll_id).first().__dict__
    questions = Questions.query.filter_by(poll_id=poll_id).all()

    list_of_questions = []
    for question in questions:
        question = question.__dict__
        answers = Answers.query.filter_by(question_id=question['id']).all()
        answers = list(map(lambda answer: answer.__dict__, answers))
        current_question = {
            'question_id': question['id'],
            'question_text': question['question_text'],
            'answers': answers
        }
        list_of_questions.append(current_question)


    responses = []

    if is_done:
        if not skip_database_requests:

            try:
                results = db.session.query(
                    Questions.question_text.label('question'),
                    Answers.answer_text.label('answer'),
                    Responses.submitted_at.label('submitted_at')
                ).join(Response_answers, Responses.id == Response_answers.response_id) \
                .join(Answers, Response_answers.answer_id == Answers.id) \
                .join(Questions, Answers.question_id == Questions.id) \
                .filter(Responses.user_id == user_id, Responses.poll_id == poll_id).all()

                responses = [{'question': row[0], 'answer': row[1], 'submit_time': row[2]} for row in results]

            except Exception as e:
                db.session.rollback()
                print(e)

            finally:
                db.session.close()

        else:
            keys_of_temp_responses = list(temp_response.keys())

            array_of_questions_and_answers = []
            for key in keys_of_temp_responses:
                if key != 'poll_id':

                    result = db.session.query(
                        Questions.question_text,
                        Answers.answer_text
                    ).join(Answers, Questions.id == Answers.question_id) \
                    .filter(
                        Questions.poll_id == poll_id,
                        Questions.id == key,
                        Answers.id == temp_response[key]
                    ).first()


                    array_of_questions_and_answers.append(result)

            responses = []
            for response in array_of_questions_and_answers:
                responses.append({'question': response[0], 'answer': response[1], 'submit_time': datetime.now()})




    return render_template('chosen_poll.html', poll=poll_information, questions=list_of_questions, user_poll_taken=is_done, results=responses)


@app.route('/submit_poll', methods=['POST'])
def submit_poll():
    if request.method == 'POST':
        responses = request.form.to_dict()
        user_id = session.get('user_id')

        if user_id:

            try:

                response = Responses(poll_id=responses['poll_id'], user_id=user_id)
                db.session.add(response)
                db.session.flush()
                response_id = response.id

                keys = list(responses.keys())
                for key in keys:
                    if key != 'poll_id':

                        response_answer = Response_answers(response_id=response_id, answer_id=responses[key])
                        db.session.add(response_answer)
                        db.session.flush()


                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print(e)

            finally:
                db.session.close()
        else:
            anonymous_response_save(responses)

    return redirect(url_for('view_poll', poll_id=responses['poll_id']))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()


        try:

            user = Users(username=username, password_hash=password_hash, email=email)
            db.session.add(user)
            db.session.commit()

            flash('Registration successful! Log in now', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            flash('Such user is already registered!', 'danger')
            db.session.rollback()
        finally:
            db.session.close()

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = Users.query.filter_by(username=username, password_hash=password_hash).first()

        db.session.close()

        if user:
            session['user_id'] = user.__dict__['id']
            session['username'] = username
            flash('You are now logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('There is no user with that username and password', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Yo\'ve logged out!', 'success')
    return redirect(url_for('home'))


def is_chosen_poll_done_by_user(user_id, poll_id):

    result = db.session.query(Responses).filter_by(user_id=user_id, poll_id=poll_id).count()
    db.session.close()

    if result > 0:
        is_done = True
    else:
        is_done = False

    return is_done

def anonymous_response_save(response):
    session['temporary_response'] = response


if __name__ == "__main__":
    with app.app_context():
        setup()
    app.run(debug=True)