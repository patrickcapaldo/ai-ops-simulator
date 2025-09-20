# src/tutorials/cuda.py

TUTORIAL_CATEGORY = "CUDA: Core Concepts"

TUTORIALS = {
    "cuda_1_1": {
        "name": "Introduction to CUDA",
        "description": "Learn the basics of CUDA and the difference between host and device code.",
        "skills_learned": [
            "Understanding the basics of CUDA",
            "Understanding the difference between host and device code"
        ],
        "steps": [
            {
                "text": "Welcome to the CUDA tutorial!\n\nCUDA is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). With CUDA, developers are able to dramatically speed up computing applications by harnessing the power of GPUs.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "In CUDA, you write code that runs on both the CPU (the host) and the GPU (the device). The host code is standard C++ code, while the device code is written in a C++-like language with some extensions. The device code is what runs in parallel on the many cores of the GPU.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "type": "mcq",
                "text": "What is the difference between host code and device code?",
                "answers": [
                    "a) Host code runs on the GPU, and device code runs on the CPU.",
                    "b) Host code runs on the CPU, and device code runs on the GPU.",
                    "c) There is no difference."
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You have successfully learned the basics of CUDA!"
            }
        ]
    },
    "cuda_1_2": {
        "name": "Compiling and Running a CUDA Program",
        "description": "Learn how to compile and run a simple CUDA program.",
        "skills_learned": [
            "Compiling a CUDA program using nvcc",
            "Running a simple CUDA program"
        ],
        "steps": [
            {
                "text": "To compile a CUDA program, you use the NVIDIA CUDA Compiler (nvcc). nvcc is a compiler that can compile both host and device code.\n\nTo compile a CUDA program, you would typically use a command like this:\n\n`nvcc -o my_program my_program.cu`\n\nThis command compiles the file `my_program.cu` and creates an executable file called `my_program`. The `.cu` extension is used for CUDA source files.\n\nType `next` to continue.",
                "expected_command": "next"
            },
            {
                "text": "Let's simulate compiling and running a simple CUDA program. Type `nvcc -o hello_cuda hello_cuda.cu` to compile the program.",
                "expected_command": "nvcc -o hello_cuda hello_cuda.cu"
            },
            {
                "text": "Now that you have compiled the program, you can run it by typing `./hello_cuda`.",
                "expected_command": "./hello_cuda"
            },
            {
                "type": "mcq",
                "text": "What is the command to compile a CUDA program?",
                "answers": [
                    "a) gcc -o my_program my_program.c",
                    "b) nvcc -o my_program my_program.cu",
                    "c) python my_program.py"
                ],
                "correct_answer": "b",
                "final_step": True,
                "final_message": "You have successfully compiled and run a CUDA program!"
            }
        ]
    }
}
