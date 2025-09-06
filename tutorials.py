"""
Defines the content and structure for interactive tutorials.
"""

TUTORIALS = {
    "basics": {
        "name": "1. The Basics of Job Management",
        "skills_learned": [
            "Viewing pending jobs (`ls-jobs`)",
            "Checking cluster and node status (`status`)",
            "Understanding resource requirements (CPU, GPU, RAM)",
            "Submitting a job to a node (`submit`)",
            "Monitoring a running job"
        ],
        "steps": [
            {
                "text": "Welcome to the AI Ops Simulator! This tutorial will guide you through the basics.\nFirst, let's see what jobs are waiting in the queue. Type `ls-jobs` to continue.",
                "expected_command": "ls-jobs",
                "trigger": lambda game: game.setup_tutorial_state(jobs=1)
            },
            {
                "text": "Great! You see a list of pending jobs with their requirements.\nNow, let's check our cluster to see if we have a server (node) to run this job. Type `status`.",
                "expected_command": "status"
            },
            {
                "text": "Excellent. The status view shows your nodes and their available resources.\nIt looks like `node-0` has enough resources for our job. Let's assign the job to the node.\nType `submit <job_id> node-0`, replacing `<job_id>` with the ID from the `ls-jobs` list.",
                "expected_command": "submit",
                "is_dynamic": True  # Indicates the full command depends on game state
            },
            {
                "text": "Perfect! The job is now running. You can see it listed under the node in the `status` view.\nIn a real game, you'd wait for it to complete to earn points.\nThis concludes the basic tutorial!",
                "expected_command": None  # End of tutorial
            }
        ]
    },
    "scaling": {
        "name": "2. Scaling Your Cluster with Terraform",
        "skills_learned": [
            "Core Terraform Concepts: Providers, Resources, and State",
            "Core Workflow: `init`, `plan`, and `apply`",
            "Infrastructure as Code (IaC) for provisioning resources",
            "State Management and Collaboration: Remote backends and locking",
            "Security: Never hard-code secrets, use tools like Vault",
            "CI/CD Integration for automation"
        ],
        "steps": [
            {
                "text": "This tutorial covers scaling your infrastructure.\nWe have a lot of jobs in the queue, more than our current nodes can handle. Type `ls-jobs`.",
                "expected_command": "ls-jobs",
                "trigger": lambda game: game.setup_tutorial_state(jobs=5, nodes=1)
            },
            {
                "text": "See all those jobs? Our single node can't handle them all in time.\nWe need more servers. Let's preview the new resources we can create. Type `terraform plan`.",
                "expected_command": "terraform plan"
            },
            {
                "text": "The plan shows that we will create new nodes according to our configuration.\nNow, let's apply this plan to actually create the nodes. Type `terraform apply`.",
                "expected_command": "terraform apply"
            },
            {
                "text": "Success! The new nodes have been provisioned.\nVerify they are active and ready to take jobs. Type `status` to see your expanded cluster.",
                "expected_command": "status"
            },
            {
                "text": "Now you have enough resources to tackle the job queue!\nThis concludes the scaling tutorial.",
                "expected_command": None
            }
        ]
    }
}
