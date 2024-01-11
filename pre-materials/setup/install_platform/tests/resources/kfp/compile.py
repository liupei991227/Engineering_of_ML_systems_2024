from kfp import dsl, client
from kfp import compiler
import os 

@dsl.component(
    base_image="python:3.11",
    packages_to_install=["mlflow==2.9.2"],
)
def mlflow_train():
    import mlflow

    MLFLOW_TRACKING_URI = "http://mlflow.mlflow.svc.cluster.local:5000"
    MLFLOW_EXPERIMENT_NAME = "Kubeflow Pipeline test run"

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    experiment = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)

    if experiment is None:
        experiment_id = mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
    else:
        experiment_id = experiment.experiment_id

    with mlflow.start_run(experiment_id=experiment_id) as run:
        mlflow.log_param("my", "param")
        mlflow.log_metric("score", 100)


@dsl.pipeline()
def my_pipeline():
    mlflow_train()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    compiler.Compiler().compile(my_pipeline, package_path=os.path.join(dir_path, "pipeline.yaml"))
    # kfp_client = client.Client()
    # run = kfp_client.get_run(run_id='c5666ef8-ac1c-489e-a1f5-784adcff124e')
    # print(type(run))
    # print(run.to_dict()['state'])
