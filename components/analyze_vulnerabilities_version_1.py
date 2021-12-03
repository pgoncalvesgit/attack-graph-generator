# This file was made in order to better analyze the vulnerabilities files

# imports
import os
import json

vulnerabilities_path = "/folder/attack-graph-generator/examples-results/TeaStore"

keys_to_identify = ["attackComplexity", "privilegesRequired", "userInteraction", "baseScore", "availabilityImpact", "attackVector"]
sort_default_list = ["NONE", "LOW", "MEDIUM", "HIGH"]


def printj(dictionary):
	print(json.dumps(dictionary, indent = 4));

def get_vulnerability_file_names(path):
	return ["{}/{}".format(path,file) for file in os.listdir(path) if "vulnerabilities.json" in file]

def read_vulnerability_file(file_name):
	return json.load(open(file_name, "r"))

def possible_values_for_key(key_to_address, vulnerabilities_description_list):
	possible_values_list = []
	[possible_values_list.append(vul_desc[0][key_to_address]) for vul_desc in vulnerabilities_description_list if vul_desc[0][key_to_address] not in possible_values_list]
	return possible_values_list

def possible_values_for_various_keys(keys_to_address, vulnerabilities_description_list):
	possible_values_dict = dict()
	[possible_values_dict.update({key_to_address : possible_values_for_key(key_to_address, vulnerabilities_description_list)}) for key_to_address in keys_to_address]
	return possible_values_dict

# Defined twice, im tired...
def sort_possible_values_list(keys_to_use, possible_values_dict, reverse=False):
        for key_to_use in keys_to_use:
                possible_values_list = possible_values_dict[key_to_use]
                if key_to_use == 'attackVector' or key_to_use == 'userInteraction':
                        continue
                elif key_to_use == 'baseScore':
                        possible_values_list.sort(reverse = not reverse)
                else:
                        possible_values_list.sort(key=lambda adjective: sort_default_list.index(adjective), reverse = reverse)



file_keys = read_vulnerability_file(get_vulnerability_file_names(vulnerabilities_path)[0])

vulnerabilities_keys = file_keys["vulnerabilities"].keys()

enchrichements_keys = list(file_keys["enrichments"].values())[0][0].keys()

vulnerabilities_described_keys = [vulnerability for vulnerability in enchrichements_keys if vulnerability in set(vulnerabilities_keys)]
description_dict = list(file_keys["enrichments"].values())[0][0]
description_list = [description_dict[vulnerability_key] for vulnerability_key in enchrichements_keys]
possible_values_dict = possible_values_for_various_keys(keys_to_identify, description_list)
sort_possible_values_list(keys_to_identify, possible_values_dict)



# Completly useless with filter_positive_list
# Only the negative makes sense
def get_keys_in_vul_desc(vulnerabilities_description_list, filter_positive_list = [], filter_negative_list = []):
	keys_to_identify = []
	if filter_positive_list:
		[keys_to_identify.append(new_key)
			for vul_desc in vulnerabilities_description_list
			for new_key in vul_desc[0].keys()
				if (new_key in filter_positive_list and new_key not in keys_to_identify)]
	else:
		[keys_to_identify.append(new_key)
			for vul_desc in vulnerabilities_description_list
			for new_key in vul_desc[0].keys()
				if new_key not in (filter_negative_list or keys_to_identify)]
	return keys_to_identify

def invert_vul_dict_based_on_key_value(vul_dict, key_to_use, possible_values):
	new_dict = dict()
	[new_dict.update({possible_value : []}) for possible_value in possible_values]
	for vul_id, vul_desc_dict in vul_dict.items():
		vul_desc_dict = vul_desc_dict[0]
		new_dict[vul_desc_dict[key_to_use]].append(vul_id)
	return new_dict

def invert_vul_dict_based_on_many_keys(vul_dict, keys_to_use, possible_values_dict):
	new_dict = dict()
	[new_dict.update({key_to_use : invert_vul_dict_based_on_key_value(vul_dict,key_to_use,possible_values_dict[key_to_use])})
		for key_to_use in keys_to_use]
	return new_dict

# This sorting is probably really bad down horrible really bad
# I just wanted it to work... sorry
# So here it is
# Availability Impact is not being sorted correctly
sort_default_list = ["NONE", "LOW", "MEDIUM", "HIGH"]
#dict_items([('baseScore', [3.7, 7.5, 6.5, 4.7, 8.8, 5.5, 6.3, 7.8, 5.3, 4.4, 3.1, 5.9, 9.8, 7.4]),
#('attackVector', ['NETWORK', 'LOCAL']), ('userInteraction', ['NONE', 'REQUIRED']), ('attackComplexity', ['HIGH', 'LOW']), ('availabilityImpact', ['NONE', 'HIGH', 'LOW']),
#('privilegesRequired', ['NONE', 'LOW', 'HIGH'])])
def sort_possible_values_list(keys_to_use, possible_values_dict, reverse=False):
	for key_to_use in keys_to_use:
		possible_values_list = possible_values_dict[key_to_use]
		if key_to_use == 'attackVector' or key_to_use == 'userInteraction':
			continue
		elif key_to_use == 'baseScore':
			possible_values_list.sort(reverse = not reverse)
		else:
			possible_values_list.sort(key=lambda adjective: sort_default_list.index(adjective), reverse = reverse)


def sort_vulnerability_key(vul_details, keys_to_use, possible_values_dict, values_dict, reverse=False):
	sort_value = 0
	for key_to_use in keys_to_use:
		current_position = possible_values_dict[key_to_use].index(vul_details[key_to_use])
		sort_value += possible_values_dict[key_to_use].index(vul_details[key_to_use]) * values_dict[key_to_use]
	return sort_value

def get_values_multiplied(keys_to_use, possible_values_dict):
	values_dict = dict()
	for i in range(len(keys_to_use)):
		mult = 1
		for j in range(i + 1, len(keys_to_use)):
			mult *= len(possible_values_dict[keys_to_use[j]])
		values_dict[keys_to_use[i]] = mult
	return values_dict


def sort_vulnerabilities_1(vul_dict, keys_to_use, possible_values_dict, reverse=False):
	vul_list = list(vul_dict.keys())
	values_dict = get_values_multiplied(keys_to_use, possible_values_dict)
	vul_list.sort(key=lambda vul_key: sort_vulnerability_key(vul_dict[vul_key][0], keys_to_use, possible_values_dict, values_dict), reverse = False)
	return vul_list


def get_vulnerabilities_ids(vul_list_CVE, vul_dict):
	vul_CVE_id_dict = dict()
	vul_id_CVE_dict = dict()

	for vul_id, vul_desc in vul_dict.items():
		if vul_desc['name'] in vul_list_CVE:
			vul_CVE_id_dict[vul_desc['name']] = vul_id
			vul_id_CVE_dict[vul_id] = vul_desc['name']
	return (vul_CVE_id_dict, vul_id_CVE_dict)

# TODO - This obviously needs refactoring
# It is late and im tired
def sort_vulnerabilities(vul_list_CVE, vul_full_dict, reverse = False):
	#print(vul_full_dict.keys())
	vul_simple_description_dict = vul_full_dict["vulnerabilities"]
	if len(vul_simple_description_dict.keys()) == 0:
		return []

	enrichments_dict_temp = vul_full_dict["enrichments"].keys()
	if len(enrichments_dict_temp) == 0:
		return []

	vul_full_description_dict = list(vul_full_dict["enrichments"].values())[0][0]
	(vul_CVE_id_dict, vul_id_CVE_dict) = get_vulnerabilities_ids(vul_list_CVE, vul_simple_description_dict)

	ids_CVE_list = list(vul_id_CVE_dict.keys())
	sorted_vul_list = sort_vulnerabilities_1(vul_full_description_dict, keys_to_identify, possible_values_dict, reverse = reverse)

	new_sorted_CVE_list = []
	for element in sorted_vul_list:
		if element in ids_CVE_list:
			new_sorted_CVE_list.insert(0, vul_id_CVE_dict[element])

	return new_sorted_CVE_list


# CAREFULL - I GOT CONFUSED WITH FILTERS
# NEXT SECTION IS CONFUSION OF THE HIGHEST ORDER

# Checks if it is filtered
# If the details are not equal to the filter, return true
def is_filtered(vul_details, filter_tuples):
	for filter_tuple in filter_tuples:
		filter_key = filter_tuple[0]
		filter_value = filter_tuple[1]
		if filter_value != vul_details[filter_key]:
			return True
	return False






# Returns keys that are to be filtered
# Meaning it returns keys that are to be removed
def get_keys_to_remove_from_vulnerabilities_dict(vul_dict, filter_tuples):
        vul_id_list = list()
        for vul_id, vul_details in vul_dict.items():
                if is_filtered(vul_details[0], filter_tuples):
                        vul_id_list.append(vul_id)
        return vul_id_list


# If keys are in filter, remove from dictionary
def filter_dictionary_by_keys(vul_dict, keys_to_filter):
        [vul_dict.pop(key) for key in keys_to_filter]


#If keys are not in filter, remove from dictionary
def filter_dictionary_by_keys_negative(dictionary_to_filter, keys_in_dictionary, keys_to_filter):
	for key_in_dictionary in list(keys_in_dictionary):
		if key_in_dictionary not in keys_to_filter:
			dictionary_to_filter.pop(key_in_dictionary)

def filter_vulnerabilities_not_detailed(vul_simple_description_dict, vul_full_description_dict, enchrichements_keys, vulnerabilities_keys):
	vulnerabilities_described_keys = [vulnerability for vulnerability in enchrichements_keys if vulnerability in set(vulnerabilities_keys)]

	filter_dictionary_by_keys_negative(vul_simple_description_dict, vulnerabilities_keys, vulnerabilities_described_keys)
	filter_dictionary_by_keys_negative(vul_full_description_dict, enchrichements_keys, vulnerabilities_described_keys)

def filter_full_vulnerabilities(vul_full_dict, filter_tuples):
	#print(vul_full_dict)
	if not vul_full_dict:
		return
	vul_simple_description_dict = vul_full_dict["vulnerabilities"]
	if len(vul_simple_description_dict.keys()) == 0:
		vul_full_dict["enrichments"] = dict()
		return

	enrichments_dict_temp = vul_full_dict["enrichments"].keys()
	if len(enrichments_dict_temp) == 0:
		vul_full_dict["vulnerabilities"] = dict()
		return

	vul_full_description_dict = list(vul_full_dict["enrichments"].values())[0][0]

	vulnerabilities_keys = vul_simple_description_dict.keys()
	enchrichements_keys = vul_full_description_dict.keys()

	filter_vulnerabilities_not_detailed(vul_simple_description_dict, vul_full_description_dict, enchrichements_keys, vulnerabilities_keys)

	keys_to_remove = get_keys_to_remove_from_vulnerabilities_dict(vul_full_description_dict, filter_tuples)
	filter_dictionary_by_keys(vul_simple_description_dict, keys_to_remove)
	filter_dictionary_by_keys(vul_full_description_dict, keys_to_remove)


# Test get_vulnerability_file_names
#print(get_vulnerability_file_names(vulnerabilities_path))

# Test read_vulnerability_file
'''
file_keys = read_vulnerability_file(get_vulnerability_file_names(vulnerabilities_path)[0])

vulnerabilities_keys = file_keys["vulnerabilities"].keys()

enchrichements_keys = list(file_keys["enrichments"].values())[0][0].keys()

vulnerabilities_described_keys = [vulnerability for vulnerability in enchrichements_keys if vulnerability in set(vulnerabilities_keys)]
description_dict = list(file_keys["enrichments"].values())[0][0]
description_list = [description_dict[vulnerability_key] for vulnerability_key in enchrichements_keys]

filter_negative_list = ["version", "vectorString"]
filter_positive_list = ["attackComplexity", "attackVector", "availabilityImpact", "baseScore", "privilegesRequired", "userInteraction"]

filter_list = filter_positive_list

keys_to_identify = get_keys_in_vul_desc(description_list, filter_positive_list = filter_list)

#filter_full_vulnerabilities(file_keys,[("attackVector","LOCAL")])
filter_full_vulnerabilities(file_keys,[("attackVector","NETWORK")])


keys_to_identify = ["attackComplexity", "privilegesRequired", "userInteraction", "baseScore", "availabilityImpact", "attackVector"]
possible_values_dict = possible_values_for_various_keys(keys_to_identify, description_list)

sort_possible_values_list(keys_to_identify, possible_values_dict)

#description_dict = filter_vulnerabilities(description_dict, [("attackVector","LOCAL")]);

# print(possible_values_dict)
vul_list = sort_vulnerabilities(description_dict, keys_to_identify, possible_values_dict)


print(description_dict[vul_list[0]])
'''
