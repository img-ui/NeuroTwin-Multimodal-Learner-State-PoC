# NeuroTwin-Multimodal-Learner-State-PoC
Proof of concept for multimodal learner interaction interpretation using CogAgent and InternLM-XComposer-2.5 for our NeuroTwin project

## Overview

This repository contains a part of proof of concept for the NeuroTwin project.

The goal of this experiment was to investigate whether multimodal vision-language models can extract useful interaction evidence from learner-interface screenshots and whether this evidence can later be converted into simple behavioral labels.

Two models were tested:

- **CogAgent** — mainly for detailed single-screen UI and interaction analysis.
- **InternLM-XComposer-2.5 (IXC)** — for multi-image sequence understanding.

The models were not used to directly infer cognitive load, confusion, stress, attention, emotion, or other internal cognitive states.

Instead, the PoC follows the pipeline:

**Learner interaction → Visual evidence → Model observation → Rule-based behavioral mapping**

---

## Models

### CogAgent

CogAgent was tested primarily as a single-image UI understanding model.

It was first tested on a GUI-grounding example to verify that the model could process interface screenshots and identify interface interactions.

It was then applied independently to five NeuroTwin learner-interaction screenshots.

CogAgent generally produced detailed descriptions of individual objects and UI interactions.

### InternLM-XComposer-2.5

InternLM-XComposer-2.5 was tested on the learner screenshots as a sequence.

Instead of treating every screenshot independently, IXC received the ordered interaction sequence and was asked to describe observable changes in learner behavior and task progress.

This allowed the model to use temporal context when interpreting the interaction.

---

## Experimental Examples

Five simple learner-interaction cases were used:

| Example | Interaction |
|---|---|
| 1 | Correct interaction |
| 2 | Incorrect interaction |
| 3 | Repeated incorrect interaction |
| 4 | Help-seeking |
| 5 | Activity completion |

These examples were designed as a small controlled test of whether the models could extract evidence relevant to learner behavior.

---

## Behavioral Mapping

Model observations were converted into simple behavioral labels using deterministic rules.

The models themselves were not asked to directly predict psychological or cognitive states.

The final behavioral labels used in the PoC were:

- **Normal Process**
- **Needs Support**
- **Repeated Error**

This separation keeps the visual interpretation stage and the behavioral decision stage distinct.

Conceptually:

```text
Screenshot / Interaction Sequence
            ↓
      Multimodal Model
            ↓
    Observable Evidence
            ↓
    Rule-Based Mapping
            ↓
      Behavioral Label
````

---

## Results

The two models produced the same behavioral label for four of the five examples.

| Example                        | CogAgent       | IXC            |
| ------------------------------ | -------------- | -------------- |
| Correct interaction            | Normal Process | Normal Process |
| Incorrect interaction          | Needs Support  | Needs Support  |
| Repeated incorrect interaction | Repeated Error | Repeated Error |
| Help-seeking                   | Normal Process | Needs Support  |
| Activity completion            | Normal Process | Normal Process |

The main disagreement occurred in the help-seeking example.

CogAgent did not correctly interpret the Help interface and instead described an correct interaction with the red sphere.

IXC correctly detected that the learner had opened the help options. However, it also introduced a stronger sequential interpretation by suggesting that another incorrect selection occurred after Help was opened, which was not clearly supported by the screenshot.

---

## Model Comparison

### CogAgent

**Strengths**

* Detailed object-level descriptions
* Useful for individual UI interactions
* Stronger emphasis on visual grounding
* Lower computational requirements when processing screenshots individually

**Limitations**

* Limited temporal context when screenshots are processed independently
* Misinterpreted the help-seeking example
* A separate task-aware test did not reliably produce an explicit correct/incorrect classification and instead returned a grounded-operation output (`END()`)

### InternLM-XComposer-2.5

**Strengths**

* Can process multiple screenshots as an interaction sequence
* Better representation of task progression across time
* Correctly detected the help-seeking interaction
* Useful for identifying repeated behavioral patterns

**Limitations**

* More computationally demanding
* Multi-image inference initially exceeded available GPU memory
* Required reduced image/inference settings
* Can introduce temporal interpretations that are stronger than the visual evidence alone supports

---

## Main Finding

For the current NeuroTwin proof of concept, **InternLM-XComposer-2.5 was more useful for learner-behavior interpretation**.

CogAgent was useful for detailed analysis of individual interface interactions, while IXC was better suited to understanding how learner behavior changed across a sequence of screenshots.

Because NeuroTwin ultimately aims to interpret learner behavior over time rather than only identify isolated UI elements, sequence-level multimodal analysis appears more suitable for the next stage of the project.

This conclusion is limited to the small controlled PoC presented here and should not be interpreted as a general benchmark comparison between the two models.

---

## Repository Contents

```text
NeuroTwin/
│
├── cogagent_poc.ipynb
├── internlm_xcomposer_poc.ipynb
├── behavioral_mapper.py
├── README.md
└── [experiment outputs / supporting files]
```

### `cogagent_poc.ipynb`

Contains the CogAgent setup, GUI-grounding test, and learner-interaction screenshot experiments.

### `internlm_xcomposer_poc.ipynb`

Contains the InternLM-XComposer-2.5 setup, single-image sanity check, multi-image learner sequence analysis, and resulting model output.

### `behavioral_mapper.py`

Contains the deterministic mapping logic used to convert observable interaction evidence into simple behavioral labels.

---

## Technical Notes

The experiments were conducted in Google Colab.

Because both models are relatively large, GPU memory was an important practical constraint.

CogAgent was primarily evaluated using individual screenshots.

For IXC, processing all five screenshots together required reduced inference settings to fit within the available GPU memory.

Model weights are not included in this repository.

---

## Limitations

This is a small proof of concept rather than a validated learner-state estimation system.

The experiment uses only five controlled examples and does not provide evidence that the models can reliably infer cognitive states in real learning environments.

The current behavioral labels are based on manually defined rules.
