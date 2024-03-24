import subprocess
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_evidently():
    # Just simple test if the Evidently service is running
    with subprocess.Popen(["kubectl", "-n", "monitoring", "port-forward", "svc/evidently-service", "8000:8000"], stdout=True) as proc:
        try:
            time.sleep(2)  # give some time to the port-forward connection
            res = requests.get("http://localhost:8000/api/version")
            assert res.status_code == 200
            version_info = res.json()
            assert version_info.get("application") != None and version_info.get("version", None) != None
        except Exception as e:
            logger.error(f"ERROR: {e}")
            raise e
        finally:
            proc.terminate()