#!/bin/bash

# HTML De-minification Script Wrapper
# This script provides a convenient way to run the Python HTML de-minifier

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "HTML De-minification Tool"
    echo ""
    echo "Usage:"
    echo "  $0 <input_file> [output_file]"
    echo "  $0 --batch <directory> [--recursive]"
    echo "  $0 --help"
    echo ""
    echo "Examples:"
    echo "  $0 input.html"
    echo "  $0 input.html output.html"
    echo "  $0 --batch ./html_files"
    echo "  $0 --batch ./html_files --recursive"
    echo ""
    echo "Options:"
    echo "  --batch <dir>     Process all HTML files in directory"
    echo "  --recursive       Process subdirectories recursively (with --batch)"
    echo "  --help           Show this help message"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            print_error "Python is not installed or not in PATH"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
}

# Check if the Python script exists
check_script() {
    if [ ! -f "deminify_html.py" ]; then
        print_error "deminify_html.py not found in current directory"
        exit 1
    fi
}

# Main function
main() {
    # Check dependencies
    check_python
    check_script
    
    # Parse arguments
    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi
    
    case "$1" in
        --help|-h)
            show_usage
            exit 0
            ;;
        --batch)
            if [ -z "$2" ]; then
                print_error "Directory path required for --batch option"
                exit 1
            fi
            
            if [ ! -d "$2" ]; then
                print_error "Directory does not exist: $2"
                exit 1
            fi
            
            print_info "Processing HTML files in directory: $2"
            
            if [ "$3" = "--recursive" ]; then
                print_info "Processing recursively..."
                $PYTHON_CMD deminify_html.py --batch "$2" --recursive
            else
                $PYTHON_CMD deminify_html.py --batch "$2"
            fi
            ;;
        *)
            if [ ! -f "$1" ]; then
                print_error "Input file does not exist: $1"
                exit 1
            fi
            
            if [[ "$1" != *.html ]]; then
                print_warning "File does not have .html extension: $1"
            fi
            
            print_info "Processing file: $1"
            if [ -n "$2" ]; then
                $PYTHON_CMD deminify_html.py "$1" "$2"
            else
                $PYTHON_CMD deminify_html.py "$1"
            fi
            ;;
    esac
}

# Run main function with all arguments
main "$@"
