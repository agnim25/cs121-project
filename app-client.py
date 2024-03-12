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
import mysql.connector
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


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
          user='client',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='clientpw',
          database='cs121project' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
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


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options(logged_in):
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    if not logged_in:
        print('  (l) - Log in')
        print('  (s) - Sign up')
    else:
        print('  (m) - Find top 10 mentors')
        print('  (p) - Find most recent publications for a specific mentor')
        print('  (d) - Find top mentors in a specific department')
        print('  (y) - Find top mentors taking students in a specific year')
        print('  (o) - Log out')
    print('  (q) - Quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        username = input('Enter your username: ').lower()
        password = input('Enter your password: ').lower()
        result = log_in(username, password)
        show_options(result)
    elif ans == 's':
        username = input('Choose your username: ').lower()
        password = input('Choose your password: ').lower()
        sign_up(username, password)
        show_options(True)
    elif ans == 'o':
        show_options(False)
    elif ans == 'm':
        find_top_mentors()
        show_options(logged_in)
    elif ans == 'p':
        print('Enter the name of the mentor: ')
        name = input()
        find_publications(name)
        show_options(logged_in)
    elif ans == 'd':
        print('Enter the department name: ')
        department = input()
        find_top_mentors_department(department)
        show_options(logged_in)
    elif ans == 'y':
        # finds top mentors for student's year
        print('Enter the student\'s year: ')
        year = input()
        find_top_mentors_year(year)
        show_options(logged_in)
    else:
        show_options(logged_in)


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
        result = cursor.fetchone()[0]
        if result:
            print('Successfully logged in.')
        else:
            print(f'Incorrect password for {username}')
        return result
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def sign_up(username, password):
    """
    Adds a new user with the specified username and password
    Args:
        username (string)
        password (string)
    """
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_add_user', (username, password))
        conn.commit()
        print('Account sucessfully registered')
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if err.errno == errorcode.ER_DUP_ENTRY:
            sys.stderr('Username already exists, log in instead')
        else:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr('An error occurred, please contact an admistrator...')

def find_top_mentors():
    cursor = conn.cursor()
    sql = ''
    try:
        rows = cursor.execute(sql)
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def find_publications(name):
    cursor = conn.cursor()
    sql = 'SELECT link FROM publications WHERE mentor_id = ' + \
    '(SELECT mentor_id FROM mentors WHERE mentor_name = \'%s\') ORDER BY publication_date;' % (name, )
    try:
        rows = cursor.execute(sql)
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')

def find_top_mentors_year(year):
    cursor = conn.cursor()
    sql = ''
    try:
        rows = cursor.execute(sql)
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please contact an admistrator...')
            
def find_top_mentors_department(department):
    cursor = conn.cursor()
    sql = 'SELECT mentor_name FROM mentors WHERE department_name = \'%s\';' % (department, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
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


def main():
    """
    Main function for starting things up.
    """
    show_options(False)


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
