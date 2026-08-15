# Step 5 — Behavioral Mapping


This step converts observable model outputs into three simple behavioral labels using deterministic rule-based mapping.

The purpose of this layer is not to infer the learner's internal cognitive or emotional state. Instead, observable interaction evidence extracted by the multimodal models is mapped to simple behavioral states that can later be used by the adaptive XR system.

## Behavioral Labels

| Label | Operational Definition |
|---|---|
| **Normal Process** | Correct interaction or successful task progression/completion. |
| **Needs Support** | No task progress without evidence of repeated error. This includes a single incorrect interaction, explicit help-seeking, or inactivity beyond a predefined task-specific threshold. |
| **Repeated Error** | Two or more consecutive/repeated incorrect interactions with the same task. |

## Mapping Logic

The current proof-of-concept uses the following deterministic rules:

1. Repeated incorrect interaction → **Repeated Error**
2. No task progress without repeated error → **Needs Support**
3. Successful task progress or completion → **Normal Process**

For the current five-example sequence:

| Example | Observable Behavior | Behavioral Label |
|---|---|---|
| 1 | Correct red sphere selection | Normal Process |
| 2 | Incorrect blue cube selection | Needs Support |
| 3 | Repeated incorrect interaction | Repeated Error |
| 4 | Help interface opened | Needs Support |
| 5 | Correct selection and activity completion | Normal Process |

## Inactivity Threshold

The inactivity threshold is not fixed at the current proof-of-concept stage.

In future validation, task-specific thresholds will be determined through a pilot study based on typical interaction times during successful task performance. This avoids selecting an arbitrary inactivity duration.

## Implementation

The mapping logic is implemented in:

`behavior_mapper.py`

The current pipeline is:

Model Output → Observable Behavioral Evidence → Rule-Based Mapping → Behavioral Label
