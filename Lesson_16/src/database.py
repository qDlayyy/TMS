from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Places(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String)

    def info(self):
        return{
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'description': self.description
        }

class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)

    def info(self):
        return{
            'id': self.id,
            'name': self.name,
            'place_id': self.place_id,
            'date': self.date,
            'description': self.description
        }

class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    place = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    price = Column(Float, nullable=False)
    booking = Column(String, default='Available')

    def info(self):
        return{
            'id': self.id,
            'place': self.place,
            'event_id': self.event_id,
            'price': self.price
        }

engine = create_engine('sqlite:///ticket_reservation.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)