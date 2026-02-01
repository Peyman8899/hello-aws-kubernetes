🤖 OpenAI Chatbot on Kubernetes (EKS Ready)This project demonstrates a full DevOps lifecycle: containerizing a Streamlit-based OpenAI chatbot, managing private image registries via AWS ECR, and orchestrating a self-healing deployment using Kubernetes.🏗️ ArchitectureFrontend: Streamlit (Python)Containerization: Docker (Multi-arch support for Apple Silicon & Linux)Registry: AWS Elastic Container Registry (ECR)Orchestration: Kubernetes (Local Docker Desktop / EKS)Security: Kubernetes Secrets for OpenAI API keys and AWS ECR Authentication.🚀 Execution Steps1. AWS ECR AuthenticationAuthenticate your local Docker CLI to your private AWS registry:Bashaws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin [YOUR_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com
2. Docker Build & PushBuild the image natively (ARM64 for Mac M-series) and push to ECR:Bash# Build
docker build -t hello-aws .

# Tag
docker tag hello-aws:latest [YOUR_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/hello-aws:latest

# Push
docker push [YOUR_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/hello-aws:latest
3. Kubernetes Secret ConfigurationKubernetes needs "keys" to pull from private ECR and to talk to OpenAI:Bash# OpenAI Secret
kubectl create secret generic openai-key --from-literal=API_KEY='sk-your-key'

# AWS ECR Secret (Refreshes every 12 hours)
kubectl create secret docker-registry ecr-registry-key \
  --docker-server=[YOUR_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-2)
4. DeploymentApply the manifests to start the pods and the service:Bashkubectl apply -f deployment.yaml
kubectl apply -f service.yaml
🔍 Useful Troubleshooting CommandsCommandPurposekubectl get pods -wWatch pods transition to 'Running' in real-time.kubectl describe pod [NAME]Check 'Events' for ImagePullBackOff or Architecture errors.kubectl logs -f -l app=chatbotStream live application logs from all pods.kubectl rollout restart deployment chatbot-deploymentForce a refresh after updating ECR images.