# Run llama-api-server.wasm
```bash
wasmedge --dir .:. --nn-preload default:GGML:AUTO:Llama-3-Groq-8B-Tool-Use-Q5_K_M.gguf \
llama-api-server.wasm \
--prompt-template groq-llama3-tool  --log-all \
--ctx-size 2048 \
--model-name llama3
```

# Set BASE_URL & MODEL_NAME
```bash
export OPENAI_MODEL_NAME="llama3"
export OPENAI_BASE_URL="http://127.0.0.1:8080/v1"
```

# Install dependencies & Run
```bash
pip install -r requirements.txt
python main.py
```