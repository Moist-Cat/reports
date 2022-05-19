from datetime import datetime
from sqlalchemy import desc, create_engine, update
from sqlalchemy.orm import sessionmaker
import json
import logging
# the project is too unstable atm to make type hints
#from typing import Union, List, Set, Tuple, Dict
import os
from glob import glob
from pathlib import Path

from report.conf import settings
from report.db import Task, Report, STATUS, PRIORITY
from report.log import logged

log = logging.getLogger("global")

_ENGINE = settings.DATABASES["default"]["engine"]
CONFIG = settings.DATABASES["default"]["config"]

@logged
class DBClient:

    def __init__(self, engine=_ENGINE, config=CONFIG):
        self.logger.debug("Started %s. Engine: %s", self.__class__.__name__, _ENGINE)

        db_file = Path(_ENGINE[10:])
        assert db_file.exists(), "DB file doesn't exist!"
        assert db_file.stat().st_size > 0, "DB file is just an empty file!"

        engine = create_engine(engine)
        Session = sessionmaker(bind=engine, **config)
        self.session = Session()

    def __delete__(self):
        self.session.close()

    # task
    def list_task(self):
        return self.session.query(Task).all()

    def get_task(self, id):
        return self.session.query(Task).filter(Task.id==id).one()

    def create_task(self, /, **kwargs):
        task = Task(**kwargs)
        self.session.add(task)

        return task

    def update_task(self, id, **kwargs):
        return self.session.execute(
            update(Task).
            where(Task.id==id).
            values(**kwargs, date_updated=datetime.now())
        )
    
    def delete_task(self, id):
        task = self.session.query(Task).filter(Task.id==id)
        self.session.delete(task)

        return None

    #  report
    def list_report(self):
        return self.session.query(Report).all()

    def get_report(self, id):
        return self.session.query(Report).filter(Report.id==id).one()

    def create_report(self, /, **kwargs):
        report = Report(**kwargs)
        self.session.add(report)

        return report

    def update_report(self, id, **kwargs):
        return self.session.execute(
            update(Report).
            where(Report.id==id).
            values(**kwargs)
        )
    def delete_report(self, id):
        report = self.session.query(report).filter(Report.id==id)
        self.session.delete(report)

        return None

