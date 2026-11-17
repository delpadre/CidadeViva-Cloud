import os
from flask import Flask, jsonify

# Telemetria para o Application Insights (só liga se houver a connection string).
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor

        configure_azure_monitor()
    except Exception as exc:  # o app nunca deve cair por causa da telemetria
        print(f"Telemetria desativada: {exc}")

app = Flask(__name__)


@app.get("/")
def home():
    return (
        "<h1>CitizenTech no Ar</h1>"
        "<p>MVP em construção. Pipeline CI/CD e infraestrutura funcionando.</p>"
        '<p><a href="/health">/health</a> · <a href="/erro">/erro</a> (gera falha para testar alerta)</p>'
    )


@app.get("/health")
def health():
    return jsonify(status="ok", version=os.getenv("APP_VERSION", "dev")), 200


@app.get("/erro")
def erro():
    # Usado só para provocar HTTP 500 e testar o alerta do Application Insights
    raise RuntimeError("Falha provocada de propósito para testar o alerta")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
