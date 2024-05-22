@echo off
cd C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot
set "year=%date:~8,2%"
set "month=%date:~0,2%"
set "day=%date:~3,2%"
git add .
git commit -m "%year%%month%%day%"
git push