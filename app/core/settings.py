from pathlib import Path
from pyrogram import Client
from app.gpt.controller import GPTController
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath


class EnvSettings(BaseSettings):
    root_dir: DirectoryPath = Path(__file__).parent.parent.parent
    model_config = SettingsConfigDict(
        env_file=f'{root_dir}/.env',
        env_file_encoding='utf-8',
    )

    api_id : str
    app_name : str
    api_hash : str
    session_string : str
    device_model : str
    system_version : str
    app_version : str
    system_lang_code : str
    lang_code : str
    bot_token : str
    api_key : str
    trigger_words : list
    gpt_model : str
    chats_input : list
    chats_output : list
    prompt : str

class AppSettings(EnvSettings):
    @property
    def get_client(self):
        return Client(name=self.app_name,
             api_hash=self.api_hash,
             api_id=self.api_id,
             device_model=self.device_model,
             system_version=self.system_version,
             app_version=self.app_version,
             lang_code=self.lang_code,
             in_memory=True,
             session_string=self.session_string)

class GPTSettings(EnvSettings):
    @property
    def get_gpt(self):
        return GPTController(
            api_key=self.api_key,
            trigger_words=self.trigger_words,
            gpt_model= self.gpt_model)

class Settings:
    env: EnvSettings = EnvSettings()
    app : AppSettings = AppSettings()
    gpt : GPTSettings = GPTSettings()

def get_settings() -> Settings:
    return Settings()


print(get_settings().env.gpt_model)


