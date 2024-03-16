# CS 121 Project

This project provides recommendations for graduate student mentors to 
prospective undergraduate researchers. Undergrads can provide their own
personal research interests and get matching grad students with similar
interests/publications. Grad student data is initially scraped online, but
through this program, they can update their personal information and add 
information regarding student prereqs for any students applying to their
group.

Contributors: Damon Lin, Agnim Agarwal

Data sources: Google Scholar, Caltech CMS Website

### Instructions for setting up the database:

Make sure you have MySQL downloaded and available through your
device's command-line.

First, create a database in MySQL:

```
mysql> create database cs121project;
mysql> use cs121project;
```

Run the following setup commands:

```
mysql> source setup.sql;
mysql> source load-data.sql;
mysql> source setup-routines.sql;
mysql> source grant-permissions.sql;
```

### Instructions for running the Python program:

First, exit MySQL:

`mysql> quit;`

Install requirements and run the program:

```
$ pip install -r requirements.txt
$ python3 app.py
```

For students, the following user is registered:
```
    USERNAME | PASSWORD
agnimagarwal | password
```

For mentors, the following user is registered:
```
    USERNAME | PASSWORD
    damonlin | password
```
Though, feel free to sign up as a new student/mentor.

Here is an example run through to demonstrate our matching process:
First, sign up as a mentor with the following information:

```
What would you like to do? 
  (l) - Log in
  (s) - Sign up as student
  (t) - Sign up as mentor
  (q) - Quit

Enter an option: t
Choose your username: test
Choose your password: pass
Enter your Caltech email: test@caltech.edu
Looks like you don't have your profile. Please enter the following information: 
Full name: test
Year (1-9)?: 1
Looking for a SURF student? (Y/N): Y
Looking for an academic-year student? (Y/N): Y
Keywords describing your research interests (comma-separated): web development,databases,distributed systems,networking,computer systems,low-level programming
Advisor Name: Hovik
Department: Computing and Mathematical Sciences
Mentor profile successfully registered.
Successfully logged in.
```

Now, log out and sign up as a student with similar interests:
```
What would you like to do? 
  (p) - Find most recent publications for a specific mentor
  (d) - Find mentors in a specific department
  (u) - Find mentors in a specific department taking students for SURF
  (a) - Find mentors in a specific department taking students for academic year research
  (o) - Log out
  (q) - Quit

Enter an option: o
What would you like to do? 
  (l) - Log in
  (s) - Sign up as student
  (t) - Sign up as mentors
  (q) - Quit

Enter an option: s
Choose your username: stu
Choose your password: pass
As the next step, enter the following information: 
Full name: stu
Caltech email: stu@caltech.edu
Year? (1/2/3/4 for Frosh/Smore/Junior/Senior): 1
Looking for a SURF? (Y/N): Y
Looking for academic-year research? (Y/N): Y
Brief statement of research interests (min 10 words): web development databases distributed systems networking computer systems low-level programming
Student profile successfully registered.
Successfully logged in.
```
Now, if you query for top mentors (m), you will find the test mentor as the top result:

```
What would you like to do? 
  (m) - Find top 10 mentors for you
  (p) - Find most recent publications for a specific mentor
  (d) - Find mentors in a specific department
  (u) - Find mentors in a specific department taking students for SURF
  (a) - Find mentors in a specific department taking students for academic year research
  (o) - Log out
  (q) - Quit

Enter an option: m
1 test 1.0000000000000002
2 Damon Lin 0.8667379082026435
3 Matthieu D. Darcy 0.7925991733534379
4 Ethan N. Epperly 0.7845285786487378
5 Wenda Chu 0.7722294877570769
6 Noel V. Csomay-Shanklin 0.7718775709018902
7 Adrian Boedtker Ghansah 0.770719028115248
8 Aadarsh Sahoo 0.7570744971086892
9 Danil Akhtiamov 0.7543615705917754
10 Apurva Badithela 0.7541295604083703
```

Press Ctrl+C to leave the program at any time.

Files written to user's system:
- No files are written to the user's system.

Unfinished features:
- Rigorous checks to validate user input (currently only basic checks are implemented)
- More detailed output for each feature
- Rigorous permissions for students and mentors (currently permissions are through user_type flag)
- Allowing users to insert/update data after signing up
- Rigorous sign up for mentors (currently a mentor's sign up is linked to existing profiles just through matching emails)
- Showing appropriate mySQL errors in the Python interface.