[Setup]
AppName=Code Extractor
AppVersion=1.0
DefaultDirName={pf}\CodeExtractor
DefaultGroupName=Code Extractor
OutputDir=installer
OutputBaseFilename=CodeExtractor_Setup

[Files]
Source: "dist\CodeExtractor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Code Extractor"; Filename: "{app}\CodeExtractor.exe"
Name: "{commondesktop}\Code Extractor"; Filename: "{app}\CodeExtractor.exe"