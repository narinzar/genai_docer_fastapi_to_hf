# Text Generation API

A simple FastAPI application that uses Hugging Face's `google/flan-t5-small` model for text generation.

## Features

- REST API built with FastAPI
- Text generation using the FLAN-T5 Small model
- Dockerized application for easy deployment
- Optimized for cloud deployment (including Hugging Face Spaces)

## Requirements

- Python 3.9+
- Docker (optional, for containerized deployment)
- Dependencies listed in `requirements.txt`

## Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/text-generation-api.git
   cd text-generation-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860 --reload
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t text-generation-api .
   ```

2. Run the container:
   ```bash
   docker run -p 7860:7860 text-generation-api
   ```

## API Usage

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

## Examples

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

## Deployment

This project is automatically deployed to Hugging Face Spaces using GitHub Actions.

- GitHub Repository: [https://github.com/yourusername/text-generation-api](https://github.com/yourusername/text-generation-api)
- Hugging Face Space: [https://huggingface.co/spaces/narinzar/genai_docer_fastapi_to_hf](https://huggingface.co/spaces/narinzar/genai_docer_fastapi_to_hf)

### Automatic Deployment

When you push changes to the `main` branch of the GitHub repository, GitHub Actions automatically deploys the updates to the Hugging Face Space.

To manually trigger a deployment, go to the Actions tab in the GitHub repository and run the "Sync to Hugging Face Space" workflow.

### Setup Instructions

To set up automated deployments for your own project:

1. Create a `.env` file with your GitHub and Hugging Face credentials (see `.env.example`)
2. Run the deployment script:
   ```bash
   python deployment_script.py --create-github --push
   ```
3. Add the `HF_TOKEN` secret to your GitHub repository:
   - Go to your repository settings → Secrets → Actions
   - Add a new repository secret with name 'HF_TOKEN' and your Hugging Face token as the value

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the [FLAN-T5 Small model](https://huggingface.co/google/flan-t5-small) developed by Google
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Transformers](https://huggingface.co/docs/transformers/index)
## GitHub Repository

This project is hosted on GitHub:

- Repository: [https://github.com/narinzar/genai_docer_fastapi_to_hf](https://github.com/narinzar/genai_docer_fastapi_to_hf)

### Development

1. Clone the repository:
   ```bash
   git clone https://github.com/narinzar/genai_docer_fastapi_to_hf.git
   cd genai_docer_fastapi_to_hf
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make your changes and push them to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

Last updated: 2025-04-01 09:17:51
