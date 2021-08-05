from sqlalchemy import Column, Integer, Text, LargeBinary
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pickle
from time import time


class Temp():
    def __init__(self):
        self.markup = None
        self.titulo = None
        self.username = None
        self.id_user: int = int()
        self.name = None
        self.hidden_name = None
        self.post = P_Anime()


class P_Anime():
    def __init__(self):
        self.titulo = ''
        self.imagen = None
        self.tipo = '#Desconocido'
        self.tags = ''
        self.year = ''
        self.format = ''
        self.status = ''
        self.episodes = ''
        self.genero = ''
        self.descripcion = ''
        self.episo_up = ''
        self.temporada = ''
        self.audio = ''
        self.link = ''
        self.txt = ''
        self.inf = ''
        self.tomos = ''
        self.plata = ''
        self.estudio = ''
        self.idioma = ''
        self.duracion = ''
        self.volumen = ''
        self.creador = ''
        self.version = ''
        self.peso = ''
        self.sis_j = ''
        self.name_txt = ''
        self.hidden_name = ''


Base = declarative_base()


class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    temp = Column(LargeBinary)
    aport = Column(Integer)


class Post(Base):
    __tablename__ = 'posts'
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Integer)
    id_sms = Column(Integer)
    id_user = Column(Integer)
    titulo = Column(Text)


class General(Base):
    __tablename__ = 'generales'
    id_sms = Column(Integer, primary_key=True)


class DBHelper:
    def __init__(self, dbname: str):
        if dbname.startswith('sqlite'):
            self.engine = create_engine(
                dbname, connect_args={'check_same_thread': False})
        elif dbname.startswith('postgres://'):
            dbname = dbname.replace('postgres://', 'postgresql://', 1)
            self.engine = create_engine(dbname)
        else:
            self.engine = create_engine(dbname)
        Base.metadata.bind = self.engine
        Base.metadata.create_all(checkfirst=True)

    def get_u(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(
                id=id).first()
            if db_item:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e

    def new_u(self, id: int, temp: Temp):
        session: Session = sessionmaker(self.engine)()
        try:
            new_item = User(id=id, temp=pickle.dumps(temp), aport=0)
            session.add(new_item)
            session.commit()
        except Exception as e:
            print(f'An error occurred in insertion. The item to insert was\n' +
                  f'{id}')
            print(e)
            return False

    def set_temp(self, id: int, temp: Temp):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(
                id=id).first()
            if db_item:
                session.delete(db_item)
                updated = User(id=db_item.id, aport=db_item.aport,
                               temp=pickle.dumps(temp))
                session.add(updated)
                session.commit()
        except Exception as e:
            print(f'An error occurred updating. The item to update was\n{id}')
            raise e

    def get_temp(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(id=id).first()
            if db_item:
                return pickle.loads(db_item.temp)
            else:
                self.new_u(id, Temp())
                self.get_temp(id)
                return False
        except Exception as e:
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e

    def aport(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(id=id).first()
            if db_item:
                session.delete(db_item)
                session.add(User(
                    id=db_item.id,
                    aport=db_item.aport+1, temp=db_item.temp))
                session.commit()
        except Exception as e:
            print(f'An error occurred updating. The item to update was\n{id}')

    def get_aport(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(id=id).first()
            if db_item:
                return db_item.aport
        except Exception as e:
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e

    def new_p(self, id_sms: int, id_user: int, titulo: str):
        session: Session = sessionmaker(self.engine)()
        curret_time = time()//3600
        try:
            new_item = Post(time=curret_time, id_sms=id_sms,
                            id_user=id_user, titulo=titulo)
            session.add(new_item)
            session.commit()
        except Exception as e:
            print(
                f'An error occurred in insertion. The item to insert was\n{id_sms} {id_user} {titulo} {curret_time}')
            raise e

    def del_post(self, id_sms: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(Post).filter_by(id_sms=id_sms).first()
            session.delete(db_item)
            session.commit()
        except Exception as e:
            print(
                f'An error occurred in deletion. The item to delete was\n{id_sms}')
            return False
        return True

    def get_resumen(self):
        session: Session = sessionmaker(self.engine)()
        current_time = time()//3600
        query = text(":current_time - time < 25")
        try:
            items = session.query(Post).filter(
                query).params(current_time=current_time).all()
            # not quite shure of tuple
            return [(item.id_sms, item.titulo) for item in items]
        except Exception as e:
            print(f'An error occurred retrieving resumee')
            raise e

    def get_id_re(self):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(General).first()
            if db_item:
                return db_item.id_sms
            else:
                return None
        except Exception as e:
            print(f'An error occurred retrieving resumee id')
            raise e

    def set_id_re(self, id_sms: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(General).first()
            if db_item:
                session.delete(db_item)
                session.add(General(id_sms=id_sms))
                session.commit()
        except Exception as e:
            print(f'An error occurred settig resumee id')
            return False
        return True
