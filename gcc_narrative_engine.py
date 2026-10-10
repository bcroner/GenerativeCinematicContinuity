"""
Generative Cinematic Continuity (GCC) - Core Narrative Engine & Server
Authoritative execution script with expanded multi-dimensional character indexing 
and runtime behavioral modification logic blocks.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List


class CharacterArcModifier:
    """
    Tracks and modulates high-fidelity multi-dimensional character traits.
    Integrates psychological volatility and physical structural strain dynamically.
    """
    def __init__(
        self, 
        character_id: str, 
        name: str, 
        core_flaw: str, 
        initial_stability: float,
        volatility_rating: float,
        joint_integrity: float,
        trauma_mult: float = 1.5, 
        redemption_mult: float = 0.8
    ):
        self.character_id = character_id
        self.name = name
        self.core_flaw = core_flaw
        
        # Core Matrix Tracking Variabilities
        self.stability = initial_stability
        self.volatility_rating = volatility_rating
        self.hand_wrist_joint_integrity = joint_integrity
        
        # Formula Weight Constants
        self.trauma_multiplier = trauma_mult
        self.redemption_multiplier = redemption_mult

    def calculate_big_arc_shift(self, trauma_index: float, redemption_index: float) -> float:
        """
        The Expanded Big Arc Equation:
        Trauma impact scales exponentially relative to the character's unique volatility rating.
        Severe trauma over a 0.5 threshold simultaneously causes degradation to physical joint integrity.
        """
        # Volatility scales trauma exponentially: (1 + volatility_rating)
        effective_trauma = trauma_index * (1.0 + self.volatility_rating) * self.trauma_multiplier
        effective_redemption = redemption_index * self.redemption_multiplier
        
        # Execute character stability shift
        self.stability = max(0.0, min(1.0, self.stability - effective_trauma + effective_redemption))
        
        # Compute physical system strain side effects programmatically
        if trauma_index > 0.5:
            strain_damage = (trauma_index - 0.5) * 0.5
            self.hand_wrist_joint_integrity = max(0.0, self.hand_wrist_joint_integrity - strain_damage)
            
        return self.stability


class AdvancedEnvironmentTracker:
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
        self.tension_level = max(0.0, min(1.0, self.tension_level + (user_choice_severity * 0.15)))
        
        if self.current_act == 1 and self.tension_level >= 0.4:
            self.current_act = 2
        elif self.current_act == 2 and self.tension_level >= 0.8:
            self.current_act = 3

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


# Persistent instance tracking slots across network updates
GLOBAL_ENV_ENGINE = AdvancedEnvironmentTracker()
GLOBAL_ACTIVE_CAST: Dict[str, CharacterArcModifier] = {}

# =============================================================================
# DATA PIPELINE LAYER: EXTENDED PROFILE LOADER
# =============================================================================
def load_character_profile_from_json(json_string_payload: str) -> CharacterArcModifier:
    """
    Parses an expanded high-fidelity JSON blueprint string and generates 
    a functional, reactive runtime CharacterArcModifier node.
    """
    data = json.loads(json_string_payload)
    
    bio = data["biographical_data"]
    psych = data["psychological_traits_matrix"]
    phys = data["physical_integrity_constraints"]
    align = data["narrative_alignment_vectors"]
    weights = data["custom_formula_weights"]
    
    return CharacterArcModifier(
        character_id=data["character_id"],
        name=bio["name"],
        core_flaw=bio["core_flaw"],
        initial_stability=align["starting_stability_index"],
        volatility_rating=psych["volatility_rating"],
        joint_integrity=phys["hand_wrist_joint_integrity"],
        trauma_mult=weights.get("trauma_multiplier", 1.5),
        redemption_mult=weights.get("redemption_multiplier", 0.8)
    )


class GCCStreamingServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/blueprint":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # Continuous delta drift loop execution mock
            compiled_blueprint = GLOBAL_ENV_ENGINE.process_tension_shift(user_choice_severity=0.05)
            
            # Inject dynamic updates from the active cast characters if tracked
            if "psycho_town_miller" in GLOBAL_ACTIVE_CAST:
                miller = GLOBAL_ACTIVE_CAST["psycho_town_miller"]
                # Simulate progressive wear across active scenes
                miller.calculate_big_arc_shift(trauma_index=0.01, redemption_index=0.0)
                compiled_blueprint["character_state_delta"] = {
                    "id": miller.character_id,
                    "stability": round(miller.stability, 4),
                    "wrist_joint_integrity": round(miller.hand_wrist_joint_integrity, 4)
                }

            response_data = json.dumps(compiled_blueprint)
            self.wfile.write(response_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def serve_pipeline(port: int = 8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, GCCStreamingServer)
    print(f"[GCC Server Armed]: Hosting local REST stream loop on -> http://localhost:{port}/blueprint")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[GCC Server]: Shutting down network socket layers safely.")
        httpd.server_close()


if __name__ == "__main__":
    print("--- Initializing Local Python GCC Master Engine Node ---")
    
    # Pre-loading mock instance data for Officer Miller to initialize values
    mock_payload = """
    {
      "character_id": "psycho_town_miller",
      "biographical_data": { "name": "Officer Miller", "assigned_role": "protagonist", "core_flaw": "Severe Paranoia" },
      "psychological_traits_matrix": { "isolation_index": 0.92, "intellectual_curiosity_weight": 0.85, "volatility_rating": 0.40 },
      "physical_integrity_constraints": { "hand_wrist_joint_integrity": 0.75, "cardio_reserve_index": 0.80 },
      "narrative_alignment_vectors": { "starting_stability_index": 0.65, "manifest_want_declaration": "Expose Coverup", "latent_need_matrix": "Grief" },
      "custom_formula_weights": { "trauma_multiplier": 1.8, "redemption_multiplier": 0.5 }
    }
    """
    
    # Store reference into core runtime registers
    print("[Ingestion]: Loading and parsing high-fidelity character matrix payload...")
    GLOBAL_ACTIVE_CAST["psycho_town_miller"] = load_character_profile_from_json(mock_payload)
    
    # Fire up communications
    serve_pipeline()
