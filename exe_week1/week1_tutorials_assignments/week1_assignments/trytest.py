import mlflow

# 获取当前运行的信息
run_info = mlflow.active_run()
print("Current run ID:", run_info.info.run_id)
