# src/tutorials/terraform_core.py

import re

TUTORIAL_CATEGORY = "Terraform: Core Workflow"

TUTORIALS = {
    "tf_1_1": {
        "name": "Your First Resource (terraform apply)",
        "description": "Learn the basic Terraform workflow: init, plan, apply.",
        "skills_learned": [
            "Understanding `terraform apply` to provision resources",
            "Concept of a Terraform resource"
        ],
        "steps": [
            {
                "text": "Welcome to the Terraform tutorials!\n\nTerraform is an Infrastructure as Code (IaC) tool that allows you to build, change, and version infrastructure safely and efficiently. Instead of manually configuring servers and services, you define your infrastructure in configuration files.\n\nThis tutorial will introduce you to the basic Terraform workflow.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "The core of Terraform is the configuration file. These files describe the components needed to run a single application or your entire datacenter. In this simulation, we have a simple configuration that defines a single node.\n\nTo apply the configuration and create the node, use the `terraform apply` command.",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
            },
            {
                "text": "Excellent! You've just used `terraform apply` to create a node. This command executes the changes defined in your configuration.\nType `status` to see your new node.",
                "expected_command": "status",
                "doc_link": "https://www.terraform.io/cli/commands/apply",
                "doc_quote": "The `terraform apply` command is used to execute the actions proposed in a Terraform plan."
            },
            {
                "type": "mcq",
                "text": "What does the `terraform apply` command do?",
                "answers": [
                    "a) It previews the changes to be made.",
                    "b) It destroys all existing infrastructure.",
                    "c) It creates or updates infrastructure to match the configuration."
                ],
                "correct_answer": "c",
                "final_step": True,
                "final_message": "You've successfully provisioned your first resource!\nThis concludes the first tutorial."
            }
        ]
    },
    "tf_1_2": {
        "name": "Planning Your Changes (terraform plan)",
        "description": "Learn how to manage Terraform state and destroy resources.",
        "skills_learned": [
            "Understanding `terraform plan` to preview changes",
            "Reading plan output (create, update, destroy)",
            "The `plan -> apply` workflow"
        ],
        "steps": [
            {
                "text": "In the last tutorial, you used `terraform apply` to immediately create infrastructure. In a real-world scenario, you'll want to preview the changes before you apply them. This is where `terraform plan` comes in.\n\nYour configuration has been updated to specify 3 nodes. Type `terraform plan` to see what changes Terraform intends to make.",
                "expected_command": "terraform plan",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''
global TERRAFORM_CONFIG
TERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 3', TERRAFORM_CONFIG)
''')
            },
            {
                "text": "Notice Terraform plans to create 2 new nodes. This is a 'dry run' that shows the execution plan without making any changes.\nNow, apply these changes. Type `terraform apply`.",
                "expected_command": "terraform apply",
                "doc_link": "https://www.terraform.io/cli/commands/plan",
                "doc_quote": "The `terraform plan` command creates an execution plan, which lets you preview the changes that Terraform plans to make to your infrastructure."
            },
            {
                "text": "Great! You've successfully planned and applied changes.\nType `status` to confirm you now have 3 nodes.",
                "expected_command": "status"
            },
            {
                "type": "mcq",
                "text": "What is the purpose of `terraform plan`?",
                "answers": [
                    "a) To create a new configuration file.",
                    "b) To preview the changes that will be made to the infrastructure.",
                    "c) To immediately apply changes to the infrastructure."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You've mastered planning and applying changes!\nThis concludes the planning tutorial."
            }
        ]
    },
    "tf_1_3": {
        "name": "Destroying Resources (terraform destroy)",
        "description": "Learn how to destroy resources using `terraform destroy`.",
        "skills_learned": [
            "Using `terraform destroy` to remove resources",
            "Understanding resource lifecycle",
            "Cost management implications of idle resources"
        ],
        "steps": [
            {
                "text": "Just as you can create infrastructure, you can also destroy it. This is an important part of the resource lifecycle and is crucial for managing costs.\n\nYou currently have 3 nodes, but no jobs. Let's remove one of the nodes to save costs. Type `terraform destroy node-0`.\n\n**Note:** In real Terraform, `terraform destroy` would remove all resources defined in the configuration. In this simulator, you can destroy a single node for learning purposes.",
                "expected_command": "terraform destroy node-0",
                "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=3)"
            },
            {
                "text": "You've successfully destroyed `node-0`. This command terminates resources managed by Terraform.\nType `status` to confirm you now have 2 nodes.",
                "expected_command": "status",
                "doc_link": "https://www.terraform.io/cli/commands/destroy",
                "doc_quote": "The `terraform destroy` command deprovisions all objects managed by a Terraform configuration."
            },
            {
                "type": "mcq",
                "text": "When would you use `terraform destroy`?",
                "answers": [
                    "a) To update existing resources.",
                    "b) To remove resources that are no longer needed.",
                    "c) To create new resources."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You've learned to destroy resources!\nThis concludes the destroy tutorial."
            }
        ]
    },
    "tf_1_4": {
        "name": "Initializing a Working Directory (terraform init)",
        "description": "Understand the purpose of `terraform init`.",
        "skills_learned": [
            "Understanding `terraform init`",
            "Initializing a Terraform working directory"
        ],
        "steps": [
            {
                "text": "Before you can run any other Terraform commands, you need to initialize your working directory. This command performs several different initialization steps in order to prepare the current working directory for use with Terraform.\n\nType `terraform init`.",
                "expected_command": "terraform init",
                "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=0, clear_terraform_config=True)"
            },
            {
                "type": "mcq",
                "text": "What is the main purpose of `terraform init`?",
                "answers": [
                    "a) To apply the configuration.",
                    "b) To download necessary providers and modules.",
                    "c) To destroy the infrastructure."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "Terraform has successfully initialized the directory. You're now ready to apply configurations.\nThis concludes the initialization tutorial."
            }
        ]
    },
    "tf_1_5": {
        "name": "Validating Your Configuration (terraform validate)",
        "description": "Learn how to validate Terraform configurations.",
        "skills_learned": [
            "Understanding `terraform validate`",
            "Checking configuration syntax and consistency"
        ],
        "steps": [
            {
                "text": "After making changes to your Terraform configuration, it's good practice to validate it to catch syntax errors or inconsistencies before planning or applying. The `terraform validate` command is a great way to do this.\n\nType `terraform validate`.",
                "expected_command": "terraform validate",
                "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=0)"
            },
            {
                "type": "mcq",
                "text": "What does `terraform validate` check for?",
                "answers": [
                    "a) It checks for security vulnerabilities.",
                    "b) It checks for syntax errors and internal consistency.",
                    "c) It checks for cost optimizations."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "Terraform has validated the configuration. If there were any errors, they would be displayed here. This helps ensure your configuration is syntactically correct and internally consistent.\nThis concludes the validation tutorial."
            }
        ]
    },
    "tf_1_6": {
        "name": "Formatting Your Configuration (terraform fmt)",
        "description": "Learn how to format Terraform configurations using `terraform fmt`.",
        "skills_learned": [
            "Using `terraform fmt`",
            "Maintaining consistent code style"
        ],
        "steps": [
            {
                "text": "Consistent formatting improves readability and maintainability of your Terraform configurations. Terraform has a built-in command to automatically format your files.\n\nLet's introduce a formatting error and then fix it. Type `terraform apply` to create a node, then we'll mess up the config.",
                "expected_command": "terraform apply",
                "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\n    global TERRAFORM_CONFIG\n    TERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 1', TERRAFORM_CONFIG)\n''')"
            },
            {
                "text": "Now, let's intentionally mess up the formatting of your Terraform configuration. Type `edit-terraform-config` and remove some indentation or add extra spaces.",
                "expected_command": "edit-terraform-config"
            },
            {
                "text": "Your configuration is now poorly formatted. To automatically fix this, type `terraform fmt`.",
                "expected_command": "terraform fmt",
                "doc_link": "https://www.terraform.io/cli/commands/fmt",
                "doc_quote": "The `terraform fmt` command formats Terraform configuration file contents so that it matches the canonical format and style. This command applies a subset of the Terraform language style conventions, along with other minor adjustments for readability."
            },
            {
                "type": "mcq",
                "text": "What is the purpose of `terraform fmt`?",
                "answers": [
                    "a) To fix semantic errors in the configuration.",
                    "b) To apply the configuration.",
                    "c) To rewrite configuration files to a canonical format and style."
                ],
                "correct_answer": "c",
                "final_step": True,
                "final_message": "Terraform has automatically reformatted your configuration. You can type `edit-terraform-config` again to see the changes, or just proceed.\nThis concludes the formatting tutorial."
            }
        ]
    }
}
