#!/usr/bin/env python3
"""
Test script for validating the Commitizen JSON Schema.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("❌ jsonschema package not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
    import jsonschema
    from jsonschema import validate, ValidationError, Draft7Validator


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def test_schema_validity():
    """Test that the schema itself is valid."""
    print("\n📋 Test 1: Validating schema structure...")
    schema_path = Path("cz-schema.json")

    try:
        schema = load_json(schema_path)
        Draft7Validator.check_schema(schema)
        print("✅ Schema structure is valid (Draft 7 compliant)")
        return True, schema
    except Exception as e:
        print(f"❌ Schema structure is invalid: {e}")
        return False, None


def test_example_file(schema):
    """Test that the example file validates against the schema."""
    print("\n📋 Test 2: Validating example file...")
    example_path = Path("cz.example.json")

    try:
        example = load_json(example_path)
        validate(instance=example, schema=schema)
        print("✅ Example file validates successfully")
        return True
    except ValidationError as e:
        print(f"❌ Example file validation failed: {e.message}")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_valid_configs(schema):
    """Test various valid configurations."""
    print("\n📋 Test 3: Testing valid configurations...")

    valid_configs = [
        # Minimal config
        {
            "commitizen": {
                "name": "cz_conventional_commits"
            }
        },
        # Config with version
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "version": "1.0.0",
                "version_provider": "commitizen"
            }
        },
        # Config with all version providers
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "version_provider": "scm"
            }
        },
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "version_provider": "poetry"
            }
        },
        # Config with version schemes
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "version_scheme": "pep440"
            }
        },
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "version_scheme": "semver"
            }
        },
        # Config with hooks
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "pre_bump_hooks": ["echo 'before'"],
                "post_bump_hooks": ["echo 'after'"]
            }
        },
        # Config with style
        {
            "commitizen": {
                "name": "cz_conventional_commits",
                "style": [
                    ["qmark", "fg:#ff9d00 bold"],
                    ["question", "bold"]
                ]
            }
        },
        # Config with customize
        {
            "commitizen": {
                "name": "cz_customize",
                "customize": {
                    "message_template": "{{change_type}}: {{message}}",
                    "example": "feature: add new feature",
                    "schema": "<type>: <message>",
                    "schema_pattern": "^(feature|fix):\\s.*",
                    "bump_pattern": "^(feature|fix)",
                    "bump_map": {
                        "feature": "MINOR",
                        "fix": "PATCH"
                    },
                    "questions": [
                        {
                            "type": "list",
                            "name": "change_type",
                            "message": "Select type",
                            "choices": [
                                {
                                    "value": "feature",
                                    "name": "Feature"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]

    all_passed = True
    for i, config in enumerate(valid_configs, 1):
        try:
            validate(instance=config, schema=schema)
            print(f"  ✅ Valid config {i}/{len(valid_configs)} passed")
        except ValidationError as e:
            print(f"  ❌ Valid config {i}/{len(valid_configs)} failed: {e.message}")
            all_passed = False

    return all_passed


def test_invalid_configs(schema):
    """Test that invalid configurations are rejected."""
    print("\n📋 Test 4: Testing invalid configurations (should fail)...")

    invalid_configs = [
        # Missing commitizen key
        ({"name": "cz_conventional_commits"}, "missing commitizen key"),
        # Invalid version_provider
        ({"commitizen": {"version_provider": "invalid"}}, "invalid version_provider"),
        # Invalid version_scheme
        ({"commitizen": {"version_scheme": "invalid"}}, "invalid version_scheme"),
        # Invalid type for version_files
        ({"commitizen": {"version_files": "not-an-array"}}, "version_files not array"),
        # Invalid type for annotated_tag
        ({"commitizen": {"annotated_tag": "yes"}}, "annotated_tag not boolean"),
        # Invalid type for pre_bump_hooks
        ({"commitizen": {"pre_bump_hooks": "not-an-array"}}, "pre_bump_hooks not array"),
        # Invalid style element (not 2 items)
        ({"commitizen": {"style": [["qmark"]]}}, "style element wrong length"),
        # Invalid customize question type
        ({"commitizen": {"name": "cz_customize", "customize": {"questions": [{"type": "invalid", "name": "test", "message": "test"}]}}}, "invalid question type"),
    ]

    all_passed = True
    for i, (config, description) in enumerate(invalid_configs, 1):
        try:
            validate(instance=config, schema=schema)
            print(f"  ❌ Invalid config {i}/{len(invalid_configs)} ({description}) - SHOULD HAVE FAILED but passed")
            all_passed = False
        except ValidationError:
            print(f"  ✅ Invalid config {i}/{len(invalid_configs)} ({description}) - correctly rejected")

    return all_passed


def test_schema_completeness(schema):
    """Test that schema covers all known configuration options."""
    print("\n📋 Test 5: Checking schema completeness...")

    expected_properties = [
        "name", "version", "version_provider", "version_scheme", "version_type",
        "version_files", "tag_format", "legacy_tag_formats", "ignored_tag_formats",
        "annotated_tag", "gpg_sign", "changelog_file", "changelog_format",
        "changelog_incremental", "changelog_merge_prerelease", "changelog_start_rev",
        "update_changelog_on_bump", "template", "bump_message", "pre_bump_hooks",
        "post_bump_hooks", "prerelease_offset", "major_version_zero", "encoding",
        "allow_abort", "allowed_prefixes", "message_length_limit", "always_signoff",
        "breaking_change_exclamation_in_title", "retry_after_failure", "use_shortcuts",
        "style", "customize", "extras"
    ]

    schema_properties = schema["properties"]["commitizen"]["properties"].keys()
    missing = set(expected_properties) - set(schema_properties)
    extra = set(schema_properties) - set(expected_properties)

    if missing:
        print(f"  ⚠️  Missing properties: {', '.join(missing)}")
    if extra:
        print(f"  ℹ️  Extra properties (might be new): {', '.join(extra)}")

    if not missing:
        print(f"  ✅ All {len(expected_properties)} expected properties are present")
        return True
    return False


def main():
    """Run all tests."""
    print("🧪 Testing Commitizen JSON Schema")
    print("=" * 60)

    results = []

    # Test 1: Schema validity
    success, schema = test_schema_validity()
    results.append(("Schema validity", success))

    if not schema:
        print("\n❌ Cannot continue - schema is invalid")
        return 1

    # Test 2: Example file
    results.append(("Example file", test_example_file(schema)))

    # Test 3: Valid configs
    results.append(("Valid configs", test_valid_configs(schema)))

    # Test 4: Invalid configs
    results.append(("Invalid configs", test_invalid_configs(schema)))

    # Test 5: Schema completeness
    results.append(("Schema completeness", test_schema_completeness(schema)))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
