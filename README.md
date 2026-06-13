# SSH Connectivity Verification Foundation

## 🎯 Goals

This project establishes a foundational SSH infrastructure for testing and validating connectivity to Dockerized systems.

**Core Objectives:**
- Validate SSH connectivity to target hosts and containers
- Verify authentication (SSH keys, sudo) works correctly
- Create a reusable framework for SSH management
- Foundation for future Docker, Prometheus, and service integrations

## ✨ Features

### Quick Verification with Demo Role

The **demo role** provides immediate feedback to verify Ansible is working correctly without requiring SSH connectivity.

**Run:**
```bash
cd prometheus_observability
DEMO_DETAILED=false molecule converge
```

**Output includes:**
- Demo title and status messages
- Ansible version and connection type
- System facts (OS, distribution, architecture)
- Available Ansible facts (70+)
- Command output examples (whoami, time, etc.)
- Conditional task demonstrations

**Verbose mode:**
```bash
DEMO_DETAILED=true molecule converge
```

See [`roles/demo/`](roles/demo/) for demo role configuration.

### 1. Prerequisites

```bash
# Install Docker
docker --version

# Make sure the Docker host network bridge IP is accessible
# (typically 172.17.0.1 for Docker's default bridge)
```

### 2. Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.yml

# (Optional) Install Galaxy collections if needed
ansible-galaxy install -r requirements.yml
```

### 3. Run Tests

**Available Targets:**
- `localhost` - Run on your host machine (faster, no Docker needed for tests)
- `docker-ubuntu2204` - Run in isolated Docker container

```bash
# Run on localhost (current setup)
cd prometheus_observability
DEMO_DETAILED=false molecule converge --targets localhost

# Run on Docker container
molecule converge --targets docker-ubuntu2204

# Run on all targets
molecule test

# Run specific targets
molecule test --targets localhost docker-ubuntu2204
```

### 4. Individual Commands

```bash
# Create and provision containers
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

## 📁 Project Structure

```
prometheus_observability/
├── molecule/
│   └── default/
│       ├── molecule.yml      # Molecule configuration
│       └── converge.yml      # Converge playbook
├── roles/
│   ├── demo/                 # Demo role for quick verification
│   │   ├── tasks/main.yml
│   │   ├── defaults/main.yml
│   │   ├── vars/main.yml
│   │   └── handlers/main.yml
│   ├── ssh_verify/           # SSH verification role
│   │   ├── tasks/main.yml
│   │   └── templates/
│   └── ssh_keys/            # SSH key management role
│       ├── tasks/main.yml
│       └── files/
├── group_vars/
│   └── all.yml               # Shared variables
└── site.yml                  # Site-level playbook
```

## 🔧 Configuration

Edit `group_vars/all.yml` to customize:

```yaml
docker_host_ip: "172.17.0.1"
docker_host_user: "ubuntu"
ssh_verify_commands:
  - whoami
  - pwd
  - ls -la
  - id
```

## 📝 Notes

- **Multi-target setup**: `localhost` and `docker-ubuntu2204` targets in molecule.yml
- **localhost target**: Best for quick iteration, demo role testing
- **docker-ubuntu2204 target**: Isolated container environment for full testing
- **Future**: Extend to staging environments (multi-host deployments)
- **geerlingguy.docker** is a role, not a Galaxy collection - using `community.docker` instead
- **molecule-docker** is deprecated; will migrate to `molecule-plugins[docker]` in future iteration
- SSH connection tests run against Docker host (`172.17.0.1:ubuntu`)

## 🔍 What Gets Tested

- **localhost target**: Demo role, system facts, Ansible capabilities
- **docker-ubuntu2204**: SSH connectivity, authentication, sudo, verification commands
- Connection timeouts and errors
