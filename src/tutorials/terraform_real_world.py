# src/tutorials/terraform_real_world.py

TUTORIAL_CATEGORY = "Terraform: Real-World Scenarios"

TUTORIALS = {
    "tf_3_1": {
        "name": "Importing Existing Infrastructure (`import`)",
        "description": "Learn how to import existing infrastructure into Terraform.",
        "skills_learned": [
            "Understanding state drift",
            "Using `terraform import` to manage existing resources"
        ],
        "steps": [
            {
                "text": "Sometimes infrastructure is created manually and needs to be brought under Terraform's control. An admin has manually created `node-manual`.\nType `status` to see it.",
                "expected_command": "status",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\ngame.create_node_trigger(\"node-manual\", 8, 2, 64, \"2.0\", unmanaged=True)\n''')
            },
            {
                "text": "Notice `node-manual` is there. Now, let's see what Terraform thinks. Type `terraform plan`.",
                "expected_command": "terraform plan"
            },
            {
                "text": "Terraform wants to create a new node because it doesn't know about `node-manual`. Let's import it.\nType `terraform import node-manual`.",
                "expected_command": "terraform import node-manual",
                "doc_link": "https://www.terraform.io/cli/commands/import",
                "doc_quote": "The `terraform import` command is used to bring existing infrastructure under Terraform's management."
            },
            {
                "text": "`node-manual` is now imported! Terraform has updated its state. Now, run `terraform plan` again.",
                "expected_command": "terraform plan",
                "final_step": True,
                "final_message": "Terraform now correctly shows no changes needed! You've successfully imported a resource.\nThis concludes the import tutorial."
            }
        ]
    }
}
