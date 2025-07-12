Obscyrus 1.1


Overview


Obscyrus 1.1 is a state-of-the-art local offline Large Language Model (LLM) designed for seamless, self-contained AI interactions. Built on a Mixture of Experts (MoE) 
Qwen3 8B model and fine-tuned on Claude 4 Opus data, Obscyrus excels in generating, editing, and optimizing code for offline web applications. It specializes in Python 
backends (using frameworks like Flask and SocketIO) paired with HTML, CSS, and JavaScript frontends, leveraging JSON for efficient data storage and management.

This repository contains everything needed to run Obscyrus fully offline — no internet required after initial setup. Obscyrus can code new projects, edit workspace files, 
save conversations for future reference, and maintain memory across sessions, making it an ideal tool for developers building isolated, performant applications.


Features


--Offline Operation: Runs entirely on your local machine without any external dependencies after setup.

--Code Generation and Editing: Hardwired to create complete offline web apps, including Python servers, HTML/CSS/JS clients, and JSON-based data handling.

--Workspace Management: Edit and manage files in a dedicated workspace directory.

--Conversation Persistence: Save and load conversations, with the ability to refer to past memory for context-aware responses.

--Advanced Capabilities: Supports tools for problem-solving, humor-infused responses, and comparisons to other LLMs when relevant.


Prerequisites


--Python 3.8 or higher (tested up to 3.12).


Setup


--Run the AutoPIP.py script to handle all dependencies (Flask, SocketIO, Llama.cpp, Hugging Face Hub (First-
   Time Only) This script attempts standard installation, falls back to user-level install if permissions are 
   an issue, and as a last resort, installs to a local PIP_Packages directory (modifying sys.path for immediate 
   use).
   
--Run the VERIFY_PIP.py script to check if all packages are installed correctly.
  Output will show color-coded status (green for installed, red for missing).
  
--Download the LLM Model (First-Time Only): Automatically fetch the GGUF model file from Hugging Face (requires 
  internet for this step only)


Usage


After setup, interact with Obscyrus anytime— online or offline — by running the main script:

--Run:
  python Obscyrus1.1.py
  
--This launches a local web server (at http://127.0.0.1:8854 by default), opening a browser interface for chatting, coding, 
  and managing workspaces. The LLM loads automatically, and you can select models from the GGUFs directory.


Contributions


Contributions are welcome! Fork the repo, make your changes, and submit a pull request. Focus on enhancements to Python, HTML/CSS/JS integration, or JSON handling for offline apps.
