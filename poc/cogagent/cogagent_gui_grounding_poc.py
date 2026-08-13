"""
NeuroTwin - CogAgent GUI Grounding Proof of Concept

This script demonstrates:
Screenshot -> CogAgent -> UI State Detection -> Action Selection
-> GUI Grounding -> Structured JSON Output
"""

import json
import os
import re
from datetime import datetime, timezone

import torch
from PIL import Image, ImageDraw
from transformers import AutoModelForCausalLM, AutoTokenizer


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_ID = "zai-org/cogagent-9b-20241220"

IMAGE_PATH = "examples/app_1.png"

OUTPUT_IMAGE = "outputs/grounded_app_1.png"
OUTPUT_JSON = "outputs/neurotwin_command.json"

TASK = """
Turn off screen recording permission for Microsoft Teams.

First inspect the Microsoft Teams permission toggle in the screenshot.
Determine whether the toggle is currently ON or OFF.

- If the Microsoft Teams toggle is ON, click the toggle to turn it OFF.
- If the Microsoft Teams toggle is already OFF, end the task.
"""


# =========================================================
# LOAD MODEL
# =========================================================

def load_cogagent():
    print("Loading CogAgent tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True
    )

    print("Loading CogAgent in BF16...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        device_map="cuda"
    ).eval()

    print("CogAgent loaded successfully.")

    return tokenizer, model


# =========================================================
# RUN INFERENCE
# =========================================================

def run_inference(model, tokenizer, image):

    query = (
        f"Task: {TASK}\n"
        "History steps:\n"
        "(Platform: Mac)\n"
        "(Answer in Status-Action-Operation format.)"
    )

    inputs = tokenizer.apply_chat_template(
        [{
            "role": "user",
            "image": image,
            "content": query
        }],
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True,
    ).to(model.device)

    print("Running inference...")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            top_k=1
        )

    new_tokens = outputs[:, inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        new_tokens[0],
        skip_special_tokens=True
    )

    return response


# =========================================================
# PARSE COGAGENT RESPONSE
# =========================================================

def parse_response(response):

    result = {
        "status": None,
        "action": None,
        "operation": None,
        "box": None,
        "element_info": None
    }

    status_match = re.search(
        r"Status:\s*(.*?)(?=\s*Action:|$)",
        response,
        re.DOTALL
    )

    if status_match:
        result["status"] = status_match.group(1).strip()

    action_match = re.search(
        r"Action:\s*(.*?)(?=\s*Grounded Operation:|$)",
        response,
        re.DOTALL
    )

    if action_match:
        result["action"] = action_match.group(1).strip()

    operation_match = re.search(
        r"Grounded Operation:\s*([A-Z]+)",
        response
    )

    if operation_match:
        result["operation"] = operation_match.group(1)

    box_match = re.search(
        r"box=\[\[(\d+),(\d+),(\d+),(\d+)\]\]",
        response
    )

    if box_match:
        result["box"] = [
            int(box_match.group(1)),
            int(box_match.group(2)),
            int(box_match.group(3)),
            int(box_match.group(4))
        ]

    element_match = re.search(
        r"element_info='([^']*)'",
        response
    )

    if element_match:
        result["element_info"] = element_match.group(1)

    return result


# =========================================================
# CREATE NEUROTWIN JSON COMMAND
# =========================================================

def create_neurotwin_command(parsed):

    box = parsed["box"]

    if box:
        center = [
            int((box[0] + box[2]) / 2),
            int((box[1] + box[3]) / 2)
        ]
    else:
        center = None

    return {
        "source": "CogAgent",
        "type": "ui_action",

        "state": {
            "description": parsed["status"]
        },

        "decision": {
            "action": parsed["action"]
        },

        "command": {
            "operation": (
                parsed["operation"].lower()
                if parsed["operation"]
                else None
            ),

            "target": {
                "element": parsed["element_info"],
                "bbox_1000": box,
                "center_1000": center
            }
        },

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


# =========================================================
# DRAW GROUNDING BOX
# =========================================================

def draw_grounding(image, box):

    if box is None:
        print("No bounding box returned by CogAgent.")
        return

    grounded_image = image.copy()

    # CogAgent coordinates are normalized to a 0-1000 space.
    x1 = int(box[0] / 1000 * image.width)
    y1 = int(box[1] / 1000 * image.height)
    x2 = int(box[2] / 1000 * image.width)
    y2 = int(box[3] / 1000 * image.height)

    draw = ImageDraw.Draw(grounded_image)

    draw.rectangle(
        [x1, y1, x2, y2],
        outline="red",
        width=5
    )

    grounded_image.save(OUTPUT_IMAGE)

    print("Grounded image saved to:", OUTPUT_IMAGE)


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():

    print("\n=== NeuroTwin CogAgent GUI Grounding PoC ===\n")

    os.makedirs("outputs", exist_ok=True)

    # Load model
    tokenizer, model = load_cogagent()

    # Load screenshot
    image = Image.open(IMAGE_PATH).convert("RGB")

    # CogAgent inference
    response = run_inference(
        model,
        tokenizer,
        image
    )

    print("\n=== COGAGENT RESPONSE ===\n")
    print(response)

    # Parse response
    parsed = parse_response(response)

    # Create structured command
    command = create_neurotwin_command(parsed)

    print("\n=== NEUROTWIN COMMAND ===\n")

    print(
        json.dumps(
            command,
            indent=2,
            ensure_ascii=False
        )
    )

    # Save JSON
    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            command,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\nJSON saved to:", OUTPUT_JSON)

    # Save grounding visualization
    draw_grounding(
        image,
        parsed["box"]
    )

    print("\nPoC completed successfully.")


if __name__ == "__main__":
    main()
