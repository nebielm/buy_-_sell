from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowPassword as OAuthFlowPasswordModel

OAUTH2_PASSWORD_FLOW = OAuthFlowsModel(
    password=OAuthFlowPasswordModel(
        tokenUrl="/token",
        scopes={}
    )
)

OPENAPI_SCHEMA = {
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": OAUTH2_PASSWORD_FLOW
            }
        }
    },
    "security": [
        {"OAuth2PasswordBearer": []}
    ]
}
