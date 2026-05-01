#!/usr/bin/env python3
"""
Validate CrewAI Studio JSON files against the official schema
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def validate_crew_json(json_file, schema_file):
    """Validate a crew JSON file against the schema"""

    if not HAS_JSONSCHEMA:
        print("❌ ERROR: jsonschema library not installed")
        print("Install with: pip install jsonschema")
        return False

    # Load schema
    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Schema file not found: {schema_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in schema file: {e}")
        return False

    # Load crew JSON
    try:
        with open(json_file, 'r') as f:
            crew_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: JSON file not found: {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in crew file: {e}")
        return False

    # Validate
    print(f"\n{'='*60}")
    print(f"CrewAI Studio JSON Schema Validation")
    print(f"{'='*60}")
    print(f"File: {json_file}")
    print(f"Schema: {schema_file}")
    print(f"{'='*60}\n")

    try:
        validate(instance=crew_data, schema=schema)
        print("✅ VALIDATION PASSED!")
        print(f"\n📊 Summary:")
        print(f"  - Crew ID: {crew_data.get('id')}")
        print(f"  - Crew Name: {crew_data.get('name')}")
        print(f"  - Process: {crew_data.get('process')}")
        print(f"  - Tools: {len(crew_data.get('tools', []))}")
        print(f"  - Agents: {len(crew_data.get('agents', []))}")
        print(f"  - Tasks: {len(crew_data.get('tasks', []))}")
        print(f"\n{'='*60}\n")
        return True

    except ValidationError as e:
        print(f"❌ VALIDATION FAILED!")
        print(f"\nError at: {' -> '.join(str(p) for p in e.path)}")
        print(f"Message: {e.message}")

        if e.context:
            print(f"\nAdditional errors:")
            for i, suberror in enumerate(e.context[:5]):  # Show first 5
                print(f"  {i+1}. {suberror.message}")
            if len(e.context) > 5:
                print(f"  ... and {len(e.context) - 5} more errors")

        print(f"\n{'='*60}\n")
        return False

    except SchemaError as e:
        print(f"❌ ERROR: Invalid schema: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <crew_json_file> [schema_file]")
        print(f"\nDefault schema: crewai-studio-schema.json")
        sys.exit(1)

    json_file = sys.argv[1]

    # Default schema location
    script_dir = Path(__file__).parent
    default_schema = script_dir / "crewai-studio-schema.json"

    schema_file = sys.argv[2] if len(sys.argv) > 2 else str(default_schema)

    success = validate_crew_json(json_file, schema_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
