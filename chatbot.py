import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)
    data = {
        "model": "llama3",
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None
css = """
"/* Hide the original footer elements */
footer {
    display:  none !important;
}"
"""
iface = gr.Interface(
    fn=generate_response,
    title="AskIt AI",
    description="An AI-powered conversational assistant built on the robust Llama3 model, brought to you by the innovative team at Browseit. Experience seamless and intelligent interactions like never before.",
    inputs=gr.Textbox(lines=10, placeholder="Enter your prompt here..."),
    outputs="text",
    css=css
)

iface.launch(share=True)
