import os

from agents import Model, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)


def _env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def active_model_name() -> str:
    return _env_required("MODEL")


def create_agent_model() -> Model:
    client = AsyncOpenAI(
        base_url=_env_required("BASE_URL"),
        api_key=_env_required("API_KEY"),
    )
    return OpenAIChatCompletionsModel(
        model=active_model_name(),
        openai_client=client,
    )


def configured_model_names() -> list[Model]:
    model = create_agent_model()
    return [model] * 4


def configured_model_display_names() -> list[str]:
    return [active_model_name()] * 4
