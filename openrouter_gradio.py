import gradio as gr
from typing import List, Optional, Tuple, Dict
from openai import OpenAI
from http import HTTPStatus
import os
from dotenv import load_dotenv

default_system = 'You are a helpful assistant.'

load_dotenv()

openrouter_api_key = os.getenv('openrouter_api_key')
openrouter_base_url = os.getenv('openrouter_base_url')

client = OpenAI(
    api_key=openrouter_api_key, base_url=openrouter_base_url)


class Role:
    USER = 'user'
    SYSTEM = 'system'
    BOT = 'bot'
    ASSISTANT = 'assistant'
    ATTACHMENT = 'attachment'


History = List[Tuple[str, str]]
Messages = List[Dict[str, str]]


def clear_session() -> History:
    return '', []


def modify_system_session(system: str) -> str:
    if system is None or len(system) == 0:
        system = default_system
    return system, system, []


def history_to_messages(history: History, system: str) -> Messages:
    messages = [{'role': Role.SYSTEM, 'content': system}]
    for h in history:
        messages.append({'role': Role.USER, 'content': h[0]})
        messages.append({'role': Role.ASSISTANT, 'content': h[1]})
    return messages


def messages_to_history(messages: Messages) -> Tuple[str, History]:
    assert messages[0]['role'] == Role.SYSTEM
    system = messages[0]['content']
    history = []
    for q, r in zip(messages[1::2], messages[2::2]):
        history.append([q['content'], r['content']])
    return system, history


def model_chat(query: Optional[str], history: Optional[History], system: str
               ) -> Tuple[str, History, str]:
    if query is None:
        query = ''
    if history is None:
        history = []

    messages = history_to_messages(history, system)
    messages.append({'role': Role.USER, 'content': query})

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages,
        stream=True
    )

    full_response = ""
    if response.response.status_code == HTTPStatus.OK:
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                # Yield partial response
                yield '', history + [[query, full_response]], system
    else:
        raise ValueError('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

    return '', history + [[query, full_response]], system


with gr.Blocks() as demo:
    gr.Markdown("""<center><font size=8>DeepSeek R1👾</center>""")

    with gr.Row():
        with gr.Column(scale=3):
            system_input = gr.Textbox(
                value=default_system, lines=1, label='System')
        with gr.Column(scale=1):
            modify_system = gr.Button(
                "🛠️ Set system prompt and clear history", scale=2)
        system_state = gr.Textbox(value=default_system, visible=False)
    chatbot = gr.Chatbot(label='DeepSeek R1')
    textbox = gr.Textbox(lines=1, label='Input')

    with gr.Row():
        clear_history = gr.Button("🧹 Clear history")
        sumbit = gr.Button("🚀 Send")

    textbox.submit(model_chat,
                   inputs=[textbox, chatbot, system_state],
                   outputs=[textbox, chatbot, system_input],
                   concurrency_limit=40)

    sumbit.click(model_chat,
                 inputs=[textbox, chatbot, system_state],
                 outputs=[textbox, chatbot, system_input],
                 concurrency_limit=40)
    clear_history.click(fn=clear_session,
                        inputs=[],
                        outputs=[textbox, chatbot],
                        concurrency_limit=40)
    modify_system.click(fn=modify_system_session,
                        inputs=[system_input],
                        outputs=[system_state, system_input, chatbot],
                        concurrency_limit=40)

demo.queue(api_open=False)
demo.launch(server_port=7864, max_threads=40)
