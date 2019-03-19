from app import db
from datetime import datetime

class Response(db.Model):
    __tablename__ = "responses_tables"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.Text(), nullable=False)
    thread_id = db.Column(db.Text())
    response = db.Column(db.Text())

    def __init__(self, pub_date, thread_id, response):
        pub_date = str(pub_date).split(".")[0]
        self.pub_date = pub_date
        self.thread_id = thread_id
        self.response = response
