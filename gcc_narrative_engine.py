"""
Generative Cinematic Continuity (GCC) - Core Narrative Engine & Validator
Handles batch ingestion of structural character JSON layouts and orchestrates 
advanced environment tracking matrices for downstream Unity 6 render nodes.
"""

import json
import os
import sys
from typing import Any, Dict, List


class CharacterArcModifier:
    def __init__(self, character_id: str, name: str, core_flaw: str, initial_stability: float, trauma_mult: float = 1.5, redemption_mult: float = 0.8):
        self.character_id = character_id
        self.name = name
        self.core_flaw = core_flaw
        self.stability = initial_stability
        self.trauma_multiplier = trauma_mult
        self.redemption_multiplier = redemption_mult

    def calculate_big_arc_shift(self, trauma_index: float, redemption_index: float) -> float:
        delta = -(trauma_index * self.trauma_multiplier) + (redemption_index * self.redemption_multiplier)
        self.stability = max(0.0, min(1.0, self.stability + delta))
        return self.stability


class AdvancedEnvironmentTracker:
    """
    Tracks and transforms fluid world-state variables into structural 
    render commands (lighting vectors, atmospheric densities, shader values).
    """
    def __init__(self):
        self.current_act = 1
        self.tension_level = 0.1
        self.matrix_state = {
            "lighting_intensity": 1.0,
            "fog_density": 0.01,
            "color_grading_lut": "LUT_Neutral.png",
            "audio_lowpass_cutoff_hz": 22000.0
        }

    def process_tension_shift(self, user_choice_severity: float) -> Dict[str, Any]:
        """
        Deterministic State Tracking Equations:
        As tension scales, environmental values adjust programmatically.
        """
        self.tension_level = max(0.0, min(1.0, self.tension_level + (user_choice_severity * 0.20)))
        
        # Act Threshold Transition Logic 
        if self.current_act == 1 and self.tension_level >= 0.4:
            self.current_act = 2
        elif self.current_act == 2 and self.tension_level >= 0.8:
            self.current_act = 3

        # Advanced Transform Calculations for Render Sockets
        self.matrix_state["lighting_intensity"] = max(0.2, 1.0 - (self.tension_level * 0.8))
        self.matrix_state["fog_density"] = min(0.08, 0.01 + (self.tension_level * 0.07))
        self.matrix_state["audio_lowpass_cutoff_hz"] = max(1200.0, 22000.0 - (self.tension_level * 18000.0))
        
        if self.current_act == 2:
            self.matrix_state["color_grading_lut"] = "LUT_PsychoTown_Dusk.png"
        elif self.current_act == 3:
            self.matrix_state["color_grading_lut"] = "LUT_PsychoTown_Crisis.png"

        return {
            "act": self.current_act,
            "tension": round(self.tension_level, 3),
            "render_parameters": self.matrix_state
        }


def load_character_profile_from_json(json_string_payload: str) -> CharacterArcModifier:
    data = json.loads(json_string_payload)
    bio = data["biographical_data"]
    state = data["initial_narrative_state"]
    weights = data["custom_formula_weights"]
    
    return CharacterArcModifier(
        character_id=data["character_id"],
        name=bio["name"],
        core_flaw=bio["core_flaw"],
        initial_stability=state["starting_stability_index"],
        trauma_mult=weights.get("trauma_multiplier", 1.5),
        redemption_mult=weights.get("redemption_multiplier", 0.8)
    )


def run_batch_profile_checks(directory_path: str) -> List[CharacterArcModifier]:
    """
    COMPANION TOOL: Scans an arbitrary file path directory, parses every 
    JSON file layout, and returns an array of verified character nodes.
    """
    valid_profiles = []
    print(f"\n[Batch Ingestion Active]: Scanning path '{directory_path}'...")
    
    if not os.path.exists(directory_path):
        print(f"  [Warning]: Target path '{directory_path}' missing. Creating template folder directory.")
        os.makedirs(directory_path, exist_ok=True)
        return valid_profiles

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".json"):
            full_path = os.path.join(directory_path, file_name)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    char_node = load_character_profile_from_json(content)
                    valid_profiles.append(char_node)
                    print(f"  -> [Success]: Verified Profile Layer: {char_node.name} (ID: {char_node.character_id})")
            except Exception as e:
                print(f"  -> [Compilation Failure]: Profile '{file_name}' layout invalid: {e}", file=sys.stderr)
                
    print(f"[Batch Complete]: Successfully initialized {len(valid_profiles)} active character structures.\n")
    return valid_profiles


if __name__ == "__main__":
    print("--- Firing Local Python GCC Master Engine Node ---")
    env_engine = AdvancedEnvironmentTracker()
    
    # Run batch loader across local testing directory target path
    loaded_cast = run_batch_profile_checks("./profiles")
    
    # Simulate a critical user decision loop pass
    print("[User Action Recorded]: Activating main city generator alarm.")
    rendered_output_blueprint = env_engine.process_tension_shift(user_choice_severity=2.5)
    
    print("\n[Compiled State Output Ready for Transmission to Unity 6]:")
    print(json.dumps(rendered_output_blueprint, indent=2))
