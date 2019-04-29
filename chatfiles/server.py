import re
import socket, time
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'chat'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    address = sqlalchemy.Column(sqlalchemy.String)
    nick = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
    data = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, address, nick, time, data):
        self.address = address
        self.nick = nick
        self.time = time
        self.data = data

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" % (self.address, self.nick, self.time, self.data)

Base.metadata.create_all(engine)
session = Session()

host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
values = []

quit = False
print("[ Server Started ]")

while not quit:
    try:
        data, addr = s.recvfrom(1024)
        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        data_value = re.findall(r'\w+', data.decode("utf-8"))
        values.append((str(addr[1]), str(data_value[0]), str(itsatime), str(' '.join(data_value[1:]))))

        if addr not in clients:
            clients.append(addr)

        print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/", end=" ")
        print(data.decode("utf-8"))

        for client in clients:
            if addr != client:
                s.sendto(data, client)
    except:
        print("\n[ Server Stopped ]")
        quit = True

for v in values:
    session.add(User(v[0], v[1], v[2], v[3]))
    session.commit()

for u in session.query(User).order_by(User.id):
    print(u)

s.close()



