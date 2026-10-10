"""
Generative Cinematic Continuity (GCC) - Core Narrative Engine
A foundational script for modifying the Big Arc Character Matrix and Three-Act Plot Lines.
Includes a native JSON validation and profiling pipeline for data-driven writers.
"""

import json
from typing import Any, Dict, List


class CharacterArcModifier:
    """
    Manages the 'Big Arc' formula for a character.
    Tracks internal conflict, alignment, and emotional vectors across a timeline.
    """
    def __init__(self, character_id: str, name: str, core_flaw: str, initial_stability: float, trauma_mult: float = 1.5, redemption_mult: float = 0.8):
        self.character_id = character_id
        self.name = name
        self.core_flaw = core_flaw
        # Stability ranges from 0.0 (complete psychological collapse) to 1.0 (absolute composure)
        self.stability = initial_stability
        self.trauma_multiplier = trauma_mult
        self.redemption_multiplier = redemption_mult

    def calculate_big_arc_shift(self, trauma_index: float, redemption_index: float) -> float:
        """
        The Customized Big Arc Formula:
        Stability_Next = Stability_Current - (Trauma * trauma_multiplier) + (Redemption * redemption_multiplier)
        """
        delta = -(trauma_index * self.trauma_multiplier) + (redemption_index * self.redemption_multiplier)
        self.stability = max(0.0, min(1.0, self.stability + delta))
        return self.stability


class ThreeActPlotManager:
    """
    Maintains structural cinematic continuity across explicit plot boundaries.
    Maps out tension thresholds and triggers transitions dynamically.
    """
    def __init__(self, title: str):
        self.title = title
        self.current_act = 1
        self.tension_level = 0.1  # Ranges from 0.0 to 1.0
        self.world_state: Dict[str, Any] = {"environment_status": "baseline_normal"}

    def evaluate_plot_progression(self, user_choice_severity: float) -> str:
        """
        The Generative Three-Act Formula:
        Tension escalates relative to choice severity. If tension breaches an act's threshold,
        the system forces a milestone event, preserving narrative continuity.
        """
        self.tension_level = max(0.0, min(1.0, self.tension_level + (user_choice_severity * 0.25)))
        
        if self.current_act == 1 and self.tension_level >= 0.4:
            self.current_act = 2
            self.world_state["environment_status"] = "destabilized_inciting_incident"
            return "PLOT SHIFT: Entering Act II (The Confrontation). The environment has permanently altered."
            
        elif self.current_act == 2 and self.tension_level >= 0.8:
            self.current_act = 3
            self.world_state["environment_status"] = "critical_climax_active"
            return "PLOT SHIFT: Entering Act III (The Climax). All narrative paths converge on resolution."
            
        return f"Continuity Maintained. Current Act: {self.current_act} | Tension Index: {self.tension_level:.2f}"


# =============================================================================
# DATA PIPELINE LAYER: PROFILE LOADER FUNCTION
# =============================================================================
def load_character_profile_from_json(json_string_payload: str) -> CharacterArcModifier:
    """
    Parses a standardized GCC structural JSON profile layout text string 
    and instantiates a live runtime CharacterArcModifier simulation node.
    """
    data = json.loads(json_string_payload)
    
    # Extract metadata properties from the structural JSON schema layout paths
    char_id = data["character_id"]
    bio = data["biographical_data"]
    state = data["initial_narrative_state"]
    weights = data["custom_formula_weights"]
    
    return CharacterArcModifier(
        character_id=char_id,
        name=bio["name"],
        core_flaw=bio["core_flaw"],
        initial_stability=state["starting_stability_index"],
        trauma_mult=weights.get("trauma_multiplier", 1.5),
        redemption_mult=weights.get("redemption_multiplier", 0.8)
    )


# =============================================================================
# PSYCHO TOWN SAMPLE LIVE SIMULATION RUN
# =============================================================================
if __name__ == "__main__":
    print("=================================================================")
    print("   GCC Engine Initialized: Customizing the Cinematic Continuum  ")
    print("=================================================================\n")

    # Mock instance string matching the 'profiles/officer_miller.json' file layout
    mock_json_file_contents = """
    {
      "character_id": "psycho_town_miller",
      "biographical_data": {
        "name": "Officer Miller",
        "assigned_role": "protagonist",
        "core_flaw": "Paranoia"
      },
      "initial_narrative_state": {
        "starting_stability_index": 0.65,
        "want_vector": "Expose the town conspiracy",
        "need_vector": "Accept personal loss"
      },
      "custom_formula_weights": {
        "trauma_multiplier": 1.8,
        "redemption_multiplier": 0.5
      }
    }
    """

    # 1. Execute the Profile Loader pipeline step
    print("[Pipeline Ingestion]: Parsing character payload json layout stream...")
    character = load_character_profile_from_json(mock_json_file_contents)
    plot_director = ThreeActPlotManager(title="Psycho Town Scenario")

    print(f"Scenario Target: '{plot_director.title}' Loaded.")
    print(f"Loaded Identity: {character.name} (ID: {character.character_id})")
    print(f"  -> Initial Stability Index: {character.stability * 100:.1f}%")
    print(f"  -> Custom Formula Weights Applied: [Trauma Multiplier: {character.trauma_multiplier}x, Redemption: {character.redemption_multiplier}x]\n")

    # 2. Simulate choices triggering the customized equation tracks
    print("[User Event]: Investigating town perimeter anomalies.")
    status_update = plot_director.evaluate_plot_progression(user_choice_severity=0.5)
    print(f"  -> System Response: {status_update}")
    
    # Run a mathematical transition pass using Miller's custom 1.8x multiplier
    new_stability = character.calculate_big_arc_shift(trauma_index=0.2, redemption_index=0.0)
    print(f"  -> Character Emotional Arc Drift: {character.name}'s stability dropped to {new_stability * 100:.1f}%")

    print("\n=================== Narrative Cycle Finalized ===================")
