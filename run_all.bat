@echo off
TITLE GCC System Core Orchestrator Node
CLS

echo =================================================================
echo    GCC Windows Production Platform Automated Launch Toolchain    
echo =================================================================

echo.
echo [Verification Pass]: Auditing runtime dependencies...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [Critical Error]: Python binary is missing from your Windows PATH environment.
    goto error_exit
)
where g++ >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   [Critical Error]: MinGW/GCC compiler (g++) is missing from your Windows PATH environment.
    goto error_exit
)
echo   -^> Local toolchain packages verified successfully.

echo.
echo [Structural Matrix]: Aligning project folder pathways...
if not exist "profiles" mkdir profiles
if not exist "environments" mkdir environments
if not exist "docs" mkdir docs
echo   -^> Directory footprint verified.

echo.
if exist "DimacsParser.cpp" (
    echo [Compilation Pipeline]: Building native multi-threaded constraint shared library...
    g++ -O3 -shared -std=c++11 DimacsParser.cpp -o libverification.dll
    if %ERRORLEVEL% NEQ 0 (
        echo   [Build Error]: Native compilation pass failed via g++.
        goto error_exit
    )
    echo   -^> Production library target compiled successfully: libverification.dll
) else (
    echo [Compilation Skipped]: 'DimacsParser.cpp' source file not detected. Skipping build step.
)

echo.
if exist "validate_environments.py" (
    echo [Validation Step]: Running structural JSON validation checks...
    python validate_environments.py
    if %ERRORLEVEL% NEQ 0 (
        echo   [Validation Fault]: Structural bugs identified inside environment JSON maps.
        goto error_exit
    )
)

echo.
if exist "gcc_narrative_engine.py" (
    echo [System Launch]: Booting local REST server streaming engine node...
    echo   -^> Port mapped to loopback address: http://localhost:8000/blueprint
    echo   -^> Use 'Ctrl+C' inside this window to close communication loops safely.
    echo -----------------------------------------------------------------
    python gcc_narrative_engine.py
) else (
    echo   [Critical Error]: 'gcc_narrative_engine.py' execution master node script missing.
    goto error_exit
)

:error_exit
echo.
echo =================================================================
echo    Execution Stopped. Toolchain encountered a critical breakdown.
echo =================================================================
pause
exit /b 1
