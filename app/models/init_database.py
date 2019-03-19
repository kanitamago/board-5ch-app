from app import db

def init():
    db.create_all()
    print("CREATE ALL.")
