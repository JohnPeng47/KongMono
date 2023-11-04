@echo off

set ENV_FOR_DYNACONF=development
set REACT_APP_API_ENDPOINT=http://localhost:8000

if "%1"=="server" goto server
if "%1"=="frontend" goto frontend
goto both

:server
echo Running Server...
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongServer && python app.py"
goto end

:frontend
echo Running Frontend...
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongUI && npm run start"
goto end

:both
echo Running both Server and Frontend...
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongServer && python app.py"
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongUI && npm run start"
goto end

:end
