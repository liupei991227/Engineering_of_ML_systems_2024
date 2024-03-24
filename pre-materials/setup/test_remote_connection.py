import requests


def test_connection():
    for url in [
        "kserve-gateway.local",
        "ml-pipeline-ui.local",
        "mlflow-server.local",
        "mlflow-minio-ui.local",
        "mlflow-minio.local",
        "prometheus-server.local",
        "grafana-server.local",
        "evidently-monitor-ui.local",
    ]:
        try:
            requests.get(f"http://{url}")
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")
            raise e
