### Quick Start

The setup assumes you have `uv` and AWS CLI installed.

1. Clone the repo
  ```bash
  # Clone the repo
  git clone https://github.com/avr2002/k3s-ansible.git
  ```

2. Setup the Infra: This will create 3 EC2 instances in AWS using CDK
  ```bash
  cd homelab-cluster/aws

  # Assumes `AWS_PROFILE=sandbox` and `AWS_REGION=us-west-2` 
  ./run cdk-bootstrap
  ./run cdk-deploy
  ```

3. Fetch SSH Key and Create Inventory File with EC2 instance Public IPs
  ```bash
  ./run fetch-ssh-key

  ./run create-inventory-file
  ```

4. Install `kubectl` locally
  ```bash
  brew install kubectl
  ```

5. Setup the k3s Cluster using Ansible
  ```bash
  cd ../k3s-ansible

  # Run the playbook to setup the k3s cluster
  uvx --from ansible-core ansible-playbook playbooks/site.yaml
  ```

6. Get cluster nodes locally:
  ```bash
  kubectl get nodes -o wide
  ```
