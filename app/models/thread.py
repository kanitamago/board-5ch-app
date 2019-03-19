from app import db
from datetime import datetime

class Thread(db.Model):
    __tablename__ = "threads_tables"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.Text(), nullable=False)
    title = db.Column(db.Text())
    password = db.Column(db.Text())
    content = db.Column(db.Text())

    def __init__(self, pub_date, title, password, content):
        pub_date = str(pub_date).split(".")[0]
        self.pub_date = pub_date
        self.title = title
        self.password = password
        self.content = content
