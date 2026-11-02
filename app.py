import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Smart Campus Student Dashboard", page_icon="🎓", layout="wide")

# ---------- THEME ----------
st.markdown("""
<style>
.stApp { background: #f4f7fb; }
[data-testid="stSidebar"] { background: #142b4d; }
[data-testid="stSidebar"] * { color: #f4f7fb !important; }
[data-testid="stMetric"] { background: white; border: 1px solid #dce4ef; padding: 14px; border-radius: 8px; }
.story { background:#eaf1fb; border-left:5px solid #3268a8; padding:12px 16px; border-radius:5px; }
.small-note { color:#68778b; font-size:12px; }
h1,h2,h3 { color:#1d3557; }
</style>
""", unsafe_allow_html=True)

# ---------- SAMPLE DATA ----------
@st.cache_data
def sample_data():
    names = ["Arun","Priya","Rahul","Sneha","Kiran","Divya","Ravi","Anjali","Vijay","Meena",
             "Suresh","Pooja","Naveen","Kavya","Manoj","Harika","Sai","Lakshmi","Ramesh","Teja"]
    genders = ["Male","Female"] * 10
    branches = ["CSE","AIML","ECE","CSE","AIML","ECE","CSE","AIML","ECE","CSE",
               "AIML","ECE","CSE","AIML","ECE","CSE","AIML","ECE","CSE","AIML"]
    cities = ["Anantapur","Hyderabad","Penukonda","Bengaluru","Dharmavaram","Hyderabad","Hindupur","Chennai",
              "Anantapur","Bengaluru","Penukonda","Chennai","Hyderabad","Dharmavaram","Hindupur","Anantapur",
              "Bengaluru","Hyderabad","Chennai","Penukonda"]
    return pd.DataFrame({
        "Roll Number":[f"24FH1A33{i:02d}" for i in range(1,21)],
        "Student Name":names, "Gender":genders, "Branch":branches,
        "Department":["CSE(AIML)"]*20, "Age":[18,19,20,18,21,19,20,18,22,19,21,20,18,22,19,20,21,18,22,20],
        "Address":cities, "Marks":[85,92,74,88,67,95,72,90,81,86,69,93,78,89,76,96,83,87,71,91]
    })

st.sidebar.markdown("## 🎓 CAMPUS STORY")
st.sidebar.caption("DASHBOARD")
page = st.sidebar.radio("Navigate", ["Overview","Student Trends","Student Insights","Location Analysis"])
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

upload = st.sidebar.file_uploader("Upload student CSV", type=["csv"])
if upload:
    try:
        raw = pd.read_csv(upload)
        st.sidebar.success("CSV loaded")
    except Exception as e:
        st.error(f"Unable to read CSV: {e}")
        st.stop()
else:
    raw = sample_data()
    st.sidebar.info("Using illustrative sample data")

# Normalize column names and map common aliases
raw.columns = [str(c).strip() for c in raw.columns]
aliases = {
    "Roll No":"Roll Number","Rollno":"Roll Number","roll_number":"Roll Number",
    "Name":"Student Name","Student":"Student Name","Father Name":"Father Name",
    "Mother Name":"Mother Name","Location":"Address","City":"Address",
    "Marks Percentage":"Marks","Percentage":"Marks","Age":"Age",
    "Gender":"Gender","Branch":"Branch","Department":"Department"
}
raw = raw.rename(columns={c:aliases.get(c,c) for c in raw.columns})
if "Student Name" not in raw.columns:
    raw["Student Name"] = [f"Student {i+1}" for i in range(len(raw))]
for col, default in {"Roll Number":"N/A","Gender":"Unknown","Branch":"Not specified",
                     "Department":"Not specified","Address":"Not specified","Age":None,"Marks":None}.items():
    if col not in raw.columns: raw[col] = default
df = raw.copy()
for c in ["Age","Marks"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["Student Name"] = df["Student Name"].fillna("Unknown").astype(str)
for c in ["Gender","Branch","Department","Address"]:
    df[c] = df[c].fillna("Unknown").astype(str)
df = df.dropna(subset=["Student Name"])
if df.empty:
    st.error("No usable student records found."); st.stop()

genders = sorted(df.Gender.unique())
branches = sorted(df.Branch.unique())
departments = sorted(df.Department.unique())
locations = sorted(df.Address.unique())
sg = st.sidebar.multiselect("Gender", genders, default=genders)
sb = st.sidebar.multiselect("Branch", branches, default=branches)
sd = st.sidebar.multiselect("Department", departments, default=departments)
sl = st.sidebar.multiselect("Location", locations, default=locations)
filtered = df[df.Gender.isin(sg) & df.Branch.isin(sb) & df.Department.isin(sd) & df.Address.isin(sl)].copy()
if not filtered.empty and filtered.Age.notna().any():
    amin, amax = int(filtered.Age.min()), int(filtered.Age.max())
    age_range = st.sidebar.slider("Age range", amin, max(amax,amin), (amin,amax))
    filtered = filtered[filtered.Age.between(*age_range)]
if not filtered.empty and filtered.Marks.notna().any():
    mmin, mmax = int(filtered.Marks.min()), int(filtered.Marks.max())
    marks_range = st.sidebar.slider("Marks range", mmin, max(mmax,mmin), (mmin,mmax))
    filtered = filtered[filtered.Marks.between(*marks_range)]

st.sidebar.caption("Filters apply to every view.")
st.title("🎓 Smart Campus | Student Analytics")
st.caption("A guided story from student distribution to trends, branch insights and location patterns.")
if filtered.empty:
    st.warning("No students match the selected filters."); st.stop()

total = len(filtered)
avg_age = filtered.Age.mean() if filtered.Age.notna().any() else None
avg_marks = filtered.Marks.mean() if filtered.Marks.notna().any() else None
female_pct = (filtered.Gender.str.lower().eq("female").mean()*100)
branch_count = filtered.Branch.nunique()

def kpis():
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("TOTAL STUDENTS", f"{total:,}", "Filtered records")
    c2.metric("AVG. MARKS", f"{avg_marks:.1f}" if pd.notna(avg_marks) else "N/A", "Academic snapshot")
    c3.metric("FEMALE SHARE", f"{female_pct:.1f}%", "Of selected students")
    c4.metric("BRANCHES", f"{branch_count}", "Represented")
def story(title, text, prompt=None):
    st.markdown(f'<div class="story"><b>{title}</b><br>{text}</div>', unsafe_allow_html=True)
    if prompt: st.caption("DECISION PROMPT · " + prompt)

def gender_chart():
    x=filtered.groupby("Gender").size().reset_index(name="Students")
    return px.pie(x,names="Gender",values="Students",hole=.48,title="Student composition by gender")

def branch_chart():
    x=filtered.groupby("Branch").size().reset_index(name="Students").sort_values("Students",ascending=True)
    return px.bar(x,x="Students",y="Branch",orientation="h",text="Students",title="Students by branch")

def location_chart():
    x=filtered.groupby("Address").size().reset_index(name="Students").sort_values("Students",ascending=True)
    return px.bar(x,x="Students",y="Address",orientation="h",title="Student distribution by location")

if page == "Overview":
    st.subheader("Student Performance | Executive Overview")
    kpis()
    a,b=st.columns([1.45,1])
    with a:
        st.plotly_chart(branch_chart(),use_container_width=True)
    with b:
        st.plotly_chart(gender_chart(),use_container_width=True)
    story("STORY 01 | Student distribution is the starting point",
          f"The selected dataset contains {total} students across {branch_count} branches. Use branch and gender distributions to understand the composition before exploring academic indicators.",
          "Which branches or student groups may need a closer look?")
    st.subheader("Where students are located")
    st.plotly_chart(location_chart(),use_container_width=True)
    story("HOW TO READ THIS",
          "These charts describe the filtered records—not the whole institution if filters are active. Compare categories and then open the relevant dashboard view for more detail.")
elif page == "Student Trends":
    st.subheader("Student Trends | What does the academic snapshot show?")
    kpis()
    if filtered.Marks.notna().any():
        marks=filtered.dropna(subset=["Marks"]).copy()
        if "Academic Year" in marks.columns:
            trend=marks.groupby("Academic Year",as_index=False).Marks.mean()
            fig=px.line(trend,x="Academic Year",y="Marks",markers=True,title="Average marks by academic year")
            st.plotly_chart(fig,use_container_width=True)
            story("STORY 02 | Academic-year comparison", "The line chart compares average marks for the available academic years.", "Check whether changes reflect cohort composition or other context.")
        else:
            st.plotly_chart(px.histogram(marks,x="Marks",color="Gender",nbins=10,title="Marks distribution"),use_container_width=True)
            story("STORY 02 | Marks are distributed across the selected students",
                  "This dataset does not contain academic-year values, so the view shows marks distribution rather than a time trend.",
                  "Which range contains the most students? Review student-level records before drawing conclusions.")
    else:
        st.info("Marks data is not available in the uploaded dataset.")
    if filtered.Age.notna().any():
        st.plotly_chart(px.histogram(filtered.dropna(subset=["Age"]),x="Age",color="Gender",nbins=10,title="Age distribution"),use_container_width=True)
elif page == "Student Insights":
    st.subheader("Student Insights | Compare branch and academic indicators")
    kpis()
    left,right=st.columns(2)
    with left: st.plotly_chart(branch_chart(),use_container_width=True)
    with right:
        if filtered.Marks.notna().any():
            st.plotly_chart(px.box(filtered.dropna(subset=["Marks"]),x="Branch",y="Marks",color="Branch",points="all",title="Marks spread by branch"),use_container_width=True)
        else: st.info("Marks column is not available.")
    story("STORY 03 | Student count and marks tell different stories",
          "Branch size shows how many records belong to each branch; marks summarize the academic values available. A larger branch does not automatically indicate stronger performance.",
          "Compare sample size and marks together before interpreting differences.")
    if filtered.Age.notna().any() and filtered.Marks.notna().any():
        st.plotly_chart(px.scatter(filtered,x="Age",y="Marks",color="Gender",hover_data=["Student Name","Branch"],title="Age vs marks"),use_container_width=True)
elif page == "Location Analysis":
    st.subheader("Location Analysis | Where are students represented?")
    kpis()
    st.plotly_chart(location_chart(),use_container_width=True)
    story("STORY 04 | Location distribution highlights representation",
          f"The chart compares student counts across {filtered.Address.nunique()} selected locations. It can guide questions about outreach or campus support, but location alone does not explain student needs.",
          "Are the differences expected for the selected dataset?")
    if filtered.Address.nunique()>1:
        st.plotly_chart(px.sunburst(filtered,path=["Address","Branch"],title="Location → branch composition"),use_container_width=True)

st.subheader("Filtered Student Records")
st.caption(f"Showing {len(filtered)} records · filters: Gender={len(sg)}, Branch={len(sb)}, Department={len(sd)}, Location={len(sl)}")
st.dataframe(filtered,use_container_width=True,hide_index=True)
csv=filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download filtered student data",csv,"filtered_student_details.csv","text/csv")
st.markdown('<p class="small-note">Sample records are illustrative. Verify uploaded data and protect student personal information before sharing.</p>',unsafe_allow_html=True)
