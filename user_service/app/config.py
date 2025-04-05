from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_psycopg(self):
        print(self.DB_PORT)
        return (
            'postgresql+psycopg://'
            f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:'
            f'{self.DB_PORT}/{self.DB_NAME}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
