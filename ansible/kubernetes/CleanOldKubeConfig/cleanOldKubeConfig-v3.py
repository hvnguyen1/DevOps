from kubernetes import client, config
from kubernetes.client.rest import ApiException

def delete_custom_resource(api_instance, group, version, plural, name, namespace):
    try:
        api_instance.delete_namespaced_custom_object(
            group, version, namespace, plural, name
        )
        print(f"Deleted {name} in namespace {namespace}")
    except ApiException as e:
        if e.status == 404:
            print(f"{name} not found in namespace {namespace}")
        else:
            print(f"Error deleting {name}: {e}")

def delete_cluster_role(api_instance, name):
    try:
        api_instance.delete_cluster_role(
            name
        )
        print(f"Deleted ClusterRole {name}")
    except ApiException as e:
        if e.status == 404:
            print(f"ClusterRole {name} not found")
        else:
            print(f"Error deleting ClusterRole {name}: {e}")

def delete_cluster_role_binding(api_instance, name):
    try:
        api_instance.delete_cluster_role_binding(
            name
        )
        print(f"Deleted ClusterRoleBinding {name}")
    except ApiException as e:
        if e.status == 404:
            print(f"ClusterRoleBinding {name} not found")
        else:
            print(f"Error deleting ClusterRoleBinding {name}: {e}")

def confirm_action(message):
    response = input(f"{message} (y/n): ").lower()
    return response == 'y'

def delete_all_in_namespace(api_instance, namespace):
    try:
        api_instance.delete_namespace(
            name=namespace,
            body=client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=5)
        )
        print(f"Deleted namespace {namespace}")
    except ApiException as e:
        if e.status == 404:
            print(f"Namespace {namespace} not found. Moving on to the next step.")
        else:
            print(f"Error deleting namespace {namespace}: {e}")
            return  # Abort the script if there is an error during namespace deletion

def main():
    config.load_kube_config()
    v1 = client.CustomObjectsApi()
    rbac_v1 = client.RbacAuthorizationV1Api()
    core_v1 = client.CoreV1Api()

    namespace = "Monitoring"
    confirmation_message = "Are you sure you want to delete"

    # Step 1: Delete everything beneath the "Monitoring" namespace
    try:
        delete_all_in_namespace(core_v1, namespace)
    except ApiException as e:
        if e.status == 404:
            print(f"Namespace {namespace} not found. Moving on to the next step.")
        else:
            print(f"Error deleting namespace {namespace}: {e}")
            return  # Abort the script if there is an error during namespace deletion

    # Step 2: Remove specific components from Roles, ClusterRoles, and ClusterRoleBindings
    roles = ["prometheus-operator"]
    for role in roles:
        if confirm_action(f"{confirmation_message} Role {role} in namespace {namespace}?"):
            delete_cluster_role(rbac_v1, role)

    cluster_roles = ["prometheus-operator"]
    for cluster_role in cluster_roles:
        if confirm_action(f"{confirmation_message} ClusterRole {cluster_role}?"):
            delete_cluster_role(rbac_v1, cluster_role)

    cluster_role_bindings = ["prometheus-operator"]
    for cluster_role_binding in cluster_role_bindings:
        if confirm_action(f"{confirmation_message} ClusterRoleBinding {cluster_role_binding}?"):
            delete_cluster_role_binding(rbac_v1, cluster_role_binding)

    # Step 3: Remove specific CustomResourceDefinitions (CRDs)
    crds = [
        "alertmanagerconfigs.monitoring.coreos.com",
        "alertmanagers.monitoring.coreos.com",
        "podmonitors.monitoring.coreos.com",
        "probes.monitoring.coreos.com",
        "prometheusagents.monitoring.coreos.com",
        "prometheuses.monitoring.coreos.com",
        "prometheusrules.monitoring.coreos.com",
        "scrapeconfigs.monitoring.coreos.com",
        "servicemonitors.monitoring.coreos.com",
        "thanosrulers.monitoring.coreos.com"
    ]
    for crd in crds:
        if confirm_action(f"{confirmation_message} CRD {crd}?"):
            api_instance = client.ApiextensionsV1Api()
            api_instance.delete_custom_resource_definition(crd)

if __name__ == "__main__":
    main()

