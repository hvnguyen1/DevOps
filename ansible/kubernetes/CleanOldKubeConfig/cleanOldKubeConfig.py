#!/usr/bin/python3

from kubernetes import client, config
import re

def list_cluster_roles_matching_pattern(pattern):
    config.load_kube_config()
    api = client.RbacAuthorizationV1Api()

    try:
        matching_cluster_roles = []
        cluster_roles = api.list_cluster_role().items
        for cluster_role in cluster_roles:
            if re.match(pattern, cluster_role.metadata.name):
                matching_cluster_roles.append(cluster_role)
        return matching_cluster_roles
    except client.rest.ApiException as e:
        print(f"Error listing ClusterRoles: {e}")
        return []

def delete_cluster_roles(cluster_roles):
    config.load_kube_config()
    api = client.RbacAuthorizationV1Api()

    for cluster_role in cluster_roles:
        try:
            api.delete_cluster_role(name=cluster_role.metadata.name)
            print(f"ClusterRole '{cluster_role.metadata.name}' deleted successfully")
        except client.rest.ApiException as e:
            print(f"Error deleting ClusterRole '{cluster_role.metadata.name}': {e}")

# Usage example
#pattern = r"your-regex-pattern"
pattern = re.compile(r'blackbox-exporter|kube-state-metrics|node-exporter|prometheus-k8s|v1beta1.metrics|prometheus-adapter', re.IGNORECASE)

# List ClusterRoles that match the pattern
matching_cluster_roles = list_cluster_roles_matching_pattern(pattern)

if matching_cluster_roles:
    print(f"Matching ClusterRoles:")
    for cluster_role in matching_cluster_roles:
        print(f"- {cluster_role.metadata.name}")

    confirmation = input("Do you want to delete these ClusterRoles? (yes/no): ")
    if confirmation.lower() == "yes":
        delete_cluster_roles(matching_cluster_roles)
    else:
        print("No ClusterRoles were deleted.")
else:
    print("No matching ClusterRoles found.")




