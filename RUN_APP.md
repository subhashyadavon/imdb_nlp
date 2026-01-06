# How to Run the App with Docker

This guide explains how to run the IMDB Sentiment Analysis app using Docker, either by building it locally or pulling the image from GitHub Container Registry (GHCR).

## Prerequisites

1.  **Docker**: Ensure Docker is running. [Install Guide](https://docs.docker.com/get-docker/).


## Automated Build & Push (CI/CD)

This project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically builds and pushes the Docker image to the GitHub Container Registry (GHCR) whenever you push to the `main` branch.

### 1. Verification
After pushing your code, you can verify the image was built:
1.  Go to your GitHub Repository -> **Actions** tab to see the build workflow.
2.  Once successful, go to your GitHub Profile -> **Packages** to see the `imdb-nlp` package.

### 2. Pulling the Image
You can pull the built image from anywhere (assuming you have access or it's public):

```bash
docker pull ghcr.io/subhashyadavon/imdb-nlp:latest
```

### 3. Running the Pulled Image
```bash
docker run -p 5001:8080 ghcr.io/subhashyadavon/imdb-nlp:latest
```
