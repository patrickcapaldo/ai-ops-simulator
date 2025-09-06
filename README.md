# AI Ops Simulator

A text-based command-line game where you take on the role of a Cluster Manager responsible for processing AI jobs efficiently.

## Game Concept

As a Cluster Manager, your goal is to manage a virtual cluster of resources (CPUs, GPUs, RAM) to process a queue of incoming AI jobs. Each job has specific resource requirements, deadlines, and types (e.g., PyTorch Training, Inference). You must schedule jobs, manage costs, and handle random events to maximize your score.

## Features

- **Text-Based CLI**: A classic, colorful command-line interface powered by `rich`.
- **Dynamic Job Queue**: Jobs are generated randomly with varying requirements.
- **Cluster Management**: Provision and manage nodes in your cluster.
- **IaC Simulation**: Use `terraform plan` and `terraform apply` to manage your cluster's infrastructure.
- **PyTorch & ONNX Simulation**: Handle jobs with specific version requirements and optimize them by converting to ONNX format.
- **Cost Tracking**: Keep an eye on your operational costs.
- **Autoscaling**: A toggleable feature to automatically manage cluster size based on workload.
- **Random Events**: Deal with unexpected hardware failures and urgent job requests.
- **Persistence**: Save and load your game progress at any time.

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
| `status`                  | Shows the current state of the cluster and resource usage.  |
| `ls-jobs`                 | Lists all incoming jobs in the queue.                       |
| `submit <job_id> <node_id>` | Submits a job to a specific node.                           |
| `cancel <job_id>`         | Cancels a running job.                                      |
| `show-job <job_id>`       | Provides detailed information about a job.                  |
| `terraform plan`          | Previews changes from the cluster configuration.            |
| `terraform apply`         | Provisions resources based on the configuration.            |
| `cost`                    | Displays the current resource expenditure.                  |
| `autoscale <on/off>`      | Toggles autoscaling.                                        |
| `debug <job_id>`          | Shows an error log for a failed job.                        |
| `convert-onnx <job_id>`   | Converts a completed model for optimization.                |
| `log`                     | Displays a history of game events.                          |
| `save`                    | Saves the current game state.                               |
| `load`                    | Loads a saved game state.                                   |
| `exit`                    | Quits the game.                                             |
