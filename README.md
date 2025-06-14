# YouTube Subtitle Extractor API

A Flask API that extracts clean subtitles from YouTube videos using yt-dlp.

## Quick Start

### For ARM Architecture (Apple Silicon, Raspberry Pi, etc.)

```bash
# Run the container
docker run -d -p 5000:5000 u1ih/ytcc:arm

# Test the API
curl -X POST http://localhost:5000/extract-subtitles \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### For x86/AMD64 Architecture (Intel/AMD processors)

```bash
# Run the container
docker run -d -p 5000:5000 u1ih/ytcc:x86

# Test the API
curl -X POST http://localhost:5000/extract-subtitles \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Features

- Extract English subtitles/closed captions from YouTube videos
- Clean and format subtitles (remove timestamps, XML tags, etc.)
- Return plain text subtitles as ASCII
- Dockerized for easy deployment

## Installation

### Using Docker (Recommended)

#### For ARM Architecture (Apple Silicon, Raspberry Pi, etc.)

```bash
# Pull the image from Docker Hub
docker pull u1ih/ytcc:arm

# Run the container
docker run -d -p 5000:5000 u1ih/ytcc:arm
```

#### For x86/AMD64 Architecture (Intel/AMD processors)

```bash
# Pull the image from Docker Hub
docker pull u1ih/ytcc:x86

# Run the container
docker run -d -p 5000:5000 u1ih/ytcc:x86
```

#### Available Tags

- `latest`: Always points to the most recent stable version (ARM)
- `1`: Version 1 release (ARM)
- `arm`: Specifically built for ARM architecture (Apple Silicon, Raspberry Pi, etc.)
- `x86`: Specifically built for x86/amd64 architecture (Intel/AMD processors)
- `1-x86`: Version 1 release for x86/amd64 architecture

### Building from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/ytcc.git
cd ytcc

# Build the Docker image
docker build -t ytcc .

# Run the container
docker run -d -p 5000:5000 ytcc
```

### Local Development

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
python wsgi.py
```

## Usage

### API Endpoints

#### Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{"status": "ok"}
```

#### Extract Subtitles

Send a POST request to `/extract-subtitles` with a JSON body containing the YouTube URL:

```bash
curl -X POST http://localhost:5000/extract-subtitles \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

Successful Response:
```json
{
  "subtitles": "We're no strangers to love. You know the rules and so do I. I feel commitments from what I'm thinking of. You wouldn't get this from any other guy..."
}
```

Error Response (No subtitles found):
```json
{
  "error": "No subtitles found for this video"
}
```

### Python Example

```python
import requests

url = "http://localhost:5000/extract-subtitles"
data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}

response = requests.post(url, json=data)
if response.status_code == 200:
    subtitles = response.json()["subtitles"]
    print(subtitles)
else:
    print(f"Error: {response.json()}")
```

## How It Works

The API uses yt-dlp to download subtitles from YouTube videos, then processes them to remove timestamps, formatting, and other metadata. The clean text is then returned as a JSON response.

## Error Handling

The API returns appropriate error messages for:
- Missing URL
- Failed subtitle downloads
- Videos without English subtitles
- Processing errors

## Development

If you want to run the application locally without Docker:

1. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```
   python wsgi.py
   ```
