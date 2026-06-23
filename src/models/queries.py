from enum import Enum

class UserQueries(str, Enum):
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(100) NOT NULL,
        gender VARCHAR(20) NOT NULL
    );
    """

    INSERT_USER = """
    INSERT INTO users (user_name, gender)
    VALUES (%s, %s)
    RETURNING *;
    """

    GET_ALL_USERS = """
    SELECT id, user_name, gender
    FROM users;
    """

    GET_USER_BY_ID = """
    SELECT id, user_name, gender
    FROM users
    WHERE id = %s;
    """

    UPDATE_USER = """
    UPDATE users
    SET user_name = %s
    WHERE id = %s;
    """

    DELETE_USER = """
    DELETE FROM users
    WHERE id = %s;
    """

    USER_EXISTS = """
    SELECT EXISTS(
        SELECT 1
        FROM users
        WHERE id = %s
    );
    """