from dataclasses import dataclass

@dataclass
class Order:
    userid: str
    appid: str
    orderid: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            userid = data.get('userid'),
            appid = data.get('appid'),
            orderid = data.get('orderid')
        )    