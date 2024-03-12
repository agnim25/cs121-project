import requests
from bs4 import BeautifulSoup
import pandas as pd
import mechanize
from bs4 import BeautifulSoup
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

csv_out = pd.DataFrame(columns=['mentor_name', 'department_name', 'email', 'is_surf', 'is_academic_year'])

departments = {'Computing and Mathematical Sciences': 'https://www.cms.caltech.edu/people/grads',
               'Electrical Engineering': 'https://www.ee.caltech.edu/people/graduate-students',
               'Applied Physics': 'https://aph.caltech.edu/people/graduate-students',
               'Materials Science': 'https://ms.caltech.edu/people/graduate-students',
               'Environmental Science and Engineering': 'https://www.ese.caltech.edu/people/grads',
               'Mechanical and Civil Engineering': 'https://www.mce.caltech.edu/people/graduate-students',
               'Medical Engineering': 'https://www.mede.caltech.edu/people/graduate-students',
               'Aerospace': 'https://www.galcit.caltech.edu/people/graduate-students'}

for dept in departments:
    
    url = departments[dept]
    # Send a GET request to the page
    response = requests.get(url)
    print(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements that contain names
        # This is an example; you'll need to adjust the selector based on the actual webpage structure
        name_elements = soup.find_all('a', class_='person-teaser__link')
        # Extract and print each name
        for element in name_elements:
            name = element.get_text().strip()

            try:
                # get email from caltech directory
                url = "https://directory.caltech.edu/"
                br = mechanize.Browser()
                br.open(url)
                br.select_form(nr=0)
                br.form['query'] = name
                br.submit()
                content = br.response().read()
                soup = BeautifulSoup(content, "html.parser")
                email = soup.find_all('a', {'class': 'email'})[0].contents[0]
                
                # default - surf and academic year are true
                csv_out = csv_out.append({'mentor_name': name, 'department_name': dept, 'email': email, 'is_surf': True, 'is_academic_year': True}, ignore_index=True)
                csv_out.to_csv('grad_students.csv')
                # print(csv_out)
            except Exception as e:
                print(e)
                pass
    else:
        print('Failed to retrieve the webpage')
    print(len(csv_out))

csv_out.to_csv('grad_students.csv')