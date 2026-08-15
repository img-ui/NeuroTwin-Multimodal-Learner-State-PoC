def assign_behavioral_label(
    task_progress=False,
    incorrect_interaction=False,
    repeated_error=False,
    help_requested=False,
    inactivity_threshold_exceeded=False,
):
    """
    Convert observable learner-behavior evidence into one of the
    three NeuroTwin behavioral labels.

    Labels:
    - Normal Process
    - Needs Support
    - Repeated Error
    """

    if repeated_error:
        return "Repeated Error"

    if (
        incorrect_interaction
        or help_requested
        or inactivity_threshold_exceeded
    ):
        return "Needs Support"

    if task_progress:
        return "Normal Process"

    return "Unclassified"


examples = [
    {
        "example": 1,
        "observation": "Correct red sphere selected",
        "task_progress": True,
    },
    {
        "example": 2,
        "observation": "Incorrect blue cube selected",
        "incorrect_interaction": True,
    },
    {
        "example": 3,
        "observation": "Incorrect interaction repeated",
        "repeated_error": True,
    },
    {
        "example": 4,
        "observation": "Help interface opened",
        "help_requested": True,
    },
    {
        "example": 5,
        "observation": "Correct selection and activity completion",
        "task_progress": True,
    },
]


for example in examples:
    label = assign_behavioral_label(
        task_progress=example.get("task_progress", False),
        incorrect_interaction=example.get("incorrect_interaction", False),
        repeated_error=example.get("repeated_error", False),
        help_requested=example.get("help_requested", False),
        inactivity_threshold_exceeded=example.get(
            "inactivity_threshold_exceeded", False
        ),
    )

    print(
        f"Example {example['example']}: "
        f"{example['observation']} -> {label}"
    )
