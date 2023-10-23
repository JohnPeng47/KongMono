@echo off
set ENV_FOR_DYNACONF=development
set REACT_APP_API_ENDPOINT=http://localhost:8000
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongServer && python app.py"
start cmd /C "cd C:\Users\jpeng\Documents\business\kongyiji\kongserver\KongUI && npm run start"
