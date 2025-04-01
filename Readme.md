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

### Deploy to Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Link your GitHub repository
3. Configure the Space to use Docker and specify port 7860

### Deploy to Cloud Services

The application is containerized and can be deployed to any cloud service that supports Docker containers, including:

- AWS ECS/EKS
- Google Cloud Run
- Azure Container Instances
- Digital Ocean App Platform

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the [FLAN-T5 Small model](https://huggingface.co/google/flan-t5-small) developed by Google
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Transformers](https://huggingface.co/docs/transformers/index)
