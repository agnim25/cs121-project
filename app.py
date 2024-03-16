"""
Student name(s): Damon Lin, Agnim Agarwal
Student email(s): dllin@caltech.edu, aagarwa7@caltech.edu

High-level program overview
This program provides recommendations for graduate student mentors to 
prospective undergraduate researchers. Undergrads can provide their own
personal research interests and get matching grad students with similar
interests/publications. Grad student data is initially scraped online, but
through this program, they can update their personal information and add 
information regarding student prereqs for any students applying to their
group.

"""

import sys
import mysql
import mysql.connector

from gensim.models import KeyedVectors
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt', quiet=True)
import re
import pandas as pd
import json

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = False
student_id, is_admin = None, None


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='admin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='cs121project'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
def log_in(username, password):
    """
    Attempts to log the user in by authenticating the user exists and
    has a valid password
    Args:
        username (string)
        password (string)
    """
    cursor = conn.cursor()
    sql = f'SELECT authenticate(%s, %s) AS result'
    try:
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()[0] # result = user_id if user exists otherwise 0
        if result > 0:
            print('Successfully logged in.')
        else:
            print(f'Incorrect credentials. Returning to the main menu')
            show_options(False)
            return
        
        # get user type (student vs. mentor)
        sql = 'SELECT user_type FROM users WHERE user_id = %s;'
        cursor.execute(sql, (result, ))
        user_type = cursor.fetchone()[0]

        return result, user_type == 'mentor'
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def sign_up_student():
    """
    Adds a new student
    """
    global student_id
    global is_admin
    cursor = conn.cursor()
    username = input('Choose your username: ').lower()
    
    try:
        # check if user exists
        sql = 'SELECT * FROM user_info WHERE username = %s;'
        cursor.execute(sql, (username,))
        rows = cursor.fetchall()
        if rows:
            print('Username already exists. Do you wish to login or sign up with a different username?')
            print('  (a) - Log in')
            print('  (b) - Sign up with a different username')
            print('  (c) - Return to main menu')
            ans = input('Enter an option: ').lower()
            if ans == 'a':
                password = input('Enter your password: ').lower()
                student_id, is_admin = log_in(username, password)
                show_options(student_id > 0)
            elif ans == 'b':
                sign_up_student()
            elif ans == 'c':
                show_options(False)
            else:
                print('Invalid choice. Returning to main menu.')
                show_options(False)
            return

        password = input('Choose your password: ').lower()

        # given user doesn't exist, get info for student profile
        print('As the next step, enter the following information: ')
        name = input('Full name: ')

        email = input('Caltech email: ')
        while not re.match(r'^[a-zA-Z]+@caltech\.edu$', email):
            email = input('Invalid email detected. Please enter your Caltech email address: ')

        year = input('Year? (1/2/3/4 for Frosh/Smore/Junior/Senior): ')
        while not re.match(r'^[1-4]$', year):
            year = input('Invalid year ented. Please enter your year as 1/2/3/4: ')
        year = int(year)

        surf = input('Looking for a SURF? (Y/N): ')
        while not re.match(r'^[YN]$', surf):
            surf = input('Invalid. Please enter Y/N: ')
        surf = (surf == 'Y')

        academic = input('Looking for academic-year research? (Y/N): ')
        while not re.match(r'^[YN]$', academic):
            academic = input('Invalid. Please enter Y/N: ')
        academic = (academic == 'Y')

        statement = input('Brief statement of research interests (min 10 words): ')
        while len(statement.split()) < 10:
            statement = input('Not enough words. Please enter a statement of at least 10 words: ')

        tokenized_sentence = word_tokenize(statement.lower())
        word_vectors = [pretrained_model[word] for word in tokenized_sentence if word in pretrained_model]
        embed = sum(word_vectors) / len(word_vectors)
        
        user_type = 'student'
        
        # add student to users table
        args = [name, email, year, surf, academic, user_type, json.dumps(embed.tolist()), 0]
        result_args = cursor.callproc('add_client', args)

        # The last element in result_args will be the user_id
        user_id = result_args[-1]

        if user_id is not None:
            # Add credentials to user_info
            cursor.callproc('sp_add_user', (username, password, user_id))
            conn.commit()

            # Add the research statement using the user_id
            cursor.callproc('add_student_research_statement', [user_id, statement])
            conn.commit()
            print(f'Student profile successfully registered.')
            student_id, is_admin = log_in(username, password)
        else:
            sys.stderr('An error occurred with adding a new student profile, please contact an admistrator...')
            
        
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred with registering a new user, please contact an admistrator...')


def sign_up_mentor():
    """
    Adds a new mentor
    """
    global student_id
    global is_admin
    cursor = conn.cursor()
    username = input('Choose your username: ').lower()
    try:
        # check if user exists
        sql = 'SELECT * FROM user_info WHERE username = %s;'
        cursor.execute(sql, (username,))
        rows = cursor.fetchall()
        if rows:
            print('Username already exists. Do you wish to login or sign up with a different username?')
            print('  (a) - Log in')
            print('  (b) - Sign up with a different username')
            print('  (c) - Return to main menu')
            ans = input('Enter an option: ').lower()
            if ans == 'a':
                password = input('Enter your password: ').lower()
                student_id, is_admin = log_in(username, password)
                show_options(student_id > 0)
            elif ans == 'b':
                sign_up_mentor()
            elif ans == 'c':
                show_options(False)
            else:
                print('Invalid choice. Returning to main menu.')
                show_options(False)
            return
        
        password = input('Choose your password: ').lower()

        # check if mentor profile exists, if so, connect credentials to existing account
        email = input('Enter your Caltech email: ')
        while not re.match(r'^[a-zA-Z]+@caltech\.edu$', email):
            email = input('Invalid email detected. Please enter your Caltech email address: ')
        sql = 'SELECT user_id FROM users WHERE email = %s AND user_type = \'mentor\';'
        cursor.execute(sql, (email,))
        rows = cursor.fetchall()
        if rows:
            print('Found existing profile.')
            cursor.callproc('sp_add_user', (username, password, rows[0][0]))
            conn.commit()
            print(f'Account successfully registered.')
        
        # collect info for new mentor profile
        else:
            print('Looks like we don\'t have your profile. Please enter the following information: ')
            name = input('Full name: ')

            year = input('Year (1-9)?: ')
            while not re.match(r'^[1-9]$', year):
                year = input('Invalid year ented. Please enter a valid year (1-9): ')
            year = int(year)

            surf = input('Looking for a SURF student? (Y/N): ')
            while not re.match(r'^[YN]$', surf):
                surf = input('Invalid. Please enter Y/N: ')
            surf = (surf == 'Y')

            academic = input('Looking for an academic-year student? (Y/N): ')
            while not re.match(r'^[YN]$', academic):
                academic = input('Invalid. Please enter Y/N: ')
            academic = (academic == 'Y')

            statement = input('Keywords describing your research interests (comma-separated): ')
            keywords = statement.split(',')
            sentence = ' '.join(keywords)

            advisor = input('Advisor Name: ')
            department = input('Department: ')

            tokenized_sentence = word_tokenize(sentence.lower())
            word_vectors = [pretrained_model[word] for word in tokenized_sentence if word in pretrained_model]
            embed = sum(word_vectors) / len(word_vectors)
            
            args = [name, email, year, surf, academic, 'mentor', json.dumps(embed.tolist()), 0]
            result_args = cursor.callproc('add_client', args)

            # The last element in result_args will be the user_id
            user_id = result_args[-1]

            if user_id is not None:
                # add to user_info
                cursor.callproc('sp_add_user', (username, password, user_id))
                conn.commit()

                # add to mentor table
                cursor.callproc('add_mentor', (user_id, department, advisor))
                conn.commit()

                # add each keyword as a new row to the keywords table
                for keyword in keywords:
                    cursor.callproc('add_keyword', (user_id, keyword))
                    conn.commit()

                print('Mentor profile successfully registered.')
                student_id, is_admin = log_in(username, password)

            else:
                sys.stderr('An error occurred with adding a new student profile, please contact an admistrator...')
                
            
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred with registering a new user, please contact an admistrator...')



# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options(logged_in):
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    global is_admin
    global student_id

    print('What would you like to do? ')
    if not logged_in:
        print('  (l) - Log in')
        print('  (s) - Sign up as student')
        print('  (t) - Sign up as mentor')
    else:
        if not is_admin:
            print('  (m) - Find top 10 mentors for you')
        print('  (p) - Find most recent publications for a specific mentor')
        print('  (d) - Find mentors in a specific department')
        print('  (u) - Find mentors in a specific department taking students for SURF')
        print('  (a) - Find mentors in a specific department taking students for academic year research')
        print('  (o) - Log out')
    print('  (q) - Quit')
    print()
    ans = input('Enter an option: ').lower()
    
    # intro menu options
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        username = input('Enter your username: ').lower()
        password = input('Enter your password: ').lower()
        student_id, is_admin = log_in(username, password)
        show_options(student_id > 0)
    elif ans == 's':
        sign_up_student()
        show_options(True)
    elif ans == 't':
        sign_up_mentor()
        show_options(True)
    elif ans == 'o':
        show_options(False)

    # logged in menu options        
    elif ans == 'm':
        find_top_mentors()
        show_options(logged_in)
    elif ans == 'p':
        name = input('Enter the name of the mentor: ')
        find_publications(name)
        show_options(logged_in)
    elif ans == 'd':
        department = input('Enter the department name: ')
        find_mentors_department(department)
        show_options(logged_in)
    elif ans == 'u':
        department = input('Enter the department name: ')
        find_mentors_surf(department)
        show_options(logged_in)
    elif ans == 'a':
        department = input('Enter the department name: ')
        find_mentors_academic(department)
        show_options(logged_in)
    else:
        show_options(logged_in)


def find_top_mentors():
    """
    Calculate the top mentors by similarity to the logged-in student, printed to system output
    """
    cursor = conn.cursor()

    try:
        # compute each mentor embedding vector for anyone with updated info
        
        # for these mentors, query their abstracts and keywords
        query = """
        SELECT 
            kw.user_id AS user_id, 
            kw.keywords AS keywords, 
            ab.abstracts AS abstracts
        FROM
            (SELECT u.user_id, GROUP_CONCAT(k.keyword SEPARATOR ' ') AS keywords
            FROM mentors u
            JOIN keywords k ON u.user_id = k.user_id
            WHERE u.interests_last_updated IS NOT NULL
            GROUP BY u.user_id) AS kw
        JOIN
            (SELECT u.user_id, GROUP_CONCAT(p.abstract SEPARATOR ' ') AS abstracts
            FROM mentors u
            JOIN publications p ON u.user_id = p.user_id
            WHERE u.interests_last_updated IS NOT NULL AND p.abstract IS NOT NULL
            GROUP BY u.user_id) AS ab
        ON kw.user_id = ab.user_id;
        """

        # compute embedding for each mentor
        df = pd.read_sql(query, conn)
        for i in range(len(df)):
            id = df.iloc[i]['user_id']
            abstracts = df.iloc[i]['abstracts']
            interests = df.iloc[i]['keywords']

            if len(abstracts) > 0 or len(interests) > 0:
                sentence = (interests + abstracts).lower()
                tokenized_sentence = word_tokenize(sentence)

                word_vectors = np.array([pretrained_model[word] for word in tokenized_sentence if word in pretrained_model])
                
                # if descriptors exists, update users table to store up-to-date embedding
                if word_vectors.size > 0:
                    embed = np.mean(word_vectors, axis=0)
                    
                    update_query = """
                    UPDATE users
                    SET embedding_vector = %s
                    WHERE user_id = %s
                    """
                    cursor.execute(update_query, (json.dumps(embed.tolist()), int(id),))
                    conn.commit()
            
            # update date flag to null to show embedding is up-to-date
            update_date_query = """
            UPDATE mentors
            SET interests_last_updated = NULL
            WHERE user_id = %s
            """
            cursor.execute(update_date_query, (int(id),))
            conn.commit()

        # find the similarity between the student and each mentor
        
        # get student vector
        query = "SELECT embedding_vector FROM users WHERE user_id = %s"
        cursor.execute(query, (int(student_id),))
        result = cursor.fetchone()
        student_vector = np.array(json.loads(result[0]))
        
        # get mentor vectors
        query = "SELECT user_id, embedding_vector FROM users WHERE user_type = 'mentor'"
        df = pd.read_sql(query, conn)
        scores = {}
        for i in range(len(df)):
            entry = df.iloc[i]['embedding_vector']
            if entry:
                vector = np.array(json.loads(df.iloc[i]['embedding_vector']))
                similarity_score = cosine_similarity(student_vector.reshape(1, -1), vector.reshape(1, -1))
                scores[df.iloc[i]['user_id']] = similarity_score

        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        top10 = list(scores.items())[:10]
        
        # output name of top 10 results
        for i in range(10):
            query = "SELECT name FROM users WHERE user_id = %s"
            cursor.execute(query, (int(top10[i][0]),))
            mentor_name = cursor.fetchone()[0]
            print((i+1), mentor_name, top10[i][1][0][0])

    
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')


def find_publications(name):
    """
    Query and print the publication links for a given mentor
    """
    cursor = conn.cursor(buffered=True)
    query = "SELECT user_id FROM users WHERE name = %s;"
    try:
        cursor.execute(query, (name,))
        id = cursor.fetchone()
        if id is None:
            print('User not found')
            return
        
        id = id[0]
        sql = 'SELECT link FROM publications WHERE user_id = %s ORDER BY publication_date;'
        cursor.execute(sql, (id,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row[0])
        else:
            print('No publications found')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def find_mentors_surf(department):
    """
    Find mentors who are looking for a SURF student in a specific department
    Args:
        department (string)
    """
    cursor = conn.cursor()
    sql = """SELECT name
            FROM users
            JOIN mentors ON users.user_id = mentors.user_id
            WHERE mentors.department = %s AND surf = 1
            AND users.user_type = \'mentor\';"""
    try:
        cursor.execute(sql, (department,))
        rows = cursor.fetchall()
        for row in rows:
            print(row[0].strip())
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')
            
def find_mentors_academic(department):
    """
    Find mentors looking for an academic-year student in a specific department
    Args:
        department (string)
    """
    cursor = conn.cursor()
    sql = """SELECT name
            FROM users
            JOIN mentors ON users.user_id = mentors.user_id
            WHERE mentors.department = %s AND academic_year = 1
            AND users.user_type = \'mentor\';"""
    try:
        cursor.execute(sql, (department,))
        rows = cursor.fetchall()
        for row in rows:
            print(row[0].strip())
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')
            
def find_mentors_department(department):
    """
    Find all mentors in a specific department
    Args:
        department (string)
    """
    cursor = conn.cursor()
    sql = """SELECT name
            FROM users
            JOIN mentors ON users.user_id = mentors.user_id
            WHERE mentors.department = %s
            AND users.user_type = \'mentor\';"""
    try:
        cursor.execute(sql, (department,))
        rows = cursor.fetchall()
        for row in rows:
            print(row[0].strip())
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    print('Loading Word Embedding Model...')
    model_path = 'glove.6B.50d.txt'
    pretrained_model = KeyedVectors.load_word2vec_format(model_path, binary=False, no_header=True)
    while True:
        show_options(False)
