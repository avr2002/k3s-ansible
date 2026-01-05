## Basic K8s Concepts

Before deploying anything, learn what these four things are:

1. Pods: The smallest runnable unit. Inside a Pod is a container (like Docker).

2. Deployments: A Deployment manages Pods for you.

    It ensures:
   - How many copies (replicas) of your app you want
   - Rolling updates
   - Auto-recovery

3. Services: Pods get random IPs. Services give you a stable NETWORK identity.
   - ClusterIP → internal only
   - NodePort → exposed on every node
   - LoadBalancer → cloud-provider external LB


## Basic `kubectl` Commands

The following are basic `kubectl` commands for interacting with a Kubernetes cluster:

**Getting Information:**

- `kubectl get <resource>`: Lists resources of a specific type (e.g., `pods`, `deployments`, `services`, `nodes`, `namespaces`).
    - Example: `kubectl get pods` (lists all pods in the current namespace)
    - Example: `kubectl get nodes` (lists all nodes in the cluster)
    - Example: `kubectl get all` (lists various common resources in the current namespace)

- `kubectl describe <resource> <resource-name>`: Provides detailed information about a specific resource.       
  - Example: `kubectl describe pod my-pod-name`

- `kubectl describe <resource> <resource-name>`: Provides detailed information about a specific resource.
  - Example: `kubectl describe pod my-pod-name`
 

- `kubectl logs <pod-name>`: Displays the logs of a pod's container.

- `kubectl cluster-info`: Shows information about the cluster's control plane and services.

- `kubectl config current-context`: Displays the name of the currently active Kubernetes context.

- `kubectl config get-contexts`: Lists all available Kubernetes contexts.

**Creating and Modifying Resources:**

- `kubectl apply -f <filename.yaml>`: Creates or updates resources defined in a YAML or JSON file.

- `kubectl create namespace <namespace-name>`: Creates a new namespace.

- `kubectl run <pod-name> --image=<image-name>`: Creates a basic pod from a specified image.

- `kubectl edit <resource>/<resource-name>`: Opens the resource's definition in your default editor for modification.

**Interacting with Pods:**

- `kubectl exec -it <pod-name> -- <command>`: Executes a command inside a pod's container (interactive mode).
    
    - Example: `kubectl exec -it my-pod-name -- /bin/bash` (opens a bash shell in the pod)

- `kubectl cp <source-path> <pod-name>:<destination-path>`: Copies files to or from a pod's container.

**Deleting Resources:**

- `kubectl delete <resource> <resource-name>`: Deletes a specific resource.

    - Example: `kubectl delete pod my-pod-name`

- `kubectl delete -f <filename.yaml>`: Deletes resources defined in a YAML or JSON file.

**Important Flags:**

- `n <namespace-name>` or `-namespace=<namespace-name>`: Specifies the namespace for the command.
- `o yaml` or `o json`: Specifies the output format as YAML or JSON.
- `o wide`: Provides more detailed output for `kubectl get` commands.
- `-dry-run=client`: Shows what would happen without actually making changes (useful for `apply` or `create`).
