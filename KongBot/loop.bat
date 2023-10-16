@echo off

FOR /L %%i IN (1,1,5) DO (
    echo Iteration: %%i
    python bot.py
)