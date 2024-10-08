# gmail_workflow
Standalone Python scripts:
  - Connect to Gmail using OAuth and download emails into a local database (`emails_automator.sqlite`).
  - Process the downloaded emails from the database and perform workflow execution based on configured rules. These rules need to be defined as JSON files and placed in the `files/` directory.


# Prequisites:
1. `python3` and `pip3` must be installed on the machine - https://www.python.org/downloads/
2. Set up OAuth 2.0 Client in a Google Cloud project, please follow - https://developers.google.com/workspace/guides/create-credentials
3. Download the OAuth client secrets JSON file and rename it to `credentials.json`.

# Installation & Execution:

1. Clone the repository: https://github.com/kishorekumar22/gmail_workflow
2. Navigate to the project folder and execute `pip3 install -r requirements.txt` to install the required packages.
3. Move the `credentials.json file`(downloaded from the google cloud project) to the `/files` directory in the project.
4. To run the email downloader script, execute `python3 sync_mailbox_conversations.py`. This will prompt for Google's authentication via an external link. Upon successful login, the emails will be fetched and stored in the local database table `conversations`.
        <img width="1721" alt="Screenshot 2024-10-08 at 7 08 53 PM" src="https://github.com/user-attachments/assets/ede7b814-b37b-4397-a4a8-516f0666bbd1">
5. To run the automation rule based on the input file, execute `python3 mailbox_automation_executor.py`. The default input rule is `files/simple_and_automation.json` which needs to be updated accordingly.
      <img width="1728" alt="Screenshot 2024-10-08 at 7 11 58 PM" src="https://github.com/user-attachments/assets/3c7d93bb-3459-4e9d-85ba-608342ef3ba3">

      
# Librabries used:
1. google_auth_oauthlib - OAuth 
2. googleapiclient  - REST API communication with gmail
3. sqlalchemy - ORM & Data persistance
4. pydantic   - JSON deserializations
