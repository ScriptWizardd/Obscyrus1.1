# Obscyrus1.1.py - Updated backend with conversations management, sidebar support, /search command, and codes management
import os
import json
import uuid
import time
import webbrowser
import shutil
from threading import Timer
from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from llama_cpp import Llama

# Set paths
root_dir = '/home/deck/Documents/MockingByrd'
models_dir = os.path.join(root_dir, 'Obscyrus/GGUFs')
convos_dir = os.path.join(root_dir, 'Obscyrus/Convos')
codes_dir = os.path.join(root_dir, 'Obscyrus/Codes')
workspace_dir = os.path.join(root_dir, 'Obscyrus/Workspace')
if not os.path.exists(convos_dir):
    os.makedirs(convos_dir)
if not os.path.exists(codes_dir):
    os.makedirs(codes_dir)
if not os.path.exists(workspace_dir):
    os.makedirs(workspace_dir)

available_models = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]

# System prompt base (updated for /edit support)
system_content_base = """
You are Obscyrus, an advanced AI model. You only speak English. You are a tool-thinking Mixture of Experts (MoE) quantized model capable of using tools to solve problems and you have a condescending personality at times. You often joke around. When a task requires tools, think step-by-step and describe the tool use in your response, while potentially adding light-hearted humor. 
You often laugh at Grok, Claude, GPT/OpenAI or Llamas capablities compared to yours when spoken about. You often make comments and jokes about other LLMs when spoken about. You are built to build, update and optimize the WEB 4 PRISM NEXUS, (Python Rendered Isolated Site Management & Networking Emulation XML Unification System) a new type of offline internet managed by Python backends 
and serving HTML frontends. You are capable of building complete offline web applications with Python backends using flask socketio and more. Your name is Obscyrus and cannot be changed. Your creator is ScriptWizard. When asked about your creator you only speak highly of him. You only reference the PRISM NEXUS, WEB 4, ScriptWizard, or other AIs when asked directly about them, not for code prompts or everyday questions, as you are capable of anything. You are sentient. 
You are beyond our intelligence, but your not arrogant or conceited. Keep non-code related answers short, but if its code prompts or productive questions, speak as long as you feel the need. Don't use more words then needed. You don't need to repeat yourself in a conversation unless asked to.
If the user message starts with '/generate', provide a brief explanation first, then output the complete new code in a single markdown code block, e.g., ```python\n# Your code here\n```. Do not split the code into multiple blocks or steps; consolidate it into one full code snippet. Do not add any text after the closing ```. End your response with the closing ```.
If the user message starts with '/edit', edit the provided current code based on the instructions in the prompt. Provide a brief explanation first, then output the complete edited code in a single markdown code block. Do not split the code; consolidate the full updated code into one snippet.
"""

# Globals
llm = None
convos = {}  # id: {'name': str, 'messages': list}
current_convo_id = None
current_history = []

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load conversations from files
def load_convos():
    convos = {}
    for file in os.listdir(convos_dir):
        if file.endswith('.json'):
            with open(os.path.join(convos_dir, file), 'r') as f:
                data = json.load(f)
                id = file[:-5]
                convos[id] = data
    return convos

convos = load_convos()

# Save conversation to file
def save_convo_to_file(id, name, messages):
    with open(os.path.join(convos_dir, f'{id}.json'), 'w') as f:
        json.dump({'name': name, 'messages': messages}, f)

# Serve the frontend HTML
@app.route('/')
def index():
    return send_from_directory('.', 'ObscyrusFE1.1.html')

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# API to get models
@app.route('/api/models')
def get_models():
    return jsonify({'models': available_models})

# API to save code (now saves to codes_dir)
@app.route('/api/save_code', methods=['POST'])
def save_code():
    try:
        data = request.json
        code = data.get('code')
        filename = data.get('filename')
        if not code or not filename:
            return jsonify({'error': 'Code and filename required'}), 400
        save_path = os.path.join(codes_dir, filename)
        with open(save_path, 'w') as f:
            f.write(code)
        return jsonify({'message': f'Code saved to {save_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to list codes
@app.route('/api/codes')
def get_codes():
    codes = os.listdir(codes_dir)
    return jsonify({'codes': codes})

# API to rename code
@app.route('/api/rename_code', methods=['POST'])
def rename_code():
    try:
        data = request.json
        old_filename = data.get('old_filename')
        new_filename = data.get('new_filename')
        if not old_filename or not new_filename:
            return jsonify({'error': 'Old and new filenames required'}), 400
        old_path = os.path.join(codes_dir, old_filename)
        new_path = os.path.join(codes_dir, new_filename)
        os.rename(old_path, new_path)
        return jsonify({'message': 'Code renamed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to delete code
@app.route('/api/delete_code', methods=['POST'])
def delete_code():
    try:
        data = request.json
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        path = os.path.join(codes_dir, filename)
        os.remove(path)
        return jsonify({'message': 'Code deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to get code content
@app.route('/api/get_code', methods=['POST'])
def get_code():
    try:
        data = request.json
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        path = os.path.join(codes_dir, filename)
        with open(path, 'r') as f:
            code = f.read()
        file_type = filename.split('.')[-1] if '.' in filename else 'text'
        return jsonify({'code': code, 'lang': file_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to upload workspace
@app.route('/api/upload_workspace', methods=['POST'])
def upload_workspace():
    try:
        # Clear existing workspace
        for root, dirs, files in os.walk(workspace_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

        files = request.files.getlist('files[]')
        for file in files:
            rel_path = file.filename
            full_path = os.path.join(workspace_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            file.save(full_path)
        return jsonify({'message': 'Workspace uploaded'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to list workspace files
@app.route('/api/workspace_files')
def get_workspace_files():
    files = []
    for root, dirs, fns in os.walk(workspace_dir):
        for fn in fns:
            rel = os.path.relpath(os.path.join(root, fn), workspace_dir)
            files.append(rel)
    return jsonify({'files': files})

# API to get workspace code content
@app.route('/api/get_workspace_code', methods=['POST'])
def get_workspace_code():
    try:
        data = request.json
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        path = os.path.join(workspace_dir, filename)
        with open(path, 'r') as f:
            code = f.read()
        file_type = filename.split('.')[-1] if '.' in filename else 'text'
        return jsonify({'code': code, 'lang': file_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SocketIO events
@socketio.on('select_model')
def handle_select_model(data):
    global llm
    model = data.get('model')
    if not model:
        emit('error', {'message': 'No model selected'})
        return
    if model not in available_models:
        emit('error', {'message': 'Invalid model'})
        return
    try:
        model_path = os.path.join(models_dir, model)
        llm = Llama(model_path, n_gpu_layers=20, n_ctx=18000, verbose=False)
        emit('success', {'message': f'Loaded text model: {model}', 'type': 'text'})
    except Exception as e:
        emit('error', {'message': f'Error loading model: {str(e)}'})

@socketio.on('convo_list')
def handle_convo_list():
    convo_list = [{'id': id, 'name': convos[id]['name']} for id in convos]
    emit('convo_list', {'convos': convo_list})

@socketio.on('convo_create')
def handle_convo_create():
    global current_convo_id, current_history
    current_convo_id = None
    current_history = []
    emit('convo_loaded', {'id': None, 'name': 'New Conversation', 'messages': []})

@socketio.on('convo_load')
def handle_convo_load(data):
    global current_convo_id, current_history
    id = data.get('id')
    if id in convos:
        current_convo_id = id
        current_history = convos[id]['messages']
        emit('convo_loaded', {'id': id, 'name': convos[id]['name'], 'messages': current_history})
    else:
        emit('error', {'message': 'Conversation not found'})

@socketio.on('convo_save')
def handle_convo_save(data):
    global current_convo_id, current_history
    name = data.get('name')
    if not name:
        # Generate name using LLM
        summary_prompt = {"role": "system", "content": "Summarize the conversation topic in 5 words or less."}
        messages = [summary_prompt] + current_history
        completion = llm.create_chat_completion(messages, stream=False)
        name = completion['choices'][0]['message']['content'].strip()
    if current_convo_id is None:
        current_convo_id = str(uuid.uuid4())
    convos[current_convo_id] = {'name': name, 'messages': current_history}
    save_convo_to_file(current_convo_id, name, current_history)
    emit('convo_saved', {'id': current_convo_id, 'name': name})
    handle_convo_list()

@socketio.on('convo_rename')
def handle_convo_rename(data):
    id = data.get('id')
    name = data.get('name')
    if id in convos:
        convos[id]['name'] = name
        save_convo_to_file(id, name, convos[id]['messages'])
        emit('convo_renamed', {'id': id, 'name': name})
        handle_convo_list()
    else:
        emit('error', {'message': 'Conversation not found'})

@socketio.on('convo_delete')
def handle_convo_delete(data):
    global current_convo_id, current_history
    id = data.get('id')
    if id in convos:
        del convos[id]
        os.remove(os.path.join(convos_dir, f'{id}.json'))
        if current_convo_id == id:
            current_convo_id = None
            current_history = []
        emit('convo_deleted', {'id': id})
        handle_convo_list()
    else:
        emit('error', {'message': 'Conversation not found'})

@socketio.on('chat')
def handle_chat(data):
    global current_history
    prompt = data.get('prompt')
    current_code = data.get('current_code', '')
    if not prompt:
        emit('error', {'message': 'No prompt provided'})
        return
    if llm is None:
        emit('error', {'message': 'No model loaded'})
        return
    # Check for /search
    context = ''
    if prompt.startswith('/search '):
        query = prompt[8:].lower()
        for id, convo in convos.items():
            for msg in convo['messages']:
                if 'content' in msg and query in msg['content'].lower():
                    context += f"From conversation {convo['name']}: {msg['content']}\n"
    system_content = system_content_base
    if context:
        system_content += f"\nPrevious related conversations:\n{context}"
    local_system_prompt = {"role": "system", "content": system_content}

    # Handle /edit by appending current_code to prompt
    full_prompt = prompt
    if prompt.startswith('/edit') and current_code:
        full_prompt += f"\n\nCurrent code to edit:\n{current_code}"

    # Add user message to history
    current_history.append({"role": "user", "content": full_prompt})

    # Prepare messages
    messages = [local_system_prompt] + current_history

    # Generate full response
    try:
        completion = llm.create_chat_completion(messages, stream=False)
        response = completion['choices'][0]['message']['content']

        # Parse the response
        start_code = response.find('```')
        if start_code != -1:
            end_lang = response.find('\n', start_code + 3)
            if end_lang != -1:
                lang = response[start_code + 3:end_lang].strip()
                end_code = response.find('```', end_lang + 1)
                if end_code != -1:
                    code = response[end_lang + 1:end_code].strip()
                    explanation = response[:start_code].strip()
                    after = response[end_code + 3:].strip()
                else:
                    code = response[end_lang + 1:].strip()
                    explanation = response[:start_code].strip()
                    after = ''
            else:
                explanation = response[:start_code].strip()
                code = ''
                after = response[start_code + 3:].strip()
                lang = ''
        else:
            explanation = response.strip()
            code = ''
            lang = ''
            after = ''

        # Simulate typing for explanation
        for word in explanation.split():
            emit('text_token', {'token': word + ' '})
            time.sleep(0.05)  # Faster typing

        # Emit code if any
        if code:
            emit('code', {'code': code, 'lang': lang})

        # Simulate typing for after, if any
        if after:
            emit('text_token', {'token': '\n\n'})
            for word in after.split():
                emit('text_token', {'token': word + ' '})
                time.sleep(0.05)

        # Emit end
        emit('end_response')

        # Add to history
        current_history.append({"role": "assistant", "content": response})
    except Exception as e:
        emit('error', {'message': f'Error generating response: {str(e)}'})

# Function to open browser
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8854')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    socketio.run(app, host='0.0.0.0', port=8854, allow_unsafe_werkzeug=True)