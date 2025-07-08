# 📘 System Design Prep Plan (Focused - DDIA First Approach)

## 🎯 Goal
Use *Designing Data-Intensive Applications (DDIA)* as your core learning path to master key system design concepts with minimal distractions.

---

## ✅ Step 1: Use DDIA as Your Core Guide

- Read **1 chapter per week**.
- Focus on **these key chapters** (most relevant for system design interviews):

| Chapter | Topic |
|---------|-------|
| 1       | Reliable, Scalable, Maintainable Apps |
| 2       | Data Models & Query Languages |
| 3       | Storage Engines (B-Trees, LSM Trees) |
| 4       | Encoding & Serialization |
| 5       | Replication |
| 6       | Partitioning |
| 8       | Distributed Systems (Foundations) |
| 9       | Consistency & Consensus |

---

## ✅ Step 2: After Each Chapter, Answer These 3 Questions

1. 🧠 What is the **core concept** of this chapter?
2. ⚖️ What are the **trade-offs** or pros/cons?
3. 🏗️ Where can I **apply this** in a system design scenario?

> Example (Ch. 5 - Replication):
> - Core concept: Leader-based vs multi-leader vs leaderless replication
> - Trade-offs: Consistency vs availability
> - Applies to: Kafka, Notification System, DynamoDB

---

## ✅ Step 3: Practice 1 System Design Problem per Chapter

| Chapter | Practice System |
|---------|------------------|
| Ch 2 | Product Catalog (SQL vs NoSQL) |
| Ch 3 | Log Store (WAL, storage engine) |
| Ch 5 | Kafka-like queue or chat app |
| Ch 6 | Sharded key-value store |
| Ch 9 | Distributed lock or coordination service |

📌 Time-box your practice to 30 mins. Sketch a diagram and identify trade-offs.

---

## ✅ Step 4: Reinforce With 1 Blog or Video

After each chapter:
- Watch **1 YouTube video** or
- Read **1 short blog post**

Suggested Resources:
- Gaurav Sen (YouTube)
- ByteByteGo newsletter
- AWS/GCP architecture blogs
- Martin Kleppmann’s blog (author of DDIA)

⛔ Don’t overload with too many resources. One is enough per chapter.

---

## ✅ Step 5: Maintain a Mini Cheat Sheet

Create a single-page summary with:

- 🧱 Common building blocks (cache, DB, queue, load balancer, etc.)
- 🔁 When to use SQL, NoSQL, LSM Trees, quorum, replication
- ⚖️ Design trade-offs: availability vs consistency, latency vs throughput

Use it for **quick revision before interviews**.

---

## 🗓️ Weekly Routine (Minimal Time, Max Focus)

| Day      | Task                                       |
|----------|--------------------------------------------|
| Mon–Tue  | Read ~10–15 pages of DDIA                  |
| Wed      | Summarize key ideas (3 questions above)    |
| Thu      | Watch 1 supporting blog/video              |
| Fri      | Practice 1 design problem (30 min)         |
| Sun      | Update your cheat sheet                    |

---

## ✍️ Optional: Tools to Use
- **Notion / Obsidian** – For notes + tracking
- **Excalidraw / Pen & Paper** – For architecture diagrams
- **Google Docs** – To maintain your 1-page cheat sheet

---

