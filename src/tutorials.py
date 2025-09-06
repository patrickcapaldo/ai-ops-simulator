# src/tutorials.py

'''
Defines the content and structure for interactive tutorials, grouped by tool.
'''

from src.tutorial_manager import Node, Job, JobType, TERRAFORM_CONFIG
import re # Needed for custom_setup in some tutorials

def create_node_trigger(game, node_id, cpu, gpu, ram, pytorch_version, unmanaged=False):
    """A trigger to create a specific node for a tutorial step."""
    new_node = Node(node_id, cpu, gpu, ram, pytorch_version, unmanaged=unmanaged)
    game.cluster[new_node.id] = new_node

def create_job_trigger(game, job_type, requirements, deadline, pytorch_version=None):
    """A trigger to create a specific job for a tutorial step."""
    new_job = Job(job_type, requirements, deadline, pytorch_version)
    game.job_queue.append(new_job)

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


TUTORIALS = {
    "Kubernetes: Core Concepts": {
        "k8s_1_1": {
            "name": "1. Deploying a Pod",
            "skills_learned": [
                "Understanding Kubernetes Pods",
                "Basic deployment commands"
            ],
            "steps": [
                {
                    "text": "Welcome to Kubernetes tutorials! We'll start by deploying a simple Pod.\n(This is a placeholder tutorial. No actual deployment will occur.)\nType `kubectl apply -f my-pod.yaml` to simulate deploying a Pod.",
                    "expected_command": "kubectl apply -f my-pod.yaml",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
                },
                {
                    "text": "You've simulated deploying a Pod! In a real Kubernetes environment, this would create a running instance of your application.\nThis concludes the first Kubernetes tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
    "Kubeflow: MLOps Workflows": {
        "kf_1_1": {
            "name": "1. Running a Kubeflow Pipeline",
            "skills_learned": [
                "Introduction to Kubeflow Pipelines",
                "Executing a simple ML workflow"
            ],
            "steps": [
                {
                    "text": "Welcome to Kubeflow tutorials! Let's simulate running a basic Kubeflow pipeline.\n(This is a placeholder tutorial. No actual pipeline will run.)\nType `kfctl apply -V -f kubeflow_v1.2.yaml` to simulate deploying Kubeflow.",
                    "expected_command": "kfctl apply -V -f kubeflow_v1.2.yaml",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
                },
                {
                    "text": "You've simulated deploying Kubeflow. Now, let's imagine running a pipeline.\nType `kfp run submit my-pipeline.yaml` to simulate running a pipeline.",
                    "expected_command": "kfp run submit my-pipeline.yaml"
                },
                {
                    "text": "You've simulated running a Kubeflow pipeline! In a real scenario, this would execute your end-to-end ML workflow.\nThis concludes the first Kubeflow tutorial.",
                    "expected_command": None
                }
            ]
        }
    },
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
                    "doc_quote": "The `terraform apply` command is used to execute the actions proposed in a Terraform plan."
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\nglobal TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 3', TERRAFORM_CONFIG)\n''')
                },
                {
                    "text": "Notice Terraform plans to create 2 new nodes. This is a 'dry run' that shows the execution plan.\nNow, apply these changes. Type `terraform apply`.",
                    "expected_command": "terraform apply",
                    "doc_link": "https://www.terraform.io/cli/commands/plan",
                    "doc_quote": "The `terraform plan` command creates an execution plan, which lets you preview the changes that Terraform plans to make to your infrastructure."
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
                    "doc_quote": "The `terraform destroy` command deprovisions all objects managed by a Terraform configuration."
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
                    "doc_quote": "The `terraform init` command initializes a working directory containing Terraform configuration files. This is the first command you should run after writing a new Terraform configuration or cloning an existing configuration from version control."
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
                    "doc_quote": "The `terraform validate` command validates the configuration files in a directory. It does not validate remote services, such as remote state or provider APIs."
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\nglobal TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'count = \\d+', 'count = 1', TERRAFORM_CONFIG)\n''')
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2, custom_setup='''\nglobal TERRAFORM_CONFIG\nTERRAFORM_CONFIG = re.sub(r'ram = \\d+', 'ram = 128', TERRAFORM_CONFIG)\n''')
                },
                {
                    "text": "You've successfully targeted `node-0` for an update. The `-target` flag directs Terraform's operations to a specific subset of resources.\nType `status` to confirm only `node-0` has 128GB RAM.",
                    "expected_command": "status",
                    "doc_link": "https://www.terraform.io/cli/commands/apply#target-a-specific-resource",
                    "doc_quote": "The `-target` option can be used to focus Terraform's attention on only a subset of the resources in a configuration."
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
                    "doc_quote": "The `terraform show` command provides human-readable output from a state or plan file. Use the command to inspect a plan to ensure that the planned operations are expected, or to inspect the current state as Terraform sees it."
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=2)
                },
                {
                    "text": "This command shows a list of all resources that Terraform is currently managing. This is useful for auditing your infrastructure or preparing for state manipulations.\nThis concludes the state listing tutorial.",
                    "expected_command": None,
                    "doc_link": "https://www.terraform.io/cli/commands/state/list",
                    "doc_quote": "The `terraform state list` command lists resources within a Terraform state file."
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
                    "doc_quote": "The `terraform import` command is used to bring existing infrastructure under Terraform's management."
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
    "JAX: Accelerated Computing": {
        "jax_1_1": {
            "name": "1. JIT Compilation with JAX",
            "skills_learned": [
                "Introduction to JAX",
                "Understanding JIT compilation for performance"
            ],
            "steps": [
                {
                    "text": "Welcome to JAX tutorials! JAX is a library for high-performance numerical computing.\nOne of its key features is JIT (Just-In-Time) compilation.\n(This is a placeholder tutorial. No actual JAX code will run.)\nType `jax.jit(my_function)` to simulate JIT compiling a function.",
                    "expected_command": "jax.jit(my_function)",
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
                },
                {
                    "text": "You've simulated JIT compiling a function with JAX! This would typically lead to significant performance improvements.\nThis concludes the first JAX tutorial.\n",
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0, custom_setup='''\ncreate_node_trigger(game, \"node-0\", 8, 2, 64, \"2.0\")\ncreate_node_trigger(game, \"node-1\", 8, 2, 64, \"1.9\") # Legacy node\ncreate_job_trigger(game, JobType.PYTORCH_TRAINING, {\"cpu\": 2, \"gpu\": 1, \"ram\": 8}, game.time + 50, pytorch_version=\"1.9\")\n''')
                },
                {
                    "text": "Notice the job requires PyTorch 1.9. Let's try to submit it to `node-0` which has version 2.0 and see what happens.\nType `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True,
                    "doc_quote": "The `debug` command in this simulator provides a simplified view of an error log for a failed job, helping to diagnose issues like version mismatches or resource constraints."
                },
                {
                    "text": "The error shows a version mismatch. Now check your cluster to find the right node. Type `status`.",
                    "expected_command": "status"
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ncreate_job_trigger(game, JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\")\n''')
                },
                {
                    "text": "You see the new job. Now, submit it to `node-0`.\nType `submit <job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True,
                    "doc_quote": "The `submit` command allows you to assign a pending job to an available node in the cluster, initiating its execution."
                },
                {
                    "text": "The job is now running on `node-0`.",
                    "expected_command": "status"
                },
                {
                    "text": "To see the job's progress, type `show-job <job_id>`.",
                    "expected_command": "show-job",
                    "is_dynamic": True,
                    "doc_quote": "The `show-job` command provides detailed information about a specific job, including its type, status, resource requirements, and progress."
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ncreate_job_trigger(game, JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\")\n''')
                },
                {
                    "text": "The training job is running. For this tutorial, we'll instantly complete it.",
                    "expected_command": "status", # Just ask user to check status to proceed
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ncreate_job_trigger(game, JobType.ONNX_INFERENCE, {\"cpu\": 2, \"gpu\": 0, \"ram\": 8}, game.time + 50)\n''')
                },
                {
                    "text": "Now, submit the ONNX job to `node-0`. Type `submit <onnx_job_id> node-0`.",
                    "expected_command": "submit",
                    "is_dynamic": True,
                    "doc_quote": "Submitting an ONNX job involves assigning the optimized model to a compatible node for efficient inference, leveraging its reduced resource footprint."
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
                    "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=1, custom_setup='''\ncreate_job_trigger(game, JobType.PYTORCH_TRAINING, {\"cpu\": 4, \"gpu\": 1, \"ram\": 16}, game.time + 50, pytorch_version=\"2.0\")\n''')
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
                    "text": "The optimized job is running. This concludes the end-to-end workflow tutorial!",
                    "expected_command": None
                }
            ]
        }
    }
}