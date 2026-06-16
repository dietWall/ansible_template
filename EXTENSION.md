# Production Deployment Extension

## Overview

This extension documents the transition from Molecule testing to real server deployments. It introduces:

- **Production inventory** with real server definitions
- **Ansible Vault** for secure secrets management
- **Main playbook** (`site.yml`) for orchestrating role deployments

## Directory Structure

```
prometheus_observability/
├── inventories/
│   └── production/
│       ├── hosts.ini            # Production server definitions
│       └── group_vars/
│           └── all/
│               └── vault.yml    # Encrypted secrets
├── group_vars/                  # Global (unencrypted) variables
├── roles/
│   └── ssh_keys/               # Working role for SSH key deployment
├── site.yml                     # Main deployment playbook
├── ansible.cfg
└── molecule/                    # Molecule scenarios (for testing)
```

## Setup Steps

### Step 1: Create Production Inventory

Create `inventories/production/hosts.ini` to define your production infrastructure. You can organize servers into groups by function:

```ini
[monitoring_servers]
<hostname> ansible_host=<ip_address> ansible_user=<user>
<hostname> ansible_host=<ip_address> ansible_user=<user>

[all:vars]
# Global connection variables for this inventory
```

**Replace the placeholders with actual values:**
- `<hostname>` - Server hostname (e.g., `prometheus-01`)
- `<ip_address>` - Server IP address
- `<user>` - SSH username (e.g., `root`, `ubuntu`, `admin`)

### Step 2: Setup Ansible Vault

Create encrypted vault files for sensitive data. Never store passwords or private keys in plain text in Git.

Run the following command to create a vault file:

```bash
ansible-vault create inventories/production/group_vars/all/vault.yml
```

Ansible will prompt you for a vault password. Save this password securely.

Add your sensitive data to `vault.yml`:

```yaml
---
vault_ssh_private_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
  ...
  -----END OPENSSH PRIVATE KEY-----

vault_initial_root_password: "SuperSecurePassword123!"
```

### Step 3: Configure Global Variables

In `group_vars/all.yml`, define how to reference both unencrypted and encrypted variables:

```yaml
# Variables for the 'ssh_keys' role
ssh_keys_users:
  - name: admin
    authorized_keys:
      - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI..."  # Public keys are safe
    private_key: "{{ vault_ssh_private_key }}"        # Secure value from vault
```

### Step 4: Update Main Playbook

Modify `site.yml` to control deployments. Add roles as needed:

```yaml
---
- name: Deploy SSH Keys
  hosts: all
  become: yes
  roles:
    - role: ssh_keys

# Add more roles for specific functionality:
# - name: Deploy Prometheus Stack
#   hosts: monitoring_servers
#   become: yes
#   roles:
#     - role: prometheus_install
```

## Deployment

Run the deployment command:

```bash
ansible-playbook -i inventories/production/hosts.ini site.yml --ask-vault-pass
```

This command:
1. Prompts for the vault password
2. Decrypts secrets in memory
3. Connects to servers defined in `hosts.ini`
4. Deploys roles from `roles/` directory

## Workflow

### Development Cycle

1. **Develop:** Create roles in `roles/` directory
2. **Test:** Use Molecule scenarios in `molecule/` for isolation
3. **Configure:** Add server IPs to `hosts.ini`, update `vault.yml`
4. **Deploy:** Run `site.yml` with production inventory

### Adding New Roles

When adding new functionality:

1. Create the role (e.g., `roles/prometheus_install`)
2. Test with Molecule
3. Add to `site.yml`:
   ```yaml
   - name: Install Prometheus
     hosts: monitoring_servers
     become: yes
     roles:
       - role: prometheus_install
   ```
4. Deploy with updated playbook
