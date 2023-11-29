# This script is used to delete OpenAI assistants.
# It first fetches a list of all assistants and displays them.
# The user is then asked for confirmation to delete the listed assistants.
# If confirmed, the script deletes the assistants in parallel using multithreading.
# The user is then asked if they want to delete all assistants.
# If confirmed, the script enters a loop where it fetches and 
# deletes assistants until there are no more to delete.



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

def delete_assistant(assistant_id):
    delete_response = requests.delete(f"https://api.openai.com/v1/assistants/{assistant_id}", headers=headers)
    print(f"Deleted assistant {assistant_id}: {delete_response.json()}")

# Get the list of all assistants
response = requests.get("https://api.openai.com/v1/assistants?order=desc&limit=100", headers=headers)

# Check the status code of the response
if response.status_code == 200:
    assistants = response.json().get('data', [])
    if not assistants:
        print("No assistants found.")
    else:
        # Log and display all assistants
        print("Here are all the assistants:")
        for i, assistant in enumerate(assistants, start=1):
            print(f"{i}. ID: {assistant['id']}, Name: {assistant.get('name', 'No name')}, File IDs: {assistant.get('file_ids', [])}")

        # Ask for confirmation before deletion
        confirm = input("\nDo you want to delete all these listed assistants? (yes/no): ")
        if confirm.lower() == 'yes':
            # Use a ThreadPoolExecutor to delete the assistants in parallel
            with ThreadPoolExecutor() as executor:
                executor.map(delete_assistant, [assistant['id'] for assistant in assistants])

        # Ask for confirmation to delete all assistants
        confirm_all = input("\nDo you want to delete ALL assistants? (yes/no): ")
        if confirm_all.lower() == 'yes':
            while True:
                # Get the list of all assistants
                response = requests.get("https://api.openai.com/v1/assistants?order=desc&limit=100", headers=headers)

                # Check the status code of the response
                if response.status_code == 200:
                    assistants = response.json().get('data', [])
                    if not assistants:
                        print("No more assistants found.")
                        break
                    else:
                        # Use a ThreadPoolExecutor to delete the assistants in parallel
                        with ThreadPoolExecutor() as executor:
                            executor.map(delete_assistant, [assistant['id'] for assistant in assistants])
                else:
                    print(f"API request failed with status code {response.status_code}. Response: {response.text}")
                    break
else:
    print(f"API request failed with status code {response.status_code}. Response: {response.text}")