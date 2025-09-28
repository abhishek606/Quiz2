# Flask Employee Dashboard

A simple **Flask-based Employee Management Dashboard** with interactive summary tables and charts.  
This project demonstrates Flask, SQLAlchemy, Plotly, and basic UI templates.

---

## Features

- List all employees with details: name, department, role, salary, age, joining date.
- Summary endpoints:
  - Employee count and average salary per department.
  - Employee count per age group.
  - Employee count per joining year.
- Interactive charts using **Plotly** (bar charts) for:
  - Employees per department
  - Employees per age group
  - Employees per joining year
- REST API endpoints returning JSON data.
- Simple, clean UI for employees and summaries.

---

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Employees Table
![Employees Table](screenshots/employees.png)

### Department Summary
![Department Summary](screenshots/summary_department.png)

### Department Chart
![Department Chart](screenshots/chart_department.png)

> Add your own screenshots in `screenshots/` folder and update the paths above.

---

## API Endpoints

| Endpoint                  | Description                                      |
|----------------------------|--------------------------------------------------|
| `/`                        | Home page with links to all endpoints           |
| `/employees`               | Returns all employees as JSON                   |
| `/summary/department`      | Summary of employees by department              |
| `/summary/age`             | Summary of employees by age group               |
| `/summary/joining`         | Summary of employees by joining year           |
| `/charts/department`       | Interactive department chart (HTML)            |
| `/charts/age`              | Interactive age group chart (HTML)             |
| `/charts/joining`          | Interactive joining year chart (HTML)          |

---

## Installation

1. Clone the repository:

git clone https://github.com/abhishek606/flask-employee-dashboard.git
cd flask-employee-dashboard


2. Create a virtual environment:

python -m venv venv


3. Create a virtual environment:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install dependencies:

pip install -r requirements.txt

5. Run the Flask app:

python app.py

6. Open your browser at http://127.0.0.1:5000

---

## Technologies Ued

Python 3.x
Flask
Flask-SQLAlchemy
Plotly
Pandas
Faker (for sample data)
HTML/CSS templates

---

## Project Structure

flask-employee-dashboard/
├── app.py
├── employees.db
├── templates/
│   ├── home.html
│   ├── employees.html
│   └── summary.html
├── requirements.txt
├── README.md
└── .gitignore

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Abhishek Mane
GitHub: https://github.com/abhishek606

