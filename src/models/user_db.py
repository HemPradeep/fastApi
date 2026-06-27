from typing import Any

from dotenv import load_dotenv
from psycopg2.extensions import connection as ConnectionType
from psycopg2.extras import RealDictCursor

from .api_schemas import UserResponse
from .queries import UserQueries

load_dotenv()


class UserRepository:
    def __init__(self, conn: ConnectionType) -> None:
        self.conn: ConnectionType = conn
        self.cursor: Any = self.conn.cursor(cursor_factory=RealDictCursor)
        self.create_user_table()

    def reset_db(self) -> None:
        self.cursor.execute(UserQueries.TRUNCATE_DATA.value)

    def create_user_table(self) -> None:
        self.cursor.execute(UserQueries.CREATE_TABLE.value)
        self.conn.commit()

    def convert_row_to_user(self, row: Any) -> UserResponse | None:
        if not row:
            return None
        return UserResponse(id=row['id'], user=row['user_name'], gender=row['gender'])

    def get_all_users(self) -> list[UserResponse]:
        self.cursor.execute(UserQueries.GET_ALL_USERS.value)
        rows = self.cursor.fetchall()
        users: list[UserResponse] = []
        for row in rows:
            user = self.convert_row_to_user(row)
            if user is not None:
                users.append(user)
        return users

    def get_user_by_id(self, user_id: int) -> UserResponse | None:
        self.cursor.execute(UserQueries.GET_USER_BY_ID.value, (user_id,))
        return self.convert_row_to_user(self.cursor.fetchone())

    def does_user_exist(self, user_id: int) -> bool:
        self.cursor.execute(UserQueries.USER_EXISTS.value, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def add_a_user(self, name: str, gender: str) -> UserResponse | None:
        self.cursor.execute(UserQueries.INSERT_USER.value, (name, gender))
        new_user = self.convert_row_to_user(self.cursor.fetchone())
        self.conn.commit()
        return new_user

    def update_user_name(self, user_id: int, name: str) -> UserResponse | None:
        self.cursor.execute(UserQueries.UPDATE_USER.value, (name, user_id))
        self.conn.commit()
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: int) -> None:
        self.cursor.execute(UserQueries.DELETE_USER.value, (str(user_id),))
        self.conn.commit()
