---
layout: post
title:  "Kubernetes"
date:   2021-02-07 23:00:00 +0900
author: Taeho Oh
tags: [ 오태호, Kubernetes ]
---

안녕하세요. 오태호입니다.

Kubernetes는 다수의 Container들을(보통은 Docker Container들을) 체계적으로 관리할 수 있게 도와주는 Platform입니다.

Kubernetes는 상당히 방대한 내용을 가진 주제라서 어디서부터 살펴보면 좋을지 파악하기가 쉽지 않습니다. 이 글에서는 Kubernetes에 대해 사전지식이 없는 사람이 Kubernetes에 대해 조금이라도 쉽게 이해할 수 있도록 도와드립니다.

이 글은 Kubernetes 1.20, Ubuntu 18.04.5, VirtualBox 5.2.42, Docker 19.03.6, Flannel 0.13.1-rc2, MetalLB 0.9.5, Metrics Server 0.4.1을 기준으로 작성하였습니다.

Test한 Host의 CPU는 Intel i7-4790S이며 Memory는 16GB입니다.

이 글을 이해하기 위해서는 Ubuntu, VirtualBox, Docker, Network에 대한 기초지식이 필요합니다.

## Pod and Node {#Pod-and-Node}

Kubernetes를 보면 Pod와 Node라는 다소 생소한 용어를 접하게 됩니다. Pod와 Node에 대해 간단히 살펴보겠습니다.

#### Pod {#Pod}

Pod는 여러 Container들을 가지고 있는 묶음입니다. 각각의 Pod는 Cluster안에서 Unique한 IP Address를 가집니다. 그래서, 한 Cluster안에서는, 어느 한 Pod에서 다른 Pod로 NAT(Network Address Translation)의 도움 없이 쉽게 접속할 수 있습니다. Pod의 IP Address는 Private IP Address라서 Internet에서는 사용이 불가능한 IP Address지만 Cluster내에서는 Public IP Address처럼 사용할 수 있습니다.

#### Node {#Node}

Node는 여러개의 Pod를 가지고, 가지고 있는 Pod들을 실행하는 Machine으로, Physical Machine일 수도 있고 Virtual Machine일 수도 있습니다. Node는 Master Node와 Worker Node가 있으며 Master Node가 여러 Worker Node들을 관리합니다. 각각의 Node는 IP Address를 가집니다. Node들이 모여서 Cluster를 구성합니다. 한 Pod 안에 있는 모든 Container들은 한 Node에서 실행됩니다. 즉, 한 Pod 안에 있는 각각의 Container들이 여러 Node에 분산되어 실행되지는 않습니다.

정리하면 Cluster는 여러 Node들을 가지고, 한 Node는 여러 Pod들을 가지며, 한 Pod는 여러 Container들을 가집니다.

## Setup Kubernetes Cluster on VirtualBox {#Setup-Kubernetes-Cluster-on-VirtualBox}

Kubernetes Cluster를 설정하는 방법은 여러가지 방법이 있습니다. Minikube를 사용하면 아주 간편하게 Kubernetes Cluster를 설정할 수 있지만, Minikube는 Single Node로만 사용이 가능한 단점이 있는 관계로, 여기서는 다소 번거롭지만 VirtualBox 1대를 Master Node로 설정하고 VirtualBox 3대를 Worker Node로 설정해서 Kubernetes Cluster를 구성해 보도록 하겠습니다.

#### Network {#Network}

VirtualBox의 Network Adapter는 실제 Network 환경과 매우 유사한 형태인 Bridged Adapter로 설정할 예정입니다. Bridged Adapter로 설정하게 되면 VirtualBox의 Guest들은 Host와 같은 Switch Hub에 연결되어 있는 것처럼 동작하게 됩니다. 즉, Guest들은 Host와 동일한 대역의 IP Address를 사용하게 되고 동일한 인터넷 공유기의 DHCP Server를 사용해서 IP Address를 할당받게 됩니다.

Kubernetes의 Master Node는 한 번 설정한 후에 IP Address가 변경되게 되면 다시 설정하기가 매우 번거롭게 되어 있습니다. 그래서 여기서는 VirtualBox의 모든 Network 설정을 인터넷 공유기의 DHCP Server를 사용하지 않고 Static IP Address로 설정할 예정입니다. Static IP Address로 설정할 주소를 알아보기 위해 현재 사용중인 Network에서 인터넷 공유기의 DHCP Server가 할당하지 않는 IP Address들을 조사하고 필요하면 적당한 IP Address들을 인터넷 공유기의 DHCP Server가 할당하지 않도록 설정합니다. 해당 IP Address들을 Kubernetes Cluster를 설정하면서 사용할 예정입니다.

여기서는 다음과 같은 IP Address 구성으로 Kubernetes Cluster를 설정할 예정입니다. External IP Address에 대해서는 나중에 다시 설명할 예정입니다. 일단 여기서는 External IP Address로 사용할 IP Address들을 적당히 확보합니다.

* Master Node IP Address
  * 172.30.1.231
* Worker Node IP Address
  * 172.30.1.232
  * 172.30.1.233
  * 172.30.1.234
* External IP Address
  * 172.30.1.235
  * 172.30.1.236
  * 172.30.1.237
  * 172.30.1.238
  * 172.30.1.239
  * 172.30.1.240

Static IP Address의 구성을 위한 현재 Network 환경의 설정을 조사합니다. 이 글에서는 다음과 같은 Network 환경의 설정을 기반으로 설명을 진행합니다.

* Netmask
  * 255.255.255.0
* Gateway
  * 172.30.1.254
* Name Server
  * 168.126.63.1
  * 168.126.63.2

#### VirtualBox {#Install-VirtualBox}

Host에서 다음과 같이 실행하여 VirtualBox를 설치합니다.

```
$ sudo apt-get install -y virtualbox
```

#### Install Ubuntu {#Install-Ubuntu}

VirtualBox에 Virtual Machine을 하나 새로 만들어서 Ubuntu를 Guest로 설치합니다. 여기서는 Ubuntu Desktop보다 가벼운 Ubuntu Server를 설치합니다.

VirtualBox의 Settings를 다음과 같이 설정해서 설치합니다.

* General > Basic > Name
  * master-node
* General > Basic > Type
  * Linux
* General > Basic > Version
  * Ubuntu (64-bit)
* System > Motherboard > Base Memory
  * 2048MB
* System > Processor > Processor
  * 2CPUs
* Storage > Optical Drive
  * ubuntu-18.04.5-live-server-amd64.iso
* Network > Adapter 1 > Attached to
  * Bridged Adapter

참고로 System > Motherboard > Base Memory를 1024MB로 설정하면 Kubernetes 설정중에 `[ERROR Mem]: the system RAM (984 MB) is less than the minimum 1700 MB` Error가 발생합니다.

참고로 System > Processor > Processor를 1CPU로 설정하면 Kubernetes 설정중에 `[ERROR NumCPU]: the number of available CPUs 1 is less than the required 2` Error가 발생합니다.

Ubuntu 설치중에 Server Name은 master-node로 설정합니다. 편리한 사용을 위해 OpenSSH Server도 설치하도록 설정합니다.

Ubuntu의 설치가 끝나면 Reboot합니다.

#### Install Guest Additions {#Install-Guest-Additions}

VirtualBox에서는 Guest OS에 Guest Additions를 설치하면 더 쾌적하게 Guest를 사용할 수 있습니다. Devices > Insert Guest Additions CD image를 선택하고, 다음과 같이 Guest Additions를 설치하고, Reboot합니다.

```
$ sudo apt-get install -y dkms build-essential linux-headers-generic linux-headers-$(uname -r)
$ sudo mkdir /media/cdrom
$ sudo mount /dev/cdrom /media/cdrom
$ cd /media/cdrom
$ sudo ./VBoxLinuxAdditions.run
$ sudo reboot
```

#### Disable Swap {#Disable-Swap}

Kubernetes는 각 Node에 Pod를 적절하게 배치시켜서 최대한의 성능을 끌어내려고 시도합니다. 그런데 이때 Swap이 Enable되어 있으면 성능을 제대로 끌어내지 못합니다. 그래서 다음과 같이 Guest에서 실행해서 Swap을 Disable합니다.

```
$ sudo vi /etc/fstab
(Comment out swap)
$ sudo swapoff -a
$ free
              total        used        free      shared  buff/cache   available
Mem:        2040968       79272     1545724         668      415972     1811544
Swap:             0           0           0
$
```

#### Install Docker {#Install-Docker}

다음과 같이 Guest에서 실행해서 Docker를 설치합니다.

```
$ sudo apt-get update -y
$ sudo apt-get install -y docker.io
```

Docker를 Kubernetes와 사용하기 위해서는 Docker의 cgroup driver를 systemd로 변경해야 합니다. 다음과 같이 Guest에서 실행해서 Docker의 cgroup driver를 systemd로 변경합니다.
```
$ sudo vi /etc/docker/daemon.json
```

다음과 같이 입력하고 저장합니다.
```
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

참고로 Docker의 cgroup driver를 systemd로 변경하지 않으면 Kubernetes 설정중에 `[WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd"` Warning Message가 출력됩니다.

다음과 같이 Guest에서 실행해서 Docker를 실행합니다.
```
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

#### Install Kubernetes {#Install-Kubernetes}

다음과 같이 Guest에서 실행해서 Kubernetes를 설치하고 전원을 끕니다. kubeadm, kubelet, kubectl이 의도치않게 Upgrade되지 않도록 설치후 Version을 apt-mark hold를 사용해서 고정합니다.

```
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
$ sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
$ sudo apt-get update -y
$ sudo apt-get install -y kubelet kubeadm kubectl
$ sudo apt-mark hold kubeadm kubelet kubectl
$ sudo poweroff
```

#### Clone Virtual Machine {#Clone-Virtual-Machine}

VirtualBox에서 지금까지 작업한 master-node Virtual Machine을 Clone하는 것을 3번 반복해서 Worker Node Virtual Machine 3개를 만듭니다. 각각 Clone하면서 Machine Name을 worker-node-1, worker-node-2, worker-node-3로 설정합니다.

#### Setup Master Node {#Setup-Master-Node}

다음과 같이 master-node Guest에서 실행해서 Static IP Address를 설정합니다.

```
$ sudo vi /etc/netplan/00-installer-config.yaml
```

[Network](#Network)에서 조사한 Master Node의 IP Address와 각종 Network 설정을 다음과 같이 저장합니다.
```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [172.30.1.231/24]
      gateway4: 172.30.1.254
      nameservers:
        addresses: [168.126.63.1, 168.126.63.2]
  version: 2
```

다음과 같이 master-node Guest를 Reboot합니다.
```
$ sudo reboot
```

다음과 같이 master-node Guest에서 실행해서 Kubernetes Master Node를 실행합니다.

```
$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16
kubeadm join 172.30.1.231:6443 --token lfbi3t.hm53io2x0p9g1tk3 \
    --discovery-token-ca-cert-hash sha256:92996fe943733c19f86d7848ace86f81e871e68a2baa6aa7aba795e133c95ddc 
```

실행결과에 보이는 `kubeadm` Command를 기록해 둡니다. 나중에 Worker Node에서 Master Node에 연결할 때 사용합니다. 참고로 `--pod-network-cidr=10.244.0.0/16`를 설정하지 않으면 나중에 Flannel을 설치한 후에 coredns가 `ContainerCreating`이라고 출력되면서 정상적으로 실행되지 않습니다.

#### Setup Worker Node {#Setup-Worker-Node}

다음과 같이 worker-node-1 Guest에서 실행해서 Static IP Address를 설정합니다.

```
$ sudo vi /etc/netplan/00-installer-config.yaml
```

[Network](#Network)에서 조사한 Worker Node의 IP Address와 각종 Network 설정을 다음과 같이 저장합니다.
```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [172.30.1.232/24]
      gateway4: 172.30.1.254
      nameservers:
        addresses: [168.126.63.1, 168.126.63.2]
  version: 2
```

다음과 같이 Server Name을 master-node에서 worker-node-1으로 변경합니다.
```
$ sudo hostnamectl set-hostname worker-node-1
$ sudo vi /etc/hosts
(Change master-node to worker-node-1)
```

다음과 같이 worker-node-1 Guest를 Reboot합니다.
```
$ sudo reboot
```

[Setup Master Node](#Setup-Master-Node)에서 기록해 둔 `kubeadm` Command를 worker-node-1 Guest에서 다음과 같이 실행합니다.
```
$ sudo kubeadm join 172.30.1.231:6443 --token lfbi3t.hm53io2x0p9g1tk3 --discovery-token-ca-cert-hash sha256:92996fe943733c19f86d7848ace86f81e871e68a2baa6aa7aba795e133c95ddc
```

[Setup Worker Node](#Setup-Worker-Node)의 작업을 worker-node-2, worker-node-3에 대해서도 반복해서 Worker Node들을 Master Node에 연결합니다.

#### Setup Host {#Setup-Host}

Host에서 Kubernetes Cluster를 Control할 수 있도록 Host에 `kubectl`을 설치합니다.

다음와 같이 Host에서 실행해서 `kubectl`을 설치합니다. 의도치않게 Upgrade되지 않도록 설치후 Version을 apt-mark hold를 사용해서 고정합니다.

```
$ sudo apt-get install -y kubectl
$ sudo apt-mark hold kubectl
```

다음과 같이 master-node Guest에서 실행해서 /etc/kubernetes/admin.conf의 내용을 확인합니다.

```
$ sudo cat /etc/kubernetes/admin.conf
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM1ekNDQWMrZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeE1ESXdOREU0TXpBMU9Gb1hEVE14TURJd01qRTRNekExT0Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTVlaCkFlTUdtSHVuYzQxNWpkM2tTMzBrRkZMdWN2TGpqUzhvcHpGaDJZelZwNjBhR0N6dFpJU1lKUGhxMlVWVHZLb2gKcGpUcHAyaUtyODE5ZGpjNWhkS05sV0Q0NlpTNXFqWmhFR0tIZVozbk9kZ2padzVvTWV3MTZGLzlsNlc0Unc4dwpFRjc2dFNZZ096TFdkRWFUT292NTRrUUhCNTl6ajZFYjhVL2QxakxuYzVqVFg2Z1JFby9Za2o4Qzk5OG0weHJ0CmZCdk8yUnFjMGcxSjUzblJUUDhqOFdSMk1tWGZGV3ZZUTI1WHhGWmxWc01YN1VlQ3pMdkpJVldhVy82NFk3dHoKTGxRSVZWNG4yT3VaUlZFSTc2Y0s2bmdJeE4xUkNsb1A4NGNhbU5TRFBUcGlhOStLVTY5MC9JbTJYTzdhZW9XNQpVek14VGVRTm9RcW5vRkZvRFlVQ0F3RUFBYU5DTUVBd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZJU3hCalMvTk5LQTlQYnlSSlUxQUFEUys3Q3pNQTBHQ1NxR1NJYjMKRFFFQkN3VUFBNElCQVFBYlNJeTl3blFZQU9xZkNZQmhnTW5YTVQzTUowK29qak1LMTJhakFHOUgvaGRGWFdSZApQckM3YkdrUlBNOVpRQ0Zod2grVldBYkQzd0QwdDA0K3dpYTAwUUl4Z3R3ZFpWc250Lzh3Szd2a3FScExTZzF4CmFEa2ZSeUEyelR5RWpBaEJydktpWFEyTjBadmZCeEZwYmdRWm5zSElML2JuQUxFUWVNQy9EcGtOQk1BS1Mrem8KT0cvUkoxYlVidnFmZGVBWlN1eE9jaUJuZWZTYzVOcXIwcXVmdWh6TGwvZWJMaEMyM2k1aVEvQ1ZKVk9QR0h1TQpNb08rN3ZnbjVuUXFBYlczNjMwcGpOQnZHMCtWSUdPVUdDdTBSUEZCa2VmYlBta3Q0WlNOa200RHc4MWhBL3RBCjl1dnVzaThKN0ppdDVNWExBSk5sUktFRlBMY2hCM0FidGRsZAotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://172.30.1.231:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURFekNDQWZ1Z0F3SUJBZ0lJRmUwWFVVcUYxeG93RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TVRBeU1EUXhPRE13TlRoYUZ3MHlNakF5TURReE9ETXhNREZhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQXBYb2xuZ1NrWWQ3N09GODIKck0xYzJFaTc2MEI0RHlzMXBxS1E4RFhUMjMxRkQxTmhqYnlqU1E3U3ExQStma2tTd053Qmt0NVNSSTB6WmlsawpUc2tyeDlDZUpxMzYyVnduQ28za0h0WHhJdkI2NGIwVVZlejhzemJvYXRHbXY1SjFSb1NNQVY3MnJxY253d3Q2CnpPMUhzb3ZMNDd4ekxpQkZMQjJiQzBkakk3L3c3QTByK00zUnB5QkZLdDRRNmFRQ2ZXL1ZZbXZOd0xCT21uTGoKbDFrbFE1UVFaZkVVaEhjaEgyem5yd0QzRTZmaHp1dk14QndyUVdYVm51bnpLbFp4THpTYXRJOTJjZVFSSmdpTAp4Uk02a2pSVG5xM01DbE9hVktlMENtVkkwMUNyMVN5TU5oOWtIdWx2VHZLTitIMEZPNlNLSXRtaXp6cExTK3dJCktBazZZUUlEQVFBQm8wZ3dSakFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0h3WURWUjBqQkJnd0ZvQVVoTEVHTkw4MDBvRDA5dkpFbFRVQUFOTDdzTE13RFFZSktvWklodmNOQVFFTApCUUFEZ2dFQkFBNUFGTktKNjZmbkFRYTlnbStTYVNLbmZuZWlKckpuTWNBRXJhZFkwZllPQ1haYzNWUC8yblErCjNTejVMN1hrdFRoSkFSYU9lRFZxbCtmazAzZW9iUlZaNEJqdzM2YWw5aG9QQ3V4YXhNWnJ3cDRxUVMvamN5VzUKbE1YNFk5Mk04aHFxQTFIZHRYY1BoTTlEZ2dabzQwWlZzTE9rSFNiOENvdWRmMTMvL1VxbnlZcEtScHkySXZLWApHZDRDQ3MzMEt0TXV2blEwOVdENk1CNTB3RWdFQk1YVjI5RnRuNUhlQndIYlVyTU42R3g2QUQrNG5POWo5NytNCm02RjVSOXUyRGdzVCtYWitRaS92cER2aTgrTzZnbmYvQXpYRVVGZ2VhWWVLMHlDL0RVVEJHbXhpeGdjZjZFOVAKSlIyNlRrcUl1Ti95YVFQQmo1VGxDR1AwaXRldWk2MD0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBcFhvbG5nU2tZZDc3T0Y4MnJNMWMyRWk3NjBCNER5czFwcUtROERYVDIzMUZEMU5oCmpieWpTUTdTcTFBK2Zra1N3TndCa3Q1U1JJMHpaaWxrVHNrcng5Q2VKcTM2MlZ3bkNvM2tIdFh4SXZCNjRiMFUKVmV6OHN6Ym9hdEdtdjVKMVJvU01BVjcycnFjbnd3dDZ6TzFIc292TDQ3eHpMaUJGTEIyYkMwZGpJNy93N0EwcgorTTNScHlCRkt0NFE2YVFDZlcvVlltdk53TEJPbW5Mamwxa2xRNVFRWmZFVWhIY2hIMnpucndEM0U2Zmh6dXZNCnhCd3JRV1hWbnVuektsWnhMelNhdEk5MmNlUVJKZ2lMeFJNNmtqUlRucTNNQ2xPYVZLZTBDbVZJMDFDcjFTeU0KTmg5a0h1bHZUdktOK0gwRk82U0tJdG1penpwTFMrd0lLQWs2WVFJREFRQUJBb0lCQUFwR3lhdEVrb2paZGpTTQpCVE02RmJnQTNGckJ5REw0OWY0QlBvc01iTG5HejlFaDFuOGM1ZThWa3BPOUNnU0J1VDVzNjFRWnBuWkhacGZECm5rMGVSUy9GanV6TUJUWVdlUDQ0elovMG5XTVVHQzJJdG9pWGpTSDhHUGI1U2llL2lyVDBhbFZ6ZGxKbVl4dkQKekw2SlJkaWF3ZkRFdFVwNkNwR3d6UDRvVXNuWGVpWHlGblk1alI5M3poNlQ3WnJpNDA5VytoWm5NdzhNZlF4cgp4d2drSmQyTEpzMHNGSGdOL2kxbDRlZmNPd0pWOVVQMkNieSsvUnh3K3pEb3BWS0hKWVU1YkIyU1VxZTZ6Z1l6CkpFVFZ3emNMY3dBSTBLWFAwZmdxVS9QZmVhYXRmRzh4bVl1b2p2ZEJYbWVVMjFTVHViMVNCQ3NhdmhLWUcycEYKNXJHVmJDRUNnWUVBMDNyZml4Y0FrRlUzTlQySWtMQy9GOXlxeVYrUzFvMlR1TWRNa2Fob0hGZkZVT0VvczRuVQovT3ZtYzhRSlV4dGlwc2lVcHI3SjlYa2R0U1JxSmZkZ0YrSGtuQ0Y2QzE5bDl4QmdvckRYTUpZYngvVDVUYTQzClA3eTl1aEFoVjFobG1pWnBBdDVLQVVNbjkva1pWcjNYeXBLM1VYWDcvYnRZcTlDemdKSy9KVTBDZ1lFQXlGQVUKRU5LMGc0MDZtd2xDSGN2cjh1cVliS25UdDBkRWxVT3YrbUg1RmVYVXc4YUZHV1FtTnh2L1EyQXorQmZwSzg3bwpOcE90N1J0Tmp6QXBuWEtXUEZoU3piUERnbGQyMGpEQlN0TnlRVWtLOU56cXEzdG51SkRadmJVY3VWMUl1QkpFCnIyR0RjN29sZjFPaGJmeXZwb2Q2eHVJRmN1ei9qL3YwcWRVd0QyVUNnWUVBajBvZzd3Z3QzSjJ3bzRWRzQrcXQKLzhnSGZCd2l6UGJ1a1hPUVlOei9kYnpPdUFkbllZYlJabkdjR3ZKSDh5U0tDa0c3M3VORXllcy9ncjNpb2tqagp0aXJia0NKcXBBd0dkWW1HUUpXYnFKTDh6ZFlobVUyaXA3QUZ5VzBtZWgwdDhtMTJGM2h3SWp6VGR3UXo4Lzc3Cm1Ja2lacktQaEJNTmVKVVhHdFhUWjcwQ2dZQVN5Y2dJQit0Y2gydWV6UkNCZ1BZQms5VjJJN3V5N2lGVnFzS2YKeG42NWVoUXB4TDRKTXFhTzlyWkxtSU5uV3I3SkdDQVp0bUpTNGdPMVVYd2x3M0NwK2xMUjduR0JFVGtZMysvUgpWK0hZazhST1VVWkZqVTZlTmgvbU5rMmFhVkIveTE3YjRGYVhEVGVsS0svMGhBWHBwYjF6V0JIUXhMLzN2bGNsCmN0U09MUUtCZ1FETVh0a1ExOE45Wk81M2VLaWR2VTRVc1pJbHlGN3VPVDNKM3ZXNXhrY0pyMWx2R1FybmlDdDcKQXo5TXJpQUI0TFh4VmJEb01POVpsMWJYaVFISlR0aUhlenBUQjFRYm90d1haaFF6UXNON2ppNnhhQ2NORGYrNgpUaHIzeEtMOWJjOVQ1aXhyQjZuL2NFU3VKMWw0bzNtMGx5WDZBclo3empVdVNoMTJNZHU5aGc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
```

다음과 같이 Host에서 실행해서, 방금전에 확인한 master-node Guest의 /etc/kubernetes/admin.conf의 내용을, ${HOME}/.kube/config에 설정합니다.

```
$ mkdir ${HOME}/.kube
$ vi ${HOME}/.kube/config
(Content of /etc/kubernetes/admin.conf of master-node)
$ chmod 400 ${HOME}/.kube/config
```

#### Flannel {#Flannel}

Kubernetes Cluster의 Network이 작동하기 위해서는 CNI(Container Network Interface) Plugin을 설치해야 합니다. CNI Plugin은 여러 종류가 있는데 Flannel이 속도가 빠르고 간단한 관계로 여기서는 Flannel을 Kubernetes Cluster에 설치하겠습니다.

Host에서 다음과 같이 실행해 보면 아직 CNI Plugin을 설치하지 않았기 때문에 Node들이 모두 `NotReady` 상태입니다.

```
$ kubectl get nodes
NAME            STATUS     ROLES                  AGE   VERSION
master-node     NotReady   control-plane,master   20h   v1.20.2
worker-node-1   NotReady   <none>                 86m   v1.20.2
worker-node-2   NotReady   <none>                 85m   v1.20.2
worker-node-3   NotReady   <none>                 85m   v1.20.2
```

Host에서 다음과 같이 실행해서 Flannel을 설치합니다.

```
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

Host에서 다음과 같이 실행해서 Node들의 상태가 `Ready`상태로 변한 것을 확인합니다.

```
$ kubectl get nodes
NAME            STATUS     ROLES                  AGE   VERSION
master-node     Ready      control-plane,master   20h   v1.20.2
worker-node-1   Ready      <none>                 88m   v1.20.2
worker-node-2   Ready      <none>                 88m   v1.20.2
worker-node-3   Ready      <none>                 87m   v1.20.2
```

#### MetalLB {#MetalLB}

Kubernetes Cluster에서 LoadBalancer가 External IP Address를 얻어오게 하기 위해서는 MetalLB를 설치해야 합니다. 참고로 MetalLB를 설치하지 않으면 LoadBalancer가 External IP Address를 얻어오지 못하게 되면서 Service의 External IP가 `<pending>` 상태가 됩니다.

Host에서 다음과 같이 실행해서 MetalLB를 설치합니다.

```
$ kubectl get configmap kube-proxy -n kube-system -o yaml | sed -e "s/strictARP: false/strictARP: true/" | kubectl apply -f - -n kube-system
$ kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/namespace.yaml
$ kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/metallb.yaml
$ kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
```

Host에서 다음과 같이 실행해서 metallb-config.yaml을 생성합니다.

```
$ vi metallb-config.yaml
```

다음과 같이 [Network](#Network)에서 조사한 External IP Address의 범위를 설정합니다.

```
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 172.30.1.235-172.30.1.240
```

Host에서 다음과 같이 실행해서 metallb-config.yaml을 적용합니다.

```
$ kubectl apply -f metallb-config.yaml
```

#### Metrics Server {#Metrics-Server}

HorizontalPodAutoscaler를 사용하기 위해서는 Metrics Server를 설치해야 합니다. 참고로 Metrics Server를 설치하지 않으면 HorizontalPodAutoscaler의 TARGETS가 `<unknown>` 상태가 되고, `kubectl top node`를 실행했을 때 `error: Metrics API not available` Error가 발생합니다.

Host에서 다음과 같이 실행해서 Metrics Server를 설치합니다.

```
$ curl -L https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.4.1/components.yaml | sed 's/      - args:/      - args:\n        - --kubelet-insecure-tls/g' | kubectl apply -f -
```

참고로 `- --kubelet-insecure-tls`를 추가하지 않으면 Metrics Server 실행도중에 `unable to fully scrape metrics` Error가 발생합니다. Kubernetes Cluster를 안전하게 하기 위해서는 TLS설정을 제대로 하는 것이 좋습니다만, 여기서는 Kubernetes를 조금 맛을 보는 것이 목적이므로 TLS설정을 하지 않겠습니다.

## Kubernetes Hands-on {#Kubernetes-Hands-on}

[https://github.com/luksa/kubernetes-in-action](https://github.com/luksa/kubernetes-in-action)에 공개되어 있는 여러 Docker Container Image들을 Kubernetes Cluster에서 실행해 보면서 여러가지 특징을 살펴보도록 하겠습니다. 여기에서 언급된 명령어는 모두 Host에서 실행합니다.

#### Pod {#Pod}

다음과 같이 [luksa/kubia](https://github.com/luksa/kubernetes-in-action/tree/master/Chapter02/kubia) Docker Container Image를 실행해서 luksa/kubia Server가 잘 작동하는지 확인합니다. luksa/kubia는 자신의 Hostname을 응답하는 HTTP Server입니다.

```
$ docker run -p 8080:8080 --rm --name kubia-container -d luksa/kubia
ab8a6547a844e376004f13da77e3c54b73553b112357f3519befae6ae6a0a3d2
$ curl http://localhost:8080
You've hit ab8a6547a844
$ docker exec -it kubia-container /bin/bash
root@ab8a6547a844:/# hostname
ab8a6547a844
root@ab8a6547a844:/# exit
exit
$ docker stop kubia-container
kubia-container
$
```

docker가 설치되어 있지 않아서 실행이 불가능한 경우에는 다음과 같이 docker를 설치합니다.

```
$ sudo apt-get install -y docker.io
```

다음과 같이 echo-pod.yaml을 생성합니다.

echo-pod.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: echo-pod
spec:
  containers:
  - name: echo-container
    image: luksa/kubia
```

다음과 같이 echo-pod.yaml을 적용합니다.

```
$ kubectl apply -f echo-pod.yaml
pod/echo-pod created
$ kubectl get node -o wide
NAME            STATUS   ROLES                  AGE     VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
master-node     Ready    control-plane,master   22h     v1.20.2   172.30.1.231   <none>        Ubuntu 18.04.5 LTS   4.15.0-135-generic   docker://19.3.6
worker-node-1   Ready    <none>                 3h35m   v1.20.2   172.30.1.232   <none>        Ubuntu 18.04.5 LTS   4.15.0-135-generic   docker://19.3.6
worker-node-2   Ready    <none>                 3h35m   v1.20.2   172.30.1.233   <none>        Ubuntu 18.04.5 LTS   4.15.0-135-generic   docker://19.3.6
worker-node-3   Ready    <none>                 3h34m   v1.20.2   172.30.1.234   <none>        Ubuntu 18.04.5 LTS   4.15.0-135-generic   docker://19.3.6
$ kubectl get pods -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP           NODE            NOMINATED NODE   READINESS GATES
echo-pod   1/1     Running   0          36m   10.244.1.2   worker-node-1   <none>           <none>
$ curl http://10.244.1.2:8080
curl: (7) Failed to connect to 10.244.1.2 port 8080: Connection timed out
$ curl http://172.30.1.232:8080
curl: (7) Failed to connect to 172.30.1.232 port 8080: Connection refused
$
```

echo-pod Pod는 10.244.1.2 IP Address를 가지고 현재 worker-node-1 Node에서 실행되고 있습니다. echo-pod Pod의 IP Address는 10.244.1.2지만 10.244.1.2는 Kubernetes Cluster 안에서만 사용이 가능한 IP Address인 관계로 Host에서는 접속이 불가능한 것을 확인할 수 있습니다. worker-node-1 Node의 IP Address인 172.30.1.232는 Host에서 접속은 가능하지만 Port가 열려 있지 않아서 echo-pod Pod에 접속이 불가능한 것을 확인할 수 있습니다.

다음과 같이 echo-pod Pod 내부에서 curl을 사용해서 HTTP Server에 접속할 수 있습니다.

```
$ kubectl exec echo-pod -- curl http://10.244.1.2:8080
You've hit echo-pod
$
```

Host에서 echo-pod에 직접 접속해 보고 싶으면 다음과 같이 Host의 8080 Port를 echo-pod Pod의 8080 Port로 Port Forward 설정을 해서 접속할 수 있습니다.

```
$ kubectl port-forward echo-pod 8080:8080
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

Shell을 하나 더 실행해서 다음과 같이 echo-pod Pod에 접속합니다. 

```
$ curl http://localhost:8080
You've hit echo-pod
$
```

다음과 같이 echo-pod Pod를 삭제합니다.

```
$ kubectl delete pod echo-pod
pod "echo-pod" deleted
$ 
```

#### ReplicaSet {#ReplicaSet}

여러 개의 Pod를 실행하고 싶을 때 ReplicaSet를 사용합니다.

다음과 같이 echo-replica-set.yaml을 생성합니다.

echo-replica-set.yaml
```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: echo-replica-set
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
```

실행하고 싶은 Pod의 수를 spec.replicas에 설정합니다. 여기서는 5로 설정합니다. ReplicaSet이 실행하는 Pod의 갯수를 관리하기 위해서 Pod들에 Label을 부여해서 실행합니다. spec.template.metadata.labels에 실행할 Pod에 부여할 Label을 설정합니다. ReplicaSet은 Selector로 특정 조건의 Label을 가진 Pod의 수를 관리합니다. spec.selector.matchLabels에 ReplicaSet이 주목할 조건의 Label을 설정합니다. 여기서는 app=echo-label이라는 이름의 Label을 부여해서 Pod를 실행합니다. ReplicaSet은 Selector로 app=echo-label이라는 Label을 설정해서 app=echo-label의 Label을 가지는 Pod가 5개 실행되도록 합니다.

다음과 같이 echo-replica-set.yaml을 적용합니다.

```
$ kubectl apply -f echo-replica-set.yaml
replicaset.apps/echo-replica-set created
$ kubectl get pods -o wide --show-labels
NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-replica-set-2kl5g   1/1     Running   0          51s   10.244.1.10   worker-node-1   <none>           <none>            app=echo-label
echo-replica-set-7sgtv   1/1     Running   0          51s   10.244.2.13   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-p8vkt   1/1     Running   0          51s   10.244.3.8    worker-node-3   <none>           <none>            app=echo-label
echo-replica-set-x8pfs   1/1     Running   0          51s   10.244.2.14   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-xb8fs   1/1     Running   0          51s   10.244.1.11   worker-node-1   <none>           <none>            app=echo-label
$ kubectl get replicasets -o wide
NAME               DESIRED   CURRENT   READY   AGE   CONTAINERS       IMAGES        SELECTOR
echo-replica-set   5         5         5       52s   echo-container   luksa/kubia   app=echo-label
$
```

다음과 같이 echo-replica-set-2kl5g Pod를 하나 삭제해 봅니다.

```
$ kubectl delete pod echo-replica-set-2kl5g
pod "echo-replica-set-2kl5g" deleted
$ kubectl get pods -o wide --show-labels
NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-replica-set-7sgtv   1/1     Running   0          23m   10.244.2.13   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-p8vkt   1/1     Running   0          23m   10.244.3.8    worker-node-3   <none>           <none>            app=echo-label
echo-replica-set-x8pfs   1/1     Running   0          23m   10.244.2.14   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-xb8fs   1/1     Running   0          23m   10.244.1.11   worker-node-1   <none>           <none>            app=echo-label
echo-replica-set-xmt6p   1/1     Running   0          47s   10.244.3.9    worker-node-3   <none>           <none>            app=echo-label
$
```

echo-replica-set-2kl5g Pod를 삭제했더니 echo-replica-set ReplicaSet가 echo-replica-set-xmt6p Pod를 생성하는 것을 확인할 수 있습니다.

다음과 같이 Pod 내에서 Pod들의 HTTP Server에 접속해 봅니다. Pod의 IP Address들은 Kubernetes Cluster 안에서만 접속이 가능하고 Host에서는 접속이 불가능합니다.

```
$ kubectl exec echo-replica-set-x8pfs -it -- /bin/bash
root@echo-replica-set-x8pfs:/# curl http://10.244.2.13:8080
You've hit echo-replica-set-7sgtv
root@echo-replica-set-x8pfs:/# curl http://10.244.3.8:8080
You've hit echo-replica-set-p8vkt
root@echo-replica-set-x8pfs:/# curl http://10.244.2.14:8080
You've hit echo-replica-set-x8pfs
root@echo-replica-set-x8pfs:/# curl http://10.244.1.11:8080
You've hit echo-replica-set-xb8fs
root@echo-replica-set-x8pfs:/# curl http://10.244.3.9:8080
You've hit echo-replica-set-xmt6p
root@echo-replica-set-x8pfs:/# exit
exit
$
```

다음과 같이 echo-replica-set ReplicaSet을 삭제합니다.

```
$ kubectl delete replicaset echo-replica-set
replicaset.apps "echo-replica-set" deleted
$
```

#### DaemonSet {#DaemonSet}

ReplicaSet은 Pod를 몇 개 실행할 것인지를 지정해 줄 수 있습니다. 만약에 Node마다 한 개씩 Pod를 실행하고 싶으면 DaemonSet을 사용합니다.

다음과 같이 echo-daemon-set.yaml을 생성합니다.

echo-daemon-set.yaml
```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: echo-daemon-set
spec:
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
```

ReplicaSet에서는 Pod를 몇 개 실행할 것인지 지정하는데, DaemonSet에서는 각 Node에서 실행할 것이기 때문에 지정하지 않습니다.

다음과 같이 echo-daemon-set.yaml을 적용합니다.

```
$ kubectl apply -f echo-daemon-set.yaml 
daemonset.apps/echo-daemon-set created
$ kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES
echo-daemon-set-9k87b   1/1     Running   0          13s   10.244.1.8    worker-node-1   <none>           <none>
echo-daemon-set-js2tz   1/1     Running   0          13s   10.244.2.17   worker-node-2   <none>           <none>
echo-daemon-set-l4gjw   1/1     Running   0          13s   10.244.3.16   worker-node-3   <none>           <none>
$ 
```

각 Node에서 Pod가 하나씩 실행된 것을 확인할 수 있습니다.

다음과 같이 echo-daemon-set DaemonSet을 삭제합니다.

```
$ kubectl delete daemonset echo-daemon-set
daemonset.apps "echo-daemon-set" deleted
$
```

#### Service {#Service}

ReplicaSet이 Pod를 여러개 관리해 주지만 Pod들에 접속하려면 Pod의 IP Address 여러 개를 사용해서 접속해야 합니다. Service를 사용하면, Service에서 제공하는 IP Address에 접속했을 때 여러개의 Pod의 IP Address 들 중에 하나가 선택되어 접속됩니다.

다음과 같이 echo-server.yaml을 생성합니다.

echo-server.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: echo-service
spec:
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: echo-label
---
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: echo-replica-set
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
```

`---` 를 이용하면 여러 yaml파일을 하나로 합칠 수 있습니다. spec.selector에 Service가 접속할 대상의 Pod가 가지는 Label을 지정합니다. spec.ports.port에 Service가 접속을 받을 Port를 지정하고 spec.ports.targetPort에 접속할 Pod의 Port를 지정합니다. 여기서는 Service에서 80 Port로 접속을 받았을 때 app=echo-label Label을 가지는 Pod의 8080 Port로 접속합니다.

다음과 같이 echo-service.yaml을 적용합니다.

```
$ kubectl apply -f echo-service.yaml 
service/echo-service created
replicaset.apps/echo-replica-set created
$ kubectl get pods -o wide --show-labels
NAME                     READY   STATUS    RESTARTS   AGE     IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-replica-set-4pdj7   1/1     Running   0          3m50s   10.244.2.20   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-p76tl   1/1     Running   0          3m50s   10.244.2.19   worker-node-2   <none>           <none>            app=echo-label
echo-replica-set-qzkwv   1/1     Running   0          3m50s   10.244.3.10   worker-node-3   <none>           <none>            app=echo-label
echo-replica-set-tp7h8   1/1     Running   0          3m50s   10.244.1.13   worker-node-1   <none>           <none>            app=echo-label
echo-replica-set-zj89b   1/1     Running   0          3m50s   10.244.1.12   worker-node-1   <none>           <none>            app=echo-label
$ kubectl get replicasets -o wide
NAME               DESIRED   CURRENT   READY   AGE   CONTAINERS       IMAGES        SELECTOR
echo-replica-set   5         5         5       4m    echo-container   luksa/kubia   app=echo-label
$ kubectl get services -o wide
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE    SELECTOR
echo-service   ClusterIP   10.105.246.41   <none>        80/TCP    4m4s   app=echo-label
kubernetes     ClusterIP   10.96.0.1       <none>        443/TCP   35h    <none>
$ kubectl get endpoints
NAME           ENDPOINTS                                                        AGE
echo-service   10.244.1.12:8080,10.244.1.13:8080,10.244.2.19:8080 + 2 more...   14m
kubernetes     172.30.1.231:6443                                                35h
$
```

echo-service Service에 접속하면 app=echo-label Label을 가지는 Pod들 중 하나에 접속됩니다. echo-service Service의 Cluster IP Address는 10.105.246.41입니다. echo-service Service의 Port는 80이고 여기에 접속하면 app=echo-label Label을 가지는 Pod들 8080 Port로 접속합니다.

다음과 같이 echo-service Service에 접속합니다.

```
$ curl http://10.105.246.41
curl: (7) Failed to connect to 10.105.246.41 port 80: Connection timed out
$ kubectl exec echo-replica-set-4pdj7 -it -- /bin/bash
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-p76tl
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-4pdj7
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-4pdj7
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-tp7h8
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-zj89b
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-p76tl
root@echo-replica-set-4pdj7:/# curl http://10.105.246.41
You've hit echo-replica-set-qzkwv
root@echo-replica-set-4pdj7:/# exit
exit
$
```

echo-service Service에 할당된 10.105.246.41 Cluster IP Address는 Kubernetes Cluster 안에서만 사용이 가능한 IP Address인 관계로 Host에서는 접속이 불가능한 것을 확인할 수 있습니다. Pod 내에서는 10.105.246.41에 접속이 가능합니다. 10.105.246.41에 접속을 할 때마다 다른 Pod에 접속이 되는 것을 확인할 수 있습니다.

다음과 같이 echo-service Service와 echo-replica-set ReplicaSet을 삭제합니다.

```
$ kubectl delete service echo-service
service "echo-service" deleted
$ kubectl delete replicaset echo-replica-set
replicaset.apps "echo-replica-set" deleted
$
```

#### LoadBalancer {#LoadBalancer}

Service를 사용하면 ReplicaSet이 관리하는 Pod들에 편리하게 접속할 수 있지만 Kubernetes Cluster 내부에서만 접속할 수 있습니다. Kubernetes Cluster 외부에서도 접속할 수 있게 하기 위해 LoadBalancer Type의 Service를 사용합니다.

다음과 같이 echo-load-balancer.yaml을 생성합니다.

echo-load-balancer.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: echo-load-balancer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: echo-label
---
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: echo-replica-set
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
```

다음과 같이 echo-load-balancer.yaml을 적용합니다.

```
$ kubectl apply -f echo-load-balancer.yaml
service/echo-load-balancer created
replicaset.apps/echo-replica-set created
$ kubectl get pods -o wide
NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES
echo-replica-set-6pr9s   1/1     Running   0          78s   10.244.2.21   worker-node-2   <none>           <none>
echo-replica-set-8vn6k   1/1     Running   0          78s   10.244.3.11   worker-node-3   <none>           <none>
echo-replica-set-w4x6m   1/1     Running   0          78s   10.244.3.12   worker-node-3   <none>           <none>
echo-replica-set-wdn4p   1/1     Running   0          78s   10.244.1.14   worker-node-1   <none>           <none>
echo-replica-set-whcpc   1/1     Running   0          78s   10.244.1.15   worker-node-1   <none>           <none>
$ kubectl get services -o wide
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)        AGE     SELECTOR
echo-load-balancer   LoadBalancer   10.107.75.100   172.30.1.235   80:32183/TCP   4m58s   app=echo-label
kubernetes           ClusterIP      10.96.0.1       <none>         443/TCP        37h     <none>
$ 
```

echo-load-balancer Service의 External IP Address가, [Network](#Network)에서 선정한 External IP Address들중에서 선택된 172.30.1.235로, 설정되어 있는 것을 확인할 수 있습니다. 

다음과 같이 Host에서 직접 Pod들에게 접속이 가능한 것을 확인합니다.

```
$ curl http://172.30.1.235
You've hit echo-replica-set-whcpc
$ curl http://172.30.1.235
You've hit echo-replica-set-8vn6k
$ curl http://172.30.1.235
You've hit echo-replica-set-w4x6m
$ curl http://172.30.1.235
You've hit echo-replica-set-6pr9s
$ curl http://172.30.1.235
You've hit echo-replica-set-w4x6m
$ curl http://172.30.1.235
You've hit echo-replica-set-6pr9s
$ curl http://172.30.1.235
You've hit echo-replica-set-wdn4p
$
```

다음과 같이 echo-load-balancer Service와 echo-replica-set ReplicaSet을 삭제합니다.

```
$ kubectl delete service echo-load-balancer
service "echo-load-balancer" deleted
$ kubectl delete replicaset echo-replica-set
replicaset.apps "echo-replica-set" deleted
$
```

#### Deployment {#Deployment}

ReplicaSet을 사용해서 Pod들을 실행하고 있을 때 실행중인 Pod의 Docker Container Image의 Version을 변경하고 변경 내용을 Deploy하고 싶은 경우가 있습니다. 간단한 방법으로는 모든 Pod들을 삭제하고 Pod의 Docker Container Image의 Version을 변경하고 Pod들을 다시 시작하면 됩니다. 하지만 이렇게 하면 Version을 변경하고 있는 동안에 현재 제공중인 Service가 중단되는 문제가 있습니다. Service를 중단시키지 않고 Pod의 Docker Container Image의 Version을 변경하기 위해 Deployment를 사용합니다.

다음과 같이 echo-deployment.yaml을 생성합니다.

echo-deployment.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: echo-load-balancer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: echo-label
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-deployment
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
```

다음과 같이 echo-deployment.yaml을 적용합니다.

```
$ kubectl apply -f echo-deployment.yaml
service/echo-load-balancer created
deployment.apps/echo-deployment created
$ kubectl get pods -o wide --show-labels
NAME                              READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-7bb495f4b-g8bvf   1/1     Running   0          8s    10.244.2.39   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v55zq   1/1     Running   0          8s    10.244.1.34   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v5wt8   1/1     Running   0          8s    10.244.3.27   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xm777   1/1     Running   0          8s    10.244.2.38   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xv8nh   1/1     Running   0          8s    10.244.1.35   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
$ kubectl get services -o wide
NAME                 TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)        AGE   SELECTOR
echo-load-balancer   LoadBalancer   10.103.61.94   172.30.1.235   80:30448/TCP   19s   app=echo-label
kubernetes           ClusterIP      10.96.0.1      <none>         443/TCP        39h   <none>
$ kubectl get deployment -o wide
NAME              READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES        SELECTOR
echo-deployment   5/5     5            5           20s   echo-container   luksa/kubia   app=echo-label
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-xm777
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-g8bvf
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-xm777
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-v5wt8
$
```

살펴보면 ReplicaSet과 다르게 Deployment로 만들어진 Pod에는 pod-template-hash=7bb495f4b Label이 추가되어 있습니다. Pod의 Docker Container Image의 Version을 변경할 때 이 Label을 사용해서 Version을 구분합니다.

다음과 같이 echo-deployment-v2.yaml을 생성합니다. Docker Container Image를 luksa/kubia에서 luksa/kubia:v2로 변경합니다.

echo-deployment-v2.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: echo-load-balancer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: echo-label
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-deployment
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia:v2
```

다음과 같이 echo-deployment-v2.yaml을 적용합니다. luksa/kubia:v2 Docker Container Image를 사용하는 Pod를 Deploy합니다.

```
$ kubectl apply -f echo-deployment-v2.yaml
service/echo-load-balancer unchanged
deployment.apps/echo-deployment configured
$ kubectl get pods -o wide --show-labels
NAME                               READY   STATUS              RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-554b7697fd-bg9z2   0/1     ContainerCreating   0          2s    <none>        worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-nsft7   0/1     ContainerCreating   0          2s    <none>        worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-pg4v5   0/1     ContainerCreating   0          2s    <none>        worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-7bb495f4b-g8bvf    1/1     Running             0          80s   10.244.2.39   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v55zq    1/1     Running             0          80s   10.244.1.34   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v5wt8    1/1     Running             0          80s   10.244.3.27   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xm777    1/1     Running             0          80s   10.244.2.38   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xv8nh    1/1     Terminating         0          80s   10.244.1.35   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-g8bvf
$ curl http://172.30.1.235
This is v2 running in pod echo-deployment-554b7697fd-bg9z2
$ curl http://172.30.1.235
This is v2 running in pod echo-deployment-554b7697fd-pg4v5
$ curl http://172.30.1.235
This is v2 running in pod echo-deployment-554b7697fd-lzq4f
$ kubectl get pods -o wide --show-labels
NAME                               READY   STATUS        RESTARTS   AGE    IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-554b7697fd-bg9z2   1/1     Running       0          22s    10.244.3.28   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-lzq4f   1/1     Running       0          16s    10.244.1.37   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-nsft7   1/1     Running       0          22s    10.244.1.36   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-pg4v5   1/1     Running       0          22s    10.244.3.29   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-zssjp   1/1     Running       0          17s    10.244.2.40   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-7bb495f4b-g8bvf    1/1     Terminating   0          100s   10.244.2.39   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v55zq    1/1     Terminating   0          100s   10.244.1.34   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-v5wt8    1/1     Terminating   0          100s   10.244.3.27   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xm777    1/1     Terminating   0          100s   10.244.2.38   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-xv8nh    1/1     Terminating   0          100s   10.244.1.35   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
$ kubectl get pods -o wide --show-labels
NAME                               READY   STATUS    RESTARTS   AGE    IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-554b7697fd-bg9z2   1/1     Running   0          113s   10.244.3.28   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-lzq4f   1/1     Running   0          107s   10.244.1.37   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-nsft7   1/1     Running   0          113s   10.244.1.36   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-pg4v5   1/1     Running   0          113s   10.244.3.29   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-zssjp   1/1     Running   0          108s   10.244.2.40   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
$ kubectl get deployment -o wide
NAME              READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES           SELECTOR
echo-deployment   5/5     5            5           9m    echo-container   luksa/kubia:v2   app=echo-label
$
```

luksa/kubia Docker Container Image가 실행되는 Pod는 pod-template-hash=7bb495f4b Label을 가지고, luksa/kubia:v2 Docker Container Image가 실행되는 Pod는 pod-template-hash=554b7697fd Label을 가집니다. 새 Version의 Pod의 Deploy가 진행되는 도중에 Service가 중단되지 않는 것을 http://172.30.1.235 에 접속해 보면서 확인할 수 있습니다.

다음과 같이 최근에 수행한 Deploy를 Rollback합니다.

```
$ kubectl rollout undo deployment echo-deployment
deployment.apps/echo-deployment rolled back
$ curl http://172.30.1.235
This is v2 running in pod echo-deployment-554b7697fd-zssjp
$ curl http://172.30.1.235
This is v2 running in pod echo-deployment-554b7697fd-bg9z2
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-wpk55
$ curl http://172.30.1.235
You've hit echo-deployment-7bb495f4b-fttwq
$ kubectl get pods -o wide --show-labels
NAME                               READY   STATUS        RESTARTS   AGE     IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-554b7697fd-pg4v5   0/1     Terminating   0          9m51s   10.244.3.29   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-554b7697fd-zssjp   0/1     Terminating   0          9m46s   10.244.2.40   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=554b7697fd
echo-deployment-7bb495f4b-5bdtr    1/1     Running       0          83s     10.244.2.41   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-fttwq    1/1     Running       0          77s     10.244.2.42   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-kdpz6    1/1     Running       0          83s     10.244.1.38   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-wpk55    1/1     Running       0          83s     10.244.3.30   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-ztcf4    1/1     Running       0          77s     10.244.1.39   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
$ kubectl get pods -o wide --show-labels
NAME                              READY   STATUS    RESTARTS   AGE    IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
echo-deployment-7bb495f4b-5bdtr   1/1     Running   0          116s   10.244.2.41   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-fttwq   1/1     Running   0          110s   10.244.2.42   worker-node-2   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-kdpz6   1/1     Running   0          116s   10.244.1.38   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-wpk55   1/1     Running   0          116s   10.244.3.30   worker-node-3   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
echo-deployment-7bb495f4b-ztcf4   1/1     Running   0          110s   10.244.1.39   worker-node-1   <none>           <none>            app=echo-label,pod-template-hash=7bb495f4b
$ kubectl get deployment -o wide
NAME              READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES        SELECTOR
echo-deployment   5/5     5            5           40m   echo-container   luksa/kubia   app=echo-label
```

Deploy를 Rollback하는 도중에도 Service가 중단되지 않는 것을 http://172.30.1.235 에 접속해 보면서 확인할 수 있습니다.

다음과 같이 echo-load-balancer Service와 echo-deployment Deployment를 삭제합니다.

```
$ kubectl delete service echo-load-balancer
service "echo-load-balancer" deleted
$ kubectl delete deployment echo-deployment
deployment.apps "echo-deployment" deleted
$
```

참고로 Deployment의 spec.strategy를 적절하게 설정하면 다양하게 Deploy 방법을(Blue/Green, Rolling 등) 설정할 수 있습니다.

#### HorizontalPodAutoscaler {#HorizontalPodAutoscaler}

Deployment를 사용할 때 Pod의 수를 고정해야 합니다. 하지만 CPU Load가 높을 때 Pod의 수를 늘리고, CPU Load가 낮을 때 Pod의 수를 줄이면 Kubernetes Cluster의 자원을 더 효율적으로 활용할 수 있습니다. Pod의 수를 필요에 따라 자동으로 동적으로 조절하기 위해 HorizontalPodAutoscaler를 사용합니다.

다음과 같이 echo-horizontal-pod-autoscaler.yaml을 생성합니다.

echo-horizontal-pod-autoscaler.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: echo-load-balancer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: echo-label
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-deployment
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echo-label
  template:
    metadata:
      labels:
        app: echo-label
    spec:
      containers:
      - name: echo-container
        image: luksa/kubia
        resources:
          requests:
            cpu: 100m
---
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: echo-horizontal-pod-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: echo-deployment
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```

echo-container는 적어도 100m의 CPU자원을(0.1개의 CPU자원을) 필요로 합니다. 초기 Pod의 수는 5개이고, 최소 Pod의 수는 1개이고, 최대 Pod의 수는 10개입니다. CPU Load는 50%정도를 유지하는 것을 목표로 합니다.

다음과 같이 echo-horizontal-pod-autoscaler.yaml을 적용합니다.

```
$ kubectl apply -f echo-horizontal-pod-autoscaler.yaml
service/echo-load-balancer created
deployment.apps/echo-deployment created
horizontalpodautoscaler.autoscaling/echo-horizontal-pod-autoscaler created
$ kubectl get services
NAME                 TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)        AGE
echo-load-balancer   LoadBalancer   10.100.57.82   172.30.1.235   80:32637/TCP   8s
kubernetes           ClusterIP      10.96.0.1      <none>         443/TCP        45h
$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
echo-deployment   5/5     5            5           14s
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
echo-deployment-b4c59cbb5-85kdf   1/1     Running   0          21s
echo-deployment-b4c59cbb5-bw5b6   1/1     Running   0          21s
echo-deployment-b4c59cbb5-k88j5   1/1     Running   0          21s
echo-deployment-b4c59cbb5-n7vnv   1/1     Running   0          21s
echo-deployment-b4c59cbb5-xr5gd   1/1     Running   0          21s
$ kubectl get horizontalpodautoscalers
NAME                             REFERENCE                    TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
echo-horizontal-pod-autoscaler   Deployment/echo-deployment   0%/50%    1         10        5          93s
$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
echo-deployment   1/1     1            1           9m22s
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
echo-deployment-b4c59cbb5-xr5gd   1/1     Running   0          10m
$ kubectl get horizontalpodautoscalers
NAME                             REFERENCE                    TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
echo-horizontal-pod-autoscaler   Deployment/echo-deployment   0%/50%    1         10        1          10m
$
```

처음에는 Pod의 수가 5개였지만 가만히 몇 분간 기다리면 CPU Load가 낮아서 Pod의 수가 1개로 줄어드는 것을 확인할 수 있습니다.

다음과 같이 CPU Load를 의도적으로 높여봅니다. 필요하다면 Background로 동시에 여러 개를 실행합니다.

```
$ while true; do curl http://172.30.1.235 > /dev/null 2>&1; done
```

다른 Shell에서 다음과 같이 Pod의 수가 CPU Load로 인해 늘어난 것을 확인할 수 있습니다.

```
$ kubectl get horizontalpodautoscalers
NAME                             REFERENCE                    TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
echo-horizontal-pod-autoscaler   Deployment/echo-deployment   76%/50%   1         10        1          13m
$ kubectl get horizontalpodautoscalers
NAME                             REFERENCE                    TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
echo-horizontal-pod-autoscaler   Deployment/echo-deployment   38%/50%   1         10        2          14m
$ kubectl get deployments
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
echo-deployment   2/2     2            2           14m
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
echo-deployment-b4c59cbb5-xr5gd   1/1     Running   0          14m
echo-deployment-b4c59cbb5-z5cmg   1/1     Running   0          70s
$
```

다음과 같이 echo-load-balancer Service와 echo-deployment Deployment와 echo-horizontal-pod-autoscaler HorizontalPodAutoscaler를 삭제합니다.

```
$ kubectl delete service echo-load-balancer
service "echo-load-balancer" deleted
$ kubectl delete deployment echo-deployment
deployment.apps "echo-deployment" deleted
$ kubectl delete horizontalpodautoscaler echo-horizontal-pod-autoscaler
horizontalpodautoscaler.autoscaling "echo-horizontal-pod-autoscaler" deleted
$
```

#### ConfigMap {#ConfigMap}

각종 설정을 모아서 별도로 관리하고 싶은 경우에는 ConfigMap을 사용합니다.

다음과 같이 echo-config-map.yaml을 생성합니다.

echo-config-map.yaml
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: echo-config-map
data:
  NFS_SERVER: 172.30.1.201
  NFS_PATH: /mnt/nfs
---
apiVersion: v1
kind: Pod
metadata:
  name: echo-pod
spec:
  containers:
  - name: echo-container
    image: luksa/kubia
    envFrom:
    - configMapRef:
        name: echo-config-map
```

echo-pod Pod에 있는 echo-container Container의 환경변수에 echo-config-map ConfigMap을 추가합니다. echo-config-map에서는 NFS_SERVER, NFS_PATH를 정의합니다.

다음과 같이 echo-config-map.yaml을 적용합니다.

```
$ kubectl apply -f echo-config-map.yaml
configmap/echo-config-map created
pod/echo-pod created
$ kubectl exec echo-pod -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=echo-pod
NFS_SERVER=172.30.1.201
NFS_PATH=/mnt/nfs
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
NPM_CONFIG_LOGLEVEL=info
NODE_VERSION=7.9.0
YARN_VERSION=0.22.0
HOME=/root
$
```

echo-pod Pod에서 env명령을 실행해서 확인해 보면 NFS_SERVER와 NFS_PATH 환경변수가 설정되어 있는 것을 확인할 수 있습니다.

다음과 같이 echo-config-map ConfigMap과 echo-pod Pod를 삭제합니다.

```
$ kubectl delete configmap echo-config-map
configmap "echo-config-map" deleted
$ kubectl delete pod echo-pod
pod "echo-pod" deleted
$
```

참고로 ConfigMap에 있는 내용중에 일부만 환경변수로 추가할 수도 있고, Container에 File형태로 추가할 수도 있으며, 그 외 다양한 형태로 사용할 수 있습니다.

#### Secret {#Secret}

ConfigMap처럼 각종 설정을 모아서 별도로 관리하고 싶은데 내용이 다소 비밀스러운 경우에는 Secret을 사용합니다.

다음과 같이 echo-secret-map.yaml을 생성합니다.

echo-secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: echo-secret
data:
  NFS_SERVER: MTcyLjMwLjEuMjAx
  NFS_PATH: L21udC9uZnM=
---
apiVersion: v1
kind: Pod
metadata:
  name: echo-pod
spec:
  containers:
  - name: echo-container
    image: luksa/kubia
    envFrom:
    - secretRef:
        name: echo-secret
```

echo-pod Pod에 있는 echo-container Container의 환경변수에 echo-secret Secret을 추가합니다. echo-secret에서는 NFS_SERVER, NFS_PATH를 정의하는데 이때 Value는 Base64 Encode을 해서 설정합니다. Base64 Decode를 하면 내용을 바로 알 수 있지만 Base64 Encode가 되어 있어서 내용을 바로 알 수는 없기 때문에 비밀이 다소 유지됩니다.

다음과 같이 echo-secret.yaml을 적용합니다.

```
$ kubectl apply -f echo-secret.yaml
secret/echo-secret created
pod/echo-pod created
$ kubectl exec echo-pod -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=echo-pod
NFS_PATH=/mnt/nfs
NFS_SERVER=172.30.1.201
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
NPM_CONFIG_LOGLEVEL=info
NODE_VERSION=7.9.0
YARN_VERSION=0.22.0
HOME=/root
$
```

echo-pod Pod에서 env명령을 실행해서 확인해 보면 NFS_SERVER와 NFS_PATH 환경변수가 설정되어 있는 것을 확인할 수 있습니다.

다음과 같이 echo-secret Secret과 echo-pod Pod를 삭제합니다.

```
$ kubectl delete secret echo-secret
secret "echo-secret" deleted
$ kubectl delete pod echo-pod
pod "echo-pod" deleted
$
```

참고로 ConfigMap과 마찬가지로 Secret도 내용중에 일부만 환경변수로 추가할 수도 있고, Container에 File형태로 추가할 수도 있으며, 그 외 다양한 형태로 사용할 수 있습니다.

#### Job {#Job}

작업을 수행하고 종료하고 싶은 경우에는 Job을 사용합니다.

다음과 같이 [luksa/batch-job](https://github.com/luksa/kubernetes-in-action/tree/master/Chapter04/batch-job) Docker Container Image를 실행해서 luksa/batch-job이 잘 작동하는지 확인합니다. luksa/batch-job은 2분동안 작업을 수행하고 종료합니다.

```
$ docker run --rm luksa/batch-job
Sun Feb  7 05:32:35 UTC 2021 Batch job starting
Sun Feb  7 05:34:35 UTC 2021 Finished succesfully
$
```

다음과 같이 batch-job.yaml을 생성합니다.

batch-job.yaml
```
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: batch-job-container
        image: luksa/batch-job
```

spec.template.spec.restartPolicy에 OnFailure로 설정해서 작업이 중간에 실패했을 경우 재시작하도록 설정합니다. Never로 설정하면 작업이 중간에 실패했을 경우 재시작하지 않습니다. 참고로 작업이 실패한 것이 아니라 Pod가 자체가 실행이 불가능한 상태에 빠진 경우에는(Pod가 실행중인 Node의 갑작스러운 전원 꺼짐 등) restartPolicy를 OnFailure나 Never로 설정했는지에 무관하게 Pod가 새로 생성되어서 작업이 재시작됩니다. 즉, 상황에 따라서 restartPolicy를 Never로 설정해도 작업이 재시작될 수 있습니다.

다음과 같이 batch-job.yaml을 적용합니다.

```
$ kubectl apply -f batch-job.yaml
job.batch/batch-job created
$ kubectl get jobs -o wide
NAME        COMPLETIONS   DURATION   AGE   CONTAINERS            IMAGES            SELECTOR
batch-job   0/1           67s        67s   batch-job-container   luksa/batch-job   controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997
$ kubectl get pods -o wide --show-labels
NAME              READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
batch-job-5kjfl   1/1     Running   0          71s   10.244.3.22   worker-node-3   <none>           <none>            controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997,job-name=batch-job
$ kubectl logs batch-job-5kjfl
Sun Feb  7 06:28:22 UTC 2021 Batch job starting
$ kubectl get jobs -o wide
NAME        COMPLETIONS   DURATION   AGE     CONTAINERS            IMAGES            SELECTOR
batch-job   1/1           2m4s       2m57s   batch-job-container   luksa/batch-job   controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997
$ kubectl get pods -o wide --show-labels
NAME              READY   STATUS      RESTARTS   AGE    IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
batch-job-5kjfl   0/1     Completed   0          3m4s   10.244.3.22   worker-node-3   <none>           <none>            controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997,job-name=batch-job
$ kubectl logs batch-job-5kjfl
Sun Feb  7 06:28:22 UTC 2021 Batch job starting
Sun Feb  7 06:30:22 UTC 2021 Finished succesfully
$ kubectl apply -f batch-job.yaml
job.batch/batch-job unchanged
$ kubectl get jobs -o wide
NAME        COMPLETIONS   DURATION   AGE     CONTAINERS            IMAGES            SELECTOR
batch-job   1/1           2m4s       3m20s   batch-job-container   luksa/batch-job   controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997
$ kubectl get pods -o wide --show-labels
NAME              READY   STATUS      RESTARTS   AGE     IP            NODE            NOMINATED NODE   READINESS GATES   LABELS
batch-job-5kjfl   0/1     Completed   0          3m25s   10.244.3.22   worker-node-3   <none>           <none>            controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997,job-name=batch-job
$
```

Pod에 controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997 Label을 설정하고 Job에서는 controller-uid=5b5dfa4b-4216-4913-9d89-0892f29fb997 Selector를 설정해서 Job에서 Pod를 관리합니다. 작업이 종료된 후에는 Pod의 Status가 `Completed`로 바뀌지만 아무런 조치를 취하지 않으면 Pod가 사라지지는 않습니다. 작업이 끝난 뒤에 Pod가 사라지지 않기 때문에 작업이 끝난 뒤에 `kubectl logs`를 사용해서 Log를 확인할 수 있습니다. 작업이 끝난 뒤에도 Job을 삭제하지 않았다면 다시 동일한 Job을 적용해도 작업이 시작되지 않습니다.

다음과 같이 batch-job Job을 삭제합니다.

```
$ kubectl delete job batch-job
job.batch "batch-job" deleted
$
```

참고로 Job은 spec.completions과 spec.parallelism를 적절하게 설정하면 작업의 실행 횟수나 작업의 동시 실행 갯수 등을 설정할 수 있습니다.

## Conclusion {#Conclusion}

Kubernetes를 직접 설치해 보고 직접 조금 사용해 보면서 Kubernetes가 어떤 것인가에 대해서 살짝 살펴보았습니다. 이 글 하나로 방대한 Kubernetes에 대해 깊은 이해는 할 수 없겠지만 Kubernetes에 대해 조금이라도 쉽게 이해하는데 도움이 되기를 바랍니다.
