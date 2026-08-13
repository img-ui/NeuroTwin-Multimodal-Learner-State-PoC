
# CogAgent GUI Grounding PoC

This proof of concept demonstrates whether CogAgent can inspect a GUI screenshot, recognize the current interface state, select an appropriate action, and visually ground the target UI element.

## Pipeline

Screenshot  
→ CogAgent  
→ UI state recognition  
→ Action selection  
→ Grounded GUI operation  
→ Structured NeuroTwin JSON command

## Model

- Model: `zai-org/cogagent-9b-20241220`
- Precision: BF16
- GPU used: NVIDIA A100-SXM4-80GB
- Transformers: 4.47.1

## Test Task

The input screenshot shows the macOS:

`Privacy & Security → Screen & System Audio Recording`

The task given to CogAgent was:

> Turn off screen recording permission for Microsoft Teams.

The prompt explicitly asked CogAgent to first determine whether the Microsoft Teams toggle was ON or OFF.

## Result

CogAgent correctly identified that the Microsoft Teams screen recording permission was ON.

It generated the following action:

> Click the toggle switch next to Microsoft Teams to turn off the screen recording permission.

It also grounded the correct UI element:

```text
CLICK(box=[[857,367,908,397]], element_info='[AXGroup]')
````

The predicted bounding box correctly overlaps the Microsoft Teams toggle in the screenshot.

## Files

* `cogagent_gui_grounding_poc.py` — complete inference and parsing pipeline
* `examples/app_1.png` — input screenshot
* `outputs/grounded_app_1.png` — screenshot with the predicted bounding box
* `outputs/neurotwin_command.json` — structured command generated from CogAgent output

## Example Structured Output

```json
{
  "source": "CogAgent",
  "type": "ui_action",
  "state": {
    "description": "The Microsoft Teams toggle is currently on."
  },
  "decision": {
    "action": "Click the toggle switch next to Microsoft Teams to turn off the screen recording permission."
  },
  "command": {
    "operation": "click",
    "target": {
      "element": "[AXGroup]",
      "bbox_1000": [857, 367, 908, 397],
      "center_1000": [882, 382]
    }
  }
}
```

## Notes

An earlier shorter prompt caused the model to incorrectly conclude that the task was already completed. Adding an explicit state-inspection step allowed CogAgent to correctly identify the toggle state and produce the correct grounded action.

This PoC confirms that CogAgent can be used as the GUI-understanding and grounding component of the NeuroTwin pipeline.
