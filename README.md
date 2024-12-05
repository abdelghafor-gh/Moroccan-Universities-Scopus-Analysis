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
├── notebooks/             # Jupyter notebooks for data exploration & cleaning
├── models/                # Data model and schema definitions
├── dashboards/            # Power BI files (.pbix)
├── mappers/               # json files used for mapping Moroccan universities, affiliations and cities
├── scripts/               # ETL scripts for data transformation
├── reports/               # Exported reports and visualizations
└── README.md              # Project documentation
```

---

## ⚙️ Tech Stack

| Tool/Technology        | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| 🐍**Python**     | Data cleaning, transformation, and preprocessing     |
| 🐘**PostgreSQL** | Data warehousing and modeling                        |
| ❄️**Snowflake** | Data warehousing and modeling                        |
| 🔄**Apache Airflow**    | Data ingestion and transformation orchestration      |
| 📝**Jupyter**    | Interactive data exploration and transformation        |
| 📈**Power BI**   | Interactive dashboards and advanced visual analytics |
| 📊**Pandas**     | Data manipulation and analysis                       |
| 🛠️**DAX**      | Power BI data analysis expressions                   |

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

 **Name** : Abdelghafor Elgharbaoui
 **Email** : [abdelghaforelgharbaoui@gmail.com]()
 **LinkedIn** : [Abdelghafor&#39;s LinkedIn](https://linkedin.com/in/personAprofile)

 **Name** : Aymane maghouti
 **Email** : [aymanemaghouti16@gmail.com]()
 **LinkedIn** : [Aymane&#39;s LinkedIn](https://linkedin.com/in/personBprofile)

 **Name** : Hamza Motassim
 **Email** : [motassimhamza99@gmail.com]()
 **LinkedIn** : [Hamza&#39;s LinkedIn](https://linkedin.com/in/personCprofile)

 **Name** : Ossama Outmani
 **Email** : [ossamaoutmani@gmail.com]()
 **LinkedIn** : [Ossama&#39;s LinkedIn](https://linkedin.com/in/personDprofile)
nkedIn](https://linkedin.com/in/personCprofile)

 **Name** : Ossama Outmani
 **Email** : [ossamaoutmani@gmail.com]()
 **LinkedIn** : [Ossama&#39;s LinkedIn](https://linkedin.com/in/personDprofile)
nkedIn](https://linkedin.com/in/personCprofile)

 **Name** : Ossama Outmani
 **Email** : [ossamaoutmani@gmail.com]()
 **LinkedIn** : [Ossama&#39;s LinkedIn](https://linkedin.com/in/personDprofile)

---
