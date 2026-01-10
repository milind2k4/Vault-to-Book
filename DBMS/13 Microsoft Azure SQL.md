Links: [[00 DBMS]]
___
# Microsoft Azure SQL
#case_study

**Azure SQL Database** is a fully managed Platform as a Service (PaaS) database engine that handles most of the database management functions such as upgrading, patching, backups, and monitoring without user involvement.

## Architecture (Control Plane vs Data Plane)

Azure SQL separates the management layer from the data layer to ensure high availability and scalability.

- **Control Plane**: Manages deployment, health monitoring, failover, and billing. It acts as the "Brain".
- **Data Plane**: Handles the actual user queries and data storage. It consists of the SQL Server engine nodes.

## Deployment Models

Choose the right level of isolation and resource sharing.

| Model                | Description                                                                                      | Best For                                                               |
| :------------------- | :----------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| **Single Database**  | A fully isolated database with its own set of resources (CPU, Memory).                           | New apps, microservices, predictable workloads.                        |
| **Elastic Pool**     | A collection of databases sharing a _pool_ of resources. Cost-effective for unpredictable usage. | SaaS apps with many tenants (e.g., 1000 databases with low avg usage). |
| **Managed Instance** | A nearly 100% compatible SQL Server instance. Supports cross-database queries, SQL Agent, CLR.   | Lift-and-shift migrations from on-premise SQL Server.                  |

## Purchasing Models & Service Tiers

### Purchasing Models

1.  **DTU (Database Transaction Unit):** A bundled measure of CPU, Memory, and IO. Simple, pre-configured performance.
2.  **vCore (Virtual Core):** Independent scaling of Compute and Storage. More flexibility and control (like choosing your own server specs).

### Service Tiers

| Tier                  | Description                                                           | Storage                          | HA/DR                    |
| :-------------------- | :-------------------------------------------------------------------- | :------------------------------- | :----------------------- |
| **General Purpose**   | Budget-friendly. Separates compute from storage (Azure Blob Storage). | Remote Storage (Higher Latency)  | 1 Replica                |
| **Business Critical** | High performance. Local SSD storage attached to the compute node.     | Local SSD (Low Latency)          | 3 Replicas + 1 Read-Only |
| **Hyperscale**        | Limitless scale. Storage grows automatically up to 100TB.             | Distributed Storage Architecture | Rapid Scale-out          |

## High Availability & Disaster Recovery

Azure SQL guarantees 99.99% to 99.995% availability.

- **Active Geo-Replication:** Creates readable secondary databases in different Azure regions. If the primary region fails, you can failover to a secondary.
- **Auto-Failover Groups:** Automatically manages replication and failover of a group of databases to another region.
- **Point-in-Time Restore (PITR):** Restore the database to _any second_ in the past (up to 35 days) to recover from accidental data deletion.

## Security Features (The "Defense in Depth" Strategy)

1.  **Network Security:**
    - **Firewall Rules:** Allow traffic only from specific IPs.
    - **VNET Integration:** Private connection within Azure.
2.  **Access Management:**
    - **Azure Active Directory (AAD):** Centralized identity management (MFA, SSO).
3.  **Data Protection:**
    - **TDE (Transparent Data Encryption):** Encrypts data _at rest_ (on disk).
    - **TLS:** Encrypts data _in transit_.
    - **Always Encrypted:** Encrypts sensitive data (like credit cards) _in use_ (client-side encryption). The DB engine never sees the plaintext.
4.  **Advanced Threat Protection:**
    - Detects SQL Injection, anomalous login attempts, and potential vulnerabilities.

## Intelligent Features

- **Automatic Tuning:** The AI analyzes your queries and automatically:
  - Creates missing indexes.
  - Drops unused indexes.
  - Fixes query plan regressions.
- **Intelligent Query Processing:** Optimizes query execution plans based on runtime data.

## Comparison: Azure SQL vs SQL Server (On-Premises)

| Feature           | Azure SQL (PaaS)                                 | SQL Server (On-Premises)                     |
| :---------------- | :----------------------------------------------- | :--------------------------------------- |
| **Management**    | Fully Managed (Auto-patching, Backups)           | Manual (You manage OS, patches, backups) |
| **CapEx vs OpEx** | OpEx (Pay-as-you-go)                             | CapEx (Buy hardware/licenses upfront)    |
| **Version**       | Always the latest stable version ("Versionless") | Specific versions (2019, 2022)           |
| **OS Access**     | No OS access                                     | Full OS control                          |
