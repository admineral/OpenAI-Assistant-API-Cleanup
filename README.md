
# OpenAI-Cleanup-Scripts

This repository contains Python scripts for efficient bulk deletion of OpenAI assistants and files. It's a handy tool for OpenAI resource management and cleanup.

## Scripts

1. `delete_assistants.py`: This script deletes OpenAI assistants. It fetches a list of all assistants, displays them, and asks for user confirmation before deletion. If confirmed, the assistants are deleted in parallel using multithreading.

2. `delete_files.py`: This script deletes OpenAI files. It fetches a list of all files, displays them, and asks for user confirmation before deletion. If confirmed, the files are deleted in parallel using multithreading.

## Usage

1. Set your OpenAI API key in a `.env` file or as an environment variable named `OPENAI_API_KEY`.

2. Run the scripts using Python 3:

3. `python3 delete_assistants.py`
   
4. `python3 delete_files.py`


# Please use these scripts responsibly as they can delete all your OpenAI assistants or files.
