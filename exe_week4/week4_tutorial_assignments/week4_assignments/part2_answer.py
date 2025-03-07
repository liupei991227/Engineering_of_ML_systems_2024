
from kubernetes import client
from kserve import KServeClient
from kserve import constants
from kserve import V1beta1InferenceService
from kserve import V1beta1InferenceServiceSpec
from kserve import V1beta1PredictorSpec
from kserve import V1beta1ModelSpec
from kserve import V1beta1ModelFormat

def deploy_model(model_name: str, model_uri: str):
    """
    Args:
        model_name: the name of the deployed inference service
        model_uri: the S3 URI of the model saved in MLflow
    """
    
    namespace = "kserve-inference"
    service_account_name="kserve-sa"
    kserve_version="v1beta1"
    api_version = constants.KSERVE_GROUP + "/" + kserve_version
    
    print(f"MODEL URI: {model_uri}")
    
    modelspec = V1beta1ModelSpec(
        storage_uri=model_uri,
        model_format=V1beta1ModelFormat(name="mlflow"),
        protocol_version="v2"
    )
    
    isvc = V1beta1InferenceService(

        ### START CODE HERE
        api_version=api_version,
        kind="InferenceService",
        metadata=client.V1ObjectMeta(name=model_name, namespace=namespace),
        ### END CODE HERE

        spec=V1beta1InferenceServiceSpec(
            predictor=V1beta1PredictorSpec(
                ### START CODE HERE
                model=modelspec,
                service_account_name=service_account_name
                ### END CODE HERE
            )
        )
    )
    kserve = KServeClient()

    ### START CODE HERE
    # Check if the model is already deployed, if yes, update it; if no, create a new service
    try:
        existing_service = kserve.get(model_name, namespace=namespace)
        print(f"Service {model_name} already exists, updating...")
        kserve.patch(isvc)
    except Exception as e:
        print(f"Service {model_name} not found, creating a new one...")
        kserve.create(isvc, namespace=namespace)
    ### END CODE HERE
    
