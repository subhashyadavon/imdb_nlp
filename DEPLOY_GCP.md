# Deploying IMDB Sentiment Analysis to Google Cloud Platform

This guide outlines the steps to deploy your containerized application to **Google Cloud Run**.

## Prerequisites

1.  **Google Cloud SDK**: Ensure `gcloud` is installed. [Install Guide](https://cloud.google.com/sdk/docs/install).
2.  **Docker**: Ensure Docker is running. [Install Guide](https://docs.docker.com/get-docker/).
3.  **GCP Project**: A Google Cloud project with billing enabled.

## Deployment Steps

### 1. Initialize Google Cloud SDK
Run the following in your terminal and follow the prompts to log in and select your project:
```bash
gcloud init
```

### 2. Configure Docker Authentication
Configure Docker to use Google Cloud credentials:
```bash
gcloud auth configure-docker
```

### 3. Build and Push the Image
Replace `PROJECT_ID` with your actual GCP Project ID.

**Build the image:**
```bash
docker build -t gcr.io/PROJECT_ID/imdb-nlp .
```

**Push to Google Container Registry:**
```bash
docker push gcr.io/PROJECT_ID/imdb-nlp
```

### 4. Deploy to Cloud Run
Run the deployment command. Replace `mnlp` with your desired service name.
```bash
gcloud run deploy imdb-nlp \
  --image gcr.io/PROJECT_ID/imdb-nlp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. Access Your App
Once deployed, the terminal will output a **Service URL** (e.g., `https://imdb-nlp-xyz.a.run.app`). Click it to view your live application.

## Troubleshooting

- **502 Bad Gateway**: Check the logs in the GCP Console. It often means the app failed to start (e.g., missing dependencies).
- **Port Issues**: Ensure your `Dockerfile` uses the `$PORT` environment variable (the provided Dockerfile handles this).
