# AI Ops Simulator

A text-based command-line game where you take on the role of a Cluster Manager responsible for processing AI jobs efficiently.

## Game Concept

As a Cluster Manager, your goal is to manage a virtual cluster of resources (CPUs, GPUs, RAM) to process a queue of incoming AI jobs. Each job has specific resource requirements, deadlines, and types (e.g., PyTorch Training, Inference). You must schedule jobs, manage costs, and handle random events to maximize your score.

## Features

- **Text-Based CLI**: A classic, colorful command-line interface powered by `rich`.
- **Dynamic Job Queue**: Jobs are generated randomly with varying requirements.
- **Cluster Management**: Provision and manage nodes in your cluster.
- **Comprehensive Terraform Simulation**: Manage your cluster's infrastructure using `terraform` commands including `plan`, `apply`, `destroy`, `show`, `import`, `init`, `validate`, `fmt`, and `state list`.
- **Enhanced PyTorch & ONNX Simulation**: Handle jobs with specific version requirements, monitor job progress, and optimize models by converting to ONNX format with explicit performance comparisons.
- **Performance Metrics**: Gain insights into your cluster's performance with key operational metrics.
- **Cost Tracking**: Keep an eye on your operational costs.
- **Autoscaling**: A toggleable feature to automatically manage cluster size based on workload.
- **Random Events**: Deal with unexpected hardware failures and urgent job requests.
- **Persistence**: Save and load your game progress at any time.

## Tutorials

The AI Ops Simulator includes a comprehensive set of interactive tutorials designed to guide you through the core concepts and advanced features of the game. These tutorials are structured to provide hands-on experience with managing your AI cluster and using various commands effectively.

Each tutorial focuses on specific skills, including:

- **Terraform Core Workflow**: Learn the fundamentals of `terraform` commands like `apply`, `plan`, `destroy`, `init`, `validate`, and `fmt` to manage your infrastructure.
- **Terraform Advanced Management**: Dive deeper into `terraform` with topics such as targeting specific resources (`-target`), inspecting state (`show`), and listing state resources (`state list`).
- **PyTorch Core Concepts**: Understand how to handle PyTorch version mismatches, debug job failures, and perform basic job submissions.
- **ONNX Core Concepts**: Explore model optimization workflows using ONNX, including converting models and submitting optimized jobs for improved resource efficiency.
- **Model Workflows: Combined**: Experience the full end-to-end lifecycle of a model, from PyTorch job execution to ONNX optimization, combining all learned concepts.

To access the tutorials within the game, type `tutorial` for a list of available tutorials, `tutorial show <ID>` to see the skills offered by a specific tutorial, or `tutorial start <ID>` to begin a tutorial.

## Requirements

- Python 3.x
- `rich` library

## Installation & Setup

1.  **Clone the repository (or use the existing files):**
    ```bash
    git clone <repository_url>
    cd ai-ops-simulator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Play

To start the game, run the `main.py` script:

```bash
python main.py
```

Your initial cluster will be provisioned, and jobs will start appearing in the queue. Use the commands below to manage the cluster and process jobs.

## Commands

| Command                   | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| `help`                    | Displays a list of all available commands.                  |
| `tutorial [list|show|start <id>]` | Lists tutorials, shows skills for one, or starts one.       |
| `status`                  | Shows the current state of the cluster and resource usage.  |
| `ls-jobs`                 | Lists all incoming jobs in the queue.                       |
| `submit <job_id> <node_id>` | Submits a job to a specific node.                           |
| `cancel <job_id>`         | Cancels a running job.                                      |
| `show-job <job_id>`       | Provides detailed information about a job.                  |
| `terraform plan`          | Previews changes from the cluster configuration.            |
| `terraform apply [ -target=<node_id> ]` | Provisions resources based on the configuration, optionally targeting a specific node. |
| `terraform destroy <node_id>` | Destroys a specific node in the cluster.                    |
| `terraform show`          | Displays the current Terraform state.                       |
| `terraform import <node_id>` | Imports an unmanaged node into Terraform state.             |
| `terraform init`          | Initializes a Terraform working directory.                  |
| `terraform validate`      | Checks configuration files for syntax and consistency.      |
| `terraform fmt`           | Rewrites Terraform configuration files to a canonical format. |
| `terraform state list`    | Lists all resources within the Terraform state.             |
| `cost`                    | Displays the current resource expenditure.                  |
| `autoscale <on/off>`      | Toggles autoscaling.                                        |
| `debug <job_id>`          | Shows an error log for a failed job.                        |
| `convert-onnx <job_id>`   | Converts a completed model for optimization.                |
| `log`                     | Displays a history of game events.                          |
| `metrics`                 | Displays key performance metrics and statistics.            |
| `save`                    | Saves the current game state.                               |
| `load`                    | Loads a saved game state.                                   |
| `exit`                    | Quits the game.                                             |
