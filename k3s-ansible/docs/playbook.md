Absolutely — let’s break down **Ansible playbooks** in the simplest, clearest way possible.

A playbook is just a **YAML file** that tells Ansible:

> “Run these tasks on these hosts with these settings.”

Here are the **core basic fields** you will see in almost every playbook:

---

# 1. `- name:` → Description of the Play

```yaml
- name: Install Docker on all hosts
```

A playbook can have **multiple plays**, and each play begins with `-`.

This is just for readability — it shows up in your logs.

---

# 2. `hosts:` → Which machines to run this play on?

```yaml
  hosts: k3s_cluster
```

This refers to **groups or hosts** from your inventory file.

Examples:

* `hosts: all`
* `hosts: server`
* `hosts: agent`
* `hosts: k3s_cluster`

This is where Ansible decides “who am I acting on right now?”

---

# 3. `become:` → Use sudo or not?

```yaml
  become: true
```

* `true` → run all tasks with `sudo`
* `false` → run as normal SSH user (like `ec2-user` or `ubuntu`)

Many system tasks (install packages, change system config) need `become: true`.

---

# 4. `vars:` (optional) → Variables for the play

You can define variables inside the playbook:

```yaml
  vars:
    package_name: nginx
```

These can be used later:

```yaml
  - name: Install package
    ansible.builtin.yum:
      name: "{{ package_name }}"
```

Variables can come from many places:

* Playbooks
* `group_vars/`
* `host_vars/`
* Inventory
* Extra vars from CLI
* Roles

---

# 5. `tasks:` → The actual steps Ansible executes

This is the heart of the playbook.

```yaml
  tasks:
    - name: Install packages
      ansible.builtin.yum:
        name: nginx
        state: present
```

A task always has:

### ✔ A `name`

Human-friendly label

### ✔ A module to run

Example modules:

* `ansible.builtin.command`
* `ansible.builtin.shell`
* `ansible.builtin.copy`
* `ansible.builtin.template`
* `ansible.builtin.yum`
* `ansible.builtin.apt`
* `ansible.builtin.service`

### ✔ Module arguments

What the task should do.

Example:

```yaml
ansible.builtin.yum:
  name: nginx
  state: present
```

### ✔ Optional output registering

```yaml
register: result
```

### ✔ Optional debug output

```yaml
- debug:
    msg: "Command output is {{ result.stdout }}"
```

---

# 6. `roles:` (optional) → Use reusable collections of tasks

Example:

```yaml
  roles:
    - k3s_server
    - k3s_agent
```

Roles help organize bigger projects (like `k3s-ansible`).

You won’t use roles until you understand basic playbooks — but it's good to know what they are.

---

# 7. `handlers:` (optional) → Run only when notified

Used for actions like restarting services.

Example:

```yaml
handlers:
  - name: restart nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

Then a task can notify it:

```yaml
- name: Update config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx
```

Handlers run **once at the end**, no matter how many tasks call them.

---

# Putting it all together: Minimal annotated playbook

Below is a simple but complete playbook:

```yaml
---
- name: Learn Ansible basics           # (1) Name the play
  hosts: k3s_cluster                   # (2) Target hosts
  become: true                         # (3) Use sudo on the nodes

  vars:                                # (4) Variables used in the play
    my_package: htop

  tasks:                               # (5) The actual instructions

    - name: Install a package
      ansible.builtin.yum:
        name: "{{ my_package }}"
        state: present

    - name: Show hostname
      ansible.builtin.command: hostname
      register: host_out

    - name: Print hostname result
      ansible.builtin.debug:
        msg: "Hostname is {{ host_out.stdout }}"

  handlers:                             # (6) Only run when notified
    - name: restart sshd
      ansible.builtin.service:
        name: sshd
        state: restarted
```

---

# Summary Table — Basic Playbook Fields

| Field      | Purpose                    |
| ---------- | -------------------------- |
| `name`     | Play title (for humans)    |
| `hosts`    | Which hosts to run on      |
| `become`   | Whether to use sudo        |
| `vars`     | Variables for the play     |
| `tasks`    | The actual work (modules)  |
| `handlers` | Restart services on change |
| `roles`    | Reusable groups of tasks   |

