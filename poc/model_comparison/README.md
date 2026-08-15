# Step 6 — Model Comparison

This step compares CogAgent and InternLM-XComposer-2.5 (IXC) based on
their observations of the five learner-interaction examples and the
behavioral labels produced by the rule-based mapper in Step 5.

## Final Label Table

| Example | CogAgent Observation | IXC Observation | CogAgent Label | IXC Label |
|---|---|---|---|---|
| **1 — Correct interaction** | The learner has selected the red sphere, which is indicated by the green glow around it. | The learner selects a red sphere, which is correct, and the task progresses. | **Normal Process** | **Normal Process** |
| **2 — Incorrect interaction** | The learner has selected the blue cube instead of the red sphere. | In the second screenshot, the learner makes an incorrect selection, as indicated by the "Incorrect" message. The sphere selected is not the red one required for the task. | **Needs Support** | **Needs Support** |
| **3 — Repeated incorrect interaction** | The learner has selected the blue cube with a red outline, which is not the red sphere as instructed. | The third screenshot shows the learner making another incorrect selection, leading to another "Incorrect" message. | **Repeated Error** | **Repeated Error** |
| **4 — Help-seeking** | The learner has clicked on the red sphere in the center of the pop-up window, which is likely an element intended to close the pop-up or confirm understanding. | The fourth screenshot indicates that the learner has opened help options but still made an incorrect selection, resulting in yet another "Incorrect" message. | **Normal Process** | **Needs Support** |
| **5 — Activity completion** | The learner has selected the red sphere, which is highlighted with a green circle, and the task is marked as completed. | Finally, the fifth screenshot shows the learner selecting the correct red sphere, which is confirmed as correct with a "Correct!" message. | **Normal Process** | **Normal Process** |

The two models produced the same behavioral label for four of the five
examples.

The main disagreement occurred in Example 4. CogAgent did not correctly
identify the help-seeking interaction, while IXC recognized that the
learner had opened the help options.

---

## Comparison Criteria

| Comparison | CogAgent | IXC |
|---|---|---|
| **Object / UI recognition** | Gave clear identification of objects and UI elements. | Also identified the main elements correctly, but usually gave more general descriptions. |
| **Task outcome** | Could read the task instruction, but did not give a clear correct/incorrect classification when tested directly. | Clearly described correct and incorrect interactions and task completion. |
| **Incorrect / unsupported details** | In the help-seeking example, it misinterpreted the Help window as an interaction with the red sphere. | Correctly detected Help, but assumed that another incorrect selection happened after Help was opened. This sequence was not clearly supported by the screenshot alone. |
| **Computational cost** | Easier to run because one screenshot was processed at a time. | More computationally demanding. Multi-image inference initially exceeded the available GPU memory, so lower image/inference settings were required. |
| **Usefulness for NeuroTwin** | More useful for detailed analysis of individual UI interactions. | Better for understanding learner behavior across time. |

---

## Additional CogAgent Task-Aware Test

After the initial comparison, an additional test was performed to check
whether CogAgent could explicitly compare the task instruction with the
learner's action.

CogAgent successfully identified the task instruction:

> Task instruction: The task instruction is to 'Select the red sphere.'

However, instead of providing a correct/incorrect classification, it
returned:

> Grounded Operation: END()

A second, shorter task-aware prompt produced the same result.

This does not show that CogAgent is unable to understand whether an
interaction is correct. Instead, the tested CogAgent configuration did
not reliably produce an explicit task-outcome classification with these
prompts and tended to return to its grounded-operation output format.

---

## Main Findings

CogAgent was stronger in detailed object and UI-level descriptions.
It was useful for identifying which object or interface element was
involved in an individual screenshot.

IXC was more useful for interpreting the learner's behavior across
multiple screenshots. It identified correct and incorrect interactions,
repeated errors, help-seeking, and task completion across the sequence.

However, both models had limitations. CogAgent misinterpreted the
help-seeking example, while IXC added a sequential interpretation in the
same example that was not fully supported by the screenshot alone.

IXC also required more computational resources when multiple
high-resolution screenshots were processed together.

---

## Conclusion

Overall, InternLM-XComposer-2.5 was more useful for the current NeuroTwin
proof of concept.

The main goal of NeuroTwin in this experiment is not only to identify
individual UI elements, but to understand learner behavior across time.
IXC was more suitable for this because it could analyze multiple
screenshots as a sequence and identify behavioral patterns such as
repeated errors, help-seeking, and task progress.

CogAgent remains useful for detailed single-screen UI grounding, but
IXC was selected as the more suitable model for learner-behavior
interpretation at this stage of the project.

