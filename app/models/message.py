from datetime import datetime
from flask_pymongo import ObjectId


class MessageModel:
    def __init__(self, text=None, name_audio=None, is_audio=False, timestamp=datetime.now(), user=None):
        self.text = text
        self.name_audio = name_audio
        self.is_audio = is_audio
        self.timestamp = timestamp
        self.user = user

    def to_dict(self):
        return {
            "text": self.text,
            "name_audio": self.name_audio,
            "is_audio": self.is_audio,
            "timestamp": self.timestamp,
            "user": self.user
        }

    def save(self):
        from app import mongo
        collection = mongo.db.messages
        message_data = self.to_dict()
        result = collection.insert_one(message_data)
        return str(result.inserted_id)

    @classmethod
    def find_by_id(cls, message_id):
        from app import mongo
        collection = mongo.db.messages
        message_data = collection.find_one({"_id": ObjectId(message_id)})
        if not message_data:
            return None
        message_data.pop("_id", None)
        return cls(**message_data)

    @classmethod
    def find_all(cls):
        from app import mongo
        collection = mongo.db.messages
        messages_data = collection.find()
        messages = []
        for message_data in messages_data:
            message_data.pop("_id", None)
            messages.append(cls(**message_data))
        return messages

