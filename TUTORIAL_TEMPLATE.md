# Tutorial Template Guide

This guide provides a template and best practices for creating new tutorials for the AI Ops Simulator.

## Tutorial Structure

Each tutorial should be a self-contained lesson that teaches a specific skill or concept. A tutorial is a dictionary in a Python file, with the following structure:

```python
"<tutorial_id>": {
    "name": "<Tutorial Name>",
    "skills_learned": [
        "<Skill 1>",
        "<Skill 2>",
        ...
    ],
    "steps": [
        {
            "text": "<Instructional text for the step>",
            "expected_command": "<The command the user is expected to enter>",
            "trigger": lambda game: game.setup_tutorial_state(...), # Optional: A function to set up the tutorial state
            "doc_link": "<URL to relevant documentation>", # Optional
            "doc_quote": "<A quote from the documentation>" # Optional
        },
        {
            "type": "mcq",
            "text": "<Question text>",
            "answers": [
                "a) <Answer 1>",
                "b) <Answer 2>",
                "c) <Answer 3>"
            ],
            "correct_answer": "<b>",
            "final_step": True, # Optional: Indicates the last step of the tutorial
            "final_message": "<A message to display when the tutorial is complete>"
        },
        ...
    ]
}
```

### Tutorial ID

The `<tutorial_id>` should be a unique identifier for the tutorial, following the format `<tool>_<chapter>_<lesson>`. For example, `k8s_1_1` for the first lesson of the first chapter of the Kubernetes tutorials.

### Name

The `name` is a human-readable name for the tutorial that will be displayed in the tutorial list.

### Skills Learned

The `skills_learned` is a list of strings that describe the skills the user will learn in the tutorial. This is displayed when the user runs `tutorial show <tutorial_id>`.

### Steps

The `steps` is a list of dictionaries, where each dictionary represents a step in the tutorial. Each step can be one of two types: a command step or a multiple-choice question (MCQ) step.

#### Command Step

A command step requires the user to enter a specific command to proceed. It has the following properties:

*   `text`: The instructional text for the step. This should explain the concept and what the user needs to do.
*   `expected_command`: The command the user is expected to enter. The tutorial will only advance if the user enters this exact command.
*   `trigger` (optional): A lambda function that sets up the state for the tutorial step. This can be used to create nodes, jobs, or other resources.
*   `doc_link` (optional): A URL to relevant documentation.
*   `doc_quote` (optional): A quote from the documentation that can be displayed to the user.

#### Multiple-Choice Question (MCQ) Step

An MCQ step presents the user with a question and a list of possible answers. It has the following properties:

*   `type`: Must be set to `"mcq"`.
*   `text`: The question text.
*   `answers`: A list of strings, where each string is a possible answer.
*   `correct_answer`: The correct answer, corresponding to the letter of the answer (e.g., `"b"`).
*   `final_step` (optional): If set to `True`, this indicates that this is the last step of the tutorial.
*   `final_message` (optional): A message to display to the user when they complete the tutorial.

## Tutorial Group Structure

Tutorials for a specific tool should be grouped together in a dedicated Python file in the `src/tutorials` directory (e.g., `src/tutorials/kubernetes.py`). The tutorials should be structured in a logical progression, starting with the basics and gradually introducing more advanced concepts. Each file should contain a dictionary of tutorials for that tool, which is then imported into `src/tutorials/__init__.py` and added to the main `TUTORIALS` dictionary.

### Example

Here is an example of how the tutorials for a new tool called "MyTool" would be structured:

1.  **`src/tutorials/mytool.py`:**

    ```python
    MYTOOL_TUTORIALS = {
        "mytool_1_1": { ... },
        "mytool_1_2": { ... },
        "mytool_2_1": { ... },
    }
    ```

2.  **`src/tutorials/__init__.py`:**

    ```python
    from .mytool import MYTOOL_TUTORIALS

    TUTORIALS = {
        # ... other tutorials
        "MyTool: Core Concepts": MYTOOL_TUTORIALS,
    }
    ```

## Best Practices

*   **Keep it simple:** Tutorials should be focused on a single concept or skill.
*   **Be clear and concise:** The instructional text should be easy to understand and to the point.
*   **Provide a way to move forward:** Always provide a clear way for the user to advance to the next step, whether it's by entering a command or answering a question.
*   **Use a progressive difficulty curve:** Start with the basics and gradually introduce more complex concepts.
*   **Test your tutorials:** Make sure to test your tutorials to ensure they are working as expected.
