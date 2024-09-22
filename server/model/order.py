from dataclasses import dataclass

@dataclass
class Order:
    userid: str
    appid: str
    orderid: str