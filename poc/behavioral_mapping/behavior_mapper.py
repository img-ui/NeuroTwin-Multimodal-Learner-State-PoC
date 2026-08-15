import json


def assign_behavioral_label(
    task_progress=False,
    incorrect_interaction=False,
    repeated_error=False,
    help_requested=False,
    inactivity_threshold_exceeded=False,
):
    """
    Convert current observable learner-behavior evidence into one of:
    - Normal Process
    - Needs Support
    - Repeated Error

    Current behavior is prioritized over previous interaction history.
    """

    # Explicit help-seeking is the current action
    if help_requested:
        return "Needs Support"

    # Current interaction is the second/subsequent repeated error
    if repeated_error:
        return "Repeated Error"

    # No progress without a repeated-error event
    if incorrect_interaction or inactivity_threshold_exceeded:
        return "Needs Support"

    # Successful current progression/completion
    if task_progress:
        return "Normal Process"

    return "Unclassified"


def label_from_evidence(evidence):
    return assign_behavioral_label(
        task_progress=evidence.get("task_progress", False),
        incorrect_interaction=evidence.get("incorrect_interaction", False),
        repeated_error=evidence.get("repeated_error", False),
        help_requested=evidence.get("help_requested", False),
        inactivity_threshold_exceeded=evidence.get(
            "inactivity_threshold_exceeded", False
        ),
    )


with open("model_evidence.json", "r", encoding="utf-8") as f:
    examples = json.load(f)


for example in examples:
    cogagent_label = label_from_evidence(
        example["cogagent_evidence"]
    )

    ixc_label = label_from_evidence(
        example["ixc_evidence"]
    )

    print(f"\nExample {example['example']} — {example['scenario']}")
    print(f"CogAgent label: {cogagent_label}")
    print(f"IXC label:      {ixc_label}")
