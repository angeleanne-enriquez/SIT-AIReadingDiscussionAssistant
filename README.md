# <p align="center"> AI Reading Discussion Assistant
> Stevens Pinnacle Research Program - Summer 2024

## Project Goal
This project aims to assist online learning for undergraduate/graduate students by having an AI tool generate text summaries, reading questions, and professional reading-based discussions; this may also be helpful for discussions in the professional industry when analyzing new business approaches. While I worked in a team of five, we were all tasked with developing individual programs except for the project lead, who oversaw our progress and provided us material to test with. On my end, I developed an AI, Python application using Claude AI's API and implementing a modern GUI with CustomTkinter. There, a user can upload their own text and ask for a summary, reading-based questions, or a discussion between different AI personas. To test this program, I used a tennis case study and ensured the results were appropriate for the task. I also contributed to a research paper, detailing my programming journey and how I overcame any obstacles.

## How to Use
1. Download the Python program.
3. Replace the API key with your own.
4. Open the Python program and look throughout the program to learn how to use the other features.

## Challenges and Limitations
A huge challenge for this project was ensuring Claude's API would give consisently good results. Initially, I had difficulty with the program timing out or giving incomplete summaries/discussions. I solved this issue by refining my prompt engineering, keeping the instructions for the AI detailed but concise. 

This program cannot handle extremely large PDFs. For instance, it will have difficulty generating a complete discussion for the entirety of the tennis case study uploaded here. However, breaking it down by chapter and uploading such will have better results. 
