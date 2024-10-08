# not to be removed, the Subclasses are needed for the dynamic invocations
from actions import *
from config.base_automation_action import BaseAutomationAction

# This scans the subclasses of the base class (BaseAutomationAction) and constructs the action_registry ("registered_actions")
# registered_actions - contains a dictionary of subclass mapping as {"MarksAsRead": MarksAsRead} - key: class_name and value: class itself

action_classes = BaseAutomationAction.__subclasses__()
registered_actions = {cls.__name__: cls for cls in action_classes}
if len(registered_actions) == 0:
    raise RuntimeError('No action classes registered')
