#!/bin/bash

# Script to generate SVG diagrams for all schema YAML files
# Usage: ./scripts/generate_schema_diagrams.sh

set -e

# Get the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCHEMA_DIR="$PROJECT_ROOT/schema"
DOCS_DIR="$PROJECT_ROOT/docs"

# Check if swagger_to_uml tool is available in PATH
if ! command -v swagger_to_uml &> /dev/null; then
    echo "Error: swagger_to_uml command not found in PATH."
    echo ""
    echo "Please install swagger_to_uml from: https://github.com/ameetdesh/swagger_to_uml"
    echo ""
    echo "Installation steps:"
    echo "  1. git clone https://github.com/ameetdesh/swagger_to_uml.git"
    echo "  2. cd swagger_to_uml"
    echo "  3. pip install -e ."
    echo "  4. Add bin directory to PATH or create symlink"
    echo ""
    echo "See docs/README.md for detailed setup instructions."
    exit 1
fi

# Check if plantuml is available
if ! command -v plantuml &> /dev/null; then
    echo "Error: plantuml command not found. Please install PlantUML."
    exit 1
fi

echo "Generating SVG diagrams for all schema YAML files..."
echo "Schema directory: $SCHEMA_DIR"
echo "Output directory: $DOCS_DIR/schema"
echo ""

# Counter for processed files (use temp file for subshell compatibility)
count_file=$(mktemp)
error_file=$(mktemp)
echo "0" > "$count_file"
echo "0" > "$error_file"

# Find all attributes.yaml files and process them
find "$SCHEMA_DIR" -name "attributes.yaml" -type f | while read -r yaml_file; do
    # Extract component name and version from path
    # Example: schema/core/v2/attributes.yaml -> component=core, version=v2
    # Example: schema/EnergyResource/v0.2/attributes.yaml -> component=EnergyResource, version=v0.2
    
    relative_path="${yaml_file#$SCHEMA_DIR/}"
    # Remove /attributes.yaml from the end
    path_without_file="${relative_path%/attributes.yaml}"
    # Split by / to get component and version
    component=$(echo "$path_without_file" | cut -d'/' -f1)
    version=$(echo "$path_without_file" | cut -d'/' -f2)
    
    if [ -z "$component" ] || [ -z "$version" ]; then
        echo "Warning: Could not parse component/version from path: $yaml_file"
        echo $(($(cat "$error_file") + 1)) > "$error_file"
        continue
    fi
    
    # Create output directory
    output_dir="$DOCS_DIR/schema/$component/$version"
    mkdir -p "$output_dir"
    
    # Generate PlantUML file
    puml_file="$output_dir/attributes.puml"
    svg_file="$output_dir/attributes.svg"
    
    echo "Processing: $component/$version"
    echo "  Input:  $yaml_file"
    echo "  Output: $svg_file"
    
    # Generate PlantUML from YAML
    if swagger_to_uml "$yaml_file" > "$puml_file" 2>&1; then
        # Generate SVG from PlantUML
        if plantuml "$puml_file" -tsvg > /dev/null 2>&1; then
            # Remove the .puml file to keep only SVG (optional - comment out if you want to keep .puml)
            # rm "$puml_file"
            echo "  ✓ Success"
            echo $(($(cat "$count_file") + 1)) > "$count_file"
        else
            echo "  ✗ Error: Failed to generate SVG from PlantUML"
            echo $(($(cat "$error_file") + 1)) > "$error_file"
        fi
    else
        echo "  ✗ Error: Failed to generate PlantUML from YAML"
        echo $(($(cat "$error_file") + 1)) > "$error_file"
    fi
    echo ""
done

count=$(cat "$count_file")
errors=$(cat "$error_file")
rm -f "$count_file" "$error_file"

echo "=========================================="
echo "Summary:"
echo "  Successfully processed: $count files"
echo "  Errors: $errors files"
echo "=========================================="

if [ $errors -gt 0 ]; then
    exit 1
fi

