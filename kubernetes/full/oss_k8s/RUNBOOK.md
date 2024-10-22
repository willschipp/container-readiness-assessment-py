### Don't use debian; use Ubuntu

[enter sudo]
0. create files
1. scripts/setup.sh
[exit sudo]
2. `mkdir ~/.kube && sudo cp -i /etc/kubernetes/admin.conf .kube/config && sudo chown $(id -u):$(id -g) .kube/config`
3. scripts/step2.sh
4. `watch kubectl get pods -n calico-system`
5. create ns and operator files
6. `curl -L https://istio.io/downloadIstio | sh -`
7. `sudo mv ./istio-/bin/istioctl /usr/local/bin/.`
8. create ingress.yaml
9. scripts/step3.sh
10. `watch kubectl get pods -n gpu-operator`
11. scripts/step4.sh