import pandas as pd
import requests

# Load the Excel file
file_path = 'StoredScrapedData/Product_urls.xlsx'  # Update this to the path of your Excel file
df = pd.read_excel(file_path)

# Function to check URL accessibility
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return 'CONFIRMED'
        else:
            return 'ERROR'
    except requests.RequestException:
        return 'ERROR'

# Check each URL and write the result
df['Status'] = df['URL_Column_Name'].apply(check_url)  # Update 'URL_Column_Name' to your actual URL column name

# Save the results back to the Excel file
df.to_excel(file_path, index=False)
