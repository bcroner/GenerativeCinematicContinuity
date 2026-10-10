# Creative Guide: Customizing the GCC Narrative Formula

Welcome to the **Generative Cinematic Continuity (GCC)** framework! This guide is written specifically for authors, screenwriters, narrative directors, and world-builders. You do not need a degree in Computer Science to modify how stories adapt on this platform. 

By tweaking a few baseline numbers in our engine, you can completely redefine how characters evolve and how plot arcs escalate based on real-time user choices.

---

## 1. The Big Arc Character Matrix

Traditional media forces a character down a fixed path of change. GCC tracks a character's internal state mathematically using a fluctuating value called **Stability** (scaled from `0.0` or total psychological breakdown to `1.0` or perfect mental composure).

### The Standard Equation
Whenever a story event occurs, the engine processes this specific rule:

\[\text{Stability}_{\text{Next}} = \text{Stability}_{\text{Current}} - (\text{Trauma} \times 1.5) + (\text{Redemption} \times 0.8)\]

### How to Tweak the Math
Open `gcc_narrative_engine.py` and locate the `calculate_big_arc_shift` function. You can alter the core constants to change the flavor of your story:

*   **The Grit Modifier (`1.5`)**: This dictates how heavily a tragic event impacts your character. 
    *   *Want a gritty psychological horror where characters break easily?* Raise this number to `2.5` or higher.
    *   *Want a lighthearted adventure or a resilient superhero story?* Drop this down to `0.5`.
*   **The Hope Coefficient (`0.8`)**: This dictates how easily a character bounces back after finding peace, safety, or redemption.
    *   *Want a cynical, unforgiving world?* Lower this to `0.2`.
    *   *Want an inspiring, highly optimistic redemptive arc?* Raise this multiplier to `1.5`.

---

## 2. The Three-Act Plot Manager

The engine ensures the story still hits structural cinematic milestones by tracking a dynamic global variable called the **Tension Level** (`0.0` to `1.0`).

### Understanding Act Thresholds
Instead of a timer or a fixed page count, acts transition when the user's combined actions drive global tension past explicit gates:
*   **Act I \(\rightarrow\) Act II Threshold (`0.4`)**: The story crosses into the confrontation phase when tension hits `40%`. This triggers your Inciting Incident.
*   **Act II \(\rightarrow\) Act III Threshold (`0.8`)**: The story locks into the final climax when tension reaches `80%`.

### Customizing Pacing
In the `evaluate_plot_progression` method, you can shift these decimals:
*   **Slow-Burn/Procedural Drama**: Set the Act I threshold to `0.6` and the Act II threshold to `0.9`. This gives the viewer a long, detailed setup to explore nuances before the chaos breaks.
*   **Action/High-Octane Thriller**: Drop the Act I threshold to `0.2` and Act II to `0.5`. The world will plunge into permanent crisis almost immediately based on minimal user provocation.
