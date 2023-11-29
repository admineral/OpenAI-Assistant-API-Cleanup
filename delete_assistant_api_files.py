# This script is used to delete OpenAI files.
# It first fetches a list of all files and displays them.
# The user is then asked for confirmation to delete the listed files.
# If confirmed, the script deletes the files in parallel using multithreading.
# The user is then asked if they want to delete all files.
# If confirmed, the script enters a loop where it fetches and deletes files
# until there are no more to delete.





import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Make sure to set this environment variable

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "OpenAI-Beta": "assistants=v1"
}

def delete_file(file_id):
    delete_response = requests.delete(f"https://api.openai.com/v1/files/{file_id}", headers=headers)
    print(f"Deleted file {file_id}: {delete_response.json()}")

# Get the list of all files
response = requests.get("https://api.openai.com/v1/files?order=desc&limit=100", headers=headers)

# Check the status code of the response
if response.status_code == 200:
    files = response.json().get('data', [])
    if not files:
        print("No files found.")
    else:
        # Log and display all files
        print("Here are all the files:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. ID: {file['id']}, Name: {file.get('name', 'No name')}")

        # Ask for confirmation before deletion
        confirm = input("\nDo you want to delete all these listed files? (yes/no): ")
        if confirm.lower() == 'yes':
            # Use a ThreadPoolExecutor to delete the files in parallel
            with ThreadPoolExecutor() as executor:
                executor.map(delete_file, [file['id'] for file in files])

        # Ask for confirmation to delete all files
        confirm_all = input("\nDo you want to delete ALL files? (yes/no): ")
        if confirm_all.lower() == 'yes':
            while True:
                # Get the list of all files
                response = requests.get("https://api.openai.com/v1/files?order=desc&limit=100", headers=headers)

                # Check the status code of the response
                if response.status_code == 200:
                    files = response.json().get('data', [])
                    if not files:
                        print("No more files found.")
                        break
                    else:
                        # Use a ThreadPoolExecutor to delete the files in parallel
                        with ThreadPoolExecutor() as executor:
                            executor.map(delete_file, [file['id'] for file in files])
                else:
                    print(f"API request failed with status code {response.status_code}. Response: {response.text}")
                    break
else:
    print(f"API request failed with status code {response.status_code}. Response: {response.text}")