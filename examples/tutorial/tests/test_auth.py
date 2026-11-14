import pytest
from flask import g
from flask import session

from flaskr.db import get_db


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/auth/register").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/auth/register", data={"username": "a", "password": "password123"})
    assert response.headers["Location"] == "/auth/login"

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM user WHERE username = 'a'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "password123", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/auth/login").status_code == 200

    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers["Location"] == "/"

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Incorrect username."), ("test", "a", b"Incorrect password.")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session

# Permet executar el mateix test amb diferents dades.
@pytest.mark.parametrize(
    # Definim les dades que utilitzarem en cada prova.
    ("username", "password", "valid"),
    (
        # Prova amb 7 caràcters: no ha de ser acceptada.
        ("user7", "abc1234", False),
        # Prova amb 8 caràcters: ha de ser acceptada.
        ("user8", "abc12345", True),
        # Prova amb 9 caràcters: ha de ser acceptada.
        ("user9", "abc123456", True),
    ),
)
# Funció que comprova si la contrasenya té la longitud correcta.
def test_register_password_length(client, username, password, valid):
    # Enviem les dades del registre com si fos un usuari.
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )

    # Si la contrasenya és correcta, ens ha de portar a la pàgina d'inici de sessió.
    if valid:
        assert response.headers["Location"] == "/auth/login"
    # Si no és correcta, ha de mostrar un missatge d'error.
    else:
        assert b"Password must be at least 8 characters long." in response.data

