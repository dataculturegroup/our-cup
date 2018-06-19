from sqlalchemy.ext.declarative import declarative_base

from ourcup import alchemy_db

Base = declarative_base()


class PopulationInfo(alchemy_db.Model):
    __tablename__ = 'population_info'
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    tract_id = alchemy_db.Column(alchemy_db.String(250))
    tract_id2 = alchemy_db.Column(alchemy_db.String(12))
    label = alchemy_db.Column(alchemy_db.String(250))
    tract = alchemy_db.Column(alchemy_db.String(250))
    county = alchemy_db.Column(alchemy_db.String(250), index=True)
    state = alchemy_db.Column(alchemy_db.String(250), index=True)
    country = alchemy_db.Column(alchemy_db.String(250), index=True)
    pop_by_county_json = alchemy_db.Column(alchemy_db.String(2000))


class ZipCodeInfo(Base):
    __tablename__ = 'zip_code_info'
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    zip_code = alchemy_db.Column(alchemy_db.String(5), index=True)
    state_id = alchemy_db.Column(alchemy_db.String(2))
    county_id = alchemy_db.Column(alchemy_db.String(3))
    tract_id = alchemy_db.Column(alchemy_db.String(6))
    tract_id2 = alchemy_db.Column(alchemy_db.String(12))

