# src/tutorials/jax.py

TUTORIAL_CATEGORY = "JAX: Accelerated Computing"

TUTORIALS = {
    "jax_1_1": {
        "name": "JIT Compilation with JAX",
        "description": "Learn about JAX and the benefits of JIT compilation for accelerated computing.",
        "skills_learned": [
            "Introduction to JAX",
            "Understanding JIT compilation for performance"
        ],
        "steps": [
            {
                "text": "Welcome to the JAX tutorial!\n\nJAX is a high-performance machine learning framework from Google that is designed to be familiar to anyone who knows NumPy. It provides a powerful set of tools for numerical computation, including automatic differentiation, JIT compilation, and the ability to run on accelerators like GPUs and TPUs.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "One of the key features of JAX is **Just-In-Time (JIT) compilation**. JAX uses a compiler called XLA (Accelerated Linear Algebra) to compile your Python functions into highly optimized machine code. This can lead to significant speedups, especially for numerical code that has loops.\n\nLet's simulate JIT compiling a function. Type `jax-jit`.",
                "expected_command": "jax-jit",
                "trigger": lambda game: game.setup_tutorial_state(jobs=0, nodes=0)
            },
            {
                "type": "mcq",
                "text": "What is the primary benefit of JIT compilation in JAX?",
                "answers": [
                    "a) It makes the code easier to read.",
                    "b) It significantly speeds up numerical computations.",
                    "c) It allows you to run code on multiple machines."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You've simulated JIT compiling a function with JAX!\nThis concludes the first JAX tutorial."
            }
        ]
    }
}
