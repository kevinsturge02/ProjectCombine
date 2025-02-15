import PyInstaller.__main__

# PyInstaller configuration
PyInstaller.__main__.run([
    'ZipExtractorGUI.py',               # Your main script
    '--name=ProjectCombine',             # Name of the executable
    '--onefile',                        # Create a single executable file
    '--windowed',                       # Don't show console window
    '--icon=pc.ico',                    # Your custom icon
    '--clean',                          # Clean cache before building
    '--noconfirm',                      # Replace output directory without asking
])