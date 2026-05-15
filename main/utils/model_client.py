import os
from typing import AsyncIterator, Optional

from agents import Model, OpenAIChatCompletionsModel
from agents.agent_output import AgentOutputSchemaBase
from agents.handoffs import Handoff
from agents.items import ModelResponse, TResponseInputItem, TResponseStreamEvent
from agents.model_settings import ModelSettings
from agents.models.interface import ModelTracing
from agents.tool import Tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.responses.response_prompt_param import ResponsePromptParam

load_dotenv(override=True)

OPENCODE_GO_OPENAI_BASE_URL = "https://opencode.ai/zen/go/v1"
OPENCODE_GO_ANTHROPIC_BASE_URL = "https://opencode.ai/zen/go"

DEFAULT_OPENROUTER_MODEL = "xiaomi/mimo-v2-flash"
DEFAULT_OPENCODE_GO_MODEL = "deepseek-v4-flash"


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _strip_known_prefix(model: str, prefixes: tuple[str, ...]) -> str:
    for prefix in prefixes:
        if model.startswith(prefix):
            return model.removeprefix(prefix)
    return model


def using_openrouter() -> bool:
    return _env_bool("USE_OPENROUTER", default=True)


def openrouter_model_id(model: Optional[str] = None) -> str:
    model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)
    return _strip_known_prefix(model, ("litellm/openrouter/", "openrouter/"))


def opencode_go_model_id(model: Optional[str] = None) -> str:
    model = model or os.getenv("OPENCODE_GO_MODEL", DEFAULT_OPENCODE_GO_MODEL)
    return _strip_known_prefix(model, ("opencode-go/", "openai/", "anthropic/"))


def opencode_go_uses_anthropic_endpoint(model: Optional[str] = None) -> bool:
    model = opencode_go_model_id(model)
    return model.startswith("minimax-")


def provider_display_name(model: Optional[str] = None) -> str:
    if using_openrouter():
        return os.getenv("OPENROUTER_MODEL_SHORT_NAME") or openrouter_model_id(model)
    return os.getenv("OPENCODE_GO_MODEL_SHORT_NAME") or f"OpenCode Go {opencode_go_model_id(model)}"


def configured_model_names() -> list[Model | str]:
    if using_openrouter():
        model = f"litellm/openrouter/{openrouter_model_id()}"
        return [model] * 4
    return [OpenCodeGoAutoModel(model=opencode_go_model_id()) for _ in range(4)]


def configured_model_display_names() -> list[str]:
    return [provider_display_name()] * 4


class OpenCodeGoAutoModel(Model):
    _protocol_cache: dict[str, str] = {}

    def __init__(self, *, model: str, api_style: Optional[str] = None) -> None:
        self.model = opencode_go_model_id(model)
        self._api_style = (api_style or os.getenv("OPENCODE_GO_API_STYLE", "auto")).strip().lower()
        if self._api_style not in {"auto", "openai", "anthropic"}:
            raise ValueError("OPENCODE_GO_API_STYLE must be auto, openai, or anthropic")

        api_key = _env_required("OPENCODE_GO_API_KEY")
        openai_client = AsyncOpenAI(api_key=api_key, base_url=OPENCODE_GO_OPENAI_BASE_URL)
        self._openai_model = OpenAIChatCompletionsModel(
            model=self.model,
            openai_client=openai_client,
        )
        self._anthropic_model = LitellmModel(
            model=f"anthropic/{self.model}",
            base_url=OPENCODE_GO_ANTHROPIC_BASE_URL,
            api_key=api_key,
        )
        self._active_protocol = self._initial_protocol()

    def _initial_protocol(self) -> str:
        if self._api_style != "auto":
            return self._api_style
        if self.model in self._protocol_cache:
            return self._protocol_cache[self.model]
        if opencode_go_uses_anthropic_endpoint(self.model):
            return "anthropic"
        return "openai"

    def _client_for(self, protocol: str) -> Model:
        return self._anthropic_model if protocol == "anthropic" else self._openai_model

    def _alternate_protocol(self) -> str:
        return "anthropic" if self._active_protocol == "openai" else "openai"

    async def get_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
        tools: list[Tool],
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff],
        tracing: ModelTracing,
        *,
        previous_response_id: str | None,
        conversation_id: str | None,
        prompt: ResponsePromptParam | None,
    ) -> ModelResponse:
        try:
            response = await self._client_for(self._active_protocol).get_response(
                system_instructions,
                input,
                model_settings,
                tools,
                output_schema,
                handoffs,
                tracing,
                previous_response_id=previous_response_id,
                conversation_id=conversation_id,
                prompt=prompt,
            )
            self._protocol_cache[self.model] = self._active_protocol
            return response
        except Exception as first_error:
            if self._api_style != "auto":
                raise
            first_protocol = self._active_protocol
            self._active_protocol = self._alternate_protocol()
            try:
                response = await self._client_for(self._active_protocol).get_response(
                    system_instructions,
                    input,
                    model_settings,
                    tools,
                    output_schema,
                    handoffs,
                    tracing,
                    previous_response_id=previous_response_id,
                    conversation_id=conversation_id,
                    prompt=prompt,
                )
                self._protocol_cache[self.model] = self._active_protocol
                return response
            except Exception as second_error:
                raise RuntimeError(
                    f"OpenCode Go model '{self.model}' failed with both "
                    f"{first_protocol} and {self._active_protocol} API styles. "
                    f"First error: {first_error}"
                ) from second_error

    def stream_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
        tools: list[Tool],
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff],
        tracing: ModelTracing,
        *,
        previous_response_id: str | None,
        conversation_id: str | None,
        prompt: ResponsePromptParam | None,
    ) -> AsyncIterator[TResponseStreamEvent]:
        return self._client_for(self._active_protocol).stream_response(
            system_instructions,
            input,
            model_settings,
            tools,
            output_schema,
            handoffs,
            tracing,
            previous_response_id=previous_response_id,
            conversation_id=conversation_id,
            prompt=prompt,
        )
