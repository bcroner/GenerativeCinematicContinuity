using System;
using UnityEngine;
using UnityEngine.Rendering;

namespace GCC.Core
{
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
    }

    public class EnvironmentRenderNode : MonoBehaviour
    {
        [Header("Scene Hardware Targets")]
        [SerializeField] private Light masterDirectionalLight;
        [SerializeField] private AudioSource masterAmbienceSource;

        /// <summary>
        /// Entry-point to ingest network matrix data streams straight from Python server endpoints.
        /// </summary>
        public void ApplyNetworkRenderMatrix(string jsonPayload)
        {
            if (string.IsNullOrEmpty(jsonPayload)) return;

            try
            {
                RuntimeEnvironmentBlueprint blueprint = JsonUtility.FromJson<RuntimeEnvironmentBlueprint>(jsonPayload);
                MutateHardwareState(blueprint.render_parameters, blueprint.act);
            }
            catch (Exception ex)
            {
                Debug.LogError($"[GCC Graphics Exception] Matrix pipeline update breakdown: {ex.Message}");
            }
        }

        private void MutateHardwareState(RenderParameters parameters, int currentAct)
        {
            if (parameters == null) return;

            // 1. Dynamic Lighting Scalar Transformation Pass
            if (masterDirectionalLight != null)
            {
                masterDirectionalLight.intensity = parameters.lighting_intensity;
                // Transition lighting color spectrum dramatically to mimic dusk during late acts
                masterDirectionalLight.color = Color.Lerp(Color.white, new Color(0.85f, 0.4f, 0.2f), (currentAct - 1) / 2.0f);
            }

            // 2. Real-Time Atmospheric Particle Density Recalculations
            RenderSettings.fog = true;
            RenderSettings.fogMode = FogMode.ExponentialSquared;
            RenderSettings.fogDensity = parameters.fog_density;

            // 3. Audio Spectral Lowpass Filtering Override
            if (masterAmbienceSource != null)
            {
                AudioLowPassFilter filter = masterAmbienceSource.GetComponent<AudioLowPassFilter>();
                if (filter != null)
                {
                    filter.cutoffFrequency = parameters.audio_lowpass_cutoff_hz;
                }
            }

            Debug.Log($"[GCC Render Node Target Achieved]: Synced Atmosphere to Act {currentAct} Parameters Successfully.");
        }
    }
}
