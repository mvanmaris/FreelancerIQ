# FreelancerIQ
#### Video Demo: https://youtu.be/Cl10lY4M7pA
#### Description:

FreelancerIQ is a freelancer productivity and cost analysis tool, created to satisfy the capstone project for Harvards CS50 couse.

The project was inspired by my experience working in editorial where I collect and analyse production metrics, expenses and other operational reporting. I wanted to build an MVP that could process raw freelancer data into our KPIs without the end user having to calculate the metrics manually at every reporting cycle.

FreelancerIQ has two components: a command-line python program that calculates freelancer metrics and a dashboard built with Strealit. The user can upload CSV files containing the calendar week, freelancer name, units, hours, and hourly rate, analyse both the team's overall performance as well as individuals, and compare the data through charts.

## Features

FreelancerIQ calculates five KPIs:

1. **Total Freelancer Spend:** Total cost of freelance work, calculated by multiplying hours worked by hourly rate.
2. **Total Content Units:** Total number of completed units of work
3. **Total Freelancer Hours:** Total number of hours worked.
4. **Minutes per Unit:** Average number of minutes required to complete one content unit.
5. **Cost per Unit:** Average cost of producing one content unit.

The dashboard allows the user to filter results to a specific freelancer using the dropdown. KPI Score Cards are dynamic to the selection made in the drop down.

Two horiozontal bar charts compare the freelancers by min per unit and cost per unit. When a freelancer is chosen from the dropdown thier bars are highlighted for better visibility.

The dashboard also includes a table displaying the data from the CSV for the selected or all the freelancers.

## Project Files

### project.py

This file contains the core Python functions for loading data and calculating the metrics.

`main()` loads the sample CSV file, processes each record, and prints calculated productivity and cost metrics into the terminal.

`load_data()` reads the CSV data using python's built-in csv module. It converts numerical fields into the appropriate data trypes and supports both local CSV files and files uploaded through Streamlit.

`calculate_minutes_per_unit()` calculates productivity by converting hours into minutes and dividing by the number of completed content units.

`calculate_total_cost()` calculates spending by multiplying hours worked by hourly rate.

`calculate_cost_per_unit` divides total cost by the number of completed content units.

Both per-unit functions return `None` when content units equal zero to prevent division by zero errors.

### app.py

This file contains the interactive Streamlit dashboard.

It handles file uploads, freelancer filtering, KPI calculations, data visualization and CSV error messages.

The dashboard imports the calculation functions from `project.py`, allowing the same functions to be used in both the command-line program and the interactive app.

Altair is used to make the comparison charts and highlight the selected freelancer.

### test_project.py

This file contains 4 automated tests written using pytest.

The tests verify:

- `calculate_minutes_per_unit()`
- `calculate_total_cost()`
- `calculate_cost_per_unit()`
- `load_data()`

### sample_data.csv

This file contains fictional freealncer data used for the creation, testing and demo of this capstone project.

The data set has 6 freelacners across three reporting weeks, resulting in 18 records.

### requirements.txt

This file lists the external libraries required to run the interactive dashboard: Streamlit and Altair.

## CSV File Format

To keep the project an MVP, FreelancerIQ only accepts CSV files with the following headers:

`week,freelancer,content_units,hours,hourly_rate`

Each row represents work completed by a freelancer during a reporting period.

- `week`: The reporting period
- `freelancer`: The freelancer's full name
- `content_units`: the number of completed units of work (whole number)
- `hours`: the number of hours worked (can contain decimals)
- `hourly_rate`: The freelancer's hourly pay rate (can contain decimals)

EXAMPLE:

```csv
week,freelancer,content_units,hours,hourly_rate
W01,Alice James,20,5,30.50
W01,Bob Smith,10,4,25
W02,Alice James,30,6,30.50
```

If a file contains missing required headers or invalid numerical values, FreelancerIQ will display an error message instead of continuing with invalid data.

## How to Run FreelancerIQ

Firstly, install the required external libraries:

```bash
pip install -r requirements.txt
```

to ren the command-line program:

```bash
python project.py
```

This loads `sample_data.csv` and prints freelancer productivity and cost calculations in the terminal.

To launch the interactive dashboard:

```bash
python -m streamlit run app.py
```

Once Streamlit starts, open the dashboard in your browser and upload a compatible CSV file.

Use the freelancer dropdown menu to view individual KPIs and compare freelancers using the charts.

To run automated tests:

```bash
python -m pytest test_project.py -v
```


## Design Decisions

One of the main design choices for this porject was to separate the calculation logic from the user interface. I made the core functions in `project.py` so that they could be easily reused by both the command-line program and the Streamlit dashbaord. This also make the code easier to organize, maintain and test.

I wanted to build an interactive dashboard so that real world users could view and analyse their data without having to interpret terminal output. The dashboard gives a cleaner and more organized way for the user to view KPIs and make comparisons.

I chose CSV as the input format as it is the default file type I use at my work and it is widely supported by spreadsheet apps and easy to process using Python's standard library.

For the dashboard, I used Streamlit as it is more familiar to me from my work. It provides interactive interface components without needing a separate frontend app. I used Altair for the charts as it supports clear comparisons and conditional formatting.

I also chose to calculate overall productivity using total hours divided by total content units instead of taking a simple average of individual row productivity rates so that records with diffeerent columes contribute proportionally to the overall metric.

Finally, I included error handling for common CSV issues and division-by-zero cases to make the application more reliable and more user friendly for those not familiar with code.
