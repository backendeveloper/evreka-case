from app.core.config import Settings

def test_settings_load():
    settings = Settings()
    assert isinstance(settings.postgres_user, str)
    assert isinstance(settings.postgres_password, str)
    assert isinstance(settings.postgres_db, str)
    assert isinstance(settings.postgres_host, str)
    assert isinstance(settings.postgres_port, int)