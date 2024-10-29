# Radiat
The Integrated Energy Data Resource (IEDR) is a cloud-based, state-wide data platform developed to support New York's climate goals by 2030. The platform offers a SaaS solution accessible to registered cleantech developers, providing critical data from all eight large utilities operating in New York. Our objective is to streamline the integration and processing of utility and energy data to facilitate better decision-making, reporting, and climate impact analysis.

Problem Statement The IEDR will receive three distinct datasets from each of the five participating utilities:

Network Data: Infrastructure data for feeders, feeder segments, substations, and hosting capacity. Installed DER Data: Information about existing Distributed Energy Resources (DERs) such as solar and energy storage systems. Planned DER Data: Project data for DERs under development or awaiting interconnection. The goal is to visualize all these datasets on an interactive map, showcasing utility feeders along with icons for installed and planned DERs. Additionally, the platform will highlight missing data, provide refresh statistics, and ensure data uniformity across utility sources.

Repository Structure and DevOps Approach To manage our pipeline code and maintain a stable development process, we use a structured SDLC workflow across three environments: Development, Testing, and Production. Our repository organization follows a branch-based structure:

Main Branch: Stable code deployed to production. Development Branch: Ongoing feature development and improvements. Feature Branches: Specific enhancements or bug fixes. DevOps Highlights Continuous Integration (CI): Automated testing for all new commits. Continuous Delivery (CD): Code seamlessly promoted from development to production. Version Control: Use of feature branches and pull requests for controlled merges. Medallion Architecture Design This project employs a medallion architecture with three primary layers: Bronze, Silver, and Gold (Platinum).

Bronze Layer (Raw Data):

Stores raw data ingested from utility files (monthly updates). Example: Circuit data, DER information from Utility 1 & Utility 2. Silver Layer (Cleaned & Processed Data):

Standardizes datasets across utilities, ensuring consistency. Example: Mapping utility-specific fields to a unified schema. Gold/Platinum Layer (Aggregated Data):

Stores production-ready data accessible through API queries. Supports queries like: All feeders with max hosting capacity > X. All DERs (planned and installed) for a specific feeder ID. Data Ingestion Process Monthly Updates: New records are added, and existing records are modified with each update. Data Validation: Detects missing or inconsistent records. API-Ready Integration: Platinum layer enables seamless API queries. Tools and Technologies Used Python: Data processing scripts and automation. AWS (or Databricks): Cloud platform for scalable data pipelines. SQL: Query optimization and data aggregation. GitHub: Version control and collaboration. Getting Started Clone the repository:

bash Copy code https://github.com/zaingithub2301/Radiat cd iedr-data-pipeline Setup virtual environment:

bash Copy code python -m venv venv source venv/bin/activate # For Linux/macOS venv\Scripts\activate # For Windows Install dependencies:

bash Copy code pip install -r requirements.txt Run data ingestion scripts:

bash Copy code python ingest_data.py --utility=Utility1 --month=202310 API Usage Get feeders with hosting capacity > X: GET /api/feeders?max_capacity=X

Get all DERs for a feeder ID: GET /api/der?feeder_id=FEEDER123

Best regards,
Radiat ibrahim
