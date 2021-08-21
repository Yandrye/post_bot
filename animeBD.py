from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import pickle

from telebot.types import InlineKeyboardMarkup, Message
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
        self.search_id: int = int()
        self.log_message: Message = None


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
        self.game_modes = ''


Base = declarative_base()


class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    temp = Column(LargeBinary)
    aport = Column(Integer)


class igdb(Base):
    __tablename__ = 'igdb'
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_access_token = Column(String)
    expire = Column(Integer)


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
                db_item.aport = User.aport + 1
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

    def set_igdb_app_access_token(self, access_token: str, expire: int):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(igdb).first()
            if db_item:
                db_item.app_access_token = access_token
                db_item.expire = expire
                session.commit()
            else:
                session.add(igdb(
                    app_access_token=access_token,
                    expire=expire
                ))
                session.commit()
            session.close()
        except Exception as e:
            session.close()
            raise e

    def get_igdb_app_access_token(self):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(igdb).first()
            session.close()
            if db_item:
                app_access_token: str = str(db_item.app_access_token)
                expire: int = db_item.expire
                return (app_access_token, expire)
            else:
                return None
        except Exception as e:
            session.close()
            raise e
