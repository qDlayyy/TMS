import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

try:

    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = connection.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS polls (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
            """)
    connection.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            poll_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls (id)
        )
            """)
    connection.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id SERIAL PRIMARY KEY,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    """)
    connection.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            poll_id INTEGER NOT NULL,
            user_id INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (poll_id) REFERENCES polls (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    connection.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS response_answers (
            id SERIAL PRIMARY KEY,
            response_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            FOREIGN KEY (response_id) REFERENCES responses (id),
            FOREIGN KEY (answer_id) REFERENCES answers (id)
        )
    """)
    connection.commit()
    print("Tables created successfully.")

    cur.execute('''
        SELECT * FROM users WHERE id = %s AND username = %s
    ''', (1, 'Anonymous'))
    anonymous = cur.fetchone()

    if not anonymous:
        cur.execute('''
            INSERT INTO users (username, password_hash, email)
            VALUES (%s, %s, %s)
        ''', ('Anonymous', 'NN:nlnva9ivobweiovb^bavevbjaSDVLBd', 'none@gmail.com'))
        connection.commit()
        print('Anonymous user has been created. We are ready to go.')
    else:
        print('Everything is ok. We are ready to start.')


except Exception as e:
    connection = None
    print(f'\n### Warning. Exception {e}')

finally:
    if connection:
        cur.close()
        connection.close()