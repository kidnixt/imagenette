# upload_model.py
import wandb, os
file_path = "cnn_baseline_bestparams.pth"
print("Exists:", os.path.exists(file_path), "Size MB:", os.path.getsize(file_path)/1_000_000)

run = wandb.init(project="imagenette", job_type="manual-upload")
artifact = wandb.Artifact(name="best-model-9mrxi4y8", type="model", description="Upload manual")
artifact.add_file(file_path)
print("Added file to artifact, logging...")
run.log_artifact(artifact)
print("Logged artifact, finishing run...")
run.finish()
print("Done.")
