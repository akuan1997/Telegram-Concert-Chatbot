@echo off
cd C:\Users\pfii1\akuan\git-repos\2024_Concert_Chatbot
set currentDate=%date:~0,4%%date:~5,2%%date:~8,2%
git add .
git commit -m "%currentDate%"
git push