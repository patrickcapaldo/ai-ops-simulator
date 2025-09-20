# src/tutorials/kubernetes.py

TUTORIAL_CATEGORY = "Kubernetes: Core Concepts"

TUTORIALS = {
    "k8s_1_1": {
        "name": "Deploying a Pod",
        "description": "Learn how to deploy a basic Pod in Kubernetes.",
        "skills_learned": [
            "Understanding Kubernetes Pods",
            "Basic deployment commands"
        ],
        "steps": [
            {
                "text": "Welcome to the Kubernetes tutorial!\n\nKubernetes (often abbreviated as K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It was originally designed by Google and is now maintained by the Cloud Native Computing Foundation.\n\nAt its core, Kubernetes helps you manage applications built from multiple containers, ensuring they run reliably across a cluster of machines.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "The smallest and simplest unit in the Kubernetes object model that you create or deploy is a **Pod**. A Pod represents a single instance of a running process in your cluster and can contain one or more containers.\n\nWe will now deploy a simple pod. In a real environment, you would define the pod in a YAML file. For this simulation, we'll use a simplified command.\n\nType `kubectl apply -f my-pod.yaml` to simulate deploying a Pod.",
                "expected_command": "kubectl apply -f my-pod.yaml",
                "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=0)"
            },
            {
                "text": "Great! You've simulated deploying a Pod. To see the status of your pods, you can use the `get pods` command.\n\nType `kubectl get pods` to see your newly created pod.",
                "expected_command": "kubectl get pods"
            },
            {
                "type": "mcq",
                "text": "What is the smallest deployable unit in Kubernetes?",
                "answers": [
                    "a) A Node",
                    "b) A Pod",
                    "c) A Service"
                ],
                "correct_answer": "b",
                                    "final_step": True,                "final_message": "You have successfully deployed a pod and understand the basic concepts of Kubernetes!"
            }
        ]
    }
}
