from report.conf import settings
from report.db import *
from report.api import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE = DATABASES["default"]["engine"]

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)
session = Session()
breakpoint()
