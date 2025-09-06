
'''
Defines the content and structure for interactive tutorials, grouped by category. 
'''

from data import Node, Job, JobType

def create_node_trigger(game, node_id, cpu, gpu, ram, pytorch_version, unmanaged=False):
    """A trigger to create a specific node for a tutorial step."""
    new_node = Node(node_id, cpu, gpu, ram, pytorch_version, unmanaged=unmanaged)
    game.cluster.add_node(new_node)

def create_job_trigger(game, job_type, requirements, deadline, pytorch_version=None):
    """A trigger to create a specific job for a tutorial step."""
    new_job = Job(job_type, requirements, deadline, pytorch_version)
    game.job_queue.append(new_job)

def complete_job_trigger(game, job_id):
    """A trigger function to mark a specific job as complete for a tutorial step."""
    job = game.get_job(job_id)
    if job:
        node = game.cluster.get_node(job.assigned_node)
        if node:
            game.complete_job(job, node)


TUTORIALS = {
    "Terraform: Core Workflow": {
        "tf_1_1": {
            "name": "1. Your First Resource (terraform apply)",
            "skills_learned": [
                "Understanding `terraform apply` to provision resources",
                "Concept of a Terraform resource"
            ],
            "steps": [
                {
                    "text": "Welcome to the Terraform tutorials! We'll start by provisioning your first resource.\nYour cluster is currently empty. Type `terraform apply` to create your first node.",
                    "expected_command": "terraform apply",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
                },
                {
                    "text": "Excellent! You've just used `terraform apply` to create a node. This command executes the changes defined in your configuration.\nType `status` to see your new node.",
                    "expected_command": "status",
                    "doc_link": "https://www.terraform.io/cli/commands/apply",
                    "doc_quote": "The `terraform apply` command is a fundamental part of the Terraform workflow, used to apply the changes defined in your Terraform configuration to create, update, or destroy infrastructure."
                },
                {
                    "text": "You've successfully provisioned your first resource!\nThis concludes the first tutorial.",
                    "expected_command": None
                }
            ]
        },
        "tf_1_2": {
            "name": "2. Planning Your Changes (terraform plan)",
            "skills_learned": [
                "Understanding `terraform plan` to preview changes",
                "Reading plan output (create, update, destroy)",
                "The `plan -> apply` workflow"
            ],
            "steps": [
                {
                    "text": "Now, let's learn to preview changes before applying them. Your configuration has been updated to specify 3 nodes.\nType `terraform plan` to see what changes Terraform intends to make.",
                    "expected_command": "terraform plan",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\nimport re\nfrom data import TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 3', TERRAFORM_CONFIG)\n''')
                },
                {
                    "text": "Notice Terraform plans to create 2 new nodes. This is a 'dry run' that shows the execution plan.\nNow, apply these changes. Type `terraform apply`.",
                    "expected_command": "terraform apply",
                    "doc_link": "https://www.terraform.io/cli/commands/plan",
                    "doc_quote": "The `terraform plan` command is a crucial part of the Terraform workflow that creates an execution plan, allowing you to preview the changes Terraform will make to your infrastructure before you apply them."
                },
                {
                    "text": "Great! You've successfully planned and applied changes.\nType `status` to confirm you now have 3 nodes.",
                    "expected_command": "status"
                },
                {
                    "text": "You've mastered planning and applying changes!\nThis concludes the planning tutorial.",
                    "expected_command": None
                }
            ]
        },
        "tf_1_3": {
            "name": "3. Destroying Resources (terraform destroy)",
            "skills_learned": [
                "Using `terraform destroy` to remove resources",
                "Understanding resource lifecycle",
                "Cost management implications of idle resources"
            ],
            "steps": [
                {
                    "text": "Resources cost money even when idle. You currently have 3 nodes, but no jobs.\nLet's remove one of the nodes to save costs. Type `terraform destroy node-0`.",
                    "expected_command": "terraform destroy node-0",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=3)
                },
                {
                    "text": "You've successfully destroyed `node-0`. This command terminates resources managed by Terraform.\nType `status` to confirm you now have 2 nodes.",
                    "expected_command": "status",
                    "doc_link": "https://www.terraform.io/cli/commands/destroy",
                    "doc_quote": "The `terraform destroy` command is used... to terminate all resources managed by a specific Terraform configuration."
                },
                {
                    "text": "You've learned to destroy resources!\nThis concludes the destroy tutorial.",
                    "expected_command": None
                }
            ]
        },
        "tf_1_4": {
            "name": "4. Initializing a Working Directory (terraform init)",
            "skills_learned": [
                "Understanding `terraform init`",
                "Initializing a Terraform working directory"
            ],
            "steps": [
                {
                    "text": "Before you can run any other Terraform commands, you need to initialize your working directory. This command downloads necessary providers and modules.\nType `terraform init`.",
                    "expected_command": "terraform init",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, clear_terraform_config=True)
                },
                {
                    "text": "Terraform has successfully initialized the directory. You're now ready to apply configurations.\nThis concludes the initialization tutorial.",
                    "expected_command": None,
                    "doc_link": "https://www.terraform.io/cli/commands/init",
                    "doc_quote": "The `terraform init` command is used to initialize a working directory containing Terraform configuration files. This is the first command that should be run after writing a new Terraform configuration or cloning an existing one from version control."
                }
            ]
        },
        "tf_1_5": {
            "name": "5. Validating Your Configuration (terraform validate)",
            "skills_learned": [
                "Understanding `terraform validate`",
                "Checking configuration syntax and consistency"
            ],
            "steps": [
                {
                    "text": "After making changes to your Terraform configuration, it's good practice to validate it to catch syntax errors or inconsistencies before planning or applying. \nType `terraform validate`.",
                    "expected_command": "terraform validate",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
                },
                {
                    "text": "Terraform has validated the configuration. If there were any errors, they would be displayed here. This helps ensure your configuration is syntactically correct and internally consistent.\nThis concludes the validation tutorial.",
                    "expected_command": None,
                    "doc_link": "https://www.terraform.io/cli/commands/validate",
                    "doc_quote": "The `terraform validate` command checks the configuration files in a directory for syntax errors and internal consistency, but does not access any remote services or remote state."
                }
            ]
        },
        "tf_1_6": {
            "name": "6. Formatting Your Configuration (terraform fmt)",
            "skills_learned": [
                "Using `terraform fmt`",
                "Maintaining consistent code style"
            ],
            "steps": [
                {
                    "text": "Consistent formatting improves readability and maintainability of your Terraform configurations. Let's introduce a formatting error and then fix it.\nType `terraform apply` to create a node, then we'll mess up the config.",
                    "expected_command": "terraform apply",
                    "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='\'\nimport re\nfrom data import TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 1', TERRAFORM_CONFIG)\n\'')"
                },
                {
                    "text": "Now, let's intentionally mess up the formatting of your Terraform configuration. Type `edit-terraform-config` and remove some indentation or add extra spaces.",
                    "expected_command": "edit-terraform-config"
                },
                {
                    "text": "Your configuration is now poorly formatted. To automatically fix this, type `terraform fmt`.",
                    "expected_command": "terraform fmt",
                    "doc_link": "https://www.terraform.io/cli/commands/fmt",
                    "doc_quote": "The `terraform fmt` command is used to rewrite Terraform configuration files to a canonical format and style. This command applies a subset of the Terraform language style conventions, including consistent indentation and spacing."
                },
                {
                    "text": "Terraform has automatically reformatted your configuration. You can type `edit-terraform-config` again to see the changes, or just proceed.\nThis concludes the formatting tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
    "Terraform: Advanced Management": {
        "tf_2_1": {
            "name": "1. Targeting Specific Resources (`-target`)",
            "skills_learned": [
                "Using the `-target` flag for granular control",
                "Applying changes to a subset of resources"
            ],
            "steps": [
                {
                    "text": "Sometimes you need to apply changes to only a specific resource. Your configuration has been updated to give all nodes more RAM, but you only want to upgrade `node-0`.\nType `terraform apply -target=node-0`.",
                    "expected_command": "terraform apply -target=node-0",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2, custom_setup='''\nimport re\nfrom data import TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'ram = \\d+', 'ram = 128', TERRAFORM_CONFIG)\n''')
                },
                {
                    "text": "You've successfully targeted `node-0` for an update. The `-target` flag directs Terraform's operations to a specific subset of resources.\nType `status` to confirm only `node-0` has 128GB RAM.",
                    "expected_command": "status",
                    "doc_link": "https://www.terraform.io/cli/commands/apply#target-a-specific-resource",
                    "doc_quote": "The `-target` flag... allows you to direct Terraform's operations to a specific subset of your resources."
                },
                {
                    "text": "You've mastered targeted applies!\nThis concludes the targeting tutorial.",
                    "expected_command": None
                }
            ]
        },
        "tf_2_2": {
            "name": "2. Inspecting State (`show`)",
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
                    "doc_quote": "The `terraform show` command provides human-readable output from a state or plan file... to inspect the current current state as Terraform sees it."
                },
                {
                    "text": "You've learned to inspect Terraform state!\nThis concludes the state inspection tutorial.",
                    "expected_command": None
                }
            ],
        },
        "tf_2_3": {
            "name": "3. Listing State Resources (terraform state list)",
            "skills_learned": [
                "Using `terraform state list`",
                "Understanding resources tracked in state"
            ],
            "steps": [
                {
                    "text": "The Terraform state file tracks all resources managed by your configuration. You can list these resources directly from the state.\nType `terraform state list`.",
                    "expected_command": "terraform state list",
                    "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=2)"
                },
                {
                    "text": "This command shows a list of all resources that Terraform is currently managing. This is useful for auditing your infrastructure or preparing for state manipulations.\nThis concludes the state listing tutorial.",
                    "expected_command": None,
                    "doc_link": "https://www.terraform.io/cli/commands/state/list",
                    "doc_quote": "The `terraform state list` command lists all resources within the Terraform state. This command is useful for auditing the resources managed by Terraform."
                }
            ]
        }
    },
    "Terraform: Real-World Scenarios": {
        "tf_3_1": {
            "name": "1. Importing Existing Infrastructure (`import`)",
            "skills_learned": [
                "Understanding state drift",
                "Using `terraform import` to manage existing resources"
            ],
            "steps": [
                {
                    "text": "Sometimes infrastructure is created manually and needs to be brought under Terraform's control. An admin has manually created `node-manual`.\nType `status` to see it.",
                    "expected_command": "status",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\ncreate_node_trigger(game, \"node-manual\", 8, 2, 64, \"2.0\", unmanaged=True)\n''')
                },
                {
                    "text": "Notice `node-manual` is there. Now, let's see what Terraform thinks. Type `terraform plan`.",
                    "expected_command": "terraform plan"
                },
                {
                    "text": "Terraform wants to create a new node because it doesn't know about `node-manual`. Let's import it.\nType `terraform import node-manual`.",
                    "expected_command": "terraform import node-manual",
                    "doc_link": "https://www.terraform.io/cli/commands/import",
                    "doc_quote": "The `terraform import` command is used to bring existing infrastructure, that was created outside of Terraform, under its management."
                },
                {
                    "text": "`node-manual` is now imported! Terraform has updated its state. Now, run `terraform plan` again.",
                    "expected_command": "terraform plan"
                },
                {
                    "text": "Terraform now correctly shows no changes needed! You've successfully imported a resource.\nThis concludes the import tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
    "PyTorch: Core Concepts": {
        "pt_1_1": {
            "name": "1. Handling PyTorch Version Mismatches",
            "skills_learned": [
                "Debugging job failures (`debug`)",
                "Understanding node-specific software versions",
                "Scheduling jobs to specific, compatible nodes"
            ],
            "steps": [
                {
                    "text": "This tutorial covers job failures from software incompatibility.\nWe have a special job that requires an older PyTorch version. Type `ls-jobs`.",
                    "expected_command": "ls-jobs",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\ngame.cluster.add_node(Node(\"node-0\", 8, 2, 64, \"2.0\"))\ngame.cluster.add_node(Node(\"node-1\", 8, 2, 64, \"1.9\")) # Legacy node\ngame.job_queue.append(Job(JobType.PYTORCH_TRAINING, {\"cpu\": 2, \"gpu\": 1, \"ram\": 8}, game.time + 50, pytorch_version=\"1.9\"))\n''')
                },
                {
                    "text": "Notice the job requires PyTorch 1.9. Let's try to submit it to `node-0` which has version 2.0 and see what happens.\nType `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True
                },
                {
                    "text": "The submission failed, as expected. When a job fails, you can get details.\nType `debug <job_id>` to see the error message.",
                    "expected_command": "debug",
                    "is_dynamic": True
                },
                {
                    "text": "The error shows a version mismatch. Now check your cluster to find the right node. Type `status`.",
                    "expected_command": "status",
                    "doc_link": "https://pytorch.org/get-started/previous-versions/",
                    "doc_quote": "Models saved with `torch.jit.save()` on a newer PyTorch version may not be loadable on older versions if the serialized model uses operators or behaviors not present in the older version."
                },
                {
                    "text": "You can see `node-1` has the correct PyTorch version (1.9).\nNow, submit the job to the correct node: `submit <job_id> node-1`.",
                    "expected_command": "submit",
                    "is_dynamic": True
                },
                {
                    "text": "Success! The job is running on a compatible node.\nThis concludes the versioning tutorial.",
                    "expected_command": None
                }
            ],
        },
        "pt_1_2": {
            "name": "2. Basic Job Submission",
            "skills_learned": [
                "Submitting a job to a node (`submit`)"
            ],
            "steps": [
                {
                    "text": "Now that you understand versioning, let's try a basic job submission. You have a new PyTorch training job in the queue and a node available.\nType `ls-jobs` to see the job.",
                    "expected_command": "ls-jobs",
                    "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='\'\ngame.job_queue.append(Job(JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\"))\'')"
                },
                {
                    "text": "You see the new job. Now, submit it to `node-0`.\nType `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True
                },
                {
                    "text": "The job is now running on `node-0`.",
                    "expected_command": None
                },
                {
                    "text": "To see the job's progress, type `show-job <job_id>`.",
                    "expected_command": "show-job",
                    "is_dynamic": True
                },
                {
                    "text": "You can see the job's progress percentage. This is useful for monitoring long-running tasks.\nThis concludes the basic job submission tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
    "ONNX: Core Concepts": {
        "onnx_1_1": {
            "name": "1. Optimizing with ONNX",
            "skills_learned": [
                "Model optimization workflow (`convert-onnx`)",
                "Resource efficiency of optimized models",
                "Checking job history for completed tasks"
            ],
            "steps": [
                {
                    "text": "This tutorial covers optimizing a trained model using ONNX.\nFirst, submit the PyTorch training job. Type `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True,
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ngame.job_queue.append(Job(JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\"))\n''')
                },
                {
                    "text": "The training job is running. For this tutorial, we'll instantly complete it.",
                    "expected_command": "status", # Just ask user to check status to proceed
                    "trigger": lambda game: complete_job_trigger(game, game.cluster.nodes["node-0"].running_jobs[0].id if game.cluster.nodes["node-0"].running_jobs else None)
                },
                {
                    "text": "The training job is complete. Now, we can convert it to a more efficient ONNX model.\nType `convert-onnx <completed_job_id>`.",
                    "expected_command": "convert-onnx",
                    "is_dynamic": True,
                    "doc_link": "https://pytorch.org/docs/stable/onnx.html",
                    "doc_quote": "To convert a PyTorch model to ONNX, you can use the built-in `torch.onnx.export()` function. This function traces the model's execution to record the computational graph."
                },
                {
                    "text": "Excellent! A new, optimized ONNX job has been created with lower resource requirements.\nCheck the job queue to see it. Type `ls-jobs`.",
                    "expected_command": "ls-jobs"
                },
                {
                    "text": "Notice the ONNX job requires half the resources. This makes it cheaper and easier to run.",
                    "expected_command": None
                },
                {
                    "text": "To see the resource difference, use `show-job` on the original PyTorch job (from the `completed-jobs` list) and then on the new ONNX job (from `ls-jobs`). Compare their CPU, GPU, and RAM requirements.",
                    "expected_command": "show-job",
                    "is_dynamic": True
                },
                {
                    "text": "You should observe that the ONNX job has significantly lower resource requirements, demonstrating the benefits of model optimization.\nThis concludes the ONNX tutorial.",
                    "expected_command": None
                }
            ]
        },
        "onnx_1_2": {
            "name": "2. Submitting an ONNX Job",
            "skills_learned": [
                "Submitting an optimized ONNX job",
                "Resource efficiency of optimized models"
            ],
            "steps": [
                {
                    "text": "You've successfully converted a PyTorch model to ONNX. Now, let's submit this optimized job to a node. First, ensure you have a node available. Type `status`.",
                    "expected_command": "status",
                    "trigger": "lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='\'\ngame.job_queue.append(Job(JobType.ONNX_INFERENCE, {\"cpu\": 2, \"gpu\": 0, \"ram\": 8}, game.time + 50))\'')"
                },
                {
                    "text": "Now, submit the ONNX job to `node-0`. Type `submit <onnx_job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True
                },
                {
                    "text": "The optimized ONNX job is now running. You've completed the ONNX workflow!\nThis concludes the ONNX job submission tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
    "Model Workflows: Combined": {
        "combined_1_1": {
            "name": "1. End-to-End Model Workflow",
            "skills_learned": [
                "Combining PyTorch job execution and ONNX optimization",
                "Full lifecycle of a model from training to optimized inference"
            ],
            "steps": [
                {
                    "text": "This tutorial combines previous concepts. We'll go through a full model workflow.\nFirst, submit the PyTorch training job. Type `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True,
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ngame.job_queue.append(Job(JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\"))\n''')
                },
                {
                    "text": "The training job is running. For this tutorial, we'll instantly complete it.",
                    "expected_command": "status",
                    "trigger": lambda game: complete_job_trigger(game, game.cluster.nodes["node-0"].running_jobs[0].id if game.cluster.nodes["node-0"].running_jobs else None)
                },
                {
                    "text": "Training complete. Now, convert it to ONNX. Type `convert-onnx <completed_job_id>`.",
                    "expected_command": "convert-onnx",
                    "is_dynamic": True
                },
                {
                    "text": "ONNX model created. Now, submit the optimized ONNX job. Type `submit <onnx_job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True
                },
                {
                    "text": "The optimized job is running. This concludes the end-to-end workflow tutorial!",
                    "expected_command": None
                }
            ]
        }
    }
}
