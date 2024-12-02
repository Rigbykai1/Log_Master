@echo off
set scriptDir=%~dp0
net session >nul 2>&1
    PowerShell -NoProfile -ExecutionPolicy Unrestricted  ^
        "function IsPythonInstalled { try { $versionOutput = & python --version 2>&1; if ($versionOutput -match 'Python (\d+\.\d+\.\d+)') { return $true } else { return $false } } catch { return $false } }; $pythonInstalled = IsPythonInstalled; if (-not $pythonInstalled) { Write-Host 'Python no está instalado. Instalando Python 3.13.0..; acepta los permisos de administrados para la instalación.'; $installerUrl = 'https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe'; $installerPath = \"$env:TEMP\\python-installer.exe\"; Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath; Start-Process -FilePath $installerPath -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait; $pythonInstalled = IsPythonInstalled; if (-not $pythonInstalled) { Write-Host 'La instalación de Python falló.'; exit }; Write-Host 'Python 3.13.0 instalado correctamente.' } else { Write-Host 'Python ya está instalado.' }"
    if exist "%scriptDir%optimizador.pyw" (
        echo Ejecutando el archivo Python...
        py "%scriptDir%optimizador.py"
    ) else (
        echo No se encontró el archivo optimizador.pyw en la ruta %scriptDir%.
    )
pause