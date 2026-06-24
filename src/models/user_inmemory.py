class UserManager:
    def __init__(self) -> None:
        self.users: list[dict[str, int | str]] = []
        self.user_count: int = 0

    def get_index_by_id(self, user_id: int) -> int | None:
        return next(
            (i for i, user in enumerate(self.users) if user["id"] == user_id), None
        )

    def does_user_exist(self, user_id: int) -> bool:
        return isinstance(self.get_index_by_id(user_id), int)

    def add_a_user(self, name: str, gender: str) -> dict[str, int | str]:
        self.user_count += 1
        user_record: dict[str, int | str] = {
            "id": self.user_count,
            "user": name,
            "gender": gender,
        }
        self.users.append(user_record)
        return self.users[-1]

    def get_all_users(self) -> list[dict[str, int | str]]:
        return self.users

    def get_user_by_id(self, user_id: int) -> dict[str, int | str] | None:
        index = self.get_index_by_id(user_id)
        if index is None:
            return None
        return self.users[index]

    def update_user_name(self, user_id: int, name: str) -> dict[str, int | str] | None:
        index = self.get_index_by_id(user_id)
        if index is None:
            return None
        self.users[index]["user"] = name
        return self.users[index]

    def delete_user(self, user_id: int) -> None:
        index = self.get_index_by_id(user_id)
        if index is not None:
            self.users.pop(index)
