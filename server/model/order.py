from dataclasses import dataclass

@dataclass
class Order:
    user_id: str
    app_id: str
    order_id: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id = data.get('user_id'),
            app_id = data.get('app_id'),
            order_id = data.get('order_id')
        )    