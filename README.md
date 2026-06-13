# SSH Connectivity Verification Foundation

## 🎯 Goals

This project establishes a foundational SSH infrastructure for testing and validating connectivity to Dockerized systems.

**Core Objectives:**
- Validate SSH connectivity to target hosts and containers
- Verify authentication (SSH keys, sudo) works correctly
- Create a reusable framework for SSH management
- Foundation for future Docker, Prometheus, and service integrations
- Support both localhost and Docker container test scenarios

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
# Check Ansible and Python are available
ansible --version
python --version
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

```bash
# Run on localhost (current setup)
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
│   ├── default/
│   │   ├── molecule.yml      # Molecule configuration (localhost only)
│   │   └── converge.yml      # Converge playbook
│   └── ubuntu/
│       ├── molecule.yml      # Docker scenario configuration
│       ├── converge.yml      # Converge playbook
│       ├── create.yml        # Create sequence
│       ├── destroy.yml       # Destroy sequence
│       └── verify.yml        # Verify playbook
├── roles/
│   ├── demo/                 # Demo role for quick verification
│   ├── ssh_verify/          # SSH verification role
│   └── ssh_keys/            # SSH key management role
├── group_vars/              # Shared variables
└── site.yml                 # Site-level playbook
```

## 📝 Notes

- **localhost target**: Run on your host machine for quick iteration and demo role testing
- **ubuntu target**: Runs the demo role in a Docker container for full testing

## 🔍 What Gets Tested

- **localhost target**: Demo role, system facts, Ansible capabilities
- Connection timeouts and errors
