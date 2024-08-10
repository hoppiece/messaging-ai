group "default" {
    targets = ["api"]
}

variable "ECR_REGISTRY" {
    default = "$ECR_REGISTRY"
}

variable "ECR_REPOSITORY" {
    default = "carechat-ecr-repo"
}

variable "GITHUB_SHA" {
    default = "$GITHBU_SHA"
}

target "api" {
    push = true
    context="."
    dockerfile = "Dockerfile"
    target = "runner"
    tags = [
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest",
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:${GITHUB_SHA}"
    ]
}
