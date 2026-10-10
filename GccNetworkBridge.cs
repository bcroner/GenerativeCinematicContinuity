using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace GCC.Core
{
    [RequireComponent(typeof(EnvironmentRenderNode))]
    public class GccNetworkBridge : MonoBehaviour
    {
        [Header("Network Targeting Settings")]
        [SerializeField] private string targetApiUrl = "http://localhost:8000/blueprint";
        [SerializeField] private float networkPollIntervalSeconds = 1.0f;

        private EnvironmentRenderNode renderNode;
        private bool isPollingActive = false;

        private void Awake()
        {
            renderNode = GetComponent<EnvironmentRenderNode>();
        }

        private void Start()
        {
            StartNetworkSync();
        }

        private void OnDisable()
        {
            StopNetworkSync();
        }

        public void StartNetworkSync()
        {
            if (isPollingActive) return;
            isPollingActive = true;
            StartCoroutine(PollNarrativeServerLoop());
            Debug.Log($"[GCC Network Client]: Network sync loop bound to endpoint: {targetApiUrl}");
        }

        public void StopNetworkSync()
        {
            isPollingActive = false;
            StopAllCoroutines();
            Debug.Log("[GCC Network Client]: Network sync loop cleanly disarmed.");
        }

        private IEnumerator PollNarrativeServerLoop()
        {
            while (isPollingActive)
            {
                using (UnityWebRequest request = UnityWebRequest.Get(targetApiUrl))
                {
                    // Return execution thread control back to engine until download resolves
                    yield return request.SendWebRequest();

                    if (request.result == UnityWebRequest.Result.Success)
                    {
                        string rawJsonPayload = request.downloadHandler.text;
                        // Pipe the raw payload directly into our graphics modifier matrix
                        renderNode.ApplyNetworkRenderMatrix(rawJsonPayload);
                    }
                    else
                    {
                        Debug.LogWarning("[GCC Client Sync warning]: Loopback connection endpoint unresponsive.");
                    }
                }

                // Rest the engine loop for the designated polling interval window duration
                yield return new WaitForSeconds(networkPollIntervalSeconds);
            }
        }
    }
}
