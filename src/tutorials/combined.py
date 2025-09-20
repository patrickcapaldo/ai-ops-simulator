# src/tutorials/combined.py

from src.tutorial_manager import JobType

def complete_job_trigger(game, job_id):
    """A trigger function to mark a specific job as complete for a tutorial step."""
    job = game.get_job(job_id)
    if job:
        # Find the node the job is running on
        node = None
        for n in game.cluster.values():
            if job in n.running_jobs:
                node = n
                break
        if node:
            game.complete_job(job, node)

TUTORIAL_CATEGORY = "Model Workflows: Combined"

TUTORIALS = {
    "combined_1_1": {
        "name": "End-to-End Model Workflow",
        "description": "Learn an end-to-end model workflow, from PyTorch training to ONNX optimization and inference.",
        "skills_learned": [
            "Combining PyTorch job execution and ONNX optimization",
            "Full lifecycle of a model from training to optimized inference"
        ],
        "steps": [
            {
                "text": "This tutorial combines previous concepts. We'll go through a full model workflow, from training a model in PyTorch to optimizing it with ONNX and deploying it for inference.\n\nFirst, submit the PyTorch training job. Type `submit <job_id> node-0`.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "The training job is running. For this tutorial, we'll instantly complete it.",
                "expected_command": "status",
                "trigger": lambda game: complete_job_trigger(game, list(game.cluster.values())[0].running_jobs[0].id if list(game.cluster.values()) else None)
            },
            {
                "text": "Training complete. Now, convert it to ONNX. Type `convert-onnx <completed_job_id>`.",
                "expected_command": "convert-onnx",
                "is_dynamic": True,
                "doc_quote": "The `convert-onnx` command simulates the process of converting a trained PyTorch model into the ONNX format, enabling cross-platform deployment and optimization."
            },
            {
                "text": "ONNX model created. Now, submit the optimized ONNX job. Type `submit <onnx_job_id> node-0`.",
                "expected_command": "submit",
                "is_dynamic": True,
                "doc_quote": "This step demonstrates the final stage of the model workflow, where the optimized ONNX model is deployed for inference, showcasing the efficiency gains from the conversion."
            },
            {
                "type": "mcq",
                "text": "What is the correct order of operations in this MLOps workflow?",
                "answers": [
                    "a) Train in PyTorch, convert to ONNX, deploy ONNX model.",
                    "b) Convert to ONNX, train in PyTorch, deploy ONNX model.",
                    "c) Deploy ONNX model, train in PyTorch, convert to ONNX."
                ],
                "correct_answer": "a",
                "final_step": True,
                "final_message": "The optimized job is running. This simulates the common real-world pipeline: training in PyTorch, converting to ONNX, then deploying for efficient inference.\nThis concludes the end-to-end workflow tutorial!"
            }
        ]
    }
}
