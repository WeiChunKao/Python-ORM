from orm import ORM
from sqlalchemy import Table, Column, String, Integer
from typing import List, Any


class User(object):
    def __init__(self, id, name, test):
        self.id = id
        self.name = name
        self.test = test


if __name__ == '__main__':
    orm = ORM()
    user = Table('user', orm.getMetaData(),
                 Column('id', String(50), primary_key=True),
                 Column('name', String(50)),
                 Column('test', Integer())
                 )
    orm.setMapper(User, user)
    #orm.insert([User(name='Jack', id='3',test=789), User(name='Jack',id='4',test=456)])
    #orm.deleteAll(User,"name= :name", name = 'Jack')
    #orm.deleteOne(User, "name= :name and id != :id ", name='Jack',id='4')
    #orm.updateOne(User, "name= :name", {'test': 123}, name='wendy')
    #orm.updateAll(User, "name= :name", {'test': 7777}, name='Jack')
    for instance in orm.getSessions().query(User).order_by(User.id):
        print(instance.id, instance.name, instance.test)
    orm.close()
