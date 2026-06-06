---
label: "I"
subtitle: "Overview"
group: "CI/CD"
order: 1
---
Ansible & Jenkins — overview
**Jenkins** runs the CI pipeline (build, test, gate). **Ansible** applies **desired state** on servers (packages, config, deploy, restart). Splitting responsibilities keeps deploy logic reusable outside Jenkins.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Ansible fundamentals](ii-ansible-fundamentals.md) | Agentless model, idempotency, core terms |
| [Inventory & playbooks](iii-inventory-and-playbooks.md) | Hosts, groups, tasks, handlers |
| [Roles, variables & Vault](iv-roles-variables-and-vault.md) | Role layout, var precedence, secrets |
| [Dynamic inventory & modules](v-dynamic-inventory-and-modules.md) | Cloud inventory, common modules, ansible-lint |
| [Jenkins + Ansible pipelines](vi-jenkins-ansible-pipelines.md) | Jenkinsfile, Vault creds, Ansible plugin |
| [Deploy patterns & operations](vii-deploy-patterns-and-operations.md) | Deploy playbooks, tags, hotfixes, staging/prod |

**Related:** **Tools & platforms** → [Jenkins](../tools-and-platforms/iv-jenkins.md) (CI-focused Jenkins), Part I fundamentals, **Terraform** submenu.

## CI build → Ansible deploy flow

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 110" role="img" aria-label="Jenkins CI then Ansible deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Jenkins owns CI · Ansible owns server state</text>
  <rect x="12" y="36" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="8">Jenkins</text>
  <text x="20" y="68" fill="#71717a" font-size="7">build test</text>
  <path d="M84 52 H104" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="104" y="36" width="72" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="116" y="56" fill="#e4e4e7" font-size="8">artifact</text>
  <path d="M176 52 H196" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="196" y="36" width="88" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="56" fill="#e4e4e7" font-size="8">ansible-playbook</text>
  <path d="M284 52 H304" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="304" y="36" width="88" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="56" fill="#e4e4e7" font-size="8">webservers</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Same playbook from Jenkins or laptop for hotfixes</text>
</svg></figure>

## When this pattern fits

| Good fit | Consider alternatives |
|----------|------------------------|
| VMs or bare metal fleet | Pure Kubernetes → Helm/GitOps |
| Mixed Linux config + deploy | Serverless → CI deploy to cloud API |
| On-prem with Jenkins already | Greenfield SaaS → GitHub Actions + Terraform |

## Rehearsal

- What does **agentless** mean for Ansible?
- Who owns **build** vs **server configuration** in this split?
- Why keep inventory in the same repo as the Jenkinsfile?
