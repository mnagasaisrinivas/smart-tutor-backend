from app.extensions import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer_title = db.Column(db.String(255), nullable=False)
    answer_steps = db.Column(db.Text, nullable=False)
    answer_summary = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Question {self.id} - {self.subject}>"
