from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.serialize_created_at(),
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            created_at=cls.parse_created_at(row["created_at"]),
        )

    def serialize_created_at(self) -> str:
        return self.created_at.isoformat()

    @staticmethod
    def parse_created_at(value: str) -> datetime:
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value)
