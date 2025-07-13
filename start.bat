@echo off

REM Start Cloudflare tunnel
start cmd /k "cloudflared tunnel --config C:\Users\sreed\.cloudflared\config.yml run"

REM Move to simulation directory
cd RSSI Testing

REM Start 2 python files
start cmd /k "python beacon-simulation.py"
start cmd /k "python hub-simulation.py"

REM Move to backend directory
cd ..
cd backend

REM Start Django server
start cmd /k "python manage.py runserver"

start chrome https://inspetto.ceal.in
