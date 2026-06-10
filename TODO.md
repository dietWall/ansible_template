# 📋 MVP To-Do List: SSH Connectivity & Verification

*Focus on quick feedback*

---

## 🎯 Project Overview

This project establishes a foundational SSH infrastructure for deploying and testing connectivity to Dockerized systems. The goals are:

- **Base Setup**: Create a reusable Ansible-based framework for SSH management and verification
- **Connection Validation**: Implement automated tests to confirm reliable SSH access to target containers and hosts
- **Foundation for Future Work**: Build a solid groundwork that can be extended with Docker, Prometheus, and other services

---

## 🟩 Phase 1: Project Structure & Dependencies

### Create Virtual Environment
- Set up and activate Python venv.
- Install packages:
  ```bash
  pip install ansible molecule molecule-docker docker yamllint ansible-lint
  ```

### Create Project Directory Structure
Create minimal folder structure:
```
prometheus_observability/
├── group_vars/all.yml
├── roles/ssh_keys/
├── roles/ssh_verify/
│   ├── tasks/main.yml
│   └── templates/connect_test.yml.j2
└── site.yml
```

### Define Galaxy Dependencies
- Create `requirements.yml` for `geerlingguy.docker` and `community.docker`
- Install dependencies via `ansible-galaxy install -r requirements.yml`.

---

## 🟩 Phase 2: Variables & SSH Key Deployment

### Define Central Variables
- Fill `group_vars/all.yml` with:
  ```yaml
  ---
  docker_host_ip: "172.17.0.1"
  docker_host_user: "ubuntu"
  ssh_verify_commands:
    - whoami
    - pwd
    - ls -la
    - id
  ```

### Store SSH Public Key
- Save public key as file: `prometheus_observability/roles/ssh_keys/files/authorized_keys`
- Copy your SSH public key here for testing connectivity

### Write SSH Deployment Task
- In `prometheus_observability/roles/ssh_keys/tasks/main.yml`, set up the key for the existing user (e.g., `ubuntu`) using `ansible.posix.authorized_key`.

---

## 🟩 Phase 3: SSH Verification Role (Core!)

### SSH Connection Verification Role
- Create new role: `prometheus_observability/roles/ssh_verify/`
- **Purpose**: Test SSH connectivity to:
  - Molecule containers (e.g., `ubuntu-twin`)
  - Existing systems (local host or remote servers)
- **Actions**: Run simple commands to verify connection works:
  - `whoami`
  - `pwd`
  - `ls -la`
  - `id`
- Configure the role to use SSH key authentication (from Phase 2)
- Add to `site.yml` playbook

---

## 🟩 Phase 4: Molecule Test Configuration (SSH Validation)

### Molecule Configuration
- Configure `molecule/default/molecule.yml` to use real SSH connections:
  ```yaml
  ---
  dependency:
    name: galaxy
  driver:
    name: docker
  platforms:
    - name: ubuntu-twin
      image: geerlingguy/docker-ubuntu2204-ansible:latest
      privileged: true
      command: /lib/systemd/systemd
      volumes:
        - /sys/fs/cgroup:/sys/fs/cgroup:rw
        - /var/run/docker.sock:/var/run/docker.sock:rw
      cgroupns: host
      pre_build_image: true
  provisioner:
    name: ansible
    connection_options:
      ansible_connection: ssh
  playbooks:
    converge: converge.yml
  verifier:
    name: ansible
  ```

### Molecule Playbook
- In `molecule/default/converge.yml`, define that Molecule SSHs in as user `ubuntu`
- Execute SSH verification role via `become: true`

---

## 🟩 Phase 5: First Test Run

### Run Test
- Execute `molecule test`
- Goal: Get green run (validates SSH, Sudo, SSH key authentication)

---

## ⬜ Future Enhancements

- Multi-host deployment
- Custom verification commands
- Connection timeout handling
- SSH agent forwarding tests
