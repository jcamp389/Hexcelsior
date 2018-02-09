from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('mysql://username:password@174.138.75.108/dbname')

class HexcelsiorDB(object):
    _session = None

    @property
    def session(self):
        if not self._session:
            self.session = sessionmaker(bind=engine)()
        return self._session

    @session.setter
    def session(self, val):
        self._session = val

db = HexcelsiorDB()
Base.metadata.create_all(engine)