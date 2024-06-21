from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# 定义数据库模型
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    userID = Column(Integer, primary_key=True, unique=True)
    userName = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)


# 定义操作库
class UserDB:
    def __init__(self, db_path='sqlite://data/users.db'):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_user(self, user_id, user_name):
        with self.Session() as session:
            if not session.query(User).filter_by(userID=user_id).first():
                user = User(userID=user_id, userName=user_name)
                session.add(user)
                session.commit()
                return True
            else:
                return False

    def get_user(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user
    def update_user(self, user_id, update_data):
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        for key, value in update_data.items():
            setattr(user, key, value)
        session.commit()
        session.close()

    def delete_user(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.delete(user)
        session.commit()
        session.close()
