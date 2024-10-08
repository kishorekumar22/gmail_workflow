import traceback

from components.workflow_config import WorkflowConfig
from config.db_config import db_session
from utils.db_utils import initialize_db_schema


def read_automation_rule_config(file_name):
    with (open(file_name, 'r') as input_file):
        rule_str = input_file.read()
        automation_rule = WorkflowConfig.model_validate_json(rule_str)
        return automation_rule


def initialize_workflow_from_file(workflow_config_json):
    print(f"********* Reading the automation rule config file from: '{workflow_config_json}'*******")
    workflow = read_automation_rule_config(workflow_config_json)
    print(" ********* No errors in the rule config. Initializing the Db schema. *********")
    return workflow


def main():
    try:
        # initialize_db_schema()
        workflow = initialize_workflow_from_file('files/simple_and_automation.json')
        print("**** Filtering records and execution of workflow started. *****")
        workflow.filter_matching_data()

        if workflow.is_actionable():
            workflow.execute_actions()
            print("******* Execution of automation workflow completed. *******")
        else:
            print("****** Skipping the execution of automation workflow. *******")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == '__main__':
    main()
