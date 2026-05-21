# 🏗️ Terraform & Infrastructure as Code (IaC) for GPU Platforms

In the world of AI Infrastructure, managing virtual hardware manually is unacceptable. Instantiating expensive GPU compute clusters (which cost hundreds of dollars daily) demands exact repeatability, automated resource lifecycles, and declarative management. **Terraform** is the standard tool to build, version, and destroy cloud-native GPU pools, security configurations, and Kubernetes nodes safely.

---

## 🏗️ Modular GPU Infrastructure Architecture (AWS EKS)

```
                       ┌────────────────────────┐
                       │  Terraform Root State  │
                       └───────────┬────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   VPC Module     │      │   EKS Module     │      │ GPU Node Module  │
├──────────────────┤      ├──────────────────┤      ├──────────────────┤
│ - Subnets & AZs  │      │ - Control Plane  │      │ - g5.xlarge (T4) │
│ - NAT Gateways   │      │ - OIDC Provider  │      │ - Spot/On-Demand │
│ - Internet Route │      │ - Cluster Sec Grp│      │ - Launch Template│
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 📘 Essential IaC Concepts for AI Systems

### 1. Terraform State and Remote Backends
Terraform compiles declared resource configurations into a file called `terraform.tfstate`. In team environments, this state must reside in a **remote backend** (like AWS S3 or Google Cloud Storage) with active state locking enabled via DynamoDB/GCS native locks. This prevents concurrent executions from corrupting infrastructure configurations.

### 2. GPU Instance Selection & Spot vs. On-Demand Pricing
AI platforms require planning node architectures carefully:
* **On-Demand**: Guaranteed availability. Crucial for core inference endpoints and persistent Vector Databases.
* **Spot Instances**: Up to 90% cheaper but can be terminated by the cloud provider with a 2-minute warning. Excellent for fault-tolerant distributed training, batch processing, and offline evaluations.

---

## 🛠️ Hands-on Lab: Modular AWS EKS GPU Platform

In this lab, you will configure a complete, modular Terraform project to provision an AWS VPC and an Elastic Kubernetes Service (EKS) cluster with a GPU-enabled node group utilizing NVIDIA T4 (G4dn) instances.

### Step 1: Create the Main Configuration (`main.tf`)
Create `main.tf`:
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Provision a Secure VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "ai-platform-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway  = true
  enable_dns_hostnames = true
}

# 2. Provision EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "ai-inference-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  # 3. Configure GPU Nodegroup
  eks_managed_node_groups = {
    gpu_pool = {
      name           = "nvidia-gpu-node-group"
      min_size       = 1
      max_size       = 5
      desired_size   = 2
      instance_types = ["g4dn.xlarge"] # Contains 1 NVIDIA T4 GPU (16GB VRAM)

      # Ensure nodes have correct label and taints for scheduling
      labels = {
        "hardware-type" = "gpu"
        "nvidia.com/gpu" = "true"
      }

      taints = [
        {
          key    = "sku"
          value  = "gpu"
          effect = "NO_SCHEDULE"
        }
      ]

      # Additional IAM Policy needed for GPU Nodes to register with CloudWatch/Systems Manager
      iam_role_additional_policies = {
        AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
      }
    }
  }
}
```

### Step 2: Create Variables Configuration (`variables.tf`)
Create `variables.tf`:
```hcl
variable "aws_region" {
  description = "The target AWS region to deploy AI infrastructure resources"
  type        = string
  default     = "us-east-1"
}

variable "gcp_project_id" {
  description = "Google Cloud Project ID (Optional - for cross-cloud setups)"
  type        = string
  default     = ""
}
```

### Step 3: Create Outputs Configuration (`outputs.tf`)
Create `outputs.tf`:
```hcl
output "cluster_endpoint" {
  description = "Endpoint for EKS control plane API"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS control plane"
  value       = module.eks.cluster_security_group_id
}

output "vpc_private_subnets" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}
```

### Step 4: Run provisioning plan
```bash
# 1. Initialize project and pull modules
terraform init

# 2. Review resources changes before committing
terraform plan

# 3. Apply configurations (This takes ~15 minutes to spin up AWS VPC/EKS)
# terraform apply -auto-approve
```

---

## 🔒 Security Considerations
1. **Private Subnets Only**: EKS GPU worker nodes must always run exclusively within private subnets. Use Nat Gateways to permit egress internet requests while blocking raw public ingress traffic.
2. **State Encryption**: Encrypt state bucket contents using KMS master keys. Ensure no access credentials (e.g. AWS access keys) are declared in clear text; utilize IAM instance roles instead.
3. **Limit Cluster Access**: Enable public endpoint restriction on your EKS API server, limiting traffic exclusively to authorized office CIDRs or VPN gateways.

---

## 📈 Scaling & Observability Considerations
* **Auto-Scaling Constraints**: Keep an eye on Cloud quota limits. AWS limits GPU instantiations strictly on standard accounts. Request higher limits for `G` or `P` instance types in your cloud dashboard before executing Terraform scaling rules.
* **Infracost Integration**: Run `infracost breakdown --path .` in your CI pipeline to calculate monthly dollar projections for modular GPU nodes, preventing billing surprises.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: `Error: InstanceLimitExceeded` during Node Provisioning
* **Root Cause**: The cloud account has hit the region limits for running active GPU instances (e.g. EC2 vCPU limit for G type instances).
* **Diagnostic Command**:
  ```bash
  # Check current vCPU limits using AWS CLI
  aws service-quotas get-service-quota \
    --service-code ec2 \
    --quota-code L-3819A6DF # On-demand G and VT instances quota
  ```
* **Mitigation**:
  1. Switch targeted instance types to less contested GPU shapes (e.g. L4 or G5).
  2. Request a Service Quota limit increase via the Cloud Provider dashboard.
  3. Migrate developer environments to spot configurations which consume spot quotas.

---

## 🌟 Best Practices & Open-Source Tools
* **Infracost**: A powerful billing tool to analyze and display cost diffs on GitHub Pull Requests before running terraform apply.
* **TFLint**: Utilize TFLint to catch cloud-provider specific errors, missing arguments, or sub-optimal practices in your code.
