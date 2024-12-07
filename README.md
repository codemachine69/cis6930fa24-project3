# CIS6930FA24 - Project 3

## Introduction

This project processes and visualizes incident data from the Norman, Oklahoma Police Department's publicly available PDF reports. The application allows users to either provide a URL or upload a local PDF file containing incident data. It extracts key details (such as date/time, incident number, location, nature, and ORI) and visualizes the processed data through charts.

The main objectives of this project are:

1. Fetch incident data from a URL or uploaded PDF.
2. Extract relevant fields from the PDF.
3. Visualize the processed data using Streamlit.

## Installation

To install and run this project:

1. Ensure you have Python 3.12 installed.
2. Install pipenv if you haven't already using `pip install pipenv`.
3. Clone this repository using `https://github.com/codemachine69/cis6930fa24-project3.git` and navigate to the project directory.
4. Install the required dependencies using `pipenv install -e .`

## How to Run

1. Start the Streamlit application:

   `pipenv run streamlit run src/app.py`

2. In the web application:

   - Enter a URL for an incident PDF.
   - Or upload a local PDF file.

The application will extract data from the file and display visualizations.

## Pipeline Workflow

1. Fetch Data:

   - Users can provide either a URL or upload a local PDF file.
   - The `fetch_incidents(url)` function downloads the PDF from the provided URL and returns it as a byte stream.

2. Extract Data:

   - The `extract_incidents(incident_data)` function processes the PDF using `pypdf` to extract rows containing incident details.
   - Extracted fields include:
     - Date/Time
     - Incident Number
     - Location
     - Nature
     - ORI

3. Visualize Data:

   The application generates four types of visualizations:

   - Clustering of Incident Locations: Groups incidents based on hashed location values using KMeans clustering.
   - Clustering Incidents by Hour and Type: Groups incidents based on the hour of occurrence and their type (nature).
   - Incident Nature Frequency: Displays a bar chart showing the frequency of each incident nature.
   - Incident Trend by Hour: Plots a line graph showing the number of incidents occurring at each hour of the day.

## Visualizations

1. Clustering of Incident Locations

   A scatter plot groups incidents into clusters based on hashed location values.

2. Clustering Incidents by Hour and Type

   A scatter plot groups incidents into clusters based on their hour of occurrence and type (nature). Hovering over points shows additional details like location and incident number.

3. Incident Nature Frequency

   A horizontal bar chart displays how often each type of incident occurs.

4. Trend of Incidents Over Time

   A line graph shows how incidents are distributed over time.

## Implementation Details

1. `fetch_incidents(url)`

   - Downloads a PDF from the given URL and returns it as a byte stream.

2. `extract_incidents(incident_data)`

   - Parses the PDF to extract rows containing incident details.
   - Returns a list of tuples with fields: `incident_time`, `incident_number`, `incident_location`, `nature`, `incident_ori`.

3. `visualize_data(df)`

   - Generates visualizations for clustering, frequency analysis, and trends based on the extracted data.

## Tests

Tests are implemented using pytest and cover all major functionalities:

- `test_fetch_incidents()`:
  - Verifies that the fetch_incidents function correctly downloads a PDF from a given URL.
  - Ensures the returned object is a valid BytesIO stream.
- `test_extract_incidents()`:
  - Tests the extract_incidents function to ensure it extracts incident data correctly from a PDF file.
  - Confirms that the extracted data is a list of tuples, where each tuple contains exactly five elements: incident_time, incident_number, incident_location, nature, and incident_ori.
- `test_fetch_and_extract()`:
  - Integrates fetch_incidents and extract_incidents to test the complete pipeline from fetching a PDF to extracting incident data.
  - Ensures that the extracted data can be converted into a valid Pandas DataFrame with the correct structure.

Run all tests using:

`pipenv run python -m pytest`

## Assumptions

1. The Oklahoma PD URL is assumed to be stable and accessible at all times. No retries or alternative strategies are implemented in case of API downtime.
2. It is assumed that the URL response fields will always be in the expected format. Any other data structure or missing fields could cause errors.
3. It is assumed that all incident summary PDFs from the Norman Police Department follow a consistent structure. The expected format includes lines with the following fields in this order: Date/Time, Incident Number, Location, Nature, and Incident ORI.
4. Code is designed to handle multiline location fields.

## Bugs and Limitations

1. The application assumes that all PDFs follow a consistent structure for extracting rows.
2. If the structure or format of the PDFs on the Norman Police Department website changes (e.g., new headers, field rearrangement), the extract_incidents function may fail to correctly parse the data, resulting in missing or improperly extracted incidents.
3. Processing large PDFs with many pages can take significant time and memory.
4. The script doesn't handle cases where the fields contain abnormal data.
5. The hashed location values used in clustering do not represent actual geographic proximity, limiting real-world insights for location-based clustering.
