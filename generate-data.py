import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
from faker import Faker

def scrape_caltech_courses(department_code, academic_year):
    base_url = "https://www.catalog.caltech.edu"
    department_url = f"{base_url}/current/{academic_year}/department/{department_code}/"

    # Make an HTTP request to the department's page
    response = requests.get(department_url)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    labels = soup.find_all('div', {'class': 'course-description2__label'})
    titles = soup.find_all('h2', {'class': 'course-description2__title'})

    courses = []
    for label, title in zip(labels, titles):
        label = label.text.strip()
        title = title.text.strip()
        courses.append(label + ': ' + title)

    return courses

# Example usage
department_code = "CS"
academic_year = "2023-24"
all_courses = scrape_caltech_courses(department_code, academic_year)
all_mentors = list(range(420))

courses = []
mentor_ids = []
for mentor in all_mentors:
    course = random.sample(all_courses, 5)
    courses.extend(course)
    mentor_ids.extend([mentor] * 5)



data = {
    'course': courses,
    'mentor_id': mentor_ids
}

df = pd.DataFrame(data)
df.to_csv('prerequisite_courses.csv', index=False)

fake = Faker()
names = [fake.name() for _ in range(254 * 5)]
mentors = [i for i in range(1, 255)] * 5
student_grad_years = [random.randint(2000, 2020) for _ in range(254 * 5)]

data = {
    'student_name': names,
    'mentor_id': mentors,
    'student_grad_year': student_grad_years
}

df = pd.DataFrame(data)
df.to_csv('past_students.csv', index=False)

names = [fake.name() for _ in range(500)]
emails = [name.split()[0][0].lower() + name.split()[1].lower() + '@caltech.edu' for name in names]

data = {
    'student_id': list(range(1, 501)),
    'student_name': names,
    'email': emails,
    'interests': [None] * 500,
}

df = pd.DataFrame(data)
df.to_csv('students.csv', index=False)
