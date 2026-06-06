# ModMark-Automation

<p align="center">
<img width="313" height="502" alt="Screenshot 2026-06-06 204212" src="https://github.com/user-attachments/assets/8c7f9bff-0dd8-4fce-864d-2c1087216079" />
</p>

## Overview
A lightweight, open-source desktop application designed to optimise the workflow for clerical markers using educational assessment platforms. 

Repetitive clicking during high-volume marking sessions frequently leads to user fatigue and repetitive strain injuries (RSI). This tool solves that bottleneck by translating GUI interactions into customisable keyboard hotkeys. It also features a live analytics dashboard to gamify the marking process and track session efficiency.

## Installation & Usage

***(For colleagues and non-technical users, a compiled `.exe` is available in the [Releases] tab just on the right of this page.)***

**Ignore the following part** if you just want to use the programme:
1. Clone this repository.
2. Install the required dependencies: `pip install pyautogui keyboard`
3. Run `python modmark_gui.py`
4. Use the UI to set your target coordinates and begin marking.

## Key Features
* **Dynamic Auto-Calibration:** A user-friendly, 3-second delay mechanism allowing non-technical users to easily map their specific screen coordinates without touching the code.
* **Custom Key Binding:** Users can define their own hotkeys for standard marks (e.g., 0, 1, and N/A).
* **Live Performance Tracking:** Calculates and visually updates the user's marking rate per minute in real-time.
* **Session Data Export:** Automatically logs session duration, total marks completed, and hourly rates to a `.csv` file upon closing for longitudinal workflow analysis.

## Tech Stack
* **Python 3**
* `tkinter` (Graphical User Interface)
* `pyautogui` (Coordinate mapping and macro execution)
* `keyboard` (Global hotkey listening)

## Important Disclaimer
This tool was developed independently to assist with personal accessibility and workflow efficiency. It is not affiliated with, endorsed by, or supported by Pearson or any other educational assessment organisation. 

Users are strictly responsible for verifying that the use of local accessibility macros and automated UI interactions does not violate their specific employment contracts, terms of service, or institutional IT policies before use. The developer accepts no liability for any automated system flags, account suspensions, or contractual disputes arising from the use of this software.

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](link-to-license) - meaning it is free to use and modify for personal workflow improvement, but cannot be used or distributed for commercial profit.
