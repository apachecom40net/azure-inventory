from datetime import datetime 
import pandas as pd

# Fancy Libraries
import pyfiglet # Font Art Library
import typer
from yaspin import yaspin

from query_utils import AzureARGQueryHelper

## Final Dependencies
from az_arg_queries import arg_queries
from format_output import *
## Final Depmendencies


def main(
        subscription: str = typer.Option(..., prompt=True),
):
    
    print(pyfiglet.figlet_format("Azure Resource Inventory\n by Latam BDE Team"))
    
    results = {}
    
    # First, just Iterate queries
    # Use helper to execute queries
    helper = AzureARGQueryHelper([subscription])
    for name, query in arg_queries.items():
        with yaspin(text=f"Executing query: {name}", color="green") as spinner:
            try:
                data = helper.execute_query(name)
                df = pd.DataFrame(data)
                results[name] = df
                spinner.ok("✔")
            except Exception as e:
                spinner.fail(f"✘ Error: {str(e)}")
         
    # Print results in a table format and keep dataframes to export as CSV later, if required
    
    df_vms         = print_all_vms(results["ARG_ALL_VMS"])
    df_running_vms = print_all_running_vms(results["ARG_ALL_RUNNING_VMS"])
    df_aks         = print_aks_resources(results["ARG_AKS_CLUSTERS"] )
    df_aci         = print_container_instances_groups_vms(results["ARG_CONTAINERS_GROUP_TOTAL"])
    df_pfr         = print_public_facing_resources(results["ARG_PUBLIC_FACING_RESOURCES"])
    df_azs         = print_azure_storage_resources(results["ARG_TOTAL_STORGAE_ACCOUNTS"])
    df_identities  =  print_azure_identity_info()

    if True:
        columns = [
            "subscription_id",
            "total_vms", 
            "total_vcpus", 
            "total_running_vms", 
            "total_running_vcpus", 
            "total_aks_clusters", 
            "total_aks_vms", 
            "total_aks_vcpus", 
            "total_aci_instances", 
            "total_aci_vcpus", 
            "total_pfr",                        # Public Facing Resources 
            "total_sa",                         # Total Storage Accounts
            "total_psa",                        # Total Public Storage Accounts
            "total_hri,",
            "total_identities"]
        
        data = [[
            subscription,
            df_vms.at[0, "Total VMs"] if df_vms is not None else 0,
            df_vms.at[0, "Total vCPUs"] if df_vms is not None else 0,
            df_running_vms.at[0, "Total VMs"] if df_running_vms is not None else 0,
            df_running_vms.at[0, "Total vCPUs"] if df_running_vms is not None else 0,
            df_aks.at[0, "Total Clusters"] if df_aks is not None else 0,
            df_aks.at[0, "Total VMs"] if df_aks is not None else 0,
            df_aks.at[0, "Total vCPUs on VMs"] if df_aks is not None else 0,
            df_aci.at[0, "Total Instances"] if df_aci is not None else 0,
            df_aci.at[0, "Total CPU on Instances"] if df_aci is not None else 0,
            df_pfr.at[0, "Total Public Facing Resources"] if df_pfr is not None else 0,
            df_azs.at[0, "Total Storage Accounts"] if df_azs is not None else 0,
            df_azs.at[0, "Total Public Storage Accounts"] if df_azs is not None else 0,
            df_identities.at[0, "High Rights Roles"] if df_identities is not None else 0,
            df_identities.at[0, "Total Roles"] if df_identities is not None else 0,
        ]]  
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"azure_inventory_report_{subscription}_{timestamp}.csv"
        csv_df = pd.DataFrame(data, columns=columns)
        csv_df.to_csv(filename, index=False)
          
if __name__ == "__main__":
    typer.run(main)