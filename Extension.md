1. Erweiterte VerzeichnisstrukturWir fügen das Verzeichnis inventories/ für deine echten Server und deren geheime Variablen (Vault) hinzu. Deine Struktur wird dadurch wie folgt erweitert:textprometheus_observability/
├── inventories/
│   └── production/
│       ├── hosts.ini            # Deine echten Zielserver
│       └── group_vars/          # Variablen speziell für dieses Inventory
│           └── all/
│               └── vault.yml    # Verschlüsselte Passwörter/Keys
├── group_vars/                  # Globale (unverschlüsselte) Variablen
├── roles/
│   └── ssh_keys/                # Deine funktionierende Rolle
├── site.yml                     # Dein Haupt-Playbook
├── ansible.cfg
└── ... (Molecule-Ordner bleiben unberührt)
Verwende Code mit Vorsicht.2. Schritt-für-Schritt UmsetzungSchritt 2.1: Das Inventory anlegen (inventories/production/hosts.ini)Erstelle diese Datei, um deine Infrastruktur zu definieren. Du kannst deine Server hier auch in Gruppen (z. B. nach Funktion) unterteilen:ini[monitoring_servers]
prometheus-prod-01 ansible_host=192.168.178.50 ansible_user=root
prometheus-prod-02 ansible_host=192.168.178.51 ansible_user=root

[all:vars]
# Hier können globale Verbindungsvariablen für dieses Inventory stehen
Verwende Code mit Vorsicht.Schritt 2.2: Ansible Vault für sensible Daten erstellenDa Passwörter und Private Keys niemals im Klartext im Git landen dürfen, verschlüsseln wir sie.Führe folgenden Befehl in deinem Terminal aus:bashansible-vault create inventories/production/group_vars/all/vault.yml
Verwende Code mit Vorsicht.Ansible fragt dich nun nach einem Vault-Passwort. Vergiss dieses Passwort nicht!Es öffnet sich dein Standard-Texteditor. Trage dort deine geheimen Variablen ein.Best Practice: Beginne die Namen mit vault_, um sie später sofort als verschlüsselt zu erkennen.yaml---
vault_ssh_private_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
  ...
  -----END OPENSSH PRIVATE KEY-----

vault_initial_root_password: "MeinSuperSicheresSudoPasswort123!"
Verwende Code mit Vorsicht.Speichere und schließe den Editor. Die Datei ist nun sicher verschlüsselt.Schritt 2.3: Unverschlüsselte Variablen verknüpfen (group_vars/all.yml)Nutze die globale Variablen-Datei auf oberster Ebene, um die Struktur für deine Rolle zu definieren. Hier verknüpfst du die Klartext-Daten (z. B. Public Keys) mit den verschlüsselten Werten aus dem Vault:yaml---
# Variablen für die Rolle 'ssh_keys'
ssh_keys_users:
  - name: admin
    authorized_keys:
      - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI..." # Public Keys sind unkritisch
    private_key: "{{ vault_ssh_private_key }}"     # Holt den Key sicher aus dem Vault
Verwende Code mit Vorsicht.Schritt 2.4: Das Haupt-Playbook anpassen (site.yml)Dein site.yml steuert ab jetzt den gesamten Rollout. Wenn du später neue Rollen hinzufügst, erweiterst du dieses Playbook einfach nach unten:yaml---
- name: Basis-Konfiguration (SSH-Keys) für alle Server
  hosts: all
  become: yes
  roles:
    - role: ssh_keys

# Hier kannst du zukünftig weitere Rollen für spezifische Gruppen anhängen:
# - name: Prometheus Stack installieren
#   hosts: monitoring_servers
#   become: yes
#   roles:
#     - role: prometheus_install
Verwende Code mit Vorsicht.3. Der Ausführungsbefehl (Deployment)Um deine Rolle nun live auf den Servern auszuführen, übergibst du Ansible das neue Inventory und erzwingst die Abfrage des Vault-Passworts:bashansible-playbook -i inventories/production/hosts.ini site.yml --ask-vault-pass
Verwende Code mit Vorsicht.Ansible fragt dich nach dem Passwort, entschlüsselt die vault.yml temporär im Arbeitsspeicher, verbindet sich mit den IPs aus der hosts.ini und rollt die SSH-Keys aus.4. Zukünftiger Workflow für neue RollenWenn du das System einmal so aufgesetzt hast, ist der Ablauf für jede weitere Rolle immer identisch:Rolle entwickeln: Du erstellst z. B. roles/prometheus_install.Molecule nutzen: Du testest die Rolle isoliert in deinem molecule/ Verzeichnis.Produktiv-Daten pflegen: IPs kommen in die hosts.ini, Passwörter in die vault.yml.site.yml erweitern: Du hängst die neue Rolle in die site.yml an.Deployment: Du startest den obigen ansible-playbook Befehl