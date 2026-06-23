from .queries import UserQueries
from dotenv import load_dotenv

load_dotenv()


class UserRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.create_user_table()
        
    def reset_db(self):
        self.cursor.execute(UserQueries.TRUNCATE_DATA.value)
        
    def create_user_table(self):
        self.cursor.execute(UserQueries.CREATE_TABLE.value)
        self.conn.commit()
    
    def convert_row_to_user(self, row):
        if not row:
            return None
        return {"id": row[0], "user": row[1], "gender": row[2]}

    def get_all_users(self):
        self.cursor.execute(UserQueries.GET_ALL_USERS.value)
        rows = self.cursor.fetchall()
        return [self.convert_row_to_user(row) for row in rows]
    
    def get_user_by_id(self, user_id):
        self.cursor.execute(UserQueries.GET_USER_BY_ID.value, (user_id,))
        return self.convert_row_to_user(self.cursor.fetchone())

    def does_user_exist(self, user_id):
        self.cursor.execute(UserQueries.USER_EXISTS.value, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def add_a_user(self, name, gender):
        self.cursor.execute(UserQueries.INSERT_USER.value, (name, gender))
        new_user = self.convert_row_to_user(self.cursor.fetchone())
        self.conn.commit()
        return new_user

    def update_user_name(self, user_id, name):
        self.cursor.execute(UserQueries.UPDATE_USER.value, (name, user_id))
        self.conn.commit()
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id):
        self.cursor.execute(UserQueries.DELETE_USER.value, (str(user_id),))
        self.conn.commit()
