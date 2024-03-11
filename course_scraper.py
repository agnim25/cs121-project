import pandas as pd
import random
import requests
from bs4 import BeautifulSoup

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
