from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from datetime import datetime
import random
from faker import Faker
import pandas as pd
import plotly.express as px

# ------------------- Flask App & DB Setup -------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
faker = Faker()
swagger = Swagger(app)

# ------------------- Employee Model -------------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ------------------- Seed Data -------------------
DEPARTMENTS = ["Engineering", "HR", "Sales", "Marketing", "Finance"]
ROLES = {
    "Engineering": ["Engineer", "Senior Engineer", "Tech Lead"],
    "HR": ["Recruiter", "HR Manager"],
    "Sales": ["Sales Rep", "Account Executive"],
    "Marketing": ["Content Writer", "Marketing Manager"],
    "Finance": ["Accountant", "Finance Manager"]
}

def seed_db(n=50):
    for _ in range(n):
        dept = random.choice(DEPARTMENTS)
        role = random.choice(ROLES[dept])
        emp = Employee(
            name=faker.name(),
            department=dept,
            role=role,
            salary=round(random.uniform(30000, 200000), 2),
            age=random.randint(22, 60),
            joining_date=faker.date_between(start_date="-10y", end_date="today")
        )
        db.session.add(emp)
    db.session.commit()

# ------------------- Home Route -------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------- Employees UI -------------------
@app.route("/employees")
def employees_ui():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)

# ------------------- Summary Endpoints -------------------
@app.route("/summary/department")
def summary_department():
    result = db.session.query(
        Employee.department,
        db.func.count(Employee.id).label("employee_count"),
        db.func.avg(Employee.salary).label("avg_salary")
    ).group_by(Employee.department).all()

    summary = []
    for dept, count, avg_sal in result:
        summary.append({
            "department": dept,
            "employee_count": count,
            "avg_salary": round(avg_sal, 2)
        })
    return render_template("summary.html", summary=summary, title="Department Summary")

@app.route("/summary/age")
def summary_age():
    age_groups = {
        "22-30": (22, 30),
        "31-40": (31, 40),
        "41-50": (41, 50),
        "51-60": (51, 60)
    }

    summary = []
    for group, (low, high) in age_groups.items():
        count = Employee.query.filter(Employee.age.between(low, high)).count()
        summary.append({
            "age_group": group,
            "employee_count": count
        })
    return render_template("summary.html", summary=summary, title="Age Group Summary")

@app.route("/summary/joining")
def summary_joining():
    employees = Employee.query.all()
    years = {}
    for emp in employees:
        year = emp.joining_date.year
        years[year] = years.get(year, 0) + 1

    summary = [{"year": str(year), "employee_count": count} for year, count in sorted(years.items())]
    return render_template("summary.html", summary=summary, title="Joining Year Summary")

# ------------------- Chart Endpoints -------------------
@app.route("/charts/department")
def chart_department():
    result = db.session.query(
        Employee.department,
        db.func.count(Employee.id).label("employee_count")
    ).group_by(Employee.department).all()

    df = pd.DataFrame(result, columns=["department", "employee_count"])
    fig = px.bar(df, x="department", y="employee_count",
                 text="employee_count", title="Employees per Department")
    fig.update_traces(textposition='outside')

    graph_html = fig.to_html(full_html=False)
    return graph_html

@app.route("/charts/age")
def chart_age():
    age_groups = {
        "22-30": (22, 30),
        "31-40": (31, 40),
        "41-50": (41, 50),
        "51-60": (51, 60)
    }

    data = []
    for group, (low, high) in age_groups.items():
        count = Employee.query.filter(Employee.age.between(low, high)).count()
        data.append({"age_group": group, "employee_count": count})

    df = pd.DataFrame(data)
    fig = px.bar(df, x="age_group", y="employee_count",
                 text="employee_count", title="Employees per Age Group")
    fig.update_traces(textposition='outside')

    graph_html = fig.to_html(full_html=False)
    return graph_html

@app.route("/charts/joining")
def chart_joining():
    employees = Employee.query.all()
    years = {}
    for emp in employees:
        year = emp.joining_date.year
        years[year] = years.get(year, 0) + 1

    df = pd.DataFrame([{"year": str(year), "employee_count": count} for year, count in sorted(years.items())])
    fig = px.bar(df, x="year", y="employee_count",
                 text="employee_count", title="Employees per Joining Year")
    fig.update_traces(textposition='outside')

    graph_html = fig.to_html(full_html=False)
    return graph_html

# ------------------- Initialize DB & Seed -------------------
with app.app_context():
    db.create_all()
    if Employee.query.count() == 0:
        seed_db(100)

# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True)
