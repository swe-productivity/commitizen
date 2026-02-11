# Commitizen JSON Schema

This directory contains the JSON Schema definition for Commitizen configuration files.

## What is JSON Schema?

JSON Schema is a vocabulary that allows you to annotate and validate JSON documents. It provides:

- **Validation**: Ensures your configuration file is correctly structured
- **IDE Support**: Enables autocomplete and IntelliSense in modern editors
- **Documentation**: Hover hints showing descriptions and examples for each field

## Usage

### Adding Schema to Your Configuration

Add the `$schema` property to the top of your `cz.json` or `.cz.json` file:

```json
{
  "$schema": "https://raw.githubusercontent.com/commitizen-tools/commitizen/master/schemas/cz-schema.json",
  "commitizen": {
    "name": "cz_conventional_commits",
    "version": "0.1.0",
    "version_provider": "commitizen"
  }
}
```

### IDE Support

Most modern IDEs and editors automatically detect the `$schema` property and provide:

#### Visual Studio Code
- Real-time validation (squiggly lines for errors)
- IntelliSense autocomplete (Ctrl+Space)
- Hover documentation

#### JetBrains IDEs (IntelliJ, WebStorm, PyCharm, etc.)
- Schema validation
- Code completion
- Quick documentation (Ctrl+Q)

#### Other Editors
Any editor with JSON Schema support will work, including:
- Vim/Neovim (with appropriate plugins)
- Sublime Text (with LSP)
- Atom
- Eclipse

### Local Development

If you're contributing to Commitizen and want to test schema changes locally, you can reference the local file:

```json
{
  "$schema": "../schemas/cz-schema.json",
  "commitizen": { ... }
}
```

Or use an absolute path:

```json
{
  "$schema": "file:///path/to/commitizen/schemas/cz-schema.json",
  "commitizen": { ... }
}
```

## Files

- **`cz-schema.json`**: The main JSON Schema definition
- **`cz.example.json`**: Example configuration file demonstrating schema usage
- **`README.md`**: This file

## Schema URL

The schema is hosted on GitHub and can be referenced using:

```
https://raw.githubusercontent.com/commitizen-tools/commitizen/master/schemas/cz-schema.json
```

For specific versions, use the tag or commit hash:

```
https://raw.githubusercontent.com/commitizen-tools/commitizen/v3.0.0/schemas/cz-schema.json
```

## Validation

You can validate your configuration file against the schema using tools like:

### Using `check-jsonschema`

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/cz-schema.json cz.json
```

### Using `ajv-cli`

```bash
npm install -g ajv-cli
ajv validate -s schemas/cz-schema.json -d cz.json
```

### Using Python

```python
import json
import jsonschema

with open('schemas/cz-schema.json') as schema_file:
    schema = json.load(schema_file)

with open('cz.json') as config_file:
    config = json.load(config_file)

jsonschema.validate(config, schema)
print("Configuration is valid!")
```

## Contributing

If you find issues with the schema or want to add improvements:

1. Update `schemas/cz-schema.json`
2. Update the example file `schemas/cz.example.json` if needed
3. Test your changes locally
4. Submit a pull request

### Schema Guidelines

- Keep descriptions clear and concise
- Include examples for complex fields
- Use proper JSON Schema constraints (enum, pattern, minimum, etc.)
- Follow the JSON Schema Draft 7 specification
- Maintain backward compatibility when possible

## Related Documentation

- [Configuration File Documentation](../docs/config/configuration_file.md)
- [Configuration Options](../docs/config/option.md)
- [Customization Guide](../docs/customization/config_file.md)
- [JSON Schema Specification](https://json-schema.org/)

## Support

For issues or questions about the schema:

- Open an issue on [GitHub](https://github.com/commitizen-tools/commitizen/issues)
- Check the [documentation](https://commitizen-tools.github.io/commitizen/)
- Join the discussion on [GitHub Discussions](https://github.com/commitizen-tools/commitizen/discussions)
