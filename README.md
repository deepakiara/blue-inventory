# Streamlit Sales Dashboard

This is a simple, interactive sales performance dashboard built using Python, Streamlit, and Plotly.

## Project Structure

- `app.py`: The main Streamlit application code.
- `data.csv`: Sample CSV dataset with `Date`, `Category`, and `Sales` columns.
- `requirements.txt`: Python package dependencies.

## Setup Instructions

### 1. Install Python (if not already installed)

Since Python was not detected on your system's PATH, you can install it using one of the following methods:

#### Method A: Using Windows Package Manager (winget) - Recommended
Open PowerShell or Command Prompt and run:
```powershell
winget install Python.Python.3.12
```
*Note: You may need to restart your terminal/IDE after installation for the `python` command to become available.*

#### Method B: Manual Installer
1. Go to the [Official Python Downloads Page](https://www.python.org/downloads/).
2. Download the installer for Windows (e.g., Python 3.12).
3. **Important:** Run the installer and check the box that says **"Add python.exe to PATH"** before clicking "Install Now".

---

### 2. Set Up a Virtual Environment and Run the App

Open your terminal, navigate to this project folder, and run:

```powershell
# 1. Create a virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install the required libraries (pandas, streamlit, plotly)
pip install -r requirements.txt

# 4. Start the Streamlit app
streamlit run app.py
```

Streamlit will start a local web server and automatically open the interactive dashboard in your default browser (usually at `http://localhost:8501`).
