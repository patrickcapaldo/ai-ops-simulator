# src/tutorials/onnx.py

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

TUTORIAL_CATEGORY = "ONNX: Core Concepts"

TUTORIALS = {
    "onnx_1_1": {
        "name": "Optimizing with ONNX",
        "description": "Learn how to optimize models using ONNX, including conversion and resource efficiency.",
        "skills_learned": [
            "Model optimization workflow (`convert-onnx`)",
            "Resource efficiency of optimized models",
            "Checking job history for completed tasks"
        ],
        "steps": [
            {
                "text": "Welcome to the ONNX tutorial!\n\nONNX (Open Neural Network Exchange) is an open standard for representing machine learning models. It allows you to transfer models between different frameworks and tools.\n\nThis tutorial will show you how to optimize a PyTorch model by converting it to ONNX.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "First, we need a trained model. Let's submit a PyTorch training job. Type `submit <job_id> node-0`.",
                "expected_command": "submit <job_id> node-0",
                "is_dynamic": True,
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''
game.create_job_trigger( JobType.PYTORCH_TRAINING, {"cpu": 4, "gpu": 1, "ram": 16}, game.time + 50, pytorch_version="2.0")
''')
            },
            {
                "text": "The training job is running. For this tutorial, we'll instantly complete it.",
                "expected_command": "status",
                "trigger": lambda game: complete_job_trigger(game, list(game.cluster.values())[0].running_jobs[0].id if list(game.cluster.values()) else None)
            },
            {
                "text": "The training job is complete. Now, we can convert it to a more efficient ONNX model.\nType `convert-onnx <completed_job_id>`.",
                "expected_command": "convert-onnx",
                "is_dynamic": True,
                "doc_link": "https://pytorch.org/docs/stable/onnx.html",
                "doc_quote": "PyTorch models can be converted to the ONNX format using the `torch.onnx.export()` function."
            },
            {
                "text": "Excellent! A new, optimized ONNX job has been created with lower resource requirements.\nCheck the job queue to see it. Type `ls-jobs`.",
                "expected_command": "ls-jobs"
            },
            {
                "text": "Notice the ONNX job requires fewer resources (e.g., CPU: 4 -> 2, GPU: 1 -> 0, RAM: 16 -> 8). This makes it cheaper and easier to run. To see the resource difference, use `show-job` on the original PyTorch job (from the `completed-jobs` list) and then on the new ONNX job (from `ls-jobs`). Compare their CPU, GPU, and RAM requirements.",
                "expected_command": "show-job",
                "is_dynamic": True
            },
            {
                "type": "mcq",
                "text": "What is a key benefit of using ONNX?",
                "answers": [
                    "a) It makes models larger.",
                    "b) It allows models to be used across different frameworks and hardware.",
                    "c) It makes models slower."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You should observe that the ONNX job has significantly lower resource requirements, demonstrating the benefits of model optimization.\nThis concludes the ONNX tutorial."
            }
        ]
    },
    "onnx_1_2": {
        "name": "Submitting an ONNX Job",
        "description": "Learn how to submit an optimized ONNX job for inference.",
        "skills_learned": [
            "Submitting an optimized ONNX job",
            "Resource efficiency of optimized models"
        ],
        "steps": [
            {
                "text": "You've successfully converted a PyTorch model to ONNX. Now, let's submit this optimized job to a node. First, ensure you have a node available. Type `status`.",
                "expected_command": "status",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''
game.create_job_trigger( JobType.ONNX_INFERENCE, {"cpu": 2, "gpu": 0, "ram": 8}, game.time + 50)
''')
            },
            {
                "text": "Now, submit the ONNX job to `node-0`. Type `submit <onnx_job_id> node-0`.",
                "expected_command": "submit",
                "is_dynamic": True,
                "doc_quote": "Submitting an ONNX job involves assigning the optimized model to a compatible node for efficient inference, leveraging its reduced resource footprint."
            },
            {
                "type": "mcq",
                "text": "Where can ONNX models be run?",
                "answers": [
                    "a) Only on PyTorch.",
                    "b) On a variety of frameworks and hardware.",
                    "c) Only on TPUs."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "The optimized ONNX job is now running. You've completed the ONNX workflow!\nThis concludes the ONNX job submission tutorial."
            }
        ]
    }
}
