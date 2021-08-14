from sqlalchemy import Column, Integer, LargeBinary
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import pickle

from telebot.types import InlineKeyboardMarkup
from typing import List, Dict

class Temp():
    def __init__(self):
        self.markup: InlineKeyboardMarkup = None
        self.titulo: str = None
        self.tipo: str = None
        self.search: List[Dict[str, any]] = None
        self.username: str = None
        self.id_user: int = int()
        self.name: str = None
        self.hidden_name: str = None
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
            session.close()
            if db_item:
                return True
            else:
                return False
        except Exception as e:
            session.close()
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e

    def new_u(self, id: int, temp: Temp):
        session: Session = sessionmaker(self.engine)()
        try:
            new_item = User(id=id, temp=pickle.dumps(temp), aport=0)
            session.add(new_item)
            session.commit()
            session.close()
        except Exception as e:
            session.close()
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
                session.close()
        except Exception as e:
            session.close()
            print(f'An error occurred updating. The item to update was\n{id}')
            raise e

    def get_temp(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(id=id).first()
            session.close()
            if db_item:
                return pickle.loads(db_item.temp)
            else:
                self.new_u(id, Temp())
                self.get_temp(id)
                return False
        except Exception as e:
            session.close()
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
                session.close()
        except Exception as e:
            session.close()
            print(f'An error occurred updating. The item to update was\n{id}')

    def get_aport(self, id: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(User).filter_by(id=id).first()
            session.close()
            if db_item:
                return db_item.aport
        except Exception as e:
            session.close()
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e
