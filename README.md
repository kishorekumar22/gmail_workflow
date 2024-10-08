# gmail_workflow
Stanalone python scripts
  - Connects to the gmail using OAuth and downloads the emails into a local data(emails_automator.sqlite)
  - Processes the downloaded emails from DB and performs the workflow execution based on the rules configured. These rules needs to the defined as a JSON files and needs to put under `files` directory. 


# Prequiresites:
1. `python3` and `pip3` to be installed in the machine - https://www.python.org/downloads/
2. Set up OAuth 2.0 Client in the google cloud project - https://developers.google.com/workspace/guides/create-credentials
3. Download the OAuth client secrets JSON file and rename it as `credentials.json`

# installation & execution steps:

  `Python3` and `pip3` installed 
1. Checkout the repo https://github.com/kishorekumar22/gmail_workflow
2. Navigate to the project folder
3. Execute `pip3 install -r requirements.txt` to install the required packages
4. Delete  `emails_automator.sqlite` from the project folder which included for the reference purpose.
5. Move the `credentials.json` under `/files` directory in the project

6. To run the email download script, execute `python3 sync_mailbox_conversations.py` , this will prompt for Google's authentication via external link, upon successful login, the email will be fetched and dumped into the local database table `conversations`
<img width="1721" alt="Screenshot 2024-10-08 at 7 08 53 PM" src="https://github.com/user-attachments/assets/ede7b814-b37b-4397-a4a8-516f0666bbd1">

7. To run the automation based on the defined in the input file, execute `python3 mailbox_automation_executor.py`. The default input rule is `files/simple_and_automation.json` which needs to udpated accordingly.
<img width="1728" alt="Screenshot 2024-10-08 at 7 11 58 PM" src="https://github.com/user-attachments/assets/3c7d93bb-3459-4e9d-85ba-608342ef3ba3">
