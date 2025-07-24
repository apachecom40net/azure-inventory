# 📘 Azure Inventory

This project helps customers gain visibility into the resources used across their Azure subscriptions and identify key areas that should be prioritized for protection using a CNAPP (Cloud-Native Application Protection Platform) solution.

---

## Report a Bug or New Feature Request

- Report a [🐛 Bug](https://github.com/apachecom40net/azure-inventory/issues/new?template=bug_report.md)
- [✨ New Feature](https://github.com/apachecom40net/azure-inventory/issues/new?template=feature_request.md) Request

---

## 📑 Table of Content

1. [📋 API Used and Required Roles to Execute Azure Inventory Command](#1--api-used-and-required-roles-to-execute-azure-inventory-command)
2. [⚙️ How to Install Azure Inventory Command](#2-%EF%B8%8F-how-to-install-azure-inventory-command)
3. [📌 Usage Instructions](#3--usage-instructions)
4. [💬 Managing Customer Objections](#4--managing-customer-objections)

---

# 1. 📋 API Used and Required Roles to Execute Azure Inventory Command

Azure Resource Graph (ARG) operates entirely at the control plane, not the data plane, **meaning it accesses resource metadata and configuration without interacting with live workloads or sensitive runtime data**. It queries an indexed snapshot of your Azure environment, ensuring high performance and zero impact on production resources. Because it uses **read-only access to metadata**, ARG is **safe** for **use** in **real-time dashboards, automation scripts, or governance audits — even across thousands of resources. This design makes ARG ideal for scalable, fast, and secure visibility into your Azure estate.**

## 🔐 Required Azure Role to Use Azure Resource Graph

To query all resources in a subscription using **Azure Resource Graph**, the minimum role required is:

### ✅ Reader Role

The built-in `Reader` role allows you to:
- View all Azure resources
- Run queries using Azure Resource Graph via Portal, CLI, or PowerShell

#### 📋 Summary

| Role                         | Required for ARG | Scope Needed         | Notes                                                           |
|------------------------------|------------------|-----------------------|-----------------------------------------------------------------|
| **Reader**                   | ✅ Yes           | Subscription / MG     | Minimal required role for querying via ARG                     |
| **Contributor**              | ✅ Yes (includes Reader) | Subscription / MG     | Includes resource creation/modification                        |
| **Owner**                    | ✅ Yes (includes Contributor) | Subscription / MG     | Can manage access (RBAC) as well                               |
| **Resource Graph Contributor** | ✅ Optional      | Custom Scope          | Rarely used; Reader is sufficient in most cases                |


# 2. ⚙️ How to Install Azure Inventory Command

The command-line tool is developed in Python. The installation script automatically installs the Azure CLI, adds the Azure Resource Graph extension, installs all required Python dependencies, and adds the tool to your system PATH to simplify execution from any terminal.

While the tool can be installed and used directly from the Azure Cloud Shell or Azure CLI, it is highly recommended to run it from a dedicated Ubuntu workstation.

Use the following command to install the tool

```sh
curl -sSL https://raw.githubusercontent.com/apachecom40net/azure-inventory/refs/heads/main/azure-inventory-install.sh| sudo bash
```

# 3. 📌 Usage Instructions

## ✨ Design Philosophy & Execution Logic
The tool was designed with **simplicity in mind**. Below are the key usage considerations:

- ✅ Runs on **one subscription at a time by default**
- 📥 To handle **multiple subscriptions**, you can:
  - Pass them as a **comma-separated list**  
    &nbsp;&nbsp;&nbsp;&nbsp;`--subscriptions sub1,sub2,sub3`
  - Or use a **text file** with **one subscription ID per line**  
    &nbsp;&nbsp;&nbsp;&nbsp;`--subscriptions-file path/to/file.txt`
- 📊 The output is always saved in a CSV file, making it easy to import into reporting tools such as Power BI, Excel, or other data analysis platforms.

> ⚠️ Tip: Make sure your account has **Reader role access** to each subscription you query.


## Execution Examples

### Call with a subscription as a Parameter.
```
azure-inventory --subscriptions "********-****-****-****-************"
```

### Call with comma separeted list of subscriptions as a parameter
```
azure-inventory --subscriptions "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa,bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb,cccccccc-cccc-cccc-cccc-cccccccccccc"
```

### Call using Inptu from a file
```
azure-inventory --from-file ./subscriptions.txt
```

## Example of Input File Format [subscriptions.txt]

```
aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb
cccccccc-cccc-cccc-cccc-cccccccccccc
dddddddd-dddd-dddd-dddd-dddddddddddd
```

## 📊 Example of Output Shell Console

```
Running azure-inventory for subscription: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
    _                          ____
   / \    _____   _ _ __ ___  |  _ \ ___  ___  ___  _   _ _ __ ___ ___
  / _ \  |_  / | | | '__/ _ \ | |_) / _ \/ __|/ _ \| | | | '__/ __/ _ \
 / ___ \  / /| |_| | | |  __/ |  _ <  __/\__ \ (_) | |_| | | | (_|  __/
/_/   \_\/___|\__,_|_|  \___| |_| \_\___||___/\___/ \__,_|_|  \___\___|

 ___                      _
|_ _|_ ____   _____ _ __ | |_ ___  _ __ _   _
 | || '_ \ \ / / _ \ '_ \| __/ _ \| '__| | | |
 | || | | \ V /  __/ | | | || (_) | |  | |_| |
|___|_| |_|\_/ \___|_| |_|\__\___/|_|   \__, |
                                        |___/
  _             _          _                    ____  ____  _____
 | |__  _   _  | |    __ _| |_ __ _ _ __ ___   | __ )|  _ \| ____|
 | '_ \| | | | | |   / _` | __/ _` | '_ ` _ \  |  _ \| | | |  _|
 | |_) | |_| | | |__| (_| | || (_| | | | | | | | |_) | |_| | |___
 |_.__/ \__, | |_____\__,_|\__\__,_|_| |_| |_| |____/|____/|_____|
        |___/
 _____
|_   _|__  __ _ _ __ ___
  | |/ _ \/ _` | '_ ` _ \
  | |  __/ (_| | | | | | |
  |_|\___|\__,_|_| |_| |_|


✔ Executing query: ARG_ALL_VMS
✔ Executing query: ARG_ALL_RUNNING_VMS
✔ Executing query: ARG_AKS_CLUSTERS
✔ Executing query: ARG_CONTAINERS_GROUP_TOTAL
✔ Executing query: ARG_PUBLIC_FACING_RESOURCES
✔ Executing query: ARG_TOTAL_STORGAE_ACCOUNTS


=== Summary of Resources on Virtual Machines ===

╒═════════════╤═══════════════╕
│   Total VMs │   Total vCPUs │
╞═════════════╪═══════════════╡
│         111 │          6013 │
╘═════════════╧═══════════════╛


=== Summary of Resources on Running Virtual Machines ===

╒═════════════╤═══════════════╕
│   Total VMs │   Total vCPUs │
╞═════════════╪═══════════════╡
│          73 │          2139 │
╘═════════════╧═══════════════╛


=== Summary of AKS Resources ===

╒══════════════════╤═════════════╤══════════════════════╕
│   Total Clusters │   Total VMs │   Total vCPUs on VMs │
╞══════════════════╪═════════════╪══════════════════════╡
│               11 │          29 │                   80 │
╘══════════════════╧═════════════╧══════════════════════╛


=== Summary of Azure Container Instances Resources ===

╒═══════════════════╤══════════════════════════╕
│   Total Instances │   Total CPU on Instances │
╞═══════════════════╪══════════════════════════╡
│                 1 │                        1 │
╘═══════════════════╧══════════════════════════╛


=== Summary of Public Facing Resources ===
Load Balancers, Front Door, Public IPs, Application Gateways

╒═════════════════════════════════╕
│   Total Public Facing Resources │
╞═════════════════════════════════╡
│                             247 │
╘═════════════════════════════════╛


=== Summary of Azure Storages Resources ===

╒══════════════════════════╤═════════════════════════════════╤═══════╕
│   Total Storage Accounts │   Total Public Storage Accounts │     % │
╞══════════════════════════╪═════════════════════════════════╪═══════╡
│                      446 │                             439 │ 98.43 │
╘══════════════════════════╧═════════════════════════════════╧═══════╛


=== Summary of Identities ===



                High Rights Roles:
                 * Contributor,
                 * Managed Application Operator Role
                 * Reader
                 * Network Contributor
                 * User Access Administrator
                 * Owner
                 * Key Vault Reader



╒═════════════════════╤═══════════════╤═══════╕
│   High Rights Roles │   Total Roles │     % │
╞═════════════════════╪═══════════════╪═══════╡
│                 607 │           725 │ 83.72 │
╘═════════════════════╧═══════════════╧═══════╛


```

## 📊 Example of Output CSV file

> If command is executed in multples subscription, outputs a file per subscription named with the following format.  
>   azure_inventory_report_aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa_YYYYMMDD_HHMMSS.csv

```
subscription_id,total_vms,total_vcpus,total_running_vms,total_running_vcpus,total_aks_clusters,total_aks_vms,total_aks_vcpus,total_aci_instances,total_aci_vcpus,total_pfr,total_sa,total_psa,total_hri,total_identities
aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa,111,6013.0,73,2139,11,29,80,1,1.0,247,446,439,607,725
```


# 4. 💬 Managing Customer Objections

## Objection 1: Does ARG API impact performane of my applications in Production?
## Objection 2: Does az login --use-device-login is safe?
## Objection 3: Does az login --service-principal is safe?
