from ..routers.users import get_db
from ..routers.auth import get_current_user
from fastapi import status
from .utils import (
    app,
    override_get_current_user,
    override_get_db,
    client,
    test_todo,  # noqa: F401,
    test_user  # noqa: F401
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):  # noqa: F811
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == 'testuser@email.com'
    assert response.json()['first_name'] == 'Test'
    assert response.json()['last_name'] == 'User'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'


def test_change_password_success(test_user):  # noqa: F811
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):  # noqa: F811
    response = client.put("/user/password", json={"password": "wrong_password", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT