"""
validate_environments.py
Automated validation checker suite to verify alternative environment configurations
against system specifications prior to production deployment.
"""

import json
import os
import sys
from typing import Dict, Any

# Expected authoritative parameter specifications schema
ENVIRONMENT_BLUEPRINT_SPEC = {
    "environment_id": str,
    "act_boundary_restrictions": list,
    "baseline_render_parameters": {
        "lighting_intensity": float,
        "fog_density": float,
        "color_grading_lut": str,
        "audio_lowpass_cutoff_hz": float
    }
}

def validate_nested_dictionary(target_data: Dict[str, Any], schema_spec: Dict[str, Any], parent_key: str = "") -> List[str]:
    """Recursively audits deep key paths and values against explicit structural rules."""
    error_logs = []
    
    for key, expected_type in schema_spec.items():
        current_path = f"{parent_key}.{key}" if parent_key else key
        
        if key not in target_data:
            error_logs.append(f"  [Schema Error]: Missing required constraint parameter key -> '{current_path}'")
            continue
            
        if isinstance(expected_type, dict):
            if not isinstance(target_data[key], dict):
                error_logs.append(f"  [Type Mismatch]: Key '{current_path}' must resolve to an object branch.")
            else:
                error_logs.extend(validate_nested_dictionary(target_data[key], expected_type, current_path))
        else:
            # Handle float checks safely when encoded as integers
            actual_val = target_data[key]
            if expected_type == float and isinstance(actual_val, int):
                actual_val = float(actual_val)
                
            if not isinstance(actual_val, expected_type):
                error_logs.append(f"  [Type Mismatch]: Key '{current_path}' type invalid. Expected: {expected_type.__name__}, Got: {type(target_data[key]).__name__}")
                
    return error_logs

def batch_validate_environment_directory(directory_path: str) -> bool:
    print("=================================================================")
    print("   GCC Environment Layout Verification Pipeline Boot Sequence    ")
    print("=================================================================\n")
    print(f"[Target Scan Path]: '{directory_path}'")
    
    if not os.path.exists(directory_path):
        print(f"  [System Log]: Directory path path missing. Creating output node targets.")
        os.makedirs(directory_path, exist_ok=True)
        return True

    total_checked = 0
    total_failed = 0

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".json"):
            total_checked += 1
            full_file_path = os.path.join(directory_path, file_name)
            print(f"Auditing config sequence profile: '{file_name}'...")
            
            try:
                with open(full_file_path, "r", encoding="utf-8") as f:
                    profile_payload = json.loads(f.read())
                    
                verification_anomalies = validate_nested_dictionary(profile_payload, ENVIRONMENT_BLUEPRINT_SPEC)
                
                if verification_anomalies:
                    total_failed += 1
                    for anomaly in verification_anomalies:
                        print(anomaly, file=sys.stderr)
                else:
                    print(f"  -> [Pass]: Verified structural alignment for layout token ID: {profile_payload['environment_id']}")
                    
            except Exception as e:
                total_failed += 1
                print(f"  -> [Critical Error]: Unable to parse file stream: {e}", file=sys.stderr)

    print("\n-----------------------------------------------------------------")
    print(f"  - Profiles Examined     : {total_checked}")
    print(f"  - Validation Successes  : {total_checked - total_failed}")
    print(f"  - Layout Fault Failures : {total_failed}")
    print("-----------------------------------------------------------------")
    
    return total_failed == 0

if __name__ == "__main__":
    # Create an active mockup environment profile file for layout validation demonstration
    TARGET_DIR = "./environments"
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    mock_env_profile = {
        "environment_id": "industrial_sub_sector_alpha",
        "act_boundary_restrictions":,
        "baseline_render_parameters": {
            "lighting_intensity": 0.85,
            "fog_density": 0.02,
            "color_grading_lut": "LUT_PsychoTown_Dusk.png",
            "audio_lowpass_cutoff_hz": 18000.0
        }
    }
    
    with open(f"{TARGET_DIR}/sub_sector_alpha.json", "w", encoding="utf-8") as target_out:
        target_out.write(json.dumps(mock_env_profile, indent=2))
        
    all_clear = batch_validate_environment_directory(TARGET_DIR)
    sys.exit(0 if all_clear else 1)
