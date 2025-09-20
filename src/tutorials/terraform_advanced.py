# src/tutorials/terraform_advanced.py

import re

TUTORIAL_CATEGORY = "Terraform: Advanced Management"

TUTORIALS = {
    "tf_2_1": {
        "name": "Targeting Specific Resources (`-target`)",
        "description": "Learn how to use the `-target` flag for granular control over Terraform applies.",
        "skills_learned": [
            "Using the `-target` flag for granular control",
            "Applying changes to a subset of resources"
        ],
        "steps": [
            {
                "text": "Sometimes you need to apply changes to only a specific resource. Your configuration has been updated to give all nodes more RAM, but you only want to upgrade `node-0`.\nType `terraform apply -target=node-0`.",
                "expected_command": "terraform apply -target=node-0",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2, custom_setup='''\nglobal TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'ram = \\d+', 'ram = 128', TERRAFORM_CONFIG)\n''')
            },
            {
                "text": "You've successfully targeted `node-0` for an update. The `-target` flag directs Terraform's operations to a specific subset of resources.\nType `status` to confirm only `node-0` has 128GB RAM.",
                "expected_command": "status",
                "doc_link": "https://www.terraform.io/cli/commands/apply#target-a-specific-resource",
                "doc_quote": "The `-target` option can be used to focus Terraform's attention on only a subset of the resources in a configuration.",
                "final_step": True,
                "final_message": "You've mastered targeted applies!\nThis concludes the targeting tutorial."
            }
        ]
    },
    "tf_2_2": {
        "name": "Inspecting State (`show`)",
        "description": "Learn how to inspect Terraform state using `terraform show`.",
        "skills_learned": [
            "Understanding the Terraform state file",
            "Using `terraform show` to inspect current state"
        ],
        "steps": [
            {
                "text": "Terraform maintains a state file that acts as its source of truth for your infrastructure. Let's inspect it.\nType `terraform show`.",
                "expected_command": "terraform show",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2)
            },
            {
                "text": "This output is a simplified view of Terraform's state, showing the resources it manages.\nType `status` to compare it with your actual cluster.",
                "expected_command": "status",
                "doc_link": "https://www.terraform.io/cli/commands/show",
                "doc_quote": "The `terraform show` command provides human-readable output from a state or plan file. Use the command to inspect a plan to ensure that the planned operations are expected, or to inspect the current state as Terraform sees it.",
                "final_step": True,
                "final_message": "You've learned to inspect Terraform state!\nThis concludes the state inspection tutorial."
            }
        ]
    },
    "tf_2_3": {
        "name": "Listing State Resources (terraform state list)",
        "description": "Learn how to list resources tracked in Terraform state using `terraform state list`.",
        "skills_learned": [
            "Using `terraform state list`",
            "Understanding resources tracked in state"
        ],
        "steps": [
            {
                "text": "The Terraform state file tracks all resources managed by your configuration. You can list these resources directly from the state.\nType `terraform state list`.",
                "expected_command": "terraform state list",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2),
                "final_step": True,
                "final_message": "This command shows a list of all resources that Terraform is currently managing by reading the state file; it does not check the live infrastructure. This is useful for auditing your infrastructure or preparing for state manipulations.\nThis concludes the state listing tutorial."
            }
        ]
    }
}
