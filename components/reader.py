#!/usr/bin/env python
"""Module responsible for all the input reading and validation."""

import sys
import os
import json
import yaml
from components import analyze_vulnerabilities_version_1 as aux_vul

def validate_command_line_input(arguments):
    """This function validates the command line user input."""
    print("Command-line input validation...\n")

    is_valid = True

    # Check if the user has entered right number of arguments.
    if len(arguments) != 2:
        print("Incorrect number of arguments.")
        is_valid = False

    # Check if the specified folder exists.
    if is_valid:
        if not os.path.exists(arguments[1]):
            print("The entered example folder name does not exist.")
            is_valid = False

    # Check if there is a docker-compose.yml file in the specified folder.
    if is_valid:
        content = os.listdir(arguments[1])
        if "docker-compose.yml" not in content:
            print("docker-compose.yml is missing in the folder "+arguments[1])
            is_valid = False

    return is_valid

def validate_config_file():
    """This function validates the config file content."""

    print("Config file content validation...\n")

    is_valid = True
    config_file = read_config_file()

    # Check if the main keywords are present in the config file.
    main_keywords = ["attack-vector-folder-path",
                     "examples-results-path",
                     "mode",
                     "labels_edges",
                     "labels_edges_number",
                     "generate_graphs",
                     "show_n_vuls_per_edge",
                     "n_vuls_per_edge"]

    for main_keyword in main_keywords:
        if main_keyword not in config_file.keys():
            print("'"+main_keyword+"' keyword is missing in the config file.")
            is_valid = False

    # Check if the mode keyword has the right values
    if is_valid:
        config_mode = config_file["mode"]
        if config_mode != "offline" and config_mode != "online":
            is_valid = False
            print("Value: "+ \
                  config_mode + \
                  " is invalid for keyword mode")
            sys.exit(0)

        # Checks if clairctl has been installed.
        elif config_mode == "online":
            print("Checking if clairctl has been installed")

            home = os.path.expanduser("~")
            os.path.exists(os.path.join(home,
                                        "golang"
                                        "go",
                                        "bin",
                                        "src",
                                        "github.com",
                                        "jgsqware",
                                        "clairctl"))

    # Check if the generate_graphs keyword has the right values
    if is_valid:
        config_mode = config_file["generate_graphs"]
        if config_mode != True and config_mode != False:
            is_valid = False
            print("Value: " + \
                  config_mode + \
                  " is invalid for keyword generate_graphs")
            sys.exit(0)

    # Check if the show_n_vuls_per_edge keyword has the right values
    if is_valid:
        config_mode = config_file["show_n_vuls_per_edge"]
        if config_mode != True and config_mode != False:
            is_valid = False
            print("Value: " + \
                  config_mode + \
                  " is invalid for keyword generate_graphs")
            sys.exit(0)

    # Check if the labels_edges keyword has the right values
    if is_valid:
        config_mode = config_file["labels_edges"]
        if config_mode != "single" and config_mode != "multiple":
            is_valid = False
            print("Value: " + \
                  config_mode + \
                  " is invalid for keyword labels_edges")
            sys.exit(0)
    #TODO complete with n_vuls_per_edge and labels_edges_number

    return is_valid

def check_priviledged_access(mapping_names, example_folder_path):
    """Checks if a container has the privileged flag."""
    docker_compose = read_docker_compose_file(example_folder_path)
    services = docker_compose["services"]
    priviledged_access = {}
    for service in services:
        if "privileged" in services[service] and services[service]["privileged"]:
            priviledged_access[mapping_names[service]['image_name']] = True
        elif "volumes" in services[service]:
            volumes = services[service]["volumes"]
            # Check if docker socket is mounted
            socket_mounted = False
            for volume in volumes:
                if "/var/run/docker.sock:/var/run/docker.sock" in volume:
                    socket_mounted = True
            if socket_mounted:
                priviledged_access[mapping_names[service]['image_name']] = True
            else:
                priviledged_access[mapping_names[service]['image_name']] = False
        else:
            priviledged_access[mapping_names[service]['image_name']] = False

    return priviledged_access

def read_attack_vector_files(attack_vector_folder_path):
    """It reads the attack vector files."""


    print("WARNING: read_attack_vector_files REMOVED IN THE MEANTIME!!")
    attack_vector_list = []
    return attack_vector_list

    print(attack_vector_folder_path)
    attack_vector_filenames = os.listdir(attack_vector_folder_path)

    # Iterating through the attack vector files.
    print(attack_vector_filenames)
    for attack_vector_filename in attack_vector_filenames:

        # Load the attack vector.
        # print(os.path.join(attack_vector_folder_path, attack_vector_filename))
        if not attack_vector_filename.startswith("nvdcve"):
            print("Not nvdcve {}".format(attack_vector_filename))
            continue
        with open(os.path.join(attack_vector_folder_path, attack_vector_filename)) as att_vec:
            try:
                attack_vector_list.append(json.load(att_vec))
                #print(attack_vector_list[-1])
            except json.JSONDecodeError as je:
                print("WARNING: Unable to load the json file \"{}\"".format(os.path.join(attack_vector_folder_path, attack_vector_filename)))
                continue
    #print("attack vector list -> {}".format(attack_vector_list))
    return attack_vector_list

def read_topology(example_folder_path):
    """Reads the topology .json file."""

    config = read_config_file()
    folder_name = os.path.basename(example_folder_path)
    topology_path = os.path.join(config["examples-results-path"],
                                 folder_name,
                                 "topology.json")

    with open(topology_path) as topology_file:
        topology = json.load(topology_file)

    return topology

def read_vulnerabilities(vulnerabilities_folder_path, containers):
    """This function reads the .json file for the vulnerabilities of a container."""

    vulnerabilities = {}

    for container in containers:
        container_file_name = container.replace("/","_")
        #print(container)

        vulnerabilities_path = os.path.join(vulnerabilities_folder_path,
                                            container_file_name+"-vulnerabilities.json")
        print(vulnerabilities_path)
        if os.path.exists(vulnerabilities_path):
            with open(vulnerabilities_path) as vul_file:
                try:
                    vulnerabilities_container = json.load(vul_file)
                except json.decoder.JSONDecodeError as jde:
                    print(jde)
                    print("WARNING: File {} not in the correct json format".format(vulnerabilities_path))
                    vulnerabilities_container = {}

            aux_vul.filter_full_vulnerabilities(vulnerabilities_container, [("attackVector","NETWORK")])
            #aux_vul.sort_vulnerabilities(vulnerabilities_container)

            vulnerabilities[container] = vulnerabilities_container
    return vulnerabilities

def read_docker_compose_file(example_folder_path):
    """This function is responsible for reading the docker-compose file of the container."""

    with open(os.path.join(example_folder_path, "docker-compose.yml"), "r") as compose_file:
        docker_compose_file = yaml.safe_load(compose_file)

    return docker_compose_file

def read_config_file(old_root_path=""):
    """This function is responsible for reading the config file."""

    with open(os.path.join(old_root_path, "config.yml"), "r") as stream:
        try:
            config_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return config_file

def read_clairctl_config_file(clairctl_home):
    """This function is responsible for reading the clairctl config file."""

    with open(os.path.join(clairctl_home, "clairctl.yml"), "r") as clair_config:
        clair_config = yaml.safe_load(clair_config)
    return clair_config
