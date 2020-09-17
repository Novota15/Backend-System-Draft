# database functions
import datetime
from sys import argv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine, select

Base = declarative_base()

# Tables
class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String(100))
    url = Column(Integer, ForeignKey('url.id'))
    path = Column(String(200))
    last_modified = Column(String(200))
    verified = Column(Boolean, unique=False, default=False)

class URL(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key = True, autoincrement=True)
    address = Column(String(200))
    enabled = Column(Boolean, unique=False, default=True)
    last_fetched = Column(DateTime, default=datetime.datetime.utcnow)
    interval = Column(String(50))
    
# general db functions
def create(database):
    # an engine that the session will use for resources
    engine = create_engine(database)
    # create a configured session class
    Session = sessionmaker(bind=engine)
    # create a session
    session = Session()
    return engine, session

def result_dict(r):
    return dict(zip(r.keys(), r))

def result_dicts(rs):
    return list(map(result_dict, rs))

def database_dump(session):
    Database = [File, URL]
    for table in Database:
        stmt = select('*').select_from(table)
        result = session.execute(stmt).fetchall()
        print(result_dicts(result))
    return

def create_tables(engine):
    Base.metadata.create_all(engine)
    return

def init_session():
    engine, session = create("sqlite:///db.sqlite3")
    create_tables(engine)
    return session

def close(conn):
    conn.close()
    return

# add rows to tables
def add_file(session, name, url, path, verified, last_modified):
    f = File(name=name, url=url, path=path, verified=verified, last_modified=last_modified)
    session.add(f)
    session.commit()
    return

def add_url(session, address, enabled, interval):
    url = URL(address=address, enabled=enabled, interval=interval)
    session.add(url)
    session.commit()
    return

# check if objects exist in db
def check_file(session, name):
    file = session.query(File).filter_by(name=name).scalar()
    if file == None:
        return False
    return True

def check_url(session, address):
    url = session.query(URL).filter_by(address=address).scalar()
    if url == None:
        return False
    return True

# get table objects
def get_file_by_name(session, name):
    exists = check_file(session, name)
    if exists == False:
        return None
    return session.query(File).filter_by(name=name).scalar()

def get_files_by_url(session, url_id):
    file_list = []
    files = session.query(File).all()
    for f in files:
        if f.url == url_id:
            file_list.append(f)
    return file_list

def get_url(session, name):
    exists = check_url(session, name)
    if exists == False:
        return None
    return session.query(URL).filter_by(name=name).scalar()

# get all table rows
def get_all_urls(session):
    url_list = []
    urls = session.query(URL).all()
    for url in urls:
        url_list.append(url)
    return url_list

def get_all_enabled_urls(session):
    url_list = []
    urls = session.query(URL).all()
    for url in urls:
        if url.enabled == True:
            url_list.append(url)
    return url_list

def get_all_files(session):
    file_list = []
    files = session.query(File).all()
    for f in files:
        file_list.append(f)
    return file_list

# update element in db
def update_url(session, address, column, value):
    url = session.query(URL).filter_by(address=address).scalar()
    if column == "address":
        url.address = value
    elif column == "enabled":
        if value == "True" or value == "true":
            enabled = True
        elif value == "False" or value == "false":
            enabled = False
        url.enabled = enabled
    elif column == 'last_fetched':
        url.last_fetched = value
    elif column == "interval":
        url.interval = value
    else:
        print("url not updated")
    session.commit()
    return

# file is selected by id because there could be multiple versions with the same file name
def update_file(session, id, column, value):
    f = session.query(File).filter_by(id=id).scalar()
    if column == "name":
        f.name = value
    elif column == "url":
        f.url = value
    elif column == "path":
        f.path = value
    elif column == "last_modified":
        f.last_modified = value
    elif column == "verified":
        f.verified = value
    else:
        print("file not updated")
    session.commit()
    return

# to build/modify database via command line
if len(argv) >= 2:
    session = init_session()
    if argv[1] == 'build_db' or argv[1] == 'dump':
        # session = init_session()
        database_dump(session)
    elif argv[1] == 'add_url':
        address = argv[2]
        if len(argv) == 4:
            interval = argv[3]
        else:
            interval = "1h"
        add_url(session, address, True, interval)
    elif argv[2] == 'set_interval':
        address = argv[2]
        interval = argv[3]
        update_url(session, address, "interval", interval)
    elif argv[2] == 'url_enabled':
        address = argv[2]
        enabled = argv[3]
        update_url(session, address, "enabled", enabled)
    close(session)

