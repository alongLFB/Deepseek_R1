#### 👾 DeepSeek R1 Gradio Interface

This project provides a simple Gradio interface for interacting with the DeepSeek R1 model via the OpenRouter API.

##### Prerequisites

*   Python 3.10+
*   An OpenRouter API key
*   Gradio
*   OpenAI Python library

##### Installation

1.  Clone this repository:

    ```bash
    git clone https://github.com/alongLFB/Deepseek_R1.git
    cd Deepseek_R1
    ```
2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can install the dependencies individually:

    ```bash
    pip install gradio openai
    ```
3.  Set your OpenRouter API key as an environment variable:

    ```bash
    export OPENROUTER_API_KEY="your_openrouter_api_key"
    export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
    ```

##### Usage

1.  Run the [openrouter_gradio.py](http://_vscodecontentref_/0) script:

    ```bash
    python openrouter_gradio.py
    ```
2.  Open the Gradio interface in your web browser. The URL will be displayed in the terminal (usually something like `http://127.0.0.1:7862`).

##### Features

*   **Chatbot Interface:**  A user-friendly Gradio chatbot interface for interacting with DeepSeek R1.
*   **System Prompt Customization:**  Allows you to modify the system prompt to guide the model's responses.
*   **Clear History:**  A button to clear the chat history.
*   **Streaming Responses:**  Displays the model's responses in real-time as they are generated.

##### Code Structure

*   [openrouter_gradio.py](http://_vscodecontentref_/1): The main script containing the Gradio interface and the logic for interacting with the OpenRouter API.
*   `requirements.txt`: A list of Python packages required to run the project.

##### Environment Variables

*   `OPENROUTER_API_KEY`: Your OpenRouter API key.
*   `OPENROUTER_BASE_URL`: The base URL for the OpenRouter API (defaults to `https://openrouter.ai/api/v1`).

##### Customization

*   **Model Selection:**  You can change the model used by modifying the [model](http://_vscodecontentref_/2) parameter in the [client.chat.completions.create](http://_vscodecontentref_/3) call within the [model_chat](http://_vscodecontentref_/4) function.
*   **System Prompt:**  The default system prompt can be changed by modifying the [default_system](http://_vscodecontentref_/5) variable.
*   **Gradio Interface:**  The Gradio interface can be customized by modifying the [gr.Blocks()](http://_vscodecontentref_/6) definition.

##### Troubleshooting

*   **API Key Issues:**  Make sure your OpenRouter API key is set correctly as an environment variable.
*   **Package Dependencies:**  Ensure that all required Python packages are installed.
*   **Streaming Errors:**  Check your network connection and OpenRouter API status if you encounter issues with streaming responses.
