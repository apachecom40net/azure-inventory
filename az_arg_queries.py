ARG_ALL_VMS = """
    Resources
    | where type == "microsoft.compute/virtualmachines"
    | extend vmSize = tostring(properties.hardwareProfile.vmSize)
    | summarize count() by vmSize
    | order by count_ desc
"""

ARG_ALL_RUNNING_VMS = """
    resources
    | where type == "microsoft.compute/virtualmachines"
    | where properties.extended.instanceView.powerState.code == "PowerState/running"
    | summarize count() by tostring(properties.hardwareProfile.vmSize)
    | order by count_ desc
"""

ARG_AKS_CLUSTERS = """
    Resources
    | where type == "microsoft.containerservice/managedclusters"
    | extend agentPools = parse_json(properties.agentPoolProfiles)
    | mv-expand agentPools
    | extend vmSize = tostring(agentPools.vmSize)
    | summarize totalClusters = dcount(name), totalAgentPools = count(), vmSizeCount = count() by vmSize
    | order by vmSizeCount desc
"""

ARG_CONTAINERS_GROUP_TOTAL = """
    Resources
    | where type == "microsoft.containerinstance/containergroups"
    | extend containers = parse_json(properties.containers)
    | mv-expand containers
    | extend 
        name = tostring(name),
        cpu = toreal(containers.properties.resources.requests.cpu),
        memory = toreal(containers.properties.resources.requests.memoryInGb)
    | summarize 
        totalInstances = count(), 
        totalCPU = sum(cpu), 
        totalMemoryGB = sum(memory)
"""

ARG_PUBLIC_FACING_RESOURCES = """
resources
| where type in ("microsoft.network/loadbalancers", 
                 "microsoft.network/applicationgateways", 
                 "microsoft.network/frontdoors", 
                 "microsoft.network/publicipaddresses")
| where isempty(properties.frontendIPConfigurations) == false
| summarize count() by type
| order by count_ desc
"""

ARG_TOTAL_STORGAE_ACCOUNTS = """
    resources
    | where type == "microsoft.storage/storageaccounts"
    | summarize 
        totalStorageAccounts = count(), 
        TotalPublicStorageAccounts = countif(properties.networkAcls.defaultAction == "Allow")
"""

arg_queries = {
    "ARG_ALL_VMS": ARG_ALL_VMS,
    "ARG_ALL_RUNNING_VMS": ARG_ALL_RUNNING_VMS,
    "ARG_AKS_CLUSTERS": ARG_AKS_CLUSTERS,
    "ARG_CONTAINERS_GROUP_TOTAL": ARG_CONTAINERS_GROUP_TOTAL,
    "ARG_PUBLIC_FACING_RESOURCES": ARG_PUBLIC_FACING_RESOURCES,
    "ARG_TOTAL_STORGAE_ACCOUNTS": ARG_TOTAL_STORGAE_ACCOUNTS
}
