# Running a Hello World App on K3s Cluster


Running a simple `whoami` app on the EC2 K3s cluster.
> ref:
> - https://github.com/traefik/whoami
> - https://hub.docker.com/r/traefik/whoami

## Running a container manually

- Manuallly running a one-off pod:
    ```shell
    kubectl run <pod-name> --image=<image-name>

    # Eg.
    kubectl run whoami --image=traefik/whoami --port=80
    ```

- Check the pod is running:
    ```shell
    kubectl get pods
    NAME     READY   STATUS    RESTARTS   AGE
    whoami   1/1     Running   0          53m

    kubectl get pods -o wide
    NAME     READY   STATUS    RESTARTS   AGE   IP          NODE                                        NOMINATED NODE   READINESS GATES
    whoami   1/1     Running   0          61m   10.42.1.4   ip-10-51-65-79.us-west-2.compute.internal   <none>           <none>
    ```

    Get more details about the pod: `kubectl describe pod <pod-name>`

    ```shell
    kubectl describe pod whoami

    Name:             whoami
    Namespace:        default
    Priority:         0
    Service Account:  default
    Node:             ip-10-51-65-79.us-west-2.compute.internal/10.51.65.79
    Start Time:       Sat, 22 Nov 2025 14:40:23 +0530
    Labels:           run=whoami
    Annotations:      <none>
    Status:           Running
    IP:               10.42.1.4
    IPs:
    IP:  10.42.1.4
    Containers:
    whoami:
        Container ID:   containerd://1c38c69f4db81815bf04f723e4669d7750ca32ffccf8fb8413871be7af143647
        Image:          traefik/whoami
        Image ID:       docker.io/traefik/whoami@sha256:200689790a0a0ea48ca45992e0450bc26ccab5307375b41c84dfc4f2475937ab
        Port:           80/TCP
        Host Port:      0/TCP
        State:          Running
        Started:      Sat, 22 Nov 2025 14:40:25 +0530
        Ready:          True
        Restart Count:  0
        Environment:    <none>
        Mounts:
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-wqhl6 (ro)
    Conditions:
    Type                        Status
    PodReadyToStartContainers   True 
    Initialized                 True 
    Ready                       True 
    ContainersReady             True 
    PodScheduled                True 
    Volumes:
    kube-api-access-wqhl6:
        Type:                    Projected (a volume that contains injected data from multiple sources)
        TokenExpirationSeconds:  3607
        ConfigMapName:           kube-root-ca.crt
        Optional:                false
        DownwardAPI:             true
    QoS Class:                   BestEffort
    Node-Selectors:              <none>
    Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                                node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
    Events:                      <none>
    ```

- Accessing the Pod:

    - Port-forwarding
        ```shell
        kubectl port-forward pod/whoami 8080:80
        ```
        Now access the app at: `http://localhost:8080`
        - Other endpoints:
          - `/api` - Returns a JSON response with details about the request.
          - `/headers`, `/ip`
        - `wscat -c ws://localhost:8080/echo` - WebSocket echo endpoint.


- Deleting the Pod:
    ```shell
    kubectl delete pod whoami
    ```