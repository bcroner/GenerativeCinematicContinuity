# Generative Cinematic Continuity (GCC)

The next generation of gaming technology enhanced motion picture experiences. This repository serves as the definitive reference implementation for running high-fidelity dynamic narrative transformations and environmental state matrix synchronization pipelines.

## Project Workspace Directory Matrix

To ensure absolute system compiler integrity out of the box, map files locally using this exact folder pattern:

```text
GenerativeCinematicContinuity/
├── README.md
├── gcc_narrative_engine.py
├── profiles/
│   ├── officer_miller.json
│   └── companion_hudson.json
└── unity_project/
    └── Assets/
        └── Scripts/
            └── EnvironmentRenderNode.cs
```

---

## Low-Latency Environment Architecture Setup

The platform splits the workload into two decoupled operational execution tracks optimized to achieve zero-lag simulation feedback loops on modest local hardware configurations (such as standard modern consumer laptops).

### Track A: The Python Logic Core
- **Batch Verification Loop**: Loops through the `./profiles` folder path, dynamically testing character configuration syntax, error checking parameters, and booting multiple script entities onto data registers.
- **Advanced Simulation Tracking**: Translates complex, non-linear character matrix changes into an explicit JSON parameter ledger tracking real-time rendering changes (`render_parameters`).

### Track B: The Unity 6 Graphic Layer
- **Hardware Mutation Hooks**: Parses incoming network array tokens directly via `EnvironmentRenderNode.cs`. 
- **Dynamic Simulation Overrides**: Modulates lighting vectors, interpolates color grading look-up textures (LUTs), recalculates global atmospheric exponential fog thickness variables, and opens custom sound card audio lowpass filters on a frame-by-frame basis.

---

## Onboarding Execution Steps (Local Laptop Deployment)

Follow these directions to deploy and experience a live local proof-of-technology simulation run:

### Step 1: Initialize Character Profiles Data Layers
Create a directory path folder titled `profiles` directly alongside `gcc_narrative_engine.py` and populate it with custom text records. Example blueprint structure (`profiles/officer_miller.json`):

```json
{
  "character_id": "psycho_town_miller",
  "biographical_data": { "name": "Officer Miller", "assigned_role": "protagonist", "core_flaw": "Paranoia" },
  "initial_narrative_state": { "starting_stability_index": 0.65, "want_vector": "Conspiracy", "need_vector": "Acceptance" },
  "custom_formula_weights": { "trauma_multiplier": 1.8, "redemption_multiplier": 0.5 }
}
```

### Step 2: Spin Up the Main Automation Pipeline Server
Execute the master orchestration engine within your host system console workspace:
```bash
python gcc_narrative_engine.py
```
*The compiler tool will automatically check directories, parse your custom profile payload documents, execute the tension equation matrices, and map out structured vector commands ready for engine injection.*

### Step 3: Configure Scene Links in Unity 6
1. Drop the `EnvironmentRenderNode.cs` file directly into your active Project Assets folder hierarchy.
2. Instantiate a standard **Directional Light** and an ambient **Audio Source** node inside your scene tree.
3. Attach an **Audio Low Pass Filter** component directly to your ambient Audio Source GameObject.
4. Attach the `EnvironmentRenderNode` script asset to a persistent Master Scene Orchestration Node in your Hierarchy, and drag your light and audio nodes directly onto its open inspector configuration slot fields.
5. Link your local socket or WebRequest receiver engine to target the `ApplyNetworkRenderMatrix` method. As choices flow, the graphics pipeline will instantly transform world visual conditions with flawless, absolute continuity.
