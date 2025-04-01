# FastAPI Text Generation with FLAN-T5

A simple FastAPI application that uses Hugging Face's `google/flan-t5-small` model for text generation.

## Project Structure

- `app.py` - The FastAPI application
- `Dockerfile` - Docker configuration for containerization
- `requirements.txt` - Python dependencies
- `push.py` - Simple script for pushing code to GitHub or Hugging Face

## Setup Instructions

### Prerequisites

1. Create your repositories manually before using these scripts:
   - Create a GitHub repository at: https://github.com/new
   - Create a Hugging Face Space at: https://huggingface.co/spaces/new
     - Select "Docker" as the SDK

2. Install Python requirements:
   ```bash
   pip install GitPython python-dotenv requests
   ```

3. Create a `.env` file with your credentials:
   ```
   # GitHub Configuration
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_personal_access_token
   REPO_NAME=your_repository_name
   
   # Hugging Face Configuration
   HF_USERNAME=your_huggingface_username
   HF_TOKEN=your_huggingface_token
   HF_SPACE_NAME=your_space_name
   ```

### Using the Push Script

This repository includes a simple script (`push.py`) that makes it easy to push your code to GitHub or Hugging Face.

#### Push to GitHub

```bash
python push.py github
```

#### Push to Hugging Face Space

```bash
python push.py hf
```

#### Force Push (if needed)

```bash
python push.py github --force
python push.py hf --force
```

## API Usage

Once deployed, the API provides two endpoints:

### Home Endpoint

```
GET /
```

Returns a welcome message.

### Text Generation Endpoint

```
GET /generate?text=your text here
```

Parameters:
- `text` (string, required): The input text for generation

Returns:
- JSON object with the generated text in the `output` field

## Example

### Example Request

```bash
curl -X GET "http://localhost:7860/generate?text=Explain%20quantum%20computing"
```

### Example Response

```json
{
  "output": "Quantum computing uses quantum bits or qubits which can exist in multiple states at once, allowing for parallel computations."
}
```

## License

MIT License