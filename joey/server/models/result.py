import datetime

from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class Result(Base):
    """Result of a Task as executed by a Node.

    A result belongs to one organization and one task, which is assigned in
    TaskAssignment. The result is encrypted and can be only read by the 
    intended receiver of the message.
    """

    # fields
    assignment_id = Column(Integer, ForeignKey("task_assignment.id"))
    result = Column(Text)
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    log = Column(Text)

    # relationships
    task_assignment = relationship('TaskAssignment', back_populates='result')

    @hybrid_property
    def complete(self):
        return self.finished_at is not None

    def __repr__(self):
        return (
            f"<task:{self.task_assignment.task.name}, "
            f"organization: {self.task_assignment.organization.name}, "
            f"is_complete: {self.complete}>"
        )