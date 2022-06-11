"""
ORM layer for the DB
"""
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column#, Table
from sqlalchemy import create_engine
from sqlalchemy import (
#        Boolean,
        DateTime,
        Integer,
#        Float,
        String,
        Text,
        ForeignKey
)
#from report.conf import settings


class STATUS(Enum):
    ABORTADO = -1
    PENDIENTE = 0
    COMPLETADO = 1


class PRIORITY(Enum):
    MENOR = 1
    MEDIA = 10
    MAYOR = 30
    CRITICO = 50


Base = declarative_base()

TASK_TEMPLATE = """
##Tarea #{id}
* Objetivo: {objective}

* Estado: {status}

* Prioridad: {priority}

* Solucion:
{solution}

* Observaciones:
{observations}

* Creada: {date_created}

* Actualizada: {date_updated}

* Finalizada: {date_finished}
"""

REPORT_TEMPLATE = """
REPORTE: {id}

FECHA: {date_created}

Objetivo: {objective}
=====================

{tasks}

---------------------
#Observaciones:
{observations}
"""

class Task(Base):
    """
    Fields describing the task
    """

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, nullable=False)
    report = Column(Integer, ForeignKey("report.id", link_to_name=True), nullable=False)
    objective = Column(String, nullable=False)
    solution = Column(Text)
    observations = Column(Text)
    status = Column(Integer, default=0, index=True)
    priority = Column(Integer, default=1, index=True)

    date_created = Column(DateTime, default=datetime.now(), index=True, nullable=False)
    date_updated = Column(DateTime, default=datetime.now(), index=True, nullable=False)
    date_finished = Column(DateTime)

    def __str__(self):
        return self.objective

    def as_markdown(self):
        return TASK_TEMPLATE.format(
                id=self.id,
                objective=self.objective,
                observations="\n".join(self.observations.split('\n')),
                solution="\n".join(self.solution.split('\n')),
                status=STATUS(self.status).name,
                priority=PRIORITY(self.priority).name,
                date_created=self.date_created,
                date_updated=self.date_updated,
                date_finished=self.date_finished,
        )

class Report(Base):
    """
    Report information
    """

    __tablename__ = "report"

    id = Column(Integer, primary_key=True, nullable=False)
    objective = Column(String, nullable=False)
    observations = Column(Text)

    tasks = relationship("Task")

    date_created = Column(DateTime, default=datetime.now(), index=True, nullable=False)

    def __str__(self):
        return self.objective

    def as_markdown(self):
        return REPORT_TEMPLATE.format(
            id=self.id,
            objective=self.objective,
            observations=self.observations,
            tasks="\n\n".join(task.as_markdown() for task in self.tasks),
            date_created=self.date_created,
        )

def create_db(name="sqlite:///./db.sqlite"):
    engine = create_engine(name)

    Base.metadata.create_all(engine)

    return engine


def drop_db(name="sqlite:///./db.sqlite"):
    engine = create_engine(name)
    Base.metadata.drop_all(engine)
