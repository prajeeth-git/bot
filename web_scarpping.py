import requests
from bs4 import BeautifulSoup

class AttendanceScraper:
    def __init__(self):
        self.username = "CSITHOD"
        self.password = "csit@95"
        self.session = requests.session()
        self.login()

    def login(self):
        url = "https://samvidha.iare.ac.in/pages/login/checkUser.php"
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(url, data=payload)
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed. Status code: {}".format(response.status_code))

    def scrape_attendance(self, roll_no):
        url = "https://samvidha.iare.ac.in/home?action=stud_att_hod#"
        payload = {
            "rollno": roll_no,
            "ok_roll": "GET ATTENDANCE"
        }
        response = self.session.post(url, data=payload)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all('table')

        # Extract table content
        table_content = []
        for table in tables:
            rows = table.find_all('tr')
            table_data = []
            for row in rows:
                cells = row.find_all('td')
                row_data = [cell.get_text(strip=True) for cell in cells]
                table_data.append(row_data)
            table_content.append(table_data)
        
        if len(table_content)==2:
            return "Invalid"
        print(table_content[2])
        if table_content[2][0]==[]:
            table_content[2].pop(0)
        if table_content[2][-1][1]=='' or table_content[2][-1]==[]:
            table_content[2].pop()

        table_rows = table_content[2]
        data_dict = {}

        for row in table_rows:
            course_name = row[2]
            values = [int(row[5]), int(row[6]), float(row[7]), row[8]]
            data_dict[course_name] = values

        return data_dict

    @staticmethod
    def display_attendance(data_dict):
        summary = "Attendance Summary:\n===================\n\n"
        
        for course, data in data_dict.items():
            summary += "Course Name: {}\n".format(course)
            summary += "Total Classes: {}\n".format(data[0])
            summary += "Attended Classes: {}\n".format(data[1])
            summary += "Attendance Percentage: {:.2f}%\n".format(data[2])
            summary += "Attendance Status: {}\n".format(data[3])
            summary += "-----------------------------\n\n"
        
        return summary

# Usage example
