# Ollama Cheat Sheet

## Model Management

### List Installed Models
```bash
ollama list
```

### Pull a New Model
```bash
ollama pull modelname
# Examples:
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### Remove a Model
```bash
ollama rm modelname
```

### Show Model Details
```bash
ollama show modelname
```

## Running Models

### Run a Model Interactively
```bash
ollama run modelname
# Examples:
ollama run codellama
ollama run mistral
```

### Exit Interactive Mode
```
/bye
```

## Server and API Management

### Start Ollama Server
```bash
ollama serve
```

### Check Ollama Version
```bash
ollama --version
```

## Advanced Usage

### Create Custom Model
```bash
ollama create custom-modelname -f Modelfile
```

### Run Model with Specific Prompt
```bash
ollama run modelname "Your specific prompt here"
```

## Useful Paths

### Model Storage Location
```
~/.ollama/models/
```

## Troubleshooting

### Check Running Processes
```bash
ps aux | grep ollama
```

### Restart Ollama Service
```bash
sudo systemctl restart ollama
```

## API Interaction

### Basic Curl Example
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "modelname",
  "prompt": "Your question here"
}'
```

## Best Practices
- Ensure sufficient disk space before pulling large models
- Close interactive sessions with `/bye`
- Regularly update Ollama and models
- Use appropriate model for your specific task

## Model Size Reference
- Small models: ~1-4 GB
- Medium models: ~4-8 GB
- Large models: ~8-16 GB

## Recommended Models by Use Case
- General Purpose: Mistral
- Programming: CodeLlama
- Creative Writing: Llama2
- Lightweight Tasks: Phi

## GPU Acceleration
- Ensure CUDA is installed
- Models automatically use GPU if available
- Check GPU compatibility with `nvidia-smi`
