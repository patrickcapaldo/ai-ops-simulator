# src/tutorials/kubeflow.py

TUTORIAL_CATEGORY = "Kubeflow: MLOps Workflows"

TUTORIALS = {
    "kf_1_1": {
        "name": "Running a Kubeflow Pipeline",
        "description": "Learn how to run a basic Kubeflow pipeline.",
        "skills_learned": [
            "Introduction to Kubeflow Pipelines",
            "Executing a simple ML workflow"
        ],
        "steps": [
            {
                "text": "Welcome to the Kubeflow tutorial!\n\nKubeflow is a free and open-source machine learning platform that enables you to use ML pipelines in Kubernetes. It provides a set of tools and frameworks to build, deploy, and manage ML workflows from end to end.\n\nIn short, Kubeflow is the ML toolkit for Kubernetes.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "A key feature of Kubeflow is **Pipelines**, which are a platform for building and deploying scalable and portable ML workflows. A pipeline is a description of an ML workflow, including all of the components in the workflow and how they combine in the form of a graph.\n\nFirst, let's simulate deploying Kubeflow itself.\n\nType `kfctl apply -V -f kubeflow_v1.2.yaml` to continue.",
                "expected_command": "kfctl apply -V -f kubeflow_v1.2.yaml",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
            },
            {
                "text": "Now that Kubeflow is 'deployed', let's run a pipeline. In a real scenario, you would define your pipeline in a Python file, compile it, and then upload it to the Kubeflow UI. Here, we'll just simulate running a pre-built pipeline.\n\nType `kfp run submit my-pipeline.yaml` to simulate running a pipeline.",
                "expected_command": "kfp run submit my-pipeline.yaml"
            },
            {
                "text": "You've simulated running a Kubeflow pipeline! To check its status, you would use `kfp run list`.\nType `kfp run list`.",
                "expected_command": "kfp run list"
            },
            {
                "type": "mcq",
                "text": "What is a Kubeflow Pipeline?",
                "answers": [
                    "a) A tool for monitoring Kubernetes clusters",
                    "b) A description of an ML workflow as a graph of components",
                    "c) A type of machine learning model"
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You've successfully simulated running a Kubeflow pipeline and have a basic understanding of what Kubeflow is!"
            }
        ]
    }
}
