import datetime
import re

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        class_name = cls.__name__
        class_name = re.sub(r"([a-z])([A-Z])", r"\1_\2", class_name)
        class_name = class_name.lower()

        if class_name.endswith("y"):
            return f"{class_name[:-1]}ies"  # Заменяем 'y' на 'ies'
        elif class_name.endswith("s"):
            return f"{class_name}es"

        return f"{class_name}s"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.datetime.now
    )
