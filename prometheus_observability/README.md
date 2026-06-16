# Ansible Demo Role Foundation

## 🎯 Goals

This project provides a Docker-based sandboxing environment for testing Ansible roles with Molecule, using Ubuntu 26.04 as the target OS.

**Core Objectives:**
- Demonstrate Molecule's two-stage workflow (container preparation + role testing)
- Showcase native Ansible inventory handling (Molecule v6 compatibility)
- Provide reusable `demo` role for quick verification without external SSH
- Demonstrate SSH-based role testing via cached Docker containers
- Serve as foundation for future Prometheus and service integrations
- Support full SSH workflow with `ssh_keys` role for key generation/deployment

> **Note:** The `ssh_verify` role is a placeholder for future implementation. The `ssh_keys` role is fully functional and handles SSH key generation and deployment. Both roles are tested via the `ubuntu26_ssh` scenario which connects to a cached Docker container.

## ✨ Features

### Quick Verification with Demo Role and SSH Keys

The **demo role** provides immediate feedback to verify Ansible is working correctly.

The **ssh_keys role** manages SSH key generation and deployment.

**Run converge on localhost:**
```bash
cd prometheus_observability
DEMO_DETAILED=false molecule converge --targets localhost
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
DEMO_DETAILED=true molecule converge --targets localhost
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
# Stage 1: Prepare the Docker container (runs once, then cached)
molecule converge --targets ubuntu

# Stage 2: Test roles via SSH to the cached container
DEMO_DETAILED=false molecule converge --targets ubuntu26_ssh

# Run all tests
molecule test

# Run specific scenarios
molecule test --targets ubuntu    # Prepare container
molecule test --targets ubuntu26_ssh  # Test roles
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

### Two-Stage Workflow

The project uses a two-stage Docker workflow:

**Stage 1: `ubuntu` scenario - Container Preparation**
- Runs in Docker with driver: `docker`
- Prepares the container by installing SSH server, time, and sudo utilities
- Configures the `ubuntu` user with passwordless sudo
- Enables password authentication in SSH
- Starts the SSH service on port 2222
- The container is then cached by Molecule for reuse

**Stage 2: `ubuntu26_ssh` scenario - Role Testing with SSH Access**
- Runs on your host with driver: `default` (native Ansible)
- Connects to the **same cached container** (`ubuntu26-sandbox`) via SSH
- Uses the container's SSH server to run and verify roles from `roles/` directory
- Reads host definitions from `hosts.yml` (bypasses Molecule's restrictive cache)
- Uses vault password from `.vault_pass` for SSH authentication
- Runs converge playbook: `demo` + `ssh_keys` roles

### Container Configuration

- **Image:** `geerlingguy/docker-ubuntu2604-ansible:latest`
- **Systemd:** Enabled with PID 1
- **SSH:** Available on port 2222 (configured in Stage 1)
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
|---------|-------------|---------|
| `DEMO_DETAILED` | Enable detailed demo output in `demo` role | `false` |
| `MOLECULE_EPHEMERAL_DIRECTORY` | Molecule's ephemeral cache directory (where cached containers live) | auto |

**Usage examples:**
```bash
# Show detailed facts and output
export DEMO_DETAILED=true
molecule converge --targets ubuntu26_ssh

# Disable detailed output (faster)
export DEMO_DETAILED=false
molecule converge --targets ubuntu26_ssh
```

## 📁 Project Structure

```
prometheus_observability/
├── molecule/
│   ├── default/                           # Localhost scenario (quick tests)
│   │   ├── molecule.yml                   # Localhost-only config
│   │   └── converge.yml                   # Converge playbook (localhost)
│   ├── ubuntu/                            # Docker container PREPARATION
│   │   ├── molecule.yml                   # Docker container config (prepares container)
│   │   ├── converge.yml                   # Initial converge playbook (cached)
│   │   ├── prepare.yml                    # Container preparation (SSH, sudo config)
│   │   └── _create.yml                    # Create sequence
│   └── ubuntu26_ssh/                      # Role testing scenario (uses cached container)
│       ├── molecule.yml                   # Native Ansible config (driver: default)
│       ├── converge.yml                   # Role converge (demo + ssh_keys)
│       └── hosts.yml                      # Host definitions (SSH config, port 2222)
├── roles/
│   ├── demo/                              # Demo role (runs in container)
│   ├── ssh_verify/                        # Future: SSH verification role
│   └── ssh_keys/                         # Working: SSH key management role
├── group_vars/                            # Shared variables
├── site.yml                               # Site-level playbook
├── molecule.yml                          # Global Molecule config
├── ansible.cfg                           # Ansible configuration
└── README.md
```

## 🔍 What Gets Tested

### localhost target
- Demo role execution on host machine
- System facts gathering
- Ansible capabilities verification
- Conditional task demonstrations
- Command output examples

### ubuntu target (Docker container - preparation stage)
- Container creation with systemd and cgroups
- SSH server installation and configuration
- Ubuntu user setup with passwordless sudo
- Creates cached container: `ubuntu26-sandbox`

### ubuntu26_ssh target (role testing stage)
- **Uses the SAME cached container** from ubuntu target via SSH
- Connects to container's SSH server on port 2222
- Runs converge playbook with `demo` and `ssh_keys` roles
- Validates role idempotence and output
- Demonstrates native Ansible inventory handling (hosts.yml)
- Tests roles from `roles/` directory in cached container

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

- **localhost target:** Runs on your host machine with driver: `default` for quick iteration
- **ubuntu target:** Prepares Docker container with driver: `docker` (installation, SSH, sudo) - container is cached as `ubuntu26-sandbox`
- **ubuntu26_ssh target:** Uses cached container for role testing with SSH access via driver: `default`
- **DEMO_DETAILED:** Set to `true` for verbose output, `false` for minimal output
- **cgroupns_mode:** Set to `host` for systemd compatibility
- **Volume mount:** `/sys/fs/cgroup:/sys/fs/cgroup:rw` required for systemd
- **Molecule v6:** Uses native Ansible architecture with separate `hosts.yml` inventory
- **Container caching:** The `ubuntu` scenario caches the container; `ubuntu26_ssh` reuses it
- **roles_path:** Ansible reads roles from `./roles` directory (defined in `ansible.cfg` and molecule env vars)

## 🔜 Future Work

The following items are planned for future development:

1. **ssh_verify:** SSH connectivity verification commands (placeholder role)
2. **site.yml:** Site-level playbook combining multiple roles (demo, ssh_keys)
3. **Prometheus integration:** Metrics collection and visualization for monitored services

**Current status:**
- `ssh_keys` role is fully functional and handles SSH key generation/deployment
- Both `ssh_keys` and `ssh_verify` roles are tested via the `ubuntu26_ssh` scenario
