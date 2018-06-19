from ourcup import alchemy_db as db


class PopulationInfo(db.Model):
    __tablename__ = 'population_info'
    id = db.Column(db.Integer, primary_key=True)
    tract_id = db.Column(db.String(250))
    tract_id2 = db.Column(db.String(12))
    label = db.Column(db.String(250))
    tract = db.Column(db.String(250))
    county = db.Column(db.String(250), index=True)
    state = db.Column(db.String(250), index=True)
    country = db.Column(db.String(250), index=True)
    pop_by_county_json = db.Column(db.String(2000))


class ZipCodeInfo(db.Model):
    __tablename__ = 'zip_code_info'
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(5), index=True)
    state_id = db.Column(db.String(2))
    county_id = db.Column(db.String(3))
    tract_id = db.Column(db.String(6))
    tract_id2 = db.Column(db.String(12))

