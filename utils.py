import sqlalchemy as db

def fetch_channel_data() :
    res = list()
    infilename = 'countries.csv'
    infile = open(infilename, 'r')
    line = infile.readline() #discard header
    line = infile.readline()
    while line  :
        assert(line[-1] == '\n' )
        line = line[:-1]
        assert(line[2] == '-')
        res.append((line[:2], line))

        #update
        line = infile.readline()
    infile.close()
    return res

if __name__ == '__main__' :
    engine = db.create_engine('sqlite:///foo.db')

    connection = engine.connect()
    metadata = db.MetaData()
    census = db.Table('census', metadata, autoload=True, autoload_with=engine)