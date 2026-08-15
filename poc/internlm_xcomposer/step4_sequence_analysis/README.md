# Step 4 — InternLM-XComposer-2.5 Sequence Analysis

This experiment evaluates whether InternLM-XComposer-2.5 can summarize a short learner-interaction sequence across multiple screenshots.

The same five learner-interaction screenshots used in the CogAgent experiment were provided to the model as an ordered sequence.

## Input Sequence

1. Correct selection of the red sphere
2. Incorrect selection of the blue cube
3. Repeated incorrect selection
4. Help-related interaction
5. Correct selection and activity completion

## Prompt

The model was asked to describe the learner's sequence of observable actions in order and identify:

- correct selections
- incorrect selections
- repeated mistakes
- help-related interaction
- task completion

The model was explicitly instructed not to infer cognitive load, confusion, stress, attention, emotion, or other internal cognitive states.

## Result

InternLM-XComposer-2.5 successfully captured the overall interaction sequence.

It identified:

- the initial correct interaction
- multiple incorrect interactions
- repeated mistakes
- the Help interaction
- eventual successful completion

The model also incorporated the visible incorrect-interaction feedback present behind the Help interface.

Compared with CogAgent's individual screenshot analysis, InternLM-XComposer-2.5 provided a more coherent representation of behavior across multiple frames.

## Technical Notes

The sequence was processed using five screenshots in a single multimodal prompt.

To reduce GPU memory usage during multi-image inference:

- `hd_num=4`
- `num_beams=1`
- eager attention was used instead of FlashAttention

The experiment was run on an NVIDIA A100-SXM4-80GB GPU.

## Output

The original model response is stored in:

`ixc_step4_results.json`

## Pipeline

Learner Interaction Sequence  
→ InternLM-XComposer-2.5  
→ Observable Sequence Summary
