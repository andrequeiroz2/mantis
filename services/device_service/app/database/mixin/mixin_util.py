from sqlalchemy import TIMESTAMP, Boolean, Column, func, text
from sqlalchemy.sql import expression
from sqlalchemy_utils import observes


class TimestampMixin:
    __datetime_func__ = text("CURRENT_TIMESTAMP")

    dt_inclusion = Column("dt_inclusion", TIMESTAMP(timezone=False), server_default=__datetime_func__, nullable=False)

    dt_upgrade = Column("dt_upgrade", TIMESTAMP(timezone=False), server_default=__datetime_func__, onupdate=__datetime_func__, nullable=False)


class ObjectStateMixin:
    obj_inactive = Column("obj_inactive", TIMESTAMP(timezone=False))

    obj_active = Column("obj_active", Boolean, default=True, server_default=expression.true(), nullable=False)

    @observes("obj_active")
    def obj_active_obsever(self, obj_active: bool):
        self.obj_inactive = None if obj_active else func.now()

