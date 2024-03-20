import pandas as pd
import requests

# Load the Excel file
file_path = 'StoredScrapedData/Product_urls.xlsx'  # Update this to the path of your Excel file
df = pd.read_excel(file_path)

def check_url(url):
    methods = [requests.head, requests.get]  # List of methods to try
    for method in methods:
        try:
            # Try the current method
            response = method(url, allow_redirects=True, timeout=10)
            # If the response code is 200, the URL is accessible
            if response.status_code == 200:
                return 'CONFIRMED'
        except requests.RequestException:
            # If there's an exception, log it or pass
            pass
    # If all methods failed, return 'ERROR'
    return 'ERROR'

# Check each URL and write the result
df['Confirmed'] = df['Item.url'].apply(check_url)  # Update 'URL_Column_Name' to your actual URL column name

# Save the results back to the Excel file
df.to_excel(file_path, index=False)
