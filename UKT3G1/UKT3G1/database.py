# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     db = get_db()

#     with app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


# import UKT3G1.Models
# Base.metadata.create_all(bind=engine)

# def init_db():
#     metadata.create_all(bind=engine)