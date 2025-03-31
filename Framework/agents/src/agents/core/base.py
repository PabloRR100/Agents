from pydantic import BaseModel


class Serializable(BaseModel):
    """
    A Serializable is a base class for all serializable objects
    """
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            bytes: lambda v: v.decode('utf-8'),
            str: lambda v: v.encode('utf-8'),
        }

    def __str__(self):
        """
        Return a string representation of the object
        """
        return self.model_dump_json(indent=4)
