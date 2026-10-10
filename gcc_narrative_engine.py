"""
Generative Cinematic Continuity (GCC) - Core Narrative Engine & Server
Integrates a zero-dependency local REST API server via http.server to pipe
live environmental matrices directly to the Unity 6 graphics engine.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
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


# Global engine instance to persist data across network polling loops
GLOBAL_ENV_ENGINE = AdvancedEnvironmentTracker()

# =============================================================================
# NETWORK SERVER LAYER (REST ENDPOINT PROTOTYPE)
# =============================================================================
class GCCStreamingServer(BaseHTTPRequestHandler):
    """
    Handles local HTTP communication. Exposes a GET route to serve the 
    live environment tracking blueprint matrix directly to Unity 6.
    """
    def do_GET(self):
        if self.path == "/blueprint":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # Simulate a continuous narrative drift by introducing mild choice severity values per poll
            compiled_blueprint = GLOBAL_ENV_ENGINE.process_tension_shift(user_choice_severity=0.08)
            
            # Serialize and stream payload over the loopback socket channel
            response_data = json.dumps(compiled_blueprint)
            self.wfile.write(response_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Override to suppress standard console spam during fast polling intervals
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
    serve_pipeline()
