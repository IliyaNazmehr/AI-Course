# Emotipal: Advanced AI-Driven Psychometric & Behavioral Analysis Platform

<p align="center">
  <img src="Emotipal.png" alt="Emotipal Architecture" width="50%" style="border-radius: 10px;">
  <br>
  <i>"Beyond Personality Testing: A Distributed System for Psychological Insight"</i>
</p>

## 🎓 Academic Credentials
- **Institution:** Islamic Azad University, Tehran Central Branch (IAUCTB)
- **Faculty:** Faculty of Computer Science & Engineering
- **Project Type:** Undergraduate Final Project (B.Sc.)
- **Supervisor:** Honorable Dr. Maryam Hajiesmaeili
- **Project Name:** Emotipal Backend Framework

## 👥 R&D Team
1. **Iliya Nazmehr** (Principal Architect & Senior Backend Engineer)
2. **Maryam Shahravi** (AI Engineering & Prompt Design)
3. **User 3** (Database Architect)
4. **Negar abdollahi** (Software Requirement Analysis & UI/UX)
5. **User 5** (Security Analyst & QA)

---

## 1. Executive Summary
**Emotipal** is a high-performance backend infrastructure designed for large-scale psychometric evaluations via Telegram. Unlike simple chatbot implementations, Emotipal utilizes an **Enterprise Service Bus** approach to decouple UI (Telegram), Logic (Exam Engine), and Intelligence (AI Analysis).

---

## 2. Technical Architecture & Design Patterns
The system is built upon **PHP 8.3** with a focus on memory safety and low-latency response times.

### 2.1 Service-Repository Pattern
We separated the "How to save data" from "What to do with data":
- **Repositories:** Direct interface with MariaDB using PDO. No business logic resides here.
- **Services:** High-level logic (e.g., calculating MBTI scores) that consumes Repositories.

### 2.2 Dependency Injection (DI) Container
To ensure **SOLID** principles, we implemented a custom `Container` utilizing **Reflection API**. This allows for "Lazy Loading" of services, ensuring that a database connection is only opened when a query is actually executed.



---

## 3. Core Engine Implementation (The "Bot" Logic)

### 3.1 Stateful Exam Engine
The most complex part of Emotipal is the `ExamEngine`. It handles:
- **Bidirectional Navigation:** Using a `UNIQUE KEY` constraint on `(user_id, question_id)`, we implemented an **UPSERT** logic. This allows users to go back, change an answer, and have the system update rather than duplicate the record.
- **Dynamic Keyboards:** The `KeyboardBuilder` utility generates Inline Keyboards on-the-fly, marking completed tests with a ✅ emoji by performing a `LEFT JOIN` on the results table.

### 3.2 AI Hyper-Analysis Flow
Once the threshold of completed tests is met, the system executes the following:
1. **Data Aggregation:** JSON-encoding of raw scores + psychological weights.
2. **LLM Contextualization:** Injecting the persona of a "Senior Clinical Psychologist" into the system prompt.
3. **Deterministic Output:** Forcing the AI to return a JSON Schema to ensure the backend can parse the report into the user database.



---

## 4. Database Schema Design (MariaDB)
The database is normalized to **3NF (Third Normal Form)** to ensure data integrity and scalability:

- **`users`**: Stores Telegram metadata, session states (FSM), and administrative privileges.
- **`questions` / `options`**: Linked via one-to-many. Options store `score_weight` in a JSON field to support multi-dimensional tests (e.g., a single question affecting both "Extroversion" and "Openness").
- **`user_answers`**: The primary log of user interaction.
- **`test_results`**: Stores the final AI-generated PDF/Text report and calculated scores.

---

## 5. Security & Performance Optimization
- **Prepared Statements:** 100% protection against SQL Injection via native PDO.
- **Webhook Security:** Implementing `X-Telegram-Bot-Api-Secret-Token` verification to prevent unauthorized API requests.
- **Strict Typing:** Every function signature uses `declare(strict_types=1)` to prevent runtime type-casting errors.
- **Memory Management:** Leveraging PHP Generators for the Broadcast system to handle thousands of users with < 20MB RAM usage.

---

## 6. How to Run & Code Samples

### 6.1 CLI Console
The project includes a custom CLI tool for maintenance:
```powershell
php bin/console migrate   # Executes DB Migrations
php bin/console seed      # Populates test questions

```

### 6.2 Sample Service (Dependency Injection)

```php
// src/Core/Container.php logic
$container = new Container();
$handler = $container->get(UpdateHandler::class); 
// Automatically resolves dependencies for Database, Repository, and Service.

```

---

## 7. Project Roadmap & Future Enhancements

* [ ] Multi-language support (English/Persian).
* [ ] Integration with PDF-Generator for formal certificates.
* [ ] Real-time Admin Dashboard using WebSockets.

---

**Academic Supervisor:** Dr. Maryam Hajiesmaeili

**Developers:** Computer Science Dept, IAUCTB.
