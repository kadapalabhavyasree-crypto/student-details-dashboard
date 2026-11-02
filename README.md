# Smart Campus Student Dashboard

An interactive student analytics dashboard built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. It presents student data through a storytelling-style dashboard with overview KPIs, student trends, branch insights, location analysis, interactive filters, and downloadable filtered records.

> **Privacy note:** Student records can contain personal information. Use synthetic/demo data for public GitHub repositories. Do not commit real student names, roll numbers, phone numbers, parent details, or addresses.

## Features

- Executive overview with student summary KPIs
- Student trends and marks distribution
- Branch and academic insights
- Location analysis
- Sidebar filters for gender, branch, department, location, age, and marks
- CSV upload
- Filtered student table
- Download filtered records as CSV
- Storytelling captions to explain each visualization

## Project files

```text
student_dashboard_story/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.9 or newer (recommended)
- pip
- Internet connection for installing packages

## Setup and run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd student_dashboard_story
```

### 2. Create and activate a virtual environment (recommended)

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

Streamlit will show a local URL in the terminal (usually `http://localhost:8501`). Open it in your browser.

## Dataset

The app includes illustrative sample student records so it can run without an uploaded file.

To use your own dataset, upload a CSV through the sidebar. The dashboard recognizes these fields when available:

- `Student Name`
- `Roll Number`
- `Gender`
- `Branch`
- `Department`
- `Age`
- `Address`
- `Marks`

Some common alternative column names are mapped automatically (for example, `Name` to `Student Name`, `Roll No` to `Roll Number`, and `City` to `Address`). Missing optional fields are filled with default values. For meaningful charts, provide the relevant columns in your CSV.

## Dashboard navigation
dashboard link : https://student-details-dashboard-nylb4bxx8tutlzv5cfu3xd.streamlit.app/

1. **Overview** — student count, average marks, gender share, branch count, and distribution charts.
2. **Student Trends** — marks distribution and age distribution; academic-year trend is shown if an `Academic Year` column exists.
3. **Student Insights** — branch comparison, marks spread, and age-versus-marks relationship when numeric data is available.
4. **Location Analysis** — student counts by location and location-to-branch composition.

All sidebar filters apply across the dashboard views.

## GitHub safety

Before pushing:

1. Confirm `.gitignore` is present.
2. Keep real student CSV files out of the repository.
3. Use anonymized or synthetic data for screenshots and demonstrations.
4. Review `git status` and the staged files before committing.

Example:

```bash
git status
git add app.py requirements.txt README.md .gitignore
git commit -m "Add student storytelling dashboard"
git push
```

## Limitations

- Results depend on the quality and columns of the uploaded CSV.
- The included sample data is illustrative, not institutional data.
- The dashboard is for visualization and exploration, not a secure student-record system.
- Academic-year trends require an `Academic Year` column.
- Do not deploy or share identifiable student information without appropriate authorization and safeguards.

## Technology stack

- Python
- Streamlit
- Pandas
- Plotly

## License

Add a license file if you plan to distribute or reuse this project publicly. Check your institution's project-submission requirements first.
