from clinic.services.auth_service import AuthService


class FakeUser:
    def __init__(self, username, password_ok=True):
        self.username = username
        self.password_ok = password_ok

    def check_password(self, password):
        return self.password_ok and password == "clinic123"


class FakeRepo:
    def __init__(self, user=None):
        self.user = user

    def get_user_by_username(self, username):
        if self.user and self.user.username == username:
            return self.user
        return None


def test_login_returns_error_for_unknown_username():
    service = AuthService(FakeRepo())

    user, errors = service.login("unknown", "clinic123")

    assert user is None
    assert errors == ["The username could not be found."]


def test_login_returns_error_for_wrong_password():
    service = AuthService(FakeRepo(FakeUser("mert.kaya", password_ok=False)))

    user, errors = service.login("mert.kaya", "badpass")

    assert user is None
    assert errors == ["The password you entered is incorrect."]


def test_login_succeeds_with_valid_credentials():
    service = AuthService(FakeRepo(FakeUser("mert.kaya", password_ok=True)))

    user, errors = service.login("mert.kaya", "clinic123")

    assert user is not None
    assert errors == []
