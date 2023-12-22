import os
from dotenv import load_dotenv

load_dotenv()


class WebhookConfig:
    PROJECT_NAME: str = "repeater-v3"
    APP_NAME: str = "apigateway-interceptor"
    APP_NAMESPACE: str = os.getenv("APP_NAMESPACE", "staging")
    CE_TYPE: str = (
        f"dev.knative.{APP_NAMESPACE}.cloudevent/{PROJECT_NAME}/message-relay"
    )
    CE_SOURCE: str = f"dev.knative.{APP_NAMESPACE}/{PROJECT_NAME}/{APP_NAME}"
