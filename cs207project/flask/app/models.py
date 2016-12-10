# models.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

from app import db

class TSMetadata(db.Model):
    """
    Description
    -----------
    Represents the `ts_metadata`
    table in our database `ts_metadata`

    Parameters
    ----------
    None :)

    Returns
    -------
    """
    id = db.Column(db.Integer, primary_key=True)
    mean = db.Column(db.Float, index=True)
    std = db.Column(db.Float, index=True)
    blarg = db.Column(db.Float, index=True)
    level = db.Column(db.String, index=True)
    r = lambda self, x: round(x, 3) # hack :(

    def __repr__(self):
        return '<TS Metadata: id: {}, mean: {}, std: {}, blarg: {}, level: {}>'\
               .format(self.id, *[self.r(x) for x in [self.mean, self.std, self.blarg]], self.level)


