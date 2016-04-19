[Setup]
AppName=PyPoco Test
AppVersion=%VERSION%
DefaultDirName={code:DefDirRoot}\pypoco
UsePreviousAppDir=no     
DefaultGroupName=pypoco             
UninstallDisplayIcon={app}\pypoco\pypoco.exe
OutputDir=../
WizardImageFile=./images/installer.bmp
WizardSmallImageFile=./images/logo.bmp
PrivilegesRequired=none
LicenseFile=license.txt
ChangesEnvironment=true

[Tasks]
Name: "Add2PathNone";   GroupDescription: "Add pypoco to PATH:"; Description: "Do not add pypoco to path"; Flags: exclusive unchecked
Name: "Add2PathSystem"; GroupDescription: "Add pypoco to PATH:"; Description: "Add pypoco to system path (require admin privileges)"; Flags: exclusive unchecked
Name: "Add2PathUser";   GroupDescription: "Add pypoco to PATH:"; Description: "Add pypoco to current user path (recommended)"; Flags: exclusive
Name: "DesktopShortcut";  Description: "Create pypoco desktop icon"; Flags: unchecked

[Files]
Source: "pypoco/*"; DestDir: "{app}/pypoco"; AfterInstall: CreateBatch(); Flags: ignoreversion recursesubdirs createallsubdirs;
Source: "docs/*.*"; DestDir: "{app}/docs";
                                            
[Icons]
Name: "{group}\docs"; Filename: "{app}\docs"
Name: "{userdesktop}\pypoco"; Filename: "{%COMSPEC}"; Parameters: "/K """"{app}/pypoco/pypocopath.bat"""""; WorkingDir: "{%HOMEPATH}"; IconFilename: "{app}\icon.ico"; Comment: "pypoco console"; Tasks: DesktopShortcut
Name: "{group}\pypoco"; Filename: "{%COMSPEC}"; Parameters: "/K """"{app}/pypoco/pypocopath.bat"""""; WorkingDir: "{%HOMEPATH}"; IconFilename: "{app}\icon.ico"; Comment: "pypoco console";
Name: "{group}\{cm:UninstallProgram,pypoco}"; Filename: "{uninstallexe}";
                       
[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueName: "Path"; ValueType: "string"; ValueData: "{app}\pypoco;{olddata}"; Check: NotOnSystemPathAlready(); Flags: preservestringtype; Tasks: Add2PathSystem
Root: HKCU; Subkey: "Environment"; ValueName: "Path"; ValueType: "string"; ValueData: "{app}\pypoco;{olddata}"; Check: NotOnUserPathAlready(); Flags: preservestringtype; Tasks: Add2PathUser

[Code]
function NotOnSystemPathAlready(): Boolean;
var
  BinDir, Path: String;
begin
  Log('Checking if pypoco\pypoco dir is already on the %PATH%');
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path) then
  begin // Successfully read the value
    BinDir := ExpandConstant('pypoco\pypoco');
    Log('Looking for pypoco dir in %PATH%: ' + BinDir + ' in ' + Path);
    if Pos(LowerCase(BinDir), Lowercase(Path)) = 0 then
    begin
      Log('Did not find pypoco\pypoco dir in %PATH% so will add it');
      Result := True;
    end
    else
    begin
      Log('Found pypoco\pypoco dir in %PATH% so will not add it again');
      Result := False;
    end
  end
  else // The key probably doesn't exist
  begin
    Log('Could not access so assume it is ok to add it');
    Result := True;
  end;
end;

function NotOnUserPathAlready(): Boolean;
var
  BinDir, Path: String;
begin
  Log('Checking if pypoco\pypoco dir is already on the %PATH%');
  if RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', Path) then
  begin // Successfully read the value
    BinDir := ExpandConstant('pypoco\pypoco');
    Log('Looking for pypoco dir in %PATH%: ' + BinDir + ' in ' + Path);
    if Pos(LowerCase(BinDir), Lowercase(Path)) = 0 then
    begin
      Log('Did not find pypoco\pypoco dir in %PATH% so will add it');
      Result := True;
    end
    else
    begin
      Log('Found pypoco\pypoco dir in %PATH% so will not add it again');
      Result := False;
    end
  end
  else // The key probably doesn't exist
  begin
    Log('Could not access so assume it is ok to add it');
    Result := True;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  BinDir, Path: String;
begin
  if (CurUninstallStep = usPostUninstall)
     and (RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'PATH', Path)) then
  begin
    BinDir := ExpandConstant('{app}\pypoco');
    if Pos(LowerCase(BinDir) + ';', Lowercase(Path)) <> 0 then
    begin
      StringChange(Path, BinDir + ';', '');
      RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'PATH', Path);
    end;
  end;
end;

function IsRegularUser(): Boolean;
begin
	Result := not (IsAdminLoggedOn or IsPowerUserLoggedOn);
end;

function DefDirRoot(Param: String): String;
begin
if IsRegularUser then
	Result := ExpandConstant('{localappdata}')
else
	Result := ExpandConstant('{pf}')
end;

procedure CreateBatch();
var
  fileName : string;
begin
	fileName := ExpandConstant('{app}\pypoco\pypocopath.bat');
	SaveStringToFile(fileName, '@echo off' + #13#10 + ExpandConstant('set PATH=%PATH%;{app}\pypoco'), false);
end;


[Run]
Filename: "{app}\docs\README.TXT"; Description: "View the README file"; Flags: postinstall shellexec skipifsilent unchecked
