group "default" {
    targets = ["api"]
}

variable "ECR_REGISTRY" {
    default = "$ECR_REGISTRY"
}

variable "ECR_REPOSITORY" {
    default = "zato-poc"
}

variable "GITHUB_SHA" {
    default = "$GITHBU_SHA"
}

target "api" {
    push = true
    context="."
    dockerfile = "Dockerfile"
    target = "runner"
    provenance = false
    tags = [
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest",
        "${ECR_REGISTRY}/${ECR_REPOSITORY}:${GITHUB_SHA}"
    ]
}
