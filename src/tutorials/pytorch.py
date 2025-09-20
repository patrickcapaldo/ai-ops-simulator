# src/tutorials/pytorch.py

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

TUTORIAL_CATEGORY = "PyTorch: Core Concepts"

TUTORIALS = {
    "pt_1_1": {
        "name": "Handling PyTorch Version Mismatches",
        "description": "Learn to debug PyTorch version mismatches and schedule jobs to compatible nodes.",
        "skills_learned": [
            "Debugging job failures (`debug`)",
            "Understanding node-specific software versions",
            "Scheduling jobs to specific, compatible nodes"
        ],
        "steps": [
            {
                "text": "Welcome to the PyTorch tutorial!\n\nPyTorch is a popular open-source machine learning framework based on the Torch library, used for applications such as computer vision and natural language processing. It is primarily developed by Facebook's AI Research lab (FAIR).\n\nThis tutorial will cover a common MLOps challenge: managing software versions.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "In a real-world environment, you might have different versions of software installed on different nodes in your cluster. This can lead to job failures if a job is scheduled on a node with an incompatible version.\n\nWe have a special job that requires an older PyTorch version. Type `ls-jobs`.",
                "expected_command": "ls-jobs",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''
game.create_node_trigger("node-0", 8, 2, 64, "2.0")
game.create_node_trigger("node-1", 8, 2, 64, "1.9") # Legacy node
game.create_job_trigger( JobType.PYTORCH_TRAINING, {"cpu": 2, "gpu": 1, "ram": 8}, game.time + 50, pytorch_version="1.9")
''')
            },
            {
                "text": "Notice the job requires PyTorch 1.9. Let's try to submit it to `node-0` which has version 2.0 and see what happens.\nType `submit <job_id> node-0`, replacing `<job_id>` with the actual ID shown from `ls-jobs`.",
                "expected_command": "submit",
                "is_dynamic": True,
                "doc_quote": "The `debug` command in this simulator provides a simplified view of an error log for a failed job, helping to diagnose issues like version mismatches or resource constraints."
            },
            {
                "text": "The submission failed. To diagnose the failure, you would normally use the `debug` command.\nType `debug <job_id>`, replacing `<job_id>` with the actual ID.",
                "expected_command": "debug",
                "is_dynamic": True
            },
            {
                "text": "The error, which you can also see by using the `debug` command, shows a version mismatch. Now check your cluster to find the right node. Type `status`.",
                "expected_command": "status"
            },
            {
                "text": "You can see `node-1` has the correct PyTorch version (1.9).\nNow, submit the job to the correct node: `submit <job_id> node-1`, replacing `<job_id>` with the actual ID.",
                "expected_command": "submit",
                "is_dynamic": True
            },
            {
                "type": "mcq",
                "text": "What is the best way to resolve a PyTorch version mismatch?",
                "answers": [
                    "a) Delete the job and create a new one.",
                    "b) Submit the job to a node with the correct PyTorch version.",
                    "c) Upgrade the PyTorch version on all nodes."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "Success! The job is running on a compatible node.\nThis concludes the versioning tutorial."
            }
        ]
    },
    "pt_1_2": {
        "name": "Basic Job Submission",
        "description": "Learn how to submit a basic PyTorch job to a node.",
        "skills_learned": [
            "Submitting a job to a node (`submit`)"
        ],
        "steps": [
            {
                "text": "Now that you understand versioning, let's try a basic job submission. You have a new PyTorch training job in the queue and a node available.\nType `ls-jobs` to see the job.",
                "expected_command": "ls-jobs",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''
game.create_job_trigger( JobType.PYTORCH_TRAINING, {"cpu": 4, "gpu": 1, "ram": 16}, game.time + 50, pytorch_version="2.0")
''')
            },
            {
                "text": "You see the new job. Now, submit it to `node-0`.\nType `submit <job_id> node-0`, replacing `<job_id>` with the actual ID shown from `ls-jobs`.",
                "expected_command": "submit",
                "is_dynamic": True,
                "doc_quote": "The `submit` command allows you to assign a pending job to an available node in the cluster, initiating its execution."
            },
            {
                "text": "The job is now running on `node-0`. You can check its status at any time.",
                "expected_command": "status"
            },
            {
                "text": "To see the job's progress, type `show-job <job_id>`.",
                "expected_command": "show-job",
                "is_dynamic": True,
                "doc_quote": "The `show-job` command provides detailed information about a specific job, including its type, status, resource requirements, and progress."
            },
            {
                "type": "mcq",
                "text": "What is the purpose of the `submit` command?",
                "answers": [
                    "a) To create a new job.",
                    "b) To assign a pending job to an available node.",
                    "c) To delete a job."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You can see the job's progress percentage. This is useful for monitoring long-running tasks.\nThis concludes the basic job submission tutorial."
            }
        ]
    }
}
