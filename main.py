from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper,sessionmaker
conn = 'mssql+pymssql://dbUserName:dbUserPassword@dbIp:dbPort/Database'
engine = create_engine(
    f'{conn}', echo=False)
metadata = MetaData()

user = Table('table_user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50))
        )

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

mapper(User, user)

Session = sessionmaker(bind=engine)
'''or
Session = sessionmaker()
Session.configure(bind=engine)
'''
# select
session = Session()
for instance in session.query(User).order_by(User.id):
    print(instance.id, instance.name)
# insert one
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
session.commit()
# insert many
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])
# rollback
session.rollback()