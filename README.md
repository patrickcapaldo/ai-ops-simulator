# AI Ops Simulator Tutorials

A text-based command-line tool designed to provide interactive tutorials on various AI Operations (AI Ops) tools and concepts. This simulator focuses on practical, hands-on learning through a command-line interface.

## Concept

The AI Ops Simulator Tutorials guide you through key aspects of managing AI workloads and infrastructure using simulated environments. Each tutorial focuses on a specific tool or concept, allowing you to practice commands and understand their impact in a controlled setting.

## Features

- **Interactive CLI Tutorials**: Learn by doing with step-by-step instructions and immediate feedback.
- **Tool-Specific Modules**: Tutorials are organized by popular AI Ops tools and frameworks:
    -   **Kubernetes**: Core concepts for container orchestration.
    -   **Kubeflow**: MLOps workflows and pipeline management.
    -   **Terraform**: Infrastructure as Code for provisioning and managing resources.
    -   **JAX**: Accelerated computing for high-performance numerical operations.
    -   **PyTorch**: Deep learning model training and deployment.
    -   **ONNX**: Model optimization and interoperability.
- **Simulated Environments**: Practice commands in a safe, mock environment without affecting real systems.
- **Documentation Integration**: Key commands and concepts are accompanied by embedded documentation quotes for quick reference.

## Tutorials

The simulator includes a comprehensive set of interactive tutorials designed to guide you through the core concepts and advanced features of various AI Ops tools.

To access the tutorials, type `tutorial list` for a list of available tutorials, `tutorial show <ID>` to see the skills offered by a specific tutorial, or `tutorial start <ID>` to begin a tutorial.

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

## How to Use

To start the tutorial simulator, run the `main.py` script:

```bash
python src/main.py
```

Once started, you can use the `tutorial` command to explore and begin learning.

## Help Commands

### General Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `help`                                    | Displays this help message.                                 |
| `tutorial [list|show|start <id>]`         | Lists tutorials, shows skills for one, or starts one. This is the main way to learn about different tools. |
| `exit`                                    | Quits the application.                                      |

### Simulated Kubernetes Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `kubectl apply -f <file>`                 | Simulates applying a Kubernetes manifest to deploy resources. |

### Simulated Kubeflow Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `kfctl apply -V -f <file>`                | Simulates deploying Kubeflow components.                    |
| `kfp run submit <file>`                   | Simulates submitting a Kubeflow pipeline.                   |

### Simulated Terraform Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `terraform plan`                          | Previews changes from the simulated cluster configuration.  |
| `terraform apply [ -target=<node_id> ]`   | Provisions resources based on the configuration in the simulated cluster, optionally targeting a specific node. |
| `terraform destroy <node_id>`             | Destroys a specific node in the simulated cluster.          |
| `terraform show`                          | Displays the current simulated Terraform state.             |
| `terraform import <node_id>`              | Imports an unmanaged node into the simulated Terraform state. |
| `terraform init`                          | Initializes a simulated Terraform working directory.        |
| `terraform validate`                      | Checks simulated Terraform configuration files for syntax and consistency. |
| `terraform fmt`                           | Rewrites simulated Terraform configuration files to a canonical format. |
| `edit-terraform-config`                   | Allows direct editing of the mock Terraform configuration used in tutorials. |

### Simulated JAX Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `jax-jit`                   | Simulates JIT compiling a function for performance with JAX. |

### Simulated PyTorch Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `status`                                  | Shows the current state of the simulated cluster and resource utilization. |
| `ls-jobs`                                 | Lists all incoming jobs in the simulated queue.             |
| `submit <job_id> <node_id>`               | Submits a job to a specific node in the simulated cluster.  |
| `show-job <job_id>`                       | Provides detailed information about a simulated job.        |
| `debug <job_id>`                          | Shows an error log for a failed simulated job.              |

### Simulated ONNX Commands

| Command                                   | Description                                                 |
| :---------------------------------------- | :---------------------------------------------------------- |
| `convert-onnx <job_id>`                   | Converts a completed simulated model to ONNX format for optimization. |
