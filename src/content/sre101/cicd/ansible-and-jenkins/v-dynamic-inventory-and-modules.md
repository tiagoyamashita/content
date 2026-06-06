---
label: "V"
subtitle: "Dynamic inventory & modules"
group: "CI/CD"
order: 5
---
Dynamic inventory & modules
Static INI files work for fixed fleets. **Dynamic inventory** pulls live host lists from **AWS, Azure, GCP**, or custom scripts.

## 1. AWS EC2 dynamic inventory

Install collection:

```bash
ansible-galaxy collection install amazon.aws
```

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: staging
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: aws_region
hostnames:
  - tag:Name
compose:
  ansible_host: private_ip_address
```

Run:

```bash
ansible-playbook -i inventory/aws_ec2.yml playbooks/site.yml
```

| Benefit | Detail |
|---------|--------|
| Auto-discovery | New EC2 instance tagged `Role=web` joins group |
| No manual edits | Terminated instances drop from inventory |
| CI friendly | Jenkins agent with IAM role queries AWS API |

## 2. Azure / GCP plugins (sketch)

```yaml
# Azure — azure.azcollection.azure_rm
plugin: azure.azcollection.azure_rm
include_vm_resource_groups:
  - myapp-staging-rg
```

```yaml
# GCP — google.cloud.gcp_compute
plugin: google.cloud.gcp_compute
projects:
  - my-project-id
filters:
  - status = RUNNING
  - labels.env = staging
```

Use **service account** or **OIDC** credentials on the control node — same least-privilege ideas as CI [Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md).

## 3. Common modules reference

| Module | Purpose | Example |
|--------|---------|---------|
| `apt` / `yum` | Packages | `name: nginx state: present` |
| `copy` | Push file from control node | JAR artifact to server |
| `template` | Jinja2 render → file | nginx.conf |
| `service` / `systemd` | Service state | `state: restarted` |
| `user` / `group` | Accounts | app service user |
| `file` | Dirs, symlinks, permissions | `/opt/myapp` |
| `get_url` | Download remote file | Fetch release tarball |
| `uri` | HTTP check | Health probe after deploy |
| `wait_for` | Wait for port open | App listening on 8080 |

## 4. Deploy health check example

```yaml
- name: Restart application
  ansible.builtin.systemd:
    name: myapp
    state: restarted

- name: Wait for app port
  ansible.builtin.wait_for:
    port: 8080
    host: 127.0.0.1
    delay: 2
    timeout: 60

- name: HTTP health check
  ansible.builtin.uri:
    url: http://127.0.0.1:8080/actuator/health
    status_code: 200
  register: health
  retries: 5
  delay: 10
  until: health.status == 200
```

Fail the playbook if health never passes — Jenkins stage fails, no silent bad deploy.

## 5. ansible-lint in CI

Catch style errors and risky patterns before deploy:

```bash
pip install ansible-lint
ansible-lint playbooks/
```

```yaml
# .ansible-lint
profile: production
skip_list:
  - yaml[line-length]
```

Jenkins stage:

```groovy
stage('Ansible Lint') {
  steps {
    sh 'ansible-lint playbooks/ roles/'
  }
}
```

| Rule class | Catches |
|------------|---------|
| `risky-shell-pipe` | Unsafe shell |
| `no-changed-when` | Misleading change reporting |
| `command-instead-of-module` | Non-idempotent commands |

## 6. Molecule (optional role testing)

Test roles in Docker without real servers:

```bash
cd roles/myapp
molecule test
```

Runs create → converge → verify → destroy — good for role authors, heavier for simple deploy repos.

## 7. Performance tips

| Tip | Why |
|-----|-----|
| `strategy: free` | Faster on large fleets (unordered) |
| `--forks 20` | Parallel SSH (default 5) |
| `pipelining = True` in ansible.cfg | Fewer SSH round trips |
| Fact caching | Skip repeated `setup` |

**Related:** [Ansible fundamentals](ii-ansible-fundamentals.md), [Jenkins + Ansible pipelines](vi-jenkins-ansible-pipelines.md).
