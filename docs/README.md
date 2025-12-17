# Documentation

This directory contains generated documentation and diagrams for the Beckn Protocol specifications.

## Schema Diagrams

Visual UML diagrams (in SVG format) are generated for all schema attribute files. These diagrams provide a visual representation of the schema structures, their properties, and relationships.

### Diagram Location

Schema diagrams are stored in the following directory structure:
```
docs/schema/
├── {component}/
│   └── {version}/
│       └── attributes.svg
```

For example:
- `docs/schema/core/v2/attributes.svg` - Core v2 schema diagram
- `docs/schema/EnergyResource/v0.2/attributes.svg` - Energy Resource v0.2 schema diagram
- `docs/schema/EvChargingService/v1/attributes.svg` - EV Charging Service v1 schema diagram

### Refreshing Schema Diagrams

To regenerate all schema diagrams after making changes to schema YAML files:

```bash
# From the protocol-specifications-new directory
./scripts/generate_schema_diagrams.sh
```

This script will:
1. Find all `attributes.yaml` files in the `schema/` directory
2. Generate PlantUML diagrams using the `swagger_to_uml` tool
3. Convert them to SVG format using PlantUML
4. Save them to `docs/schema/{component}/{version}/attributes.svg`

**Prerequisites:**

1. **swagger_to_uml tool**: Install from [https://github.com/ameetdesh/swagger_to_uml](https://github.com/ameetdesh/swagger_to_uml)
   
   ```bash
   # Clone the repository
   git clone https://github.com/ameetdesh/swagger_to_uml.git
   cd swagger_to_uml
   
   # Install the package (editable mode)
   pip install -e .
   
   # Add the bin directory to your PATH permanently
   # For zsh (macOS default):
   echo 'export PATH="$PATH:'$(pwd)'/bin"' >> ~/.zshrc
   source ~/.zshrc
   
   # For bash:
   # echo 'export PATH="$PATH:'$(pwd)'/bin"' >> ~/.bashrc
   # source ~/.bashrc
   
   # Or create a symlink to a directory already in PATH:
   # ln -s $(pwd)/bin/swagger_to_uml /usr/local/bin/swagger_to_uml
   
   # Verify installation:
   swagger_to_uml schema/core/v2/attributes.yaml | head -5
   ```

2. **PlantUML**: Must be installed and available in your PATH
   
   ```bash
   # On macOS with Homebrew:
   brew install plantuml graphviz
   ```

3. **Python 3**: Must be available

**Note:** The script processes all schema files automatically. If a schema file cannot be processed, an error will be reported but the script will continue with other files.

### Viewing Diagrams

SVG diagrams can be viewed in:
- Any modern web browser
- Vector graphics editors (Inkscape, Adobe Illustrator, etc.)
- Documentation tools that support SVG embedding

The SVG format is vector-based and scales without quality loss, making it ideal for both on-screen viewing and printing.
