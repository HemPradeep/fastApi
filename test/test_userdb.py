from unittest.mock import Mock

from src.models.queries import UserQueries
from src.models.user_db import UserRepository


def build_repository() -> tuple[Mock, Mock, UserRepository]:
    conn = Mock()
    cursor = Mock()
    conn.cursor.return_value = cursor
    repo = UserRepository(conn)
    return conn, cursor, repo


def test_create_table_initializes_schema_and_commits() -> None:
    conn, cursor, _ = build_repository()

    cursor.execute.assert_called_once_with(UserQueries.CREATE_TABLE.value)
    conn.commit.assert_called_once()


def test_convert_row_to_user_returns_none_for_empty_row() -> None:
    _, _, repo = build_repository()

    assert repo.convert_row_to_user(None) is None


def test_convert_row_to_user_converts_row_to_dict() -> None:
    _, _, repo = build_repository()

    row = (1, "Alice", "Female")

    response = repo.convert_row_to_user(row)
    assert response is not None
    assert response.id == 1
    assert response.user_name == "Alice"
    assert response.gender == "Female"


def test_get_all_users_executes_query_and_returns_users() -> None:
    conn, cursor, repo = build_repository()
    cursor.fetchall.return_value = [(1, "Alice", "Female")]

    users = repo.get_all_users()

    assert cursor.execute.call_args_list[1] == ((UserQueries.GET_ALL_USERS.value,),)
    cursor.fetchall.assert_called_once()
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].user_name == "Alice"
    assert users[0].gender == "Female"
    assert conn.commit.call_count == 1


def test_get_user_by_id_returns_matching_user() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = (2, "Bob", "Male")

    user = repo.get_user_by_id(2)

    assert cursor.execute.call_args_list[1] == (
        (UserQueries.GET_USER_BY_ID.value, (2,)),
    )
    assert user is not None
    assert user.id == 2
    assert user.user_name == "Bob"
    assert user.gender == "Male"


def test_does_user_exist_returns_boolean_result() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = (True,)

    assert repo.does_user_exist(3) is True
    assert cursor.execute.call_args_list[1] == ((UserQueries.USER_EXISTS.value, (3,)),)


def test_add_a_user_inserts_and_returns_new_user() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = (4, "Dana", "Other")

    user = repo.add_a_user("Dana", "Other")

    assert cursor.execute.call_args_list[1] == (
        (UserQueries.INSERT_USER.value, ("Dana", "Other")),
    )
    assert user is not None
    assert user.id == 4
    assert user.user_name == "Dana"
    assert user.gender == "Other"


def test_update_user_name_updates_and_returns_user() -> None:
    _, cursor, repo = build_repository()
    cursor.fetchone.return_value = (5, "Diana", "Female")

    user = repo.update_user_name(5, "Diana")

    assert cursor.execute.call_args_list[1] == (
        (UserQueries.UPDATE_USER.value, ("Diana", 5)),
    )
    assert user is not None
    assert user.id == 5
    assert user.user_name == "Diana"
    assert user.gender == "Female"


def test_delete_user_executes_delete_query() -> None:
    _, cursor, repo = build_repository()

    repo.delete_user(7)

    assert cursor.execute.call_args_list[1] == (
        (UserQueries.DELETE_USER.value, ("7",)),
    )
