using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

namespace GCC.Core
{
    // =========================================================================
    // SERIALIZABLE DATA SCHEMAS (Matches Python Broker Payload Definitions)
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
    public class AddressableVisualSpecs
    {
        public string mesh_source;       
        public string shader_variant;
        public string emissive_color_hex;
    }

    [Serializable]
    public class ScientificAssetPayload
    {
        public string id;
        public string type;
        public AddressableVisualSpecs visuals;
    }

    [Serializable]
    public class RuntimeEnvironmentBlueprint
    {
        public int act;
        public float tension;
        public RenderParameters render_parameters;
        public CharacterStateDelta character_state_delta;
        public List<ScientificAssetPayload> payload;
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

        [Header("Spawn Anchorage")]
        [SerializeField] private Transform sceneInstantiationAnchor;

        // Tracks active allocated elements inside memory to block run-away leaks
        private Dictionary<string, GameObject> activeInstantiatedAssets = new Dictionary<string, GameObject>();

        /// <summary>
        /// Primary entry-point to ingest network matrix data streams straight from the Python daemon.
        /// </summary>
        public void ApplyNetworkRenderMatrix(string jsonPayload)
        {
            if (string.IsNullOrEmpty(jsonPayload)) return;

            try
            {
                RuntimeEnvironmentBlueprint blueprint = JsonUtility.FromJson<RuntimeEnvironmentBlueprint>(jsonPayload);
                
                // Track 1: Map Global Environmental Atmospheric Variables
                if (blueprint.render_parameters != null)
                {
                    MutateHardwareState(blueprint.render_parameters, blueprint.act);
                }
                
                // Track 2: Parse and Execute Individual Character Vector Injections
                if (blueprint.character_state_delta != null)
                {
                    MutateCharacterRuntimePhysics(blueprint.character_state_delta);
                }

                // Track 3: Run High-Speed Asynchronous Addressable Instantiations
                if (blueprint.payload != null)
                {
                    ProcessProductionPayload(blueprint.payload, blueprint.character_state_delta);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[GCC Graphics Exception] Matrix pipeline update breakdown: {ex.Message}");
            }
        }

        private void MutateHardwareState(RenderParameters parameters, int currentAct)
        {
            // Global Environmental Modulations
            if (masterDirectionalLight != null)
            {
                masterDirectionalLight.intensity = parameters.lighting_intensity;
                // Transition lighting color spectrum dramatically to mimic dusk during late acts
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
            // Sub-Track A: Map Psychological Stability to Screen-Space Post-Processing Volume Weight
            if (postProcessingVolume != null)
            {
                // Lower stability introduces custom post-FX weight saturation shifts (simulating tunnel vision/shock)
                float stressWeightScalar = 1.0f - delta.stability; 
                postProcessingVolume.weight = Mathf.Clamp01(stressWeightScalar);
            }

            // Sub-Track B: Map Wrist Joint Integrity directly into Bone Transform Spatial Scale
            if (characterRightHandWristTransform != null)
            {
                // Degrade local spatial scaling to reflect joint strain metrics programmatically
                float integrityScale = Mathf.Clamp(delta.wrist_joint_integrity, 0.1f, 1.0f);
                characterRightHandWristTransform.localScale = new Vector3(integrityScale, integrityScale, integrityScale);
            }

            // Sub-Track C: Push Dynamic Values to Custom Shaders in Active Scene Objects
            foreach (var spawnedObject in activeInstantiatedAssets.Values)
            {
                if (spawnedObject != null)
                {
                    ApplyShaderMaterialDistortion(spawnedObject, delta.stability);
                }
            }
        }

        private void ProcessProductionPayload(List<ScientificAssetPayload> payload, CharacterStateDelta delta)
        {
            foreach (var node in payload)
            {
                if (node.visuals == null || string.IsNullOrEmpty(node.visuals.mesh_source)) continue;
                if (activeInstantiatedAssets.ContainsKey(node.id)) continue;

                Debug.Log($"[GCC Addressables Bridge]: Loading asynchronous asset key: {node.visuals.mesh_source}");
                
                Addressables.InstantiateAsync(node.visuals.mesh_source, sceneInstantiationAnchor).Completed += (handle) =>
                {
                    if (handle.Status == AsyncOperationStatus.Succeeded)
                    {
                        GameObject spawnedObject = handle.Result;
                        activeInstantiatedAssets.Add(node.id, spawnedObject);
                        
                        // Apply static visual parameters and configure initial material properties
                        ApplyRuntimeMaterialModifiers(spawnedObject, node.visuals);
                        
                        // Push initial character context parameters to vertex shader uniforms instantly
                        if (delta != null)
                        {
                            ApplyShaderMaterialDistortion(spawnedObject, delta.stability);
                        }
                    }
                    else
                    {
                        Debug.LogWarning($"[GCC Addressables Warning]: Unable to resolve runtime mesh pointer key for: {node.visuals.mesh_source}");
                    }
                };
            }
        }

        private void ApplyRuntimeMaterialModifiers(GameObject targetObject, AddressableVisualSpecs visuals)
        {
            if (string.IsNullOrEmpty(visuals.emissive_color_hex)) return;

            Renderer meshRenderer = targetObject.GetComponentInChildren<Renderer>();
            if (meshRenderer != null && ColorUtility.TryParseHtmlString(visuals.emissive_color_hex, out Color parsedColor))
            {
                MaterialPropertyBlock propertyBlock = new MaterialPropertyBlock();
                propertyBlock.SetColor("_EmissionColor", parsedColor);
                meshRenderer.SetPropertyBlock(propertyBlock);
            }
        }

        private void ApplyShaderMaterialDistortion(GameObject targetObject, float stabilityValue)
        {
            Renderer meshRenderer = targetObject.GetComponentInChildren<Renderer>();
            if (meshRenderer != null)
            {
                MaterialPropertyBlock propertyBlock = new MaterialPropertyBlock();
                meshRenderer.GetPropertyBlock(propertyBlock);
                // Sets the explicit shader uniform flag targeting our vertex wave and desaturation logic bounds
                propertyBlock.SetFloat("_Stability", stabilityValue);
                meshRenderer.SetPropertyBlock(propertyBlock);
            }
        }

        private void OnDestroy()
        {
            // Explicit clean up routines targeting active memory pool allocations to guarantee zero leakages
            foreach (var spawnedAsset in activeInstantiatedAssets.Values)
            {
                if (spawnedAsset != null) Addressables.ReleaseInstance(spawnedAsset);
            }
            activeInstantiatedAssets.Clear();
        }
    }
}
