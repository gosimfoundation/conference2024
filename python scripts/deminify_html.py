#!/usr/bin/env python3
"""
HTML De-minification Script

This script de-minifies HTML files by:
1. Adding proper indentation and line breaks
2. Formatting CSS within <style> tags
3. Formatting JavaScript within <script> tags
4. Preserving HTML structure and comments
5. Handling inline styles and attributes properly

Usage:
    python deminify_html.py <input_file> [output_file]
    python deminify_html.py --batch <directory>
    python deminify_html.py --batch <directory> --recursive
"""

import os
import sys
import re
import argparse
import html.parser
from pathlib import Path
from typing import List, Tuple, Optional


class HTMLFormatter:
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.indent_char = " " * indent_size
        self.current_indent = 0
        self.output_lines = []
        self.in_script = False
        self.in_style = False
        self.in_pre = False
        self.in_textarea = False
        self.preserve_whitespace = False
        
    def format_html(self, html_content: str) -> str:
        """Main method to format HTML content"""
        # Reset state
        self.current_indent = 0
        self.output_lines = []
        self.in_script = False
        self.in_style = False
        self.in_pre = False
        self.in_textarea = False
        self.preserve_whitespace = False
        
        # Process the HTML content
        formatted = self._process_html(html_content)
        return formatted
    
    def _process_html(self, html_content: str) -> str:
        """Process HTML content with proper formatting"""
        # Split content into tokens while preserving structure
        tokens = self._tokenize_html(html_content)
        
        for token in tokens:
            if token.startswith('<'):
                self._process_tag(token)
            else:
                self._process_text(token)
        
        return '\n'.join(self.output_lines)
    
    def _tokenize_html(self, html_content: str) -> List[str]:
        """Tokenize HTML content while preserving special sections"""
        tokens = []
        current_pos = 0
        
        # Find all script and style tags
        script_pattern = r'(<script[^>]*>.*?</script>)'
        style_pattern = r'(<style[^>]*>.*?</style>)'
        pre_pattern = r'(<pre[^>]*>.*?</pre>)'
        textarea_pattern = r'(<textarea[^>]*>.*?</textarea>)'
        
        # Combine patterns
        combined_pattern = f'({script_pattern}|{style_pattern}|{pre_pattern}|{textarea_pattern})'
        
        # Find all matches
        matches = list(re.finditer(combined_pattern, html_content, re.DOTALL | re.IGNORECASE))
        
        for i, match in enumerate(matches):
            # Add content before the match
            if match.start() > current_pos:
                before_content = html_content[current_pos:match.start()]
                tokens.extend(self._split_html_content(before_content))
            
            # Add the matched content as a single token
            tokens.append(match.group(0))
            current_pos = match.end()
        
        # Add remaining content
        if current_pos < len(html_content):
            remaining_content = html_content[current_pos:]
            tokens.extend(self._split_html_content(remaining_content))
        
        return tokens
    
    def _split_html_content(self, content: str) -> List[str]:
        """Split HTML content into tags and text"""
        tokens = []
        current_pos = 0
        
        # Find all HTML tags
        tag_pattern = r'<[^>]+>'
        matches = list(re.finditer(tag_pattern, content))
        
        for match in matches:
            # Add text before the tag
            if match.start() > current_pos:
                text_content = content[current_pos:match.start()]
                if text_content.strip():
                    tokens.append(text_content)
            
            # Add the tag
            tokens.append(match.group(0))
            current_pos = match.end()
        
        # Add remaining text
        if current_pos < len(content):
            remaining_text = content[current_pos:]
            if remaining_text.strip():
                tokens.append(remaining_text)
        
        return tokens
    
    def _process_tag(self, tag: str):
        """Process HTML tags with proper indentation"""
        tag_lower = tag.lower()
        
        # Check for special tags
        if tag_lower.startswith('<script'):
            self.in_script = True
            self._add_line(tag)
            return
        elif tag_lower.startswith('</script>'):
            self.in_script = False
            self._add_line(tag)
            return
        elif tag_lower.startswith('<style'):
            self.in_style = True
            self._add_line(tag)
            return
        elif tag_lower.startswith('</style>'):
            self.in_style = False
            self._add_line(tag)
            return
        elif tag_lower.startswith('<pre'):
            self.in_pre = True
            self.preserve_whitespace = True
            self._add_line(tag)
            return
        elif tag_lower.startswith('</pre>'):
            self.in_pre = False
            self.preserve_whitespace = False
            self._add_line(tag)
            return
        elif tag_lower.startswith('<textarea'):
            self.in_textarea = True
            self.preserve_whitespace = True
            self._add_line(tag)
            return
        elif tag_lower.startswith('</textarea>'):
            self.in_textarea = False
            self.preserve_whitespace = False
            self._add_line(tag)
            return
        
        # Handle self-closing tags
        if tag.endswith('/>') or tag_lower in ['<br>', '<hr>', '<img', '<input', '<meta', '<link']:
            self._add_line(tag)
            return
        
        # Handle opening tags
        if not tag.startswith('</'):
            self._add_line(tag)
            # Increase indent for most tags (except inline elements)
            if not self._is_inline_element(tag):
                self.current_indent += 1
            return
        
        # Handle closing tags
        if tag.startswith('</'):
            # Decrease indent before closing tag
            if not self._is_inline_element(tag):
                self.current_indent = max(0, self.current_indent - 1)
            self._add_line(tag)
            return
    
    def _process_text(self, text: str):
        """Process text content with proper formatting"""
        if self.in_script:
            # Format JavaScript
            formatted_js = self._format_javascript(text)
            self._add_line(formatted_js)
        elif self.in_style:
            # Format CSS
            formatted_css = self._format_css(text)
            self._add_line(formatted_css)
        elif self.preserve_whitespace:
            # Preserve whitespace for pre and textarea
            self._add_line(text)
        else:
            # Normal text processing
            text = text.strip()
            if text:
                self._add_line(text)
    
    def _is_inline_element(self, tag: str) -> bool:
        """Check if tag is an inline element"""
        inline_elements = [
            'span', 'a', 'strong', 'em', 'b', 'i', 'u', 'code', 'small',
            'sub', 'sup', 'mark', 'time', 'abbr', 'cite', 'q', 'samp',
            'kbd', 'var', 'dfn', 's', 'del', 'ins'
        ]
        
        tag_name = re.match(r'</?(\w+)', tag)
        if tag_name:
            return tag_name.group(1).lower() in inline_elements
        return False
    
    def _format_css(self, css_content: str) -> str:
        """Format CSS content with proper indentation"""
        if not css_content.strip():
            return css_content
        
        # Remove extra whitespace but preserve structure
        css = re.sub(r'\s+', ' ', css_content.strip())
        
        # Add line breaks for CSS rules and media queries
        css = re.sub(r'(@media[^{]+){', r'\1 {\n', css)
        css = re.sub(r'([{}])', r'\n\1\n', css)
        css = re.sub(r'([;])', r'\1\n', css)
        
        # Split into lines and format
        lines = css.split('\n')
        formatted_lines = []
        current_indent = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle opening braces
            if line == '{':
                formatted_lines.append(' ' * (current_indent * self.indent_size) + line)
                current_indent += 1
            # Handle closing braces
            elif line == '}':
                current_indent = max(0, current_indent - 1)
                formatted_lines.append(' ' * (current_indent * self.indent_size) + line)
            # Handle CSS properties
            elif line.endswith(';'):
                formatted_lines.append(' ' * (current_indent * self.indent_size) + line)
            # Handle CSS selectors and other content
            else:
                formatted_lines.append(' ' * (current_indent * self.indent_size) + line)
        
        return '\n'.join(formatted_lines)
    
    def _format_javascript(self, js_content: str) -> str:
        """Format JavaScript content with basic indentation"""
        if not js_content.strip():
            return js_content
        
        # Basic JavaScript formatting
        js = js_content.strip()
        
        # Add line breaks for common patterns
        js = re.sub(r';\s*', ';\n', js)
        js = re.sub(r'{\s*', ' {\n', js)
        js = re.sub(r'}\s*', '}\n', js)
        
        # Add basic indentation
        lines = js.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Adjust indent level
            if line.endswith('{'):
                formatted_lines.append(' ' * (indent_level * self.indent_size) + line)
                indent_level += 1
            elif line.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append(' ' * (indent_level * self.indent_size) + line)
            else:
                formatted_lines.append(' ' * (indent_level * self.indent_size) + line)
        
        return '\n'.join(formatted_lines)
    
    def _add_line(self, content: str):
        """Add a line to the output with proper indentation"""
        if self.preserve_whitespace:
            self.output_lines.append(content)
        else:
            indent = self.indent_char * self.current_indent
            self.output_lines.append(indent + content)


def deminify_file(input_path: str, output_path: Optional[str] = None) -> None:
    """De-minify a single HTML file"""
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Format the HTML
        formatter = HTMLFormatter()
        formatted_content = formatter.format_html(content)
        
        # Determine output path
        if output_path is None:
            input_path_obj = Path(input_path)
            base_name = input_path_obj.stem
            output_path = str(input_path_obj.parent / f"{base_name}_formatted.html")
        
        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"✓ Formatted: {input_path} -> {output_path}")
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")


def deminify_directory(directory: str, recursive: bool = False) -> None:
    """De-minify all HTML files in a directory"""
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"✗ Directory does not exist: {directory}")
        return
    
    # Find HTML files
    if recursive:
        html_files = list(directory_path.rglob("*.html"))
    else:
        html_files = list(directory_path.glob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in {directory}")
        return
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    for html_file in html_files:
        deminify_file(str(html_file))


def main():
    parser = argparse.ArgumentParser(
        description="De-minify HTML files with proper formatting and indentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deminify_html.py input.html
  python deminify_html.py input.html output.html
  python deminify_html.py --batch ./html_files
  python deminify_html.py --batch ./html_files --recursive
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input HTML file')
    parser.add_argument('output', nargs='?', help='Output HTML file (optional)')
    parser.add_argument('--batch', help='Process all HTML files in a directory')
    parser.add_argument('--recursive', action='store_true', 
                       help='Process subdirectories recursively (with --batch)')
    parser.add_argument('--indent', type=int, default=2,
                       help='Number of spaces for indentation (default: 2)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.input and not args.batch:
        parser.error("Either input file or --batch directory must be specified")
    
    if args.batch and args.input:
        parser.error("Cannot specify both input file and --batch directory")
    
    if args.recursive and not args.batch:
        parser.error("--recursive can only be used with --batch")
    
    # Process files
    if args.batch:
        deminify_directory(args.batch, args.recursive)
    else:
        deminify_file(args.input, args.output)


if __name__ == "__main__":
    main()
