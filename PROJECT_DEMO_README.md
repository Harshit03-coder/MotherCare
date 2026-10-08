# Cloud Computing Lab & Project Demonstration Guide

---

## 1. Executive Summary & Architecture Overview

This project presents a multi-tier private cloud environment deployed using **Virtualization**, **Containerization**, and **Cloud Monitoring Automation**.

### High-Level Architecture Diagram
```
                     +-------------------------------------------------+
                     |                  Host Machine                   |
                     |             (Windows 11 / WSL2 Host)            |
                     +-------------------------------------------------+
                                              |
                                              v
                     +-------------------------------------------------+
                     |        Virtualization Layer: Ubuntu 24.04       |
                     |           (WSL2 Linux Virtual Machine)          |
                     |                 IP: 192.168.26.112              |
                     +-------------------------------------------------+
                                              |
                   +--------------------------+--------------------------+
                   |                                                     |
                   v                                                     v
+------------------------------------+                +------------------------------------+
|       Docker Container Layer       |                |     Cloud Monitoring Subsystem     |
|         (Microservices / App)      |                |     (Go Automation Program)        |
+------------------------------------+                |    Analyzes CPU, RAM, Disk, Net,   |
| 1. mothercare_frontend (Node/Vite) |                |          and Container Status      |
| 2. mothercare_backend  (Django API)|                +------------------------------------+
| 3. mothercare_db       (Postgres15)|
| 4. mothercare_redis    (Redis 7)   |
| 5. cc_nextcloud        (Nextcloud) |
| 6. cc_mariadb          (MariaDB)   |
+------------------------------------+
```

---

## 2. Component Breakdown

### A. The Custom Application: MotherCare Hospital Management System
* **What it does:** A specialized clinical and hospital management software designed for maternity care, neonatal monitoring, patient management, electronic prescriptions, and appointment scheduling.
* **Architecture:** Decoupled client-server architecture (SPA frontend + RESTful backend API).
* **Tech Stack:**
  * **Frontend:** React, TypeScript, Tailwind CSS, Vite
  * **Backend:** Python 3.11, Django, Django REST Framework, Astral UV
  * **Relational Database:** PostgreSQL 15 (Alpine)
  * **In-Memory Cache / Message Broker:** Redis 7 (Alpine)
* **Access URL:** `http://192.168.26.112:5173`

### B. The Cloud Storage Layer: Nextcloud Private Cloud
* **What it does:** Serves as the organization's private SaaS (Software as a Service) cloud storage and collaboration platform (similar to a self-hosted Google Drive / Dropbox).
* **Why it is used here:**
  1. **Multi-Tenancy & Quotas:** Enforces per-user disk quotas (2 GB per student) and role-based access.
  2. **Decoupled Team Collaboration:** Allows team members (`student1`, `student2`, `student3`) and the Administrator (`Harshit Jain`) to share project files, documentation, and source code securely without third-party vendor lock-in.
  3. **Enterprise Storage Features:** Offers built-in version control, file previewing, group sharing policies, access control lists (ACLs), and automated database synchronization via OCC CLI.
* **Tech Stack:**
  * Nextcloud Server (Apache + PHP 8.x)
  * MariaDB 10.6 Database Backend
  * Docker Volume Mounts for persistent storage
* **Access URL:** `http://192.168.26.112:8080`

### C. Cloud Infrastructure Monitoring: Go Monitor
* **What it does:** A custom-built Go automation binary (`cloud_monitor.go`) that inspects low-level virtual machine resources:
  * CPU Load Average & System Uptime
  * Memory (RAM) Allocation & Cache distribution
  * Virtual Disk Partition Usage (`/dev/sdd`)
  * Virtual Network Interfaces (`eth0`, `docker0`, bridges)
  * Real-time Docker container runtime status

---

## 3. System Access Credentials

### A. MotherCare Clinical Management System
* **URL:** `http://192.168.26.112:5173`
* **Username:** `admin`
* **Password:** `Admin@123`
* **Role:** Hospital Administrator / Clinical Lead

### B. Nextcloud Private Cloud
* **URL:** `http://192.168.26.112:8080`

| Account | Username | Password | Role / Details |
|---|---|---|---|
| **System Admin** | `Harshit Jain` | *(Your set Admin password)* | Instance Owner / System Admin |
| **Student 1 (Lead)** | `student1` | `Stud3nt@CC2026!` | Project Owner (Vinit Patil) |
| **Student 2** | `student2` | `Stud3nt@CC2026!` | Team Member (Utkarsh Sonawane) |
| **Student 3** | `student3` | `Stud3nt@CC2026!` | Team Member (Student Three) |

*All students have an enforced **2 GB** quota and belong to the **Project-Team** group.*

---

## 4. Step-by-Step Demonstration Script

When presenting to professors or evaluators, follow this workflow:

### Step 1: Demonstrate Infrastructure & Container Orchestration
1. Open PowerShell and run:
   ```powershell
   wsl -d Ubuntu-24.04 -u root bash -c "docker ps"
   ```
2. **What to explain:**
   > *"We deployed a multi-container stack inside an Ubuntu WSL2 virtual environment. There are 6 active containers: Nextcloud, MariaDB, Postgres, Redis, Django API backend, and the Vite frontend proxy."*

---

### Step 2: Demonstrate Resource & Infrastructure Monitoring (Go Program)
1. Run the Go monitoring program:
   ```powershell
   wsl -d Ubuntu-24.04 -u root bash -c "cd /mnt/d/CC/MotherCare/cc-lab-infrastructure && go run cloud_monitor.go"
   ```
2. **What to explain:**
   > *"This Go monitoring tool inspects the underlying hypervisor/VM resources—CPU load, available memory, disk space, and virtual network interfaces—while verifying container health."*

---

### Step 3: Demonstrate Cloud Storage & Multi-Tenancy (Nextcloud)
1. Open `http://192.168.26.112:8080` in your web browser.
2. Log in as **Admin (`Harshit Jain`)**:
   * Navigate to the top-right profile icon ➔ **Users**.
   * Show that `student1`, `student2`, and `student3` exist with **2 GB storage quotas** assigned to the `Project-Team` group.
3. Log out, then log in as **`student1`**:
   * Open **Files** ➔ **Project-Team** ➔ **MotherCare**.
   * Show that all source files and project documentation have been extracted and are hosted securely in private cloud storage.
4. Log out, then log in as **`student2`**:
   * Click **Shared with you** on the left menu.
   * Open the shared **MotherCare** folder and view individual source files.
5. **What to explain:**
   > *"This verifies Role-Based Access Control (RBAC), user storage quotas, and decoupled collaboration in a private cloud environment."*

---

### Step 4: Demonstrate the Deployed Clinical Application (MotherCare)
1. Open `http://192.168.26.112:5173` in your browser.
2. Enter the credentials:
   * **Username:** `admin`
   * **Password:** `Admin@123`
3. Click **Login** to enter the MotherCare Maternity Hospital portal.
4. **What to explain:**
   > *"This is our custom production-grade application, MotherCare. It connects to the containerized Django REST API, backed by PostgreSQL and Redis caching, running side-by-side with our private cloud infrastructure."*

---

## 5. Summary Matrix for Lab Submission

| Lab Evaluation Criteria | Demonstrated Feature | Evidence |
|---|---|---|
| **Virtualization** | Ubuntu 24.04 on WSL2 | Linux kernel instance on Windows host |
| **Containerization** | Docker & Docker Compose | 6 coordinated containers across two networks |
| **Cloud Storage (SaaS)** | Nextcloud Private Cloud | Quotas, user groups, file sharing |
| **Application Deployment** | MotherCare Maternity System | Multi-tier React + Django + PostgreSQL + Redis stack |
| **Automation & Monitoring** | Go CLI Monitor (`cloud_monitor.go`) | Real-time CPU, RAM, disk, network, and container telemetry |
