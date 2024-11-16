from datetime import timedelta, datetime
import hashlib
from secretKey import APP_SECRET_KEY
from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.permanent_session_lifetime = timedelta(days=7)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
            SELECT polls.*, users.username 
            FROM polls 
            INNER JOIN users ON polls.created_by = users.id 
            ORDER BY polls.created_at DESC
        ''')
    polls = cur.fetchall()
    print(polls)
    cur.close()
    conn.close()

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
        print(f'hello: {user_id}')

        if user_id is None:
            user_id = 1

        print(user_id)

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute('''INSERT INTO POLLS (title, description, created_by) VALUES (%s,%s,%s) RETURNING id''', (polls[0]['title'], polls[0]['description'], user_id))
            poll_id = cur.fetchone()[0]

            for poll in polls:
                list_of_questions = poll['questions']
                for question in list_of_questions:
                    text = question['question']
                    cur.execute('''INSERT INTO QUESTIONS (poll_id, question_text) VALUES(%s,%s) RETURNING id''', (poll_id, text))
                    question_id = cur.fetchone()[0]

                    list_of_answers = question['answers']
                    for answer in list_of_answers:
                        cur.execute('''INSERT INTO ANSWERS (question_id, answer_text) VALUES(%s,%s)''', (question_id, answer))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(Exception)
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('home'))

    return render_template('create_poll.html')


@app.route('/poll/<int:poll_id>/delete', methods=('POST',))
def delete_poll(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''DELETE FROM response_answers 
                     WHERE answer_id IN (
                        SELECT id FROM answers 
                        WHERE question_id IN (
                            SELECT id FROM questions 
                            WHERE poll_id = %s
                        )
                    )
            ''', (poll_id,)
        )

        cur.execute(
            '''DELETE FROM responses 
                     WHERE poll_id = %s
            ''', (poll_id,)
        )

        cur.execute(
            '''DELETE FROM ANSWERS 
                     WHERE question_id IN (
                        SELECT id FROM QUESTIONS 
                        WHERE poll_id = %s
            )''', (poll_id,)
        )

        cur.execute(
            '''DELETE FROM QUESTIONS 
                     WHERE poll_id = %s
            ''', (poll_id,)
        )

        cur.execute(
            '''DELETE FROM POLLS 
                     WHERE id = %s
            ''', (poll_id,)
        )

        conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()

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



    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM POLLS
                WHERE id = %s
            ''', (poll_id,))
    poll_information = cur.fetchone()

    cur.execute('''
        SELECT * FROM QUESTIONS
        WHERE poll_id = %s
    ''', (poll_id,))
    questions = cur.fetchall()

    list_of_questions = []
    for question in questions:
        cur.execute('''
            SELECT * FROM ANSWERS
            WHERE question_id = %s
        ''', (question[0],))
        answers = cur.fetchall()
        current_question = {
            'question_id': question[0],
            'question_text': question[2],
            'answers': answers
        }
        list_of_questions.append(current_question)

    print(f'list_of_questions: {list_of_questions}')


    cur.close()
    conn.close()
    responses = []


    if is_done:
        if not skip_database_requests:
            conn = get_db_connection()
            cur = conn.cursor()

            try:
                query = '''
                    SELECT q.question_text AS question, a.answer_text AS answer, r.submitted_at AS submitted_at
                    FROM responses r
                    JOIN response_answers ra ON r.id = ra.response_id
                    JOIN answers a ON ra.answer_id = a.id
                    JOIN questions q ON a.question_id = q.id
                    WHERE r.user_id = %s AND r.poll_id = %s;
                '''

                cur.execute(query, (user_id, poll_id))
                results = cur.fetchall()
                responses = [{'question': row[0], 'answer': row[1], 'submit_time': row[2]} for row in results]
                print(responses)

            except Exception as e:
                print(e)

            finally:
                cur.close()
                conn.close()

        else:
            conn = get_db_connection()
            cur = conn.cursor()

            keys_of_temp_responses = list(temp_response.keys())

            array_of_questions_and_answers = []
            for key in keys_of_temp_responses:
                print(poll_id)
                print(f'key: {key}')
                print(f'temp_response[key]: {temp_response[key]}')
                if key != 'poll_id':
                    query = '''
                    SELECT q.question_text, a.answer_text
                    FROM questions q
                    JOIN answers a ON q.id = a.question_id
                    WHERE q.poll_id = %s AND q.id = %s AND a.id = %s;
                    '''
                    cur.execute(query, (poll_id, key, temp_response[key]))
                    results = cur.fetchone()
                    print(f'results: {results}')
                    array_of_questions_and_answers.append(results)

            responses = []
            print(f'response: {array_of_questions_and_answers}')
            for response in array_of_questions_and_answers:
                responses.append({'question': response[0], 'answer': response[1], 'submit_time': datetime.now()})

            print(f'resp: {responses}')



    return render_template('chosen_poll.html', poll=poll_information, questions=list_of_questions, user_poll_taken=is_done, results=responses)


@app.route('/submit_poll', methods=['POST'])
def submit_poll():
    if request.method == 'POST':
        responses = request.form.to_dict()
        print(f'responses: {responses}')
        user_id = session.get('user_id')

        if user_id:
            conn = get_db_connection()
            cur = conn.cursor()

            try:
                cur.execute('''
                    INSERT INTO responses(poll_id, user_id)
                    VALUES (%s, %s)
                    RETURNING id
                ''', (responses['poll_id'], user_id))
                response_id = cur.fetchone()[0]

                keys = list(responses.keys())
                for key in keys:
                    if key != 'poll_id':

                        cur.execute('''
                            INSERT INTO response_answers(response_id, answer_id)
                            VALUES (%s, %s)
                        ''',(response_id, responses[key]))

                conn.commit()

            except Exception as e:
                conn.rollback()
                print(e)

            finally:
                cur.close()
                conn.close()
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

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)', (username, password_hash, email))
            conn.commit()
            flash('Registration successful! Log in now', 'success')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            flash('Such user is already registered!', 'danger')
            conn.rollback()  # Откат транзакции
        finally:
            cur.close()
            conn.close()
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE username = %s AND password_hash = %s', (username, password_hash))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = username
            flash('You are now logged in!', 'success')
            return redirect(url_for('home'))  # Перенаправление на главную страницу
        else:
            flash('There is no user with that username and password', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Yo\'ve logged out!', 'success')
    return redirect(url_for('home'))


def is_chosen_poll_done_by_user(user_id, poll_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT COUNT(*) FROM responses WHERE user_id = %s AND poll_id = %s
    ''', (user_id, poll_id))

    result = cur.fetchone()[0]
    cur.close()
    conn.close()

    if result > 0:
        is_done = True
    else:
        is_done = False

    return is_done

def anonymous_response_save(response):
    session['temporary_response'] = response


if __name__ == '__main__':
    app.run(debug=True)
