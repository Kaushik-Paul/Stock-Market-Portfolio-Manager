RUN_EVERY_N_SECONDS = 60
RUN_EVEN_WHEN_MARKET_IS_CLOSED = True
USE_MANY_MODELS = False

MANY_MODELS_NAMES = [
    "litellm/openrouter/meituan/longcat-flash-chat:free",
    "litellm/openrouter/deepseek/deepseek-chat-v3.1:free",
    "litellm/openrouter/alibaba/tongyi-deepresearch-30b-a3b:free",
    "litellm/openrouter/x-ai/grok-4-fast:free",
]

MANY_MODELS_SHORT_NAMES = [
"Longcat", "Deepseek", "Tongyi", "Grok 4 Fast"
]

DEFAULT_MODEL_NAME = "litellm/openrouter/x-ai/grok-4-fast:free"
DEFAULT_MODEL_SHORT_NAME = "Grok 4 Fast"