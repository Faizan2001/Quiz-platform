# Technical Specification – Phase 1
## Django-Based Quiz & User Management Platform

---

## Overview
This document defines the **Phase 1 scope** for a Django-based Quiz & User Management platform.  
The goal is to deliver a fully functional quiz application first, with a minimal technology stack, keeping it easy to maintain by a 1–2 person team.  
The **Drawing Module** will be added later as a separate Django app.

---

## Technology Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| **Backend** | Django 5.2 LTS | Core framework |
| **API** | Django REST Framework 3.16.x | RESTful endpoints |
| **Frontend** | Django Templates + HTMX 1.9+ | Lightweight, dynamic UI without JS build tools |
| **Database** | PostgreSQL 15+ | Relational database |
| **Authentication** | Django Auth / DRF Token | User and API authentication |
| **Audit Log (optional)** | django-simple-history | Track model-level changes |

---

## Modules & Roles

### Organization Admin
- Manage organization profile, subscription, and payments  
- Create, update, or delete users  
- Assign roles and permissions  

### Quiz Admin
- Create/update/delete subjects, categories, and sub-categories  
- Upload questions via form or CSV/XLSX  
- Mark questions as single- or multiple-answer  
- Define quizzes (categories, number of questions, passing score, instructions)  
- Edit and soft-delete questions  

### User
- Update account information  
- View subscription and assigned subjects/categories  
- Run quizzes and review past results/history  

---

## Functional Scope

### Included
- Authentication & User Roles  
- Organization & User Management  
- Quiz Definition & Question Bank  
- Quiz Runtime (questions, navigation, flagging, review panel)  
- Results & History  
- Soft Delete & Audit Log  
- Configuration table for organization details  

---

## Database Schema

### Tables (Phase 1)
- `Configuration`  
- `Organization`  
- `Person`  
- `User`  
- `Category`  
- `Question`  
- `Option`  
- `QuizDefinition`  
- `QuizAttempt`  
- `ModuleList`

All models include common fields:  
created_at, updated_at, is_deleted, deleted_at, updated_by

Soft delete marks `is_deleted=True` instead of physically deleting rows.

---

## Forward Compatibility
Use the `ModuleList` table to future-proof the app.  
Example field:  


enable_module = (default=False)


---

## UI & Flow

### User Dashboard
- Shows available subjects/categories  
- Buttons: **Start Quiz**, **View Results**  
- Account Menu: Update profile/password  
- Help Menu: Display instructions/FAQs  

### Quiz Screen
- Instruction Panel (always visible / collapsible)  
- Display questions sequentially (1 per screen)  
- Single-answer → radio buttons  
- Multiple-answer → checkboxes  
- Buttons: **Next**, **Previous**, **Review**, **Submit**  
- Flag/unflag questions and save progress  
- Review Panel indicators:  
  - Answered = Green  
  - Unanswered = Red  
  - Flagged = Flag icon  

### Results Page
- Show score, pass/fail status, and per-question breakdown  
- Display history of previous attempts  

---

## Non-Functional Requirements
- **Security:** HTTPS, role-based access control, input validation  
- **Performance:** Local cache for offline use  
- **Maintainability:** Minimal dependencies, no frontend build chain  
- **Reliability:** Incremental backups, logs, and exception monitoring  
- **Audit:** Use `django-simple-history` for change tracking  

---

## Milestones

| ID | Milestone | Description |
|----|------------|-------------|
| **M1** | Core data models + Auth + RBAC | Build foundational data models and authentication |
| **M2** | Quiz Admin | Subjects/Categories + CSV import |
| **M3** | Quiz Runtime | UI, scoring logic, and review panel |
| **M4** | History & Reporting Dashboard | User result history and admin overview |
| **M5** | Subscription & Payment Integration | Payment gateway integration |
| **M6** | Deployment & Documentation | Final deployment and documentation |

---

## Summary
Phase 1 delivers a secure, maintainable, and modular **Django + PostgreSQL** platform with clear role management, quiz functionality, and a scalable architecture for future modules such as drawing tools and payments.

---