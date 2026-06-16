# Ansible Demo Role Foundation

## 🎯 Goals

This project provides a minimal demonstration environment for testing Ansible roles using Molecule, with Docker-based sandboxing for Ubuntu 26.04.

**Core Objectives:**
- Demonstrate Ansible role structure and Molecule workflow
- Provide a reusable demo role for quick verification
- Showcase Molecule scenarios (localhost and Docker container)
- Foundation for future Docker, Prometheus, and service integrations
- Support both localhost and Docker container test scenarios

> **Note:** The `ssh_verify` and `ssh_keys` roles are included as a demonstration for future implementation. They are not yet functional and should not be relied upon for production use. They will be developed in a separate project based on this foundation.

## ✨ Features

### Quick Verification with Demo Role and SSH Keys

The **demo role** provides immediate feedback to verify Ansible is working correctly without requiring SSH connectivity to external hosts.

The **ssh_keys role** manages SSH key generation and deployment, demonstrating full SSH workflow integration.

**Run:**
```bash
cd prometheus_observability
DEMO_DETAILED=false molecule converge
```

**Output includes:**
- Demo title and status messages
- Ansible version and connection type
- System facts (OS, distribution, architecture)
- Command output examples (whoami, time, etc.)
- Conditional task demonstrations
- SSH key generation and deployment (when ssh_keys role runs)

**Verbose mode:**
```bash
DEMO_DETAILED=true molecule converge
```

### 1. Prerequisites

```bash
# Check Ansible and Python are available
ansible --version
python --version
```

### 2. Setup

```bash
# Activate virtual environment (optional but recommended)
source venv/bin/activate

# Install dependencies
pip install -r requirements.yml

# (Optional) Install Galaxy collections if needed
ansible-galaxy install -r requirements.yml
```

### 3. Run Tests

```bash
# Run on localhost (current demo setup)
DEMO_DETAILED=false molecule converge --targets localhost

# Run on Docker container (demo role in container)
DEMO_DETAILED=false molecule converge --targets ubuntu

# Run all tests
molecule test

# Run specific targets
molecule test --targets localhost
molecule test --targets ubuntu
```

### 4. Individual Commands

```bash
# Create Docker container
molecule create

# Run converge playbook
molecule converge

# Check idempotence
molecule idempotence

# Verify connectivity
molecule verify

# Clean up
molecule destroy
```

## 🐳 Docker Container Setup

The `ubuntu` scenario runs the demo role inside a Docker container based on Ubuntu 26.04 with systemd support.

### Container Configuration

- **Image:** `geerlingguy/docker-ubuntu2604-ansible:latest`
- **Systemd:** Enabled with PID 1
- **SSH:** Available on port 2222
- **cgroups:** Host cgroup filesystem mounted for systemd compatibility

### Required System Setup

Before running the Ubuntu scenario, ensure your host has access to cgroups:

```bash
# Mount cgroups (if not already done)
mount --bind /sys/fs/cgroup /sys/fs/cgroup
mount --rbind /sys/fs/cgroup /sys/fs/cgroup
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEMO_DETAILED` | Enable detailed demo output | `false` |

**Usage examples:**
```bash
# Show detailed facts and output
export DEMO_DETAILED=true
molecule converge --targets ubuntu

# Disable detailed output (faster)
export DEMO_DETAILED=false
molecule converge --targets ubuntu
```

## 📁 Project Structure

```
prometheus_observability/
├── molecule/
│   ├── default/               # Localhost scenario
│   │   ├── molecule.yml       # Localhost-only config
│   │   └── converge.yml       # Converge playbook (localhost)
│   ├── ubuntu/                # Docker scenario
│   │   ├── molecule.yml       # Docker container config
│   │   ├── converge.yml       # Converge playbook (runs in container)
│   │   ├── prepare.yml        # Container preparation (SSH, sudo config)
│   │   └── _create.yml        # Create sequence (reference file)
│   └── ubuntu26_ssh/          # Working: SSH verification scenario (native Ansible, not Docker)
├── roles/
│   ├── demo/                 # Demo role for quick verification
│   ├── ssh_verify/          # Future: SSH verification role (not working yet)
│   └── ssh_keys/            # Working: SSH key management role
├── group_vars/              # Shared variables
├── site.yml                 # Site-level playbook (SSH demo, future work)
├── molecule.yml            # Global Molecule config
├── ansible.cfg             # Ansible configuration
└── README.md               # This file
```

## 🔍 What Gets Tested

### localhost target
- Demo role execution
- System facts gathering
- Ansible capabilities verification
- Conditional task demonstrations
- Command output examples

### ubuntu target (Docker container)
- Demo role execution inside container
- Container creation with systemd
- SSH service setup on port 2222
- Passwordless sudo configuration
- cgroup namespace sharing with host
- Idempotence verification

## 📝 Configuration

### ansible.cfg

The project uses a centralized `ansible.cfg` with the following settings:

- **roles_path:** Points to `./roles` directory
- **timeout:** 30 seconds for SSH connections
- **retry_files_enabled:** Yes, for failed command retries
- **host_key_checking:** Disabled (no StrictHostKeyChecking)
- **pipelining:** Enabled for faster execution
- **fact_caching:** Memory caching disabled

### Molecule Configuration

The `molecule.yml` files define:
- **provisioner:** Ansible with custom environment
- **verifier:** Ansible-based verification
- **scenarios:** default (localhost) and ubuntu (Docker)

## ⚠️ Important Notes

- **localhost target:** Runs on your host machine for quick iteration
- **ubuntu target:** Runs in a Docker container for full testing
- **DEMO_DETAILED:** Set to `true` for verbose output, `false` for minimal output
- **cgroupns_mode:** Set to `host` for systemd compatibility
- **Volume mount:** `/sys/fs/cgroup:/sys/fs/cgroup:rw` required for systemd

## 🔜 Future Work

The following roles are placeholders for future development:

1. **ssh_verify:** SSH connectivity verification commands
2. **ssh_keys:** SSH key generation and management
3. **site.yml:** Site-level playbook combining multiple roles

These are currently not functional and are included as demonstration structures for future implementation.
