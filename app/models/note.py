from typing import List
from app.extensions import db

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    heading = db.Column(db.String(255), nullable=False)
    _bullet_points = db.Column(db.String(255), nullable=False)
    saved_date = db.Column(db.DateTime, default=db.func.now())
    
    _DELIMITER = '<|>'

    # Property to handle list conversion
    @property
    def bullet_points(self) -> List[str]:
        if self._bullet_points:
            return self._bullet_points.split(self._DELIMITER)
        return []
    
    @bullet_points.setter
    def bullet_points(self, bullet_points: List[str]):
        self._bullet_points = self._DELIMITER.join(bullet_points)

    def __repr__(self):
        return f"<Note {self.id} - {self.topic}>"

