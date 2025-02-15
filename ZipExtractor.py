import zipfile
import os
from pathlib import Path
import argparse

def extract_code_files(zip_path, output_file, extensions=None):
    """
    Extract all files with specified extensions from a zip file and combine them into a single text file.
    
    Args:
        zip_path (str): Path to the zip file
        output_file (str): Path where the combined text file will be saved
        extensions (list): List of file extensions to extract (default: ['.c', '.cpp'])
    """
    if extensions is None:
        extensions = ['.c', '.cpp']
    
    # Convert extensions to lowercase for case-insensitive comparison
    extensions = [ext.lower() for ext in extensions]
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Get list of all files in zip
        files = zip_ref.namelist()
        
        # Open output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Process each file in the zip
            for file in files:
                # Check if file has desired extension
                if Path(file).suffix.lower() in extensions:
                    try:
                        # Extract and read the file content
                        with zip_ref.open(file) as code_file:
                            content = code_file.read().decode('utf-8')
                            
                            # Write file header
                            outfile.write(f'\n{"="*50}\n')
                            outfile.write(f'File: {file}\n')
                            outfile.write(f'{"="*50}\n\n')
                            
                            # Write file content
                            outfile.write(content)
                            outfile.write('\n')
                    except UnicodeDecodeError:
                        print(f"Warning: Could not decode {file}. Skipping...")
                    except Exception as e:
                        print(f"Error processing {file}: {str(e)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract and combine code files from a zip archive.')
    parser.add_argument('zip_path', help='Path to the zip file')
    parser.add_argument('output_file', help='Path for the output text file')
    parser.add_argument('--extensions', nargs='+', default=['.c', '.cpp'],
                        help='File extensions to extract (default: .c .cpp)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Ensure extensions start with dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
    
    # Process the zip file
    try:
        extract_code_files(args.zip_path, args.output_file, extensions)
        print(f"Successfully extracted code files to {args.output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()