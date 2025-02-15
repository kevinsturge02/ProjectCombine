PyInstaller.__main__.run([
    'ZipExtractorGUI.py',
    '--name=CodeExtractor',
    '--onefile',
    '--windowed',
    '--icon=pc.ico',
    '--clean',
    '--noconfirm',
    '--noupx'  # Add this flag to avoid compression that triggers some antivirus
])