using System;
using UnityEngine;

namespace GCC.Core
{
    // =========================================================================
    // SERIALIZABLE DATA SCHEMAS (Expanded Matrix Path Tracking Blocks)
    // =========================================================================
    [Serializable]
    public class CharacterStateDelta
    {
        public string id;
        public float stability;
        public float wrist_joint_integrity;
    }

    [Serializable]
    public class RenderParameters
    {
        public float lighting_intensity;
        public float fog_density;
        public string color_grading_lut;
        public float audio_lowpass_cutoff_hz;
    }

    [Serializable]
    public class RuntimeEnvironmentBlueprint
    {
        public int act;
        public float tension;
        public RenderParameters render_parameters;
        public CharacterStateDelta character_state_delta; // The newly integrated field block
    }

    // =========================================================================
    // MULTI-TRACK RUNTIME PROCESSING GRAPHICS ENGINE NODE
    // =========================================================================
    public class EnvironmentRenderNode : MonoBehaviour
    {
        [Header("Scene Hardware Sockets")]
        [SerializeField] private Light masterDirectionalLight;
        [SerializeField] private AudioSource masterAmbienceSource;

        [Header("Character Bone & Post-FX Rig Anchors")]
        [SerializeField] private Transform characterRightHandWristTransform;
        [SerializeField] private UnityEngine.Rendering.Volume postProcessingVolume;

        /// <summary>
        /// Entry-point to ingest network matrix data streams straight from the Python daemon.
        /// </summary>
        public void ApplyNetworkRenderMatrix(string jsonPayload)
        {
            if (string.IsNullOrEmpty(jsonPayload)) return;

            try
            {
                RuntimeEnvironmentBlueprint blueprint = JsonUtility.FromJson<RuntimeEnvironmentBlueprint>(jsonPayload);
                
                // 1. Map Global Environmental Track Changes
                MutateHardwareState(blueprint.render_parameters, blueprint.act);
                
                // 2. Parse and Execute Individual Character Vector Injections
                if (blueprint.character_state_delta != null)
                {
                    MutateCharacterRuntimePhysics(blueprint.character_state_delta);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[GCC Graphics Exception] Matrix pipeline update breakdown: {ex.Message}");
            }
        }

        private void MutateHardwareState(RenderParameters parameters, int currentAct)
        {
            if (parameters == null) return;

            // Global Environmental Modulations
            if (masterDirectionalLight != null)
            {
                masterDirectionalLight.intensity = parameters.lighting_intensity;
                masterDirectionalLight.color = Color.Lerp(Color.white, new Color(0.85f, 0.4f, 0.2f), (currentAct - 1) / 2.0f);
            }

            RenderSettings.fog = true;
            RenderSettings.fogMode = FogMode.ExponentialSquared;
            RenderSettings.fogDensity = parameters.fog_density;

            if (masterAmbienceSource != null)
            {
                AudioLowPassFilter filter = masterAmbienceSource.GetComponent<AudioLowPassFilter>();
                if (filter != null)
                {
                    filter.cutoffFrequency = parameters.audio_lowpass_cutoff_hz;
                }
            }
        }

        private void MutateCharacterRuntimePhysics(CharacterStateDelta delta)
        {
            Debug.Log($"[GCC Character Delta Synced]: Target ID: {delta.id}");

            // Track A: Map Psychological Stability to Screen Space Post-Processing Visual Filters
            if (postProcessingVolume != null && postProcessingVolume.profile != null)
            {
                // Dynamic mapping demonstration: Lower stability introduces custom post-FX weight saturation shifts
                // (e.g., pulling down rendering color saturations to represent shock/tunnel vision)
                float stressWeightScalar = 1.0f - delta.stability; 
                postProcessingVolume.weight = Mathf.Clamp01(stressWeightScalar);
            }

            // Track B: Map Hand/Wrist Joint Integrity directly into Bone Transform Spatial Scales or Limits
            if (characterRightHandWristTransform != null)
            {
                // Degrade physical spatial scaling to reflect joint strain failures programmatically
                float integrityScale = Mathf.Clamp(delta.wrist_joint_integrity, 0.1f, 1.0f);
                
                // Directly alters the geometric bone cluster transform parameters in the scene graph 
                characterRightHandWristTransform.localScale = new Vector3(integrityScale, integrityScale, integrityScale);
                
                Debug.Log($" -> Joint Strain Track Resolved. Bone transform constraints scaled to: {integrityScale * 100f}%");
            }
        }
    }
}
