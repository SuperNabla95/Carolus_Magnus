# bot.py
import sqlalchemy as db
engine = db.create_engine('sqlite:///./eurasmus.db', echo = True)
connection = engine.connect()
metadata = db.MetaData()

#tables
roles = db.Table('roles', metadata, autoload=True, autoload_with=engine)
coins = db.Table('coins', metadata, autoload=True, autoload_with=engine)
collection = db.Table('collection', metadata, autoload=True, autoload_with=engine)
swap = db.Table('swap', metadata, autoload=True, autoload_with=engine)

def compute_swap_list(uid1, uid2) :
    try :
        subq1 = db.select(collection.c.cid).where(collection.c.uid==uid2)
        #q = db.select(swap.c.cid).where(swap.c.uid==uid1).where(swap.c.cid.not_in(subq1)).order_by(swap.c.cid)
        q = db.select(coins.c.name).where(coins.c.cid==swap.c.cid).where(swap.c.uid==uid1).where(swap.c.cid.not_in(subq1)).order_by(coins.c.cid)
        rs = connection.execute(q)
        return [r[0] for r in rs]
    except db.exc.IntegrityError as err :
        print('🚨 Integrity error.\n', str(err))

def insert(table,cid,uid) :
    try :
        q = db.insert(table).values(cid=cid,uid=uid)
        connection.execute(q)
    except db.exc.IntegrityError as err :
        print('🚨 Integrity error.\n', str(err))
    return

def delete(table,cid,uid) :
    try :
        q = db.delete(table).where(table.c.cid == cid).where(table.c.uid == uid)
        connection.execute(q)
    except db.exc.IntegrityError as err :
        print('🚨 Integrity error.\n', str(err))
    return

def in_collection(cid, uid) :
    return insert(collection, cid, uid)

def in_swap(cid, uid) :
    return insert(swap, cid, uid)

def out_collection(cid, uid) :
    return delete(collection, cid, uid)

def out_swap(cid, uid) :
    return delete(swap, cid, uid)

def get_role_name(msg_num,flag) :
    res = None
    try :
        q = db.select(roles.c.role_name).where(roles.c.msg_num==msg_num).where(roles.c.flag==flag)
        rs = connection.execute(q)
        #print('quiz', [r for r in rs])
        if rs :
            res = rs.first()[0]
    except db.exc.IntegrityError as err :
        print('🚨 Integrity error.\n', str(err))    
    return res
if __name__ == '__main__' :
    pass