variable "ECR_REGISTRY" {
    default = "$ECR_REGISTRY"
}

variable "ECR_REPOSITORY" {
    default = "zato-poc"
}

variable "GITHUB_SHA" {
    default = "$GITHBU_SHA"
}

target "lambda-image" {
    push = true
    dockerfile = "Dockerfile"
    target = "runner-lambda"
    tags = [
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest",
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:${GITHUB_SHA}"
    ]
}
