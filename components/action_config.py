from typing import Optional

from pydantic import BaseModel

from config.action_registry import registered_actions


class ActionConfig(BaseModel):
    name: str
    params: Optional[dict] = {}

    def is_valid(self):
        if self.name not in registered_actions.keys():
            raise Exception("Unsupported action provided")
