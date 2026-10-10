Shader "GCC/Effects/MaterialDistortion"
{
    Properties
    {
        _MainTex ("Base Albedo Map", 2D) = "white" {}
        _DistortionMap ("Distortion Vector Map (Noise)", 2D) = "bump" {}
        _Stability ("Character Stability Index", Range(0.0, 1.0)) = 1.0
        _DistortionFrequency ("Distortion Wave Speed", Float) = 2.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "RenderPipeline"="UniversalPipeline" }
        LOD 100

        Pass
        {
            Name "ForwardLit"
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS   : POSITION;
                float2 uv           : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS   : SV_POSITION;
                float2 uv           : TEXCOORD0;
                float1 instability  : TEXCOORD1;
            };

            Texture2D _MainTex;
            SamplerState sampler_MainTex;
            Texture2D _DistortionMap;
            SamplerState sampler_DistortionMap;

            CBUFFER_START(UnityPerMaterial)
                float4 _MainTex_ST;
                float _Stability;
                float _DistortionFrequency;
            CBUFFER_END

            Varyings vert(Attributes input)
            {
                Varyings output;
                
                // Calculate reverse instability scalar tracking
                float instability = 1.0 - _Stability;
                output.instability = instability;

                // Real-time vertex position displacement mapping loop
                float3 positionWS = TransformObjectToWorld(input.positionOS.xyz);
                float waveOffset = sin(positionWS.y * 5.0 + _Time.y * _DistortionFrequency) * 0.15 * instability;
                
                // Displace vertex outward along world coordinates based on stress state
                positionWS.x += waveOffset;
                
                output.positionCS = TransformWorldToHClip(positionWS);
                output.uv = TRANSFORM_TEX(input.uv, _MainTex);
                return output;
            }

            half4 frag(Varyings input) : SV_Target
            {
                // Sample original surface texture map
                half4 baseColor = _MainTex.Sample(sampler_MainTex, input.uv);
                
                // Calculate grayscale conversion parameters
                half luminance = dot(baseColor.rgb, half3(0.2126, 0.7152, 0.0722));
                
                // Dynamic interpolation: Injected shock causes progressive color drainage (desaturation)
                baseColor.rgb = lerp(baseColor.rgb, half3(luminance, luminance, luminance), input.instability);
                
                return baseColor;
            }
            ENDHLSL
        }
    }
}
