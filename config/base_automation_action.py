from abc import ABC, abstractmethod


# This is an abstract class which needs to extended to define the new actions
class BaseAutomationAction(ABC):

    def __init__(self, api_connector, action_params):
        self.connector = api_connector
        self.action_params = action_params

    @abstractmethod
    def action_params_list(self):
        pass

    @abstractmethod
    def perform(self):
        pass

    def validate_action_params(self):
        is_valid = all(self.action_params.get(param) is not None for param in self.action_params_list())
        if not is_valid:
            raise ValueError('Insufficient data: Action param not valid')

    def execute(self):
        try:
            self.validate_action_params()
            self.perform()
        except Exception as e:
            print(f"***** Action execution failure in {self.__class__.__name__}: {str(e)} ******")
