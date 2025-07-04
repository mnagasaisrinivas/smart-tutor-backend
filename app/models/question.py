from typing import List
from app.extensions import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer_steps = db.Column(db.Text, nullable=False)
    answer_summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    _DELIMITER = '<|>'

    # Property to handle list conversion
    @property
    def answer_steps_list(self) -> List[str]:
        if self.answer_steps:
            return self.answer_steps.split(self._DELIMITER)
        return []
    
    @answer_steps_list.setter
    def answer_steps_list(self, answer_steps_list: List[str]):
        self.answer_steps = self._DELIMITER.join(answer_steps_list)


    def __repr__(self):
        return f"<Question {self.id} - {self.subject}>"
