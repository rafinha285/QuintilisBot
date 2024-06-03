from typing import TypedDict,List

class Player(TypedDict):
    _id:str
    name:str
    points:int
    clan:str

class Clan(TypedDict):
    name:str
    points:int
    members:List[str]
    enemies:List[str]
    allies:List[str]
    owner:str
    prefix:str