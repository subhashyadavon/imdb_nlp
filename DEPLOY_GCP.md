# Deploying IMDB Sentiment Analysis to Google Cloud Platform

This guide outlines the steps to deploy your containerized application to **Google Cloud Run**.

## Prerequisites

1.  **Google Cloud SDK**: Ensure `gcloud` is installed. [Install Guide](https://cloud.google.com/sdk/docs/install).
2.  **Docker**: Ensure Docker is running. [Install Guide](https://docs.docker.com/get-docker/).
3.  **GCP Project**: A Google Cloud project with billing enabled.

## Automated Deployment (CI/CD)

This project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) to automatically build and deploy changes pushed to the `main` branch.

## Troubleshooting

- **502 Bad Gateway**: Check the logs in the GCP Console. It often means the app failed to start (e.g., missing dependencies).
- **Port Issues**: Ensure your `Dockerfile` uses the `$PORT` environment variable (the provided Dockerfile handles this).

## Automated Deployment (CI/CD)

This project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) to automatically build and deploy changes pushed to the `main` branch.

### 1. Setup GitHub Secrets
Navigate to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions** and add the following secrets:

1.  `GCP_PROJECT_ID`: Your Google Cloud Project ID.
2.  `GCP_SA_KEY`: The JSON key of a Service Account with permissions to deploy.

### 2. Configure Google Cloud Permissions
1.  **Create a Service Account**:
    ```bash
    gcloud iam service-accounts create github-actions-deployer
    ```
2.  **Grant Permissions**:
    Run the following commands to assign necessary roles:
    ```bash
    gcloud projects add-iam-policy-binding PROJECT_ID \
      --member="serviceAccount:github-actions-deployer@PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/run.admin"

    gcloud projects add-iam-policy-binding PROJECT_ID \
      --member="serviceAccount:github-actions-deployer@PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/iam.serviceAccountUser"
    ```
3.  **Generate Key**:
    ```bash
    gcloud iam service-accounts keys create sa-key.json \
      --iam-account=github-actions-deployer@PROJECT_ID.iam.gserviceaccount.com
    ```
    Copy the contents of `sa-key.json` into the `GCP_SA_KEY` GitHub Secret.

### 3. Make GHCR Package Public (Important)
By default, Cloud Run cannot pull images from a private GitHub Container Registry without complex authentication. The easiest way is to:
1.  Push your code to trigger the first build (it will fail at deployment, but create the package).
2.  Go to your GitHub Profile -> **Packages**.
3.  Click on the `imdb-nlp` package.
4.  Go to **Package settings** -> **Change package visibility** -> Select **Public**.
5.  Re-run the workflow.
