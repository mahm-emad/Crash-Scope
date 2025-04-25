
# 🚦 Crash Scope

Crash Scope is an end-to-end data pipeline and analytics solution designed to unify, process, and visualize traffic accident data from multiple sources. The project leverages both batch and real-time data processing to enable actionable insights that can help city planners, public safety authorities, and analysts improve road safety and traffic efficiency.

---

## 📌 Table of Contents
1. [Background](#background)
2. [Purpose](#purpose)
3. [Competitor Analysis](#competitor-analysis)
4. [Customers](#customers)
5. [Scope](#scope)
6. [Stakeholders](#stakeholders)
7. [Business Model](#business-model)
8. [Objectives & Services](#objectives--services)
9. [System Architecture](#system-architecture)
10. [Data Warehouse Design](#data-warehouse-design)
11. [Tools & Technologies](#tools--technologies)
12. [Installation Guide](#installation-guide)
13. [Data Flow Clarification](#data-flow-clarification)
14. [Dashboards](#dashboards)

---

## 🧠 Background
Organizations generate massive data from sources like SQL databases, XML files, and CSVs. Public transport authorities struggle to analyze crash data efficiently due to its scattered and heterogeneous nature. This project addresses that by providing a centralized system for both real-time and batch data integration and analysis.

---

## 🎯 Purpose
The goal is to:
- Integrate traffic accident data from structured and semi-structured sources.
- Process data via SSIS for ETL and Apache Kafka & PySpark for streaming.
- Store it in a SQL Server data warehouse.
- Visualize insights through Power BI dashboards.

---

## 📊 Competitor Analysis
- **City of Chicago Open Data Portal**: Provides crash data but lacks real-time and automated ETL capabilities.
- **Google Maps/Waze**: Real-time alerts but limited to navigation purposes.
- **Crash Scope**: Unites ETL, real-time streaming, and dashboards, bridging existing platform gaps.

---

## 👥 Customers
- **Local Authorities**: Identify accident-prone areas.
- **Urban Planners**: Design safer roads based on real-time trends.
- **Emergency Response**: Optimize dispatch and response strategies.
- **Data Scientists**: Perform in-depth analysis and trend forecasting.

---

## 📦 Scope
### ✅ In Scope:
- ETL via SSIS  
- Streaming via Kafka and PySpark  
- Integration from CSV, XML, and databases  
- Power BI dashboards  

### ❌ Out of Scope:
- Predictive models  
- Traffic simulations  
- Third-party law enforcement APIs  

---

## 📢 Stakeholders
- **CDOT**, **CPD**, **IDOT**, **CMAP**, and **Chicago City Council** all benefit from the platform’s insight-driven decision support.

---

## 💼 Business Model
- **Subscription-based** SaaS for municipalities and city agencies  
- **Freemium** dashboard for public access  
- Custom insights for **insurance** and **logistics** companies  
- Consulting for traffic analytics solutions

---

## 🎯 Objectives & Services
- Integrate 3+ data sources with SSIS  
- Stream updates via Kafka in under 5s  
- Transform data using PySpark  
- Load data to DWH (streaming latency < 1 min; batch < 15 min)  
- Power BI dashboards with time trends and heatmaps  

---

## 🏗️ System Architecture

![System Architecture](https://github.com/user-attachments/assets/8c2d29ea-aee0-45f8-a55b-b8dcef7ada49)

---

## 🗃️ Data Warehouse Design
Star schema includes fact and dimension tables for:
- Crashes  
- People  
- Vehicles
  
![DWH_Traffic drawio](https://github.com/user-attachments/assets/19b9860b-70bd-45c6-bc26-9fc57ea2eceb)

---

## 🛠️ Tools & Technologies
- **ETL**: SQL Server Integration Services (SSIS)  
- **Streaming**: Apache Kafka, PySpark  
- **Visualization**: Power BI, Power BI Service  
- **Others**: Docker, Zookeeper, Streamlit  

---

## 💻 Installation Guide

### 🖥️ Requirements
- OS: Windows 11 Pro / Ubuntu 22.04  
- CPU: Intel i5 / AMD Ryzen 5  
- RAM: 16GB  
- SSD: 512GB  

### 🧰 Required Tools
- SQL Server 2022  
- Visual Studio (with SSIS)  
- Power BI Desktop  
- Docker Desktop  
- Anaconda / VS Code  

### 📦 Python Packages
```bash
pip install pyspark streamlit tabulate
```

### 🐳 Docker & Kafka Setup
1. Start Kafka & Zookeeper in Docker
2. Create Kafka topic, producer, and consumer
3. Use Power BI streaming dataset + REST API to stream data

### 🗃️ ETL & DWH Setup
1. Load People, Crashes, and Vehicles using SSIS packages
2. Populate fact tables (e.g., FC_Crash)
3. Schedule with SQL Server Agent


---

## 🛰️ Data Flow Clarification

- The streaming part of the project focuses on capturing critical accident data — specifically **crash location** and **number of units involved** — which is sent to the Chicago Police Department by emergency      services. This data is ingested in real-time and loaded into the **operational database** (`Traffic_Crashes`), which is a part of our Crash Management System.

- This real-time data is also visualized live in a **Power BI Service dashboard**, featuring a **map showing the crash location**, along with **the number of units involved** and **timestamp of the incident**,     allowing emergency responders and analysts to monitor incidents as they happen.

- The remaining crash report details are entered manually using a **custom-built Desktop Data Entry App**. Once a report is finalized, the `Traffic_Crashes` database is loaded into the **Data Warehouse (DWH)**     on a **weekly schedule**, ensuring that all insights and reports remain up to date and accurate.

---

## 📊 Dashboard Previews

### 🔴 Real-time Dashboard (Power BI Service)
This dashboard displays crash events as they occur, showing the **number of units involved**, **crash timestamp**, and **exact location** on a live map.

![Real Time Crash Location Dashboard](https://github.com/user-attachments/assets/b6d776c2-f3c2-4ba1-8619-7f95fe3ac5ef)

### 🟡 Analytical Dashboard
The Power BI Analytical Dashboard provides deep insights into crash patterns in Chicago, including trends by **road conditions**, **weather**, **lighting**, **time of day**, and **driver behavior**, as well as a **heatmap of crash density**.

![Crash Scope Dashboard](https://github.com/user-attachments/assets/e606a46e-7e86-4c65-b1fe-36a71c424f69)

---

## 🧑‍💻 Contributors
- **Bassant Hossam Mohamed**   
- Abdelrahman El-Sayed Nagib  
- Farida Nassar Mohamed  
- Rawan Hamdy Helmy  
- **Mahmoud Emad Ali**

