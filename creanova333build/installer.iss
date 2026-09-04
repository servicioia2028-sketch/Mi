#define MyAppName "CreaNova Studio"
#define MyAppVersion "3.3.3"
#define MyAppPublisher "Rodrigo J. Marambio M."
#define MyAppExeName "CreaNova Studio.exe"
[Setup]
AppId={{C8F4257B-8FBA-4F0D-9E2B-4B9E2A8F9C31}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName=CreaNova Studio 3.3.3 Real Full
AppPublisher={#MyAppPublisher}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=CreaNova Studio - Real Full
VersionInfoProductName=CreaNova Studio
VersionInfoProductVersion=3.3.3.0
DefaultDirName={autopf}\CreaNova Studio
DefaultGroupName=CreaNova Studio
OutputDir=installer-output
OutputBaseFilename=CreaNova-Studio-3.3.3-Real-Full-Setup
Compression=lzma2/max
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
WizardStyle=modern
WizardSizePercent=115
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=assets\creanova.ico
DisableProgramGroupPage=yes
[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
[Files]
Source: "dist\CreaNova Studio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{autoprograms}\CreaNova Studio"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\CreaNova Studio"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar CreaNova Studio"; Flags: nowait postinstall skipifsilent
