"""Tests for the JSON Schema validation (schemas/cz-schema.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft7Validator, ValidationError, validate


@pytest.fixture
def schema_dir() -> Path:
    """Return the path to the schemas directory."""
    return Path(__file__).parent.parent / "schemas"


@pytest.fixture
def schema(schema_dir: Path) -> dict[str, Any]:
    """Load and return the JSON schema."""
    schema_path = schema_dir / "cz-schema.json"
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def example_config(schema_dir: Path) -> dict[str, Any]:
    """Load and return the example configuration."""
    example_path = schema_dir / "cz.example.json"
    with open(example_path) as f:
        return json.load(f)


class TestSchemaValidity:
    """Test that the schema itself is valid."""

    def test_schema_is_valid_draft7(self, schema: dict[str, Any]) -> None:
        """Test that the schema is valid according to JSON Schema Draft 7."""
        Draft7Validator.check_schema(schema)

    def test_schema_has_required_fields(self, schema: dict[str, Any]) -> None:
        """Test that the schema has the required top-level fields."""
        assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
        assert "title" in schema
        assert "description" in schema
        assert "properties" in schema
        assert "commitizen" in schema["properties"]


class TestExampleValidation:
    """Test that the example configuration validates against the schema."""

    def test_example_validates(
        self, schema: dict[str, Any], example_config: dict[str, Any]
    ) -> None:
        """Test that the example configuration is valid."""
        validate(instance=example_config, schema=schema)


class TestValidConfigurations:
    """Test that various valid configurations are accepted."""

    @pytest.mark.parametrize(
        "config",
        [
            # Minimal config
            {"commitizen": {"name": "cz_conventional_commits"}},
            # Config with version
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "version": "1.0.0",
                    "version_provider": "commitizen",
                }
            },
            # Config with version providers
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "scm"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "poetry"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "pep621"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "uv"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "cargo"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "npm"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_provider": "composer"}},
            # Config with version schemes
            {"commitizen": {"name": "cz_conventional_commits", "version_scheme": "pep440"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_scheme": "semver"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_scheme": "semver2"}},
            {"commitizen": {"name": "cz_conventional_commits", "version_scheme": None}},
            # Config with hooks
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "pre_bump_hooks": ["echo 'before'"],
                    "post_bump_hooks": ["echo 'after'"],
                }
            },
            # Config with style
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "style": [
                        ["qmark", "fg:#ff9d00 bold"],
                        ["question", "bold"],
                    ],
                }
            },
            # Config with version files
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "version_files": [
                        "src/__version__.py",
                        "pyproject.toml:version",
                    ],
                }
            },
            # Config with booleans
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "annotated_tag": True,
                    "gpg_sign": False,
                    "update_changelog_on_bump": True,
                    "changelog_incremental": False,
                    "major_version_zero": False,
                }
            },
            # Config with integers
            {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "prerelease_offset": 0,
                    "message_length_limit": 100,
                }
            },
        ],
        ids=[
            "minimal",
            "with_version",
            "version_provider_scm",
            "version_provider_poetry",
            "version_provider_pep621",
            "version_provider_uv",
            "version_provider_cargo",
            "version_provider_npm",
            "version_provider_composer",
            "version_scheme_pep440",
            "version_scheme_semver",
            "version_scheme_semver2",
            "version_scheme_null",
            "with_hooks",
            "with_style",
            "with_version_files",
            "with_booleans",
            "with_integers",
        ],
    )
    def test_valid_config(self, schema: dict[str, Any], config: dict[str, Any]) -> None:
        """Test that valid configurations pass validation."""
        validate(instance=config, schema=schema)


class TestInvalidConfigurations:
    """Test that invalid configurations are rejected."""

    @pytest.mark.parametrize(
        ("config", "description"),
        [
            # Missing commitizen key
            ({"name": "cz_conventional_commits"}, "missing_commitizen_key"),
            # Invalid version_provider
            ({"commitizen": {"version_provider": "invalid"}}, "invalid_version_provider"),
            # Invalid version_scheme
            ({"commitizen": {"version_scheme": "invalid"}}, "invalid_version_scheme"),
            # Invalid type for version_files
            ({"commitizen": {"version_files": "not-an-array"}}, "version_files_not_array"),
            # Invalid type for annotated_tag
            ({"commitizen": {"annotated_tag": "yes"}}, "annotated_tag_not_boolean"),
            # Invalid type for gpg_sign
            ({"commitizen": {"gpg_sign": 1}}, "gpg_sign_not_boolean"),
            # Invalid type for pre_bump_hooks
            ({"commitizen": {"pre_bump_hooks": "not-an-array"}}, "pre_bump_hooks_not_array"),
            # Invalid type for post_bump_hooks
            ({"commitizen": {"post_bump_hooks": 123}}, "post_bump_hooks_not_array"),
            # Invalid style element (not 2 items)
            ({"commitizen": {"style": [["qmark"]]}}, "style_element_wrong_length"),
            # Invalid type for prerelease_offset
            ({"commitizen": {"prerelease_offset": "zero"}}, "prerelease_offset_not_number"),
            # Invalid type for message_length_limit
            ({"commitizen": {"message_length_limit": "100"}}, "message_length_limit_not_number"),
        ],
    )
    def test_invalid_config(
        self, schema: dict[str, Any], config: dict[str, Any], description: str
    ) -> None:
        """Test that invalid configurations are rejected."""
        with pytest.raises(ValidationError):
            validate(instance=config, schema=schema)


class TestVersionValidation:
    """Test version string pattern validation."""

    @pytest.mark.parametrize(
        "version",
        [
            "0.1.0",
            "1.0.0",
            "2.3.4",
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-rc.2",
            "1.0.0+build.123",
            "2.3.4-alpha.1+build.456",
        ],
    )
    def test_valid_version_formats(self, schema: dict[str, Any], version: str) -> None:
        """Test that valid version strings are accepted."""
        config = {"commitizen": {"name": "cz_conventional_commits", "version": version}}
        validate(instance=config, schema=schema)

    @pytest.mark.parametrize(
        "version",
        [
            "not-a-version",
            "1",
            "1.0",
            "v1.0.0",  # Should not have 'v' prefix
        ],
    )
    def test_invalid_version_formats(self, schema: dict[str, Any], version: str) -> None:
        """Test that invalid version strings are rejected."""
        config = {"commitizen": {"name": "cz_conventional_commits", "version": version}}
        with pytest.raises(ValidationError):
            validate(instance=config, schema=schema)


class TestCustomizeValidation:
    """Test customize configuration validation."""

    def test_valid_customize_config(self, schema: dict[str, Any]) -> None:
        """Test that valid customize configuration is accepted."""
        config = {
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
                        "fix": "PATCH",
                    },
                    "questions": [
                        {
                            "type": "list",
                            "name": "change_type",
                            "message": "Select type",
                            "choices": [
                                {
                                    "value": "feature",
                                    "name": "Feature",
                                }
                            ],
                        }
                    ],
                },
            }
        }
        validate(instance=config, schema=schema)

    @pytest.mark.parametrize(
        "question_type",
        ["list", "input", "checkbox", "confirm", "password"],
    )
    def test_valid_question_types(self, schema: dict[str, Any], question_type: str) -> None:
        """Test that valid question types are accepted."""
        config = {
            "commitizen": {
                "name": "cz_customize",
                "customize": {
                    "questions": [
                        {
                            "type": question_type,
                            "name": "test",
                            "message": "Test question",
                        }
                    ]
                },
            }
        }
        validate(instance=config, schema=schema)

    def test_invalid_question_type(self, schema: dict[str, Any]) -> None:
        """Test that invalid question types are rejected."""
        config = {
            "commitizen": {
                "name": "cz_customize",
                "customize": {
                    "questions": [
                        {
                            "type": "invalid_type",
                            "name": "test",
                            "message": "Test question",
                        }
                    ]
                },
            }
        }
        with pytest.raises(ValidationError):
            validate(instance=config, schema=schema)


class TestSchemaCompleteness:
    """Test that the schema covers all known configuration options."""

    def test_schema_has_all_expected_properties(self, schema: dict[str, Any]) -> None:
        """Test that all expected configuration properties are defined in the schema."""
        expected_properties = {
            "name",
            "version",
            "version_provider",
            "version_scheme",
            "version_type",
            "version_files",
            "tag_format",
            "legacy_tag_formats",
            "ignored_tag_formats",
            "annotated_tag",
            "gpg_sign",
            "changelog_file",
            "changelog_format",
            "changelog_incremental",
            "changelog_merge_prerelease",
            "changelog_start_rev",
            "update_changelog_on_bump",
            "template",
            "bump_message",
            "pre_bump_hooks",
            "post_bump_hooks",
            "prerelease_offset",
            "major_version_zero",
            "encoding",
            "allow_abort",
            "allowed_prefixes",
            "message_length_limit",
            "always_signoff",
            "breaking_change_exclamation_in_title",
            "retry_after_failure",
            "use_shortcuts",
            "style",
            "customize",
            "extras",
        }

        schema_properties = set(schema["properties"]["commitizen"]["properties"].keys())
        missing = expected_properties - schema_properties

        assert not missing, f"Schema is missing properties: {missing}"
