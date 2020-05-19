# Minikube

Minikube installation from source code. This role:

- creates and uses dedicated unix user account (as specified in
  `minikube_username` variable)
- installs kubectl and minikube build dependencies
- clones minikube repo

## Bulding and 1st steps

Building and setup:

```
$ make out/docker-machine-driver-kvm2
$ cp out/docker-machine-driver-kvm2 ~/bin
$ make
$ make test
$ cp out/minikube ~/bin
$ minikube config set vm-driver kvm2
```

First start (this fetches prebuild iso from the internet):

```
$ minikube start
$ minikube status
```

## TODO

setup for:

- podman
- local registry
- dashboard
- build iso myself as well? :)

## References

* [Building the minikube binary](https://minikube.sigs.k8s.io/docs/contrib/building/binaries/)
* [Installing Kubernetes with Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
* [Clustered computing on Fedora with Minikube](https://fedoramagazine.org/minikube-kubernetes/)

## What is Minikube?

It is:

> a tool that runs a single-node Kubernetes cluster in a virtual machine on
> your personal computer

Upstream source code: <https://github.com/kubernetes/minikube/>

## Why to install it from source?

Because the source is there :-)
