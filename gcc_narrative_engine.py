"""
Generative Cinematic Continuity (GCC) - Core Narrative Engine
A foundational script for modifying the Big Arc Character Matrix and Three-Act Plot Lines.
Designed for creators, writers, and technical directors to build customized, persistent stories.
"""

from typing import Dict, List


class CharacterArcModifier:
    """
    Manages the 'Big Arc' formula for a character.
    Tracks internal conflict, alignment, and emotional vectors across a timeline.
    """
    def __init__(self, name: str, core_flaw: str, initial_stability: float):
        self.name = name
        self.core_flaw = core_flaw
        # Stability ranges from 0.0 (complete psychological collapse) to 1.0 (absolute composure)
        self.stability = initial_stability
        self.experience_log: List[str] = []

    def calculate_big_arc_shift(self, trauma_index: float, redemption_index: float) -> float:
        """
        The Customized Big Arc Formula:
        Stability_Next = Stability_Current - (Trauma * 1.5) + (Redemption * 0.8)
        Modulating these multipliers alters how resilient or fragile a character is to plot shifts.
        """
        modifier_constant = 1.5
        growth_constant = 0.8
        
        # Apply the narrative equation
        delta = -(trauma_index * modifier_constant) + (redemption_index * growth_constant)
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
        self.world_state: Dict[str, any] = {"environment_status": "baseline_normal"}

    def evaluate_plot_progression(self, user_choice_severity: float):
        """
        The Generative Three-Act Formula:
        Tension escalates relative to choice severity. If tension breaches an act's threshold,
        the system forces a milestone event, preserving narrative continuity.
        """
        # Escalate tension based on user-driven tangents
        self.tension_level = max(0.0, min(1.0, self.tension_level + (user_choice_severity * 0.25)))
        
        # Act Transition Logic Hooks
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
# PSYCHO TOWN SAMPLE LIVE SIMULATION RUN
# =============================================================================
if __name__ == "__main__":
    print("=================================================================")
    print("   GCC Engine initialized: Customizing the Cinematic Continuum  ")
    print("=================================================================\n")

    # 1. Instantiate our Psycho Town Lead Character
    # Let's track a protagonist with low baseline psychological stability
    character = CharacterArcModifier(name="Officer Miller", core_flaw="Paranoia", initial_stability=0.65)
    plot_director = ThreeActPlotManager(title="Psycho Town Scenario")

    print(f"Scenario Target: '{plot_director.title}' Loaded.")
    print(f"Initial State: {character.name} (Flaw: {character.core_flaw}) | Stability: {character.stability * 100}%\n")

    # 2. Simulate narrative progression based on user inputs/tangents
    # Step A: User investigates the old town outskirts (Low impact decision)
    print("[User Event]: Investigating town perimeter anomalies.")
    status_update = plot_director.evaluate_plot_progression(user_choice_severity=0.5)
    print(f"  -> System Response: {status_update}")
    
    # Step B: Trigger a Big Arc Shift using our formula
    # Character undergoes severe psychological trauma during the Act I climax
    new_stability = character.calculate_big_arc_shift(trauma_index=0.3, redemption_index=0.0)
    print(f"  -> Big Arc Shift: {character.name}'s mental stability drops to {new_stability * 100:.1f}%\n")

    # Step C: User executes a highly severe choice (Breaching the Climax Threshold)
    print("[User Event]: Activating the emergency town lockdown protocols.")
    status_update = plot_director.evaluate_plot_progression(user_choice_severity=1.8)
    print(f"  -> System Response: {status_update}")
    print(f"  -> Persistent World Environmental Matrix State: {plot_director.world_state}")

    print("\n=================== Narrative Cycle Finalized ===================")
