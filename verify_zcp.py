import os
import sys
import json
import datetime
from os.path import expanduser

now = datetime.datetime.now()
nowdatetime = now.strftime('%Y%m%d-%H%M%S')

home = expanduser("~")

DIR = home + "/" + nowdatetime

#print(home)


def login(master_ip):
    os.system("cloudctl login -a https://%s:8443 --skip-ssl-validation" % master_ip)


def version_check():
    os.system("kubectl version -o json >> version.json")

    with open('version.json') as json_file:
        json_data = json.load(json_file)

        server_string = json_data["serverVersion"]
        server_version = server_string["minor"]

        os.system("rm -rf version.json")

    return server_version


def get_logs():

    os.system("mkdir -p %s" % DIR)

    os.system(
        "kubectl get images --all-namespaces >> %s/private_docker_registry.log" % DIR)
    os.system("cloudctl catalog charts -s >> %s/helm_chart.log" % DIR)
    os.system("kubectl get ns >> %s/namespaces.log" % DIR)
    os.system("kubectl get pod --all-namespaces >> %s/pod.log" % DIR)
    os.system("kubectl get ds --all-namespaces >> %s/daemonset.log" % DIR)
    os.system("kubectl get deploy --all-namespaces >> %s/deployment.log" % DIR)
    os.system("helm list --tls >> %s/helm_release.log" % DIR)
    os.system("kubectl get job --all-namespaces >> %s/job.log" % DIR)
    os.system("kubectl get cronjob --all-namespaces >> %s/cronjob.log" % DIR)
    os.system("kubectl get sts --all-namespaces >> %s/statefulset.log" % DIR)
    os.system("kubectl get rs --all-namespaces >> %s/replicaset.log" % DIR)
    os.system("kubectl get svc --all-namespaces >> %s/services.log" % DIR)
    os.system("kubectl get ing --all-namespaces >> %s/ingress.log" % DIR)
    os.system("kubectl get cm --all-namespaces >> %s/configmaps.log" % DIR)
    os.system("kubectl get hpa --all-namespaces >> %s/scaling_policies.log" % DIR)
    os.system("kubectl get secrets --all-namespaces >> %s/secrets.log" % DIR)


def count(log):

    file = DIR+"/"+log

    log_file = open(file, 'r')
    line = log_file.read().count("\n")

    log_file.close()

    return line


def status_check():
    version = version_check()
    daemonset()
    deployment(version)
    helm
    job
    statefulset(version)
    replicaset


def daemonset():
    os.system("kubectl get daemonset --all-namespaces -o json > daemonset.json")

    ds_error = 0

    with open('daemonset.json') as json_file:
        json_data = json.load(json_file)

        len_d = len(json_data['items'])

        print("\033[33m%55s\033[0m" % "============ CHECK  Daemonset ============" )

        for i in range(len_d):
            NAME = json_data['items'][i]['metadata']['name']
            DESIRED = json_data['items'][i]['status']['desiredNumberScheduled']
            CURRENT = json_data['items'][i]['status']['currentNumberScheduled']
            READY = json_data['items'][i]['status']['numberReady']
            if READY == 0:
                AVAILABLE = 0
            else:
                AVAILABLE = json_data['items'][i]['status']['numberAvailable']

            if DESIRED == CURRENT == READY == AVAILABLE:
                print("%-60s\033[32m" % NAME),
                print("%s\033[0m" % "READY")
            else:
                print("%-60s\033[31m" % NAME),
                print("%s\033[0m" % "NOT READY")
                ds_error = ds_error+1

    os.system("rm -rf daemonset.json")

    return ds_error


def deployment():
    os.system("kubectl get deployment --all-namespaces -o json > deployment.json")
    deploy_error = 0

    with open('deployment.json') as json_file:
        json_data = json.load(json_file)
        len_d = len(json_data['items'])

        print("\033[33m%55s\033[0m" % "============ CHECK  Deployment ============" )
            
        for i in range(len_d):
            NAME = json_data['items'][i]['metadata']['name']
            DESIRED = json_data['items'][i]['status']['replicas']
            CURRENT = json_data['items'][i]['status']['updatedReplicas']
            READY = json_data['items'][i]['status']['conditions'][0]['status']

            try:
                AVAILABLE = json_data['items'][i]['status']['availableReplicas']
            except:
                AVAILABLE = 0
                
            if DESIRED == CURRENT == AVAILABLE:
                print("%-60s\033[32m" % NAME),
                print("%s\033[0m" % "READY")
            else:
                print("%-60s\033[31m" % NAME),
                print("%s\033[0m" % "NOT READY")
                deploy_error = deploy_error+1

    os.system("rm -rf deployment.json")
    return deploy_error

# def helm():
# def job():
# def statefulset(version):
# def replicaset():

# def result()


# master_ip = raw_input("Cluster Master IP: ")
# login(master_ip)

# server_version = version_check()
#get_logs()

deployment()

# master_ip = raw_input("Cluster Master IP: ")

# os.system("cloudctl login -a https://%s:8443 --skip-ssl-validation" % master_ip)

# now = datetime.datetime.now()
# nowdatetime = now.strftime('%Y%m%d-%H%M%S')

# DIR = "~/zcp-verification/"+nowdatetime
# os.system("mkdir -p %s" % DIR)
