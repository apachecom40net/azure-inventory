import json
import pandas as pd
import subprocess
from rich import print
from vm_sizes_data import json_vm_size_data
from collections import Counter

# just for debug
from tabulate import tabulate


def print_all_vms(data):
    
    if data.empty: 
        print("[bold red]No Virtual Machines found in the provided subscription.[/bold red]")
        return None
      
    print("\n\n[bold green]=== Summary of Resources on Virtual Machines ===[/bold green]\n")
    
    cpu_data = json.loads(json_vm_size_data)
    cpus_df = pd.DataFrame(cpu_data)
    
    merged_df = pd.merge(data, cpus_df, on="vmSize", how="left")
    merged_df.dropna(inplace=True)
    merged_df["Count of vCPUs"] = merged_df["count_"] * merged_df["vCPU"] 
    merged_df["Total VMs"] = merged_df["vmSize"].count()
    
    output_data = [
        [merged_df["vmSize"].count(), merged_df["Count of vCPUs"].sum()]
    ]
    output_df = pd.DataFrame(output_data, columns=["Total VMs", "Total vCPUs"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return output_df

            
    
def print_all_running_vms(data):
    
    if data.empty:
        print("[bold red]No Running Virtual Machines found in the provided subscription.[/bold red]")
        return None
    # Just for Debug
    
    print("\n\n[bold green]=== Summary of Resources on Running Virtual Machines ===[/bold green]\n")
    
    cpu_data = json.loads(json_vm_size_data)
    cpus_df = pd.DataFrame(cpu_data)
    
    # Rename Field to match the CPU Data
    data.rename(columns={"properties_hardwareProfile_vmSize": "vmSize", "count_": "count"}, inplace=True)
    
    # Now merge the dataframes
    
    merged_df = pd.merge(data, cpus_df, on="vmSize", how="left")
    merged_df["count_vCpus"] = merged_df["count"] * merged_df["vCPU"]
    
    output_data = [
        [merged_df["vmSize"].count() , merged_df["count_vCpus"].sum() ]
    ]
    
    output_df = pd.DataFrame(output_data, columns=["Total VMs", "Total vCPUs"])
    
    # # Just for Debug       
    # print(tabulate(cpus_df.head(10), headers="keys", tablefmt="fancy_grid", showindex=False))
    # print(tabulate(data.head(10), headers="keys", tablefmt="fancy_grid", showindex=False))
    # print(tabulate(merged_df.head(10), headers="keys", tablefmt="fancy_grid", showindex=False))
   
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return output_df
    
     
def print_aks_resources(data):
    
    if data.empty:
        print("\n\n[bold red]No AKS Clusters found in the provided subscription.[/bold red]")
        return None
    
    
    print("\n\n[bold green]=== Summary of AKS Resources ===[/bold green]\n")
    cpu_data = json.loads(json_vm_size_data)
    cpus_df = pd.DataFrame(cpu_data)
    
    merged_df = pd.merge(data, cpus_df, on="vmSize", how="left")
    merged_df.dropna(inplace=True)
    
    merged_df["count_vCPUs"] = merged_df["totalClusters"] * merged_df["vmSizeCount"] * merged_df["vCPU"]    
    merged_df["count_VMs"] = merged_df["totalClusters"] * merged_df["vmSizeCount"]    
    
    
    output_data = [
        [ 
         merged_df["totalClusters"].sum(), 
         merged_df["count_VMs"].sum(),
         merged_df["count_vCPUs"].sum()
        ]
    ]
    output_df = pd.DataFrame(output_data, columns=["Total Clusters", "Total VMs", "Total vCPUs on VMs"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return output_df
    
def print_container_instances_groups_vms(data):
    
    if data.empty:
        print("\n\n[bold red]No Azure Container Instances found in the provided subscription.[/bold red]")
        return None
    
    print("\n\n[bold green]=== Summary of Azure Container Instances Resources ===[/bold green]\n")
    
    output_data = [
        [
            data["totalInstances"].sum(),
            data["totalCPU"].sum(),
        ]
    ]
    
    output_df = pd.DataFrame(output_data, columns=["Total Instances", "Total CPU on Instances"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return output_df
    
    
def print_public_facing_resources(data):
    
    if data.empty:
        print("\n\n[bold red]No Public Facing Resources found in the provided subscription.[/bold red]")
        return None
    
    # Just for Deb
    
    print("\n\n[bold green]=== Summary of Public Facing Resources ===[/bold green]")
    print("[italic dim]Load Balancers, Front Door, Public IPs, Application Gateways[/italic dim]\n")
    
    outpput_data = [
        [data["count_"].sum()]
    ]    
    output_df = pd.DataFrame(outpput_data, columns=["Total Public Facing Resources"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))   
    return output_df

#TODO: Add more details to the output    
def print_azure_storage_resources(data):
    
    if data.empty:
        print("\n\n[bold red]No Azure Storage Accounts found in the provided subscription.[/bold red]")
        return None
    # Just for Debug
    
    
    print("\n\n[bold green]=== Summary of Azure Storages Resources ===[/bold green]\n")
    
    data["Percentage of Public Storage Accounts"] = (
        data["TotalPublicStorageAccounts"] / data["totalStorageAccounts"] * 100
    ).round(2)
    output_data = [
        [
            data["totalStorageAccounts"].sum(),
            data["TotalPublicStorageAccounts"].sum(),
            data["Percentage of Public Storage Accounts"].sum()
        ]
    ]
    output_df = pd.DataFrame(output_data, columns=["Total Storage Accounts", "Total Public Storage Accounts", "%"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    return output_df


def print_azure_identity_info():
    
    """
    Retrieves all Azure role assignments using Azure CLI,
    groups them by role name, and returns a Pandas DataFrame
    with counts sorted by number of assignments.

    Returns:
        pd.DataFrame: DataFrame with columns ['Role Name', 'Assignment Count']
    """
    result = subprocess.run(
        ['az', 'role', 'assignment', 'list', '--all'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Azure CLI error: {result.stderr}")

    assignments = json.loads(result.stdout)
    role_names = [a['roleDefinitionName'] for a in assignments]
    role_counts = Counter(role_names)

    df = pd.DataFrame(role_counts.items(), columns=['Role Name', 'Assignment Count'])
    df.sort_values(by='Assignment Count', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Get the Result
    high_rights_roles_set = {
        "Contributor",
        "Managed Application Operator Role",
        "Reader",
        "Network Contributor",
        "User Access Administrator",
        "Owner",
        "Key Vault Reader",
    }
    
    # hpr = df[df["Role Name"].isin(high_rights_roles_set)]["Assignment Count"].sum(),  # High Rights Roles
    # tr  = df["Assignment Count"].sum(),  # Total Assignments,
    
    output_data = [[
        df[df["Role Name"].isin(high_rights_roles_set)]["Assignment Count"].sum(),  # High Rights Roles]
        df["Assignment Count"].sum(),  # Total Assignments,
        round(df[df["Role Name"].isin(high_rights_roles_set)]["Assignment Count"].sum() / df["Assignment Count"].sum() * 100, 2)  # Percentage
    ]]
    
    print("\n\n[bold green]=== Summary of Identities ===[/bold green]\n")
    print("""
            [italic dim]
                High Rights Roles:
                 * Contributor,
                 * Managed Application Operator Role
                 * Reader
                 * Network Contributor
                 * User Access Administrator
                 * Owner
                 * Key Vault Reader
            [/italic dim]\n
          """)
          
    
    output_df = pd.DataFrame(output_data, columns=["High Rights Roles", "Total Roles", "%"])
    print(tabulate(output_df, headers="keys", tablefmt="fancy_grid", showindex=False))
    print ("\n\n\n")
    
    return output_df