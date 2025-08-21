# HTML De-minification Script

A comprehensive Python script to de-minify HTML files with proper formatting, indentation, and structure preservation.

## Features

- ✅ **HTML Structure Preservation**: Maintains proper HTML hierarchy and indentation
- ✅ **CSS Formatting**: Formats CSS within `<style>` tags with proper indentation
- ✅ **JavaScript Formatting**: Basic JavaScript formatting within `<script>` tags
- ✅ **Comment Preservation**: Keeps HTML comments intact
- ✅ **Special Tag Handling**: Preserves whitespace in `<pre>` and `<textarea>` tags
- ✅ **Batch Processing**: Process multiple files or entire directories
- ✅ **Recursive Processing**: Process subdirectories recursively
- ✅ **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

1. Download the script files:
   - `deminify_html.py` - Main Python script
   - `deminify.sh` - Shell script wrapper (Unix/macOS/Linux)

2. Make the scripts executable:
   ```bash
   chmod +x deminify_html.py
   chmod +x deminify.sh
   ```

## Usage

### Using the Python Script Directly

```bash
# Format a single file
python3 deminify_html.py input.html

# Format a file with custom output name
python3 deminify_html.py input.html output.html

# Process all HTML files in a directory
python3 deminify_html.py --batch ./html_files

# Process all HTML files recursively
python3 deminify_html.py --batch ./html_files --recursive

# Custom indentation (default is 2 spaces)
python3 deminify_html.py --indent 4 input.html
```

### Using the Shell Script Wrapper

```bash
# Format a single file
./deminify.sh input.html

# Format a file with custom output name
./deminify.sh input.html output.html

# Process all HTML files in a directory
./deminify.sh --batch ./html_files

# Process all HTML files recursively
./deminify.sh --batch ./html_files --recursive

# Show help
./deminify.sh --help
```

## Examples

### Single File Processing

```bash
# Input: minified HTML file
./deminify.sh minified.html

# Output: formatted HTML file (minified_formatted.html)
```

### Batch Processing

```bash
# Process all HTML files in current directory
./deminify.sh --batch .

# Process all HTML files in a specific directory
./deminify.sh --batch ./website_files

# Process recursively (including subdirectories)
./deminify.sh --batch ./website_files --recursive
```

### Custom Output Names

```bash
# Specify custom output filename
./deminify.sh input.html clean_output.html
```

## Output

The script creates formatted HTML files with:

- **Proper Indentation**: Each nested element is indented with 2 spaces (configurable)
- **Line Breaks**: Elements are properly separated with line breaks
- **Formatted CSS**: CSS within `<style>` tags is formatted with proper indentation
- **Formatted JavaScript**: Basic JavaScript formatting within `<script>` tags
- **Preserved Structure**: HTML comments and special tags are preserved

### Before (Minified)
```html
<!DOCTYPE html><html><head><title>Page</title><style>body{margin:0;padding:0}</style></head><body><div><h1>Title</h1><p>Content</p></div></body></html>
```

### After (Formatted)
```html
<!DOCTYPE html>
  <html>
    <head>
      <title>
        Page
      </title>
      <style>
        body {
          margin: 0;
          padding: 0;
        }
      </style>
    </head>
    <body>
      <div>
        <h1>
          Title
        </h1>
        <p>
          Content
        </p>
      </div>
    </body>
  </html>
```

## Command Line Options

### Python Script Options

- `input` - Input HTML file path
- `output` - Output HTML file path (optional)
- `--batch <directory>` - Process all HTML files in directory
- `--recursive` - Process subdirectories recursively (with --batch)
- `--indent <number>` - Number of spaces for indentation (default: 2)

### Shell Script Options

- `input_file` - Input HTML file path
- `output_file` - Output HTML file path (optional)
- `--batch <directory>` - Process all HTML files in directory
- `--recursive` - Process subdirectories recursively (with --batch)
- `--help` - Show help message

## File Handling

### Supported File Types
- `.html` files
- Files with HTML content (regardless of extension)

### Output Naming
- If no output file is specified, the script creates `{filename}_formatted.html`
- Output files are created in the same directory as input files
- Existing files are overwritten without warning

### Error Handling
- Invalid file paths are reported with clear error messages
- Missing directories are detected and reported
- File encoding issues are handled gracefully

## Advanced Usage

### Processing Large Directories

```bash
# Process a large website directory
./deminify.sh --batch /path/to/website --recursive

# This will process all HTML files in the website and all subdirectories
```

### Integration with Build Scripts

```bash
#!/bin/bash
# Example build script integration

# De-minify all HTML files
./deminify.sh --batch ./src --recursive

# Move formatted files to build directory
mv ./src/*_formatted.html ./build/
```

### Custom Indentation

```bash
# Use 4 spaces for indentation
python3 deminify_html.py --indent 4 input.html

# Use tabs (not recommended for HTML)
python3 deminify_html.py --indent 1 input.html
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x deminify.sh
   chmod +x deminify_html.py
   ```

2. **Python Not Found**
   ```bash
   # Try python instead of python3
   python deminify_html.py input.html
   ```

3. **File Not Found**
   - Check file paths are correct
   - Ensure files have proper permissions
   - Verify file extensions

4. **Encoding Issues**
   - The script uses UTF-8 encoding by default
   - For other encodings, modify the script's file handling

### Debug Mode

For troubleshooting, you can add debug output by modifying the script:

```python
# Add to deminify_file function
print(f"Processing: {input_path}")
print(f"Output: {output_path}")
```

## Contributing

To improve the script:

1. Fork the repository
2. Make your changes
3. Test with various HTML files
4. Submit a pull request

### Areas for Improvement

- Better CSS parsing and formatting
- Advanced JavaScript formatting
- HTML validation
- Performance optimization for large files
- Support for other markup languages (XML, SVG)

## License

This script is provided as-is for educational and practical use. Feel free to modify and distribute as needed.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review the command line options
3. Test with a simple HTML file first
4. Ensure Python 3.6+ is installed

---

**Note**: This script is designed to improve readability of minified HTML files. It preserves the original structure while adding proper formatting and indentation.
