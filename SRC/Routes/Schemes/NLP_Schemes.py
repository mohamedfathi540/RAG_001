from pydantic import BaseModel
from typing import Optional

class PushRequest (BaseModel) :

    do_reset : Optional[int] = 0


class SearchRequest (BaseModel) :

    text : str
    project_name : Optional[str] = None
    limit : Optional[int] = 5
