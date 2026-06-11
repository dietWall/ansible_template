# 📋 MVP To-Do List: SSH Connectivity & Verification

*Focus on quick feedback*

## ✅ Completed
- [x] Set up Python venv
- [x] Install dependencies (ansible, molecule, docker, yamllint, ansible-lint)
- [x] Create project directory structure
- [x] Create requirements.yml with Galaxy dependencies
- [x] Define central variables in group_vars/all.yml
- [x] Create SSH verification role (ssh_verify)
- [x] Configure Molecule test environment
- [x] Create simplified converge.yml (no roles)
- [x] Create README.md with goals and setup commands
- [x] Create molecule_test.sh wrapper script
- [x] Fix molecule-docker compatibility issue

## 🟢 Ready for Testing

### Quick Start
```bash
cd /home/dw/code/ansible_foundation/prometheus_observability
source ../venv/bin/activate
molecule test
```

### Files Modified
- `molecule.yml` - Simplified to run direct SSH tests (no roles)
- `converge.yml` - Direct SSH connectivity test to `172.17.0.1:ubuntu`

## 🟡 Current Status
- Molecule configuration simplified (no role dependencies)
- SSH tests run directly to Docker host
- Ready to validate SSH connectivity to `ubuntu@172.17.0.1`

## 🔄 Next Steps
1. Run `molecule test` to validate SSH connectivity
2. Once SSH works, add back the ssh_verify role
3. Test with actual Molecule containers

---

## ⬜ Future Enhancements
- Multi-host deployment
- Custom verification commands
- Connection timeout handling
- SSH agent forwarding tests
