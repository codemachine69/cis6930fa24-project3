import pytest
import pandas as pd
from io import BytesIO
from src.app import fetch_incidents, extract_incidents

@pytest.fixture
def sample_pdf():
    with open("docs/test_sample.pdf", "rb") as f:
        return BytesIO(f.read())

@pytest.fixture
def sample_dataframe():
    data = {
        "incident_time": ["2024-01-01 12:00:00", "2024-01-01 13:00:00"],
        "incident_number": ["12345", "67890"],
        "incident_location": ["Location A", "Location B"],
        "nature": ["Nature A", "Nature B"],
        "incident_ori": ["ORI1", "ORI2"],
    }
    return pd.DataFrame(data)

def test_fetch_incidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-01_daily_incident_summary.pdf"
    try:
        pdf_data = fetch_incidents(url)
        assert isinstance(pdf_data, BytesIO)
    except Exception as e:
        pytest.fail(f"Error in fetch_incidents: {e}")

def test_extract_incidents(sample_pdf):
    incidents = extract_incidents(sample_pdf)
    assert isinstance(incidents, list)
    assert all(isinstance(incident, tuple) for incident in incidents)
    if incidents:
        assert len(incidents[0]) == 5

def test_fetch_and_extract(sample_pdf):
    try:
        pdf_data = sample_pdf
        incidents = extract_incidents(pdf_data)
        assert isinstance(incidents, list)
        assert all(len(incident) == 5 for incident in incidents)
        df = pd.DataFrame(incidents, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])
        assert not df.empty
        assert list(df.columns) == ['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
    except Exception as e:
        pytest.fail(f"Error in fetch_and_extract integration: {e}")