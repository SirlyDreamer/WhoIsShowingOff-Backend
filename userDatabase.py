from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker,declarative_base

# 定义数据库模型
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(Integer, unique=True, nullable=False)
    user_name = Column(String, nullable=False)

# 定义操作库
class Database:
    def __init__(self, db_path='sqlite:///users.db'):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_user(self, phone_number, user_name):
        session = self.Session()
        if not session.query(User).filter_by(phone_number=phone_number).first():
            user = User(phone_number=phone_number, user_name=user_name)
            session.add(user)
            session.commit()
        session.close()
    
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

# 主函数
def main():
    db = Database()
    
    # 添加用户
    db.add_user(phone_number=1234567890, user_name='John Doe')
    db.add_user(phone_number=9876543210, user_name='Jane Smith')
    
    # 测试读取、更新和删除操作
    user = db.get_user(1)
    if user:
        print(f"User 1: {user.user_name}, {user.phone_number}")
    
        # 更新用户
        db.update_user(1, {'user_name': 'John Updated'})
        updated_user = db.get_user(1)
        print(f"Updated User 1: {updated_user.user_name}, {updated_user.phone_number}")
        
        # 删除用户
        db.delete_user(1)
        deleted_user = db.get_user(1)
        print(f"Deleted User 1: {deleted_user}")

if __name__ == '__main__':
    main()
