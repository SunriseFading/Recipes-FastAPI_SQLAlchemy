from app.settings import JWTSettings, Settings

jwt_settings = JWTSettings(_env_file=".env")
settings = Settings(_env_file=".env")
