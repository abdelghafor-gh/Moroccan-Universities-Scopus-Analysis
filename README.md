# 🌍 Moroccan Universities Scopus Analysis 📊

## 📜 Project Overview

**Moroccan-Universities-Scopus-Analysis** is a data-driven project focused on analyzing academic publications affiliated with  **Moroccan universities and institutes** . The data is sourced from  **Scopus** , covering various document types such as articles, book series, and conference papers, spanning all years up to the present.

### 🎯 Key Objectives

* 📥  **Data Extraction & Transformation** : Analyze documents data exported from Scopus for Moroccan affiliations.
* 🏗️  **Data Modeling** : Build a data warehouse with a star schema, including:
  * **Fact Table** : Documents
  * **Dimension Tables** : Authors, journals, affiliations
* 📊  **Power BI Dashboard** : Develop a rich set of visualizations to explore and analyze publication trends.

---

## 🗂️ Project Structure

```
📁 Moroccan-Universities-Scopus-Analysis/
├── data/                  # Raw and transformed data files
│   ├── raw/               # Raw data files from Scopus
│   └── transformed/       # Transformed data files used for analysis
├── dags/                  # Airflow DAGs for scheduling data pipelines
├── docs/                  # Project documentation
├── notebooks/             # Jupyter notebooks for data exploration & cleaning
├── models/                # Data model and schema definitions
├── dashboards/            # Power BI files (.pbix)
├── mappers/               # json files used for mapping Moroccan universities, affiliations and cities
├── scripts/               # ETL scripts for data transformation
├── reports/               # Exported reports and visualizations
└── README.md              # Project documentation
```

## 📚 Detailed Documentation

Dive deep into our comprehensive documentation! 🤿

### 📖 Available Guides

1. **Data Model Documentation** 🏗️
   - [Data Model Guide](docs/data_model.md)
   - Learn about our star schema design ⭐
   - Understand table relationships 🔄
   - Explore field descriptions 📝

2. **ETL Process Guide** 🔄
   - [ETL Documentation](docs/etl_process.md)
   - Step-by-step pipeline explanation 📋
   - Data transformation details 🔄
   - Error handling procedures 🛠️

3. **Data Directory Guide** 📂
   - [Data Directory Documentation](docs/data_directory.md)
   - Complete data flow timeline ⏱️
   - File organization structure 📁
   - Data quality standards ✨

### 💡 Why Read Our Docs?

- 🎯 Get up to speed quickly
- 🔍 Find answers to common questions
- 🛠️ Troubleshoot effectively
- 🚀 Contribute with confidence
- 📈 Understand data flows

### 🎓 Perfect For:
- New team members 👋
- Contributors 🤝
- Data analysts 📊
- Researchers 🔬

---

## ⚙️ Tech Stack

| Tool/Technology            | Description                                          |
| -------------------------- | ---------------------------------------------------- |
| 🐍**Python**         | Data cleaning, transformation, and preprocessing     |
| 🐘**PostgreSQL**     | Data warehousing and modeling - option 1             |
| ❄️**Snowflake**    | Data warehousing and modeling - option 2             |
| 🔄**Apache Airflow** | Data ingestion and transformation orchestration      |
| 📝**Jupyter**        | Interactive data exploration and transformation      |
| 📈**Power BI**       | Interactive dashboards and advanced visual analytics |
| 📊**Pandas**         | Data manipulation and analysis                       |
| 🛠️**DAX**          | Power BI data analysis expressions                   |

---

## 🗃️ Data Model

Our data model follows a  **star schema** :

* **Fact Table** : Publications (Title, AffiliationId, Document Type, Citations, etc.)
* **Dimensions** :
* Authors (Name, AffiliationId, etc.)
* Journals (Title, Rank, ISSN, etc.)
* Affiliations (Name, City, University)

---

## 📊 Power BI Dashboard

Our interactive Power BI dashboard includes:

* 📊  **Bar Charts** : Publications by year, document type, and top Moroccan universities
* 🌍  **Maps** : Geographical distribution of collaborations
* 🌐  **Network Graphs** : Co-authorship networks and collaboration patterns
* 📉  **Trend Analysis** : Publication trends over the years
* 🔍  **Advanced Filters** : Drill-down capabilities for deep data exploration

#### 🔗 [View Dashboard Demo](#)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Moroccan-Universities-Scopus-Analysis.git
cd Moroccan-Universities-Scopus-Analysis
```

### 2. Set Up the Environment

Make sure you have Python and PostgreSQL installed. Then, create a virtual environment and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Load Data into Database 🗄️

We support two database options: PostgreSQL 🐘 and Snowflake ❄️. Choose your preferred option:

#### Option 1: PostgreSQL Setup 🐘

1. Create a `.env` file with PostgreSQL credentials ⚙️:

   ```env
   DB_TYPE=postgres
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=scopus_analysis
   ```
2. Create the database 📦:

   ```sql
   CREATE DATABASE scopus_analysis;
   ```
3. Initialize the schema 🏗️:

   ```bash
   python models/init_db.py
   ```

#### Option 2: Snowflake Setup ❄️

1. Create a `.env` file with Snowflake credentials ⚙️:

   ```env
   DB_TYPE=snowflake
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_ACCOUNT=your_account
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=SCOPUS_ANALYSIS
   SNOWFLAKE_SCHEMA=PUBLIC
   ```
2. Initialize Snowflake Schema 📦:

   ```sql
   -- Create the database
   CREATE DATABASE SCOPUS_ANALYSIS_DB;

   -- Create the data warehouse
   CREATE WAREHOUSE SCOPUS_ANALYSIS_WH;
   ```
3. Initialize the schema 🏗️:

   ```bash
   python models/init_db.py
   ```

The schema will be automatically created based on SQLAlchemy models defined in `models/schema.py`. After setup, run the ETL pipeline 🔄:

#### Run ETL Pipeline

```bash
python scripts/run_pipeline.py
```

### 4. Open Power BI Dashboard

* Open the `.pbix` file located in the `dashboards/` folder.
* Refresh the data to load the latest from your PostgreSQL database.

---

## 📅 Roadmap

* [X] Data extraction and cleaning
* [X] Data model design and implementation
* [X] Development of Power BI dashboard
* [ ] Incorporate machine learning for predictive analytics
* [ ] Expand analysis to include other North African universities

---

## 🚁 Apache Airflow Implementation

Our ETL pipeline is orchestrated using Apache Airflow, providing robust scheduling and monitoring capabilities! 🎯

### 🐳 Docker Setup

We use Docker to run Airflow in a containerized environment. The setup is located in the `airflow-docker/` directory:

```bash
📁 airflow-docker/
├── .env                      # Environment variables
├── Dockerfile                # Dockerfile for Airflow container
├── requirements-airflow.txt  # Airflow dependencies
└── docker-compose.yaml       # Docker compose configuration
```

### 🚀 Getting Started with Airflow

1. **Start Airflow Services** 🛫

```bash
cd airflow-docker
docker-compose up -d
```

2. **Access Airflow UI** 🖥️
   - Open your browser and navigate to `http://localhost:8080`
   - Default credentials:
     - Username: `admin`
     - Password: `admin`

### 📊 Available DAGs

1. **`scopus_etl_dag`** 🔄
   - Main ETL pipeline for Scopus data processing
   - Steps:
     1. 📁 Create directories
     2. 🔄 Translate affiliations
     3. 🗺️ Map cities
     4. 🏛️ Process affiliations
     5. 📚 Transform journal data
     6. 📊 Run ETL process
     7. 🔄 Combine transformed files
     8. 🏗️ Build fact and dimensions
     9. 🗄️ Initialize database
     10. 📥 Load data to PostgreSQL

### 🔍 Monitoring & Management

- **DAG View** 📋: Monitor task status and dependencies
- **Tree View** 🌳: Visualize task hierarchy
- **Graph View** 📊: Interactive task dependency graph
- **Task Instance Details** 🔎: View logs and task execution details

### ⚙️ Configuration

The Airflow setup includes:

- 🐳 **Docker Services**:
  - Airflow Webserver
  - Airflow Scheduler
  - PostgreSQL (Airflow metadata)

- 🔐 **Environment Variables**:
  - Database connections
  - Airflow configuration
  - Custom settings

### 🛠️ Troubleshooting

Common solutions for Airflow issues:

1. **Logs** 📝
   ```bash
   docker-compose logs -f webserver
   ```

2. **Reset Environment** 🔄
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

3. **Check Container Status** 🔍
   ```bash
   docker-compose ps
   ```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Create a pull request

---

## 👥 Contributors

Thanks to the amazing people who have contributed to this project! 💪🚀

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/abdelghafor-gh">
        <img src="https://avatars.githubusercontent.com/abdelghafor-gh" width="80px;" alt="Your Name"/>
        <br/>
        <sub><b>Abdelghafor Elgharbaoui</b></sub>
      </a>
      <br/>
      💻 📊
    </td>
    <td align="center">
      <a href="https://github.com/aymane-maghouti">
        <img src="https://avatars.githubusercontent.com/aymane-maghouti" width="80px;" alt="Contributor 2"/>
        <br/>
        <sub><b>Aymane Maghouti</b></sub>
      </a>
      <br/>
      📈 📖
    </td>
    <td align="center">
      <a href="https://github.com/hamzaae">
        <img src="https://avatars.githubusercontent.com/hamzaae" width="80px;" alt="Contributor 3"/>
        <br/>
        <sub><b>Hamza Motassim</b></sub>
      </a>
      <br/>
      🔍 🛠️
    </td>
    <td align="center">
      <a href="https://github.com/nexossama">
        <img src="https://avatars.githubusercontent.com/nexossama" width="80px;" alt="Colleague 3"/> <br/>
        <sub><b>Ossama Outmani</b></sub>
      </a>
      <br/>
      🗂️ 🔬 </td>
  </tr>
</table>

---

## 📧 Contact

If you have any questions or suggestions, feel free to reach out to any of us!

### Team Members

**Name**: Abdelghafor Elgharbaoui  
**Email**: [abdelghaforelgharbaoui@gmail.com](mailto:abdelghaforelgharbaoui@gmail.com)  
**LinkedIn**: [Abdelghafor's LinkedIn](https://www.linkedin.com/in/abdelghafor-elgharbaoui/)

**Name**: Aymane Maghouti  
**Email**: [aymanemaghouti16@gmail.com](mailto:aymanemaghouti16@gmail.com)  
**LinkedIn**: [Aymane's LinkedIn](https://www.linkedin.com/in/aymane-maghouti/)

**Name**: Hamza Motassim  
**Email**: [motassimhamza99@gmail.com](mailto:motassimhamza99@gmail.com)  
**LinkedIn**: [Hamza's LinkedIn](https://www.linkedin.com/in/hamza-motassim-a56801219/)

**Name**: Ossama Outmani  
**Email**: [ossamaoutmani@gmail.com](mailto:ossamaoutmani@gmail.com)  
**LinkedIn**: [Ossama's LinkedIn](https://www.linkedin.com/in/ossama-outmani/)


---
