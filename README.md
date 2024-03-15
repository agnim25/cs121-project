# CS 121 Project

This project provides recommendations for graduate student mentors to 
prospective undergraduate researchers. Undergrads can provide their own
personal research interests and get matching grad students with similar
interests/publications. Grad student data is initially scraped online, but
through this program, they can update their personal information and add 
information regarding student prereqs for any students applying to their
group.

Contributors: Damon Lin, Agnim Agarwal

Data sources: Google Scholars, Caltech CMS Website

Instructions for loading data on command-line:
Make sure you have MySQL downloaded and available through your
device's command-line.

### To run this project, do the following in the terminal:
`$ cd path-to-this-repo`

`$ mysql`

`mysql> drop database cs121project;`

`mysql> create database cs121project;`

`mysql> use cs121project;`

`mysql> source setup.sql;`

`mysql> source load-data.sql;`

`mysql> source setup-routines.sql;`

`mysql> source grant-permissions.sql;`

`mysql> quit;`

### To run the Python application:
`$ python3 app.py`

Follow the instructions in the terminal to sign up or log in.

Files written to user's system:
- No files are written to the user's system.
