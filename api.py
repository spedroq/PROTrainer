import requests
import json
import collections
#
#   A P I
api_base_url = "http://kerbin.xyz/pokes/"
api_type_matchup_argument_string = "?mode=matchup&attacking={}&defending={}"
api_poke_lookup_argument_string = "?mode=lookup&poke={}"

#
#   A P I	
#
def json_request(url):
	#print(url)
	r = requests.get(url)
	return json.loads(r.text)

#
#   A function to lookup a pokemon's stats
def api_poke_lookup(pokemon):
	url = api_base_url + api_poke_lookup_argument_string.format(pokemon).lower()
	#print(url)
	poke_data = json_request(url)
	#print(poke_data)
	return poke_data

def api_matchup(attacking, defending):
	url = api_base_url + api_type_matchup_argument_string.format(
		attacking, defending
	).lower()
	#print(url)
	poke_data = json_request(url)
	return poke_data



#poke_list = ["dewgong", "krabby", "butterfree"]
poke_list = ["rattata"]
kanto_elite_four_pokes = [
	"dewgong", "cloyster", "slowbro", "jynx", "lapras",
	"onix", "hitmonchan", "hitmonlee", "onix", "machamp",
	"gengar", "golbat", "haunter", "arbok", "gengar",
	"gyarados", "dragonair", "dragonair", "aerodactyl", "dragonite"

]
#
#	Find the most effective type
poke_types = [
	"normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy"

]

overall_dank_types = {}

attacking_dank_types = []

def empty_function():
	i = 0

#
#	A function to analyse the api data
def analyse_api_data(api_data, desired_modifiers=[], function_to_run=empty_function, args_to_run=[]):
	for modifier in desired_modifiers:
		if api_data["modifier"] == modifier:
			function_to_run()
	return api_data



#
#	Return the number of types a pokemon has from its api_data
def get_a_pokemons_type_count_from_api_data(api_data):
	return len(api_data["types"])



FINAL_OUTPUT = []
for poke in poke_list:
	poke_data = api_poke_lookup(poke)
	#print(poke_data)
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("P O K E M O N  :  {}".format(poke))
	#
	#	How many types does it have?
	
	
	print("T Y P E S  :  {}".format(poke_data["types"]))
	this_poke_type = poke_data["types"][0].lower()
	
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	
	two_times_count = 0
	one_times_count = 0
	half_times_count = 0
	zero_times_count = 0
	#
	#	For each pokemon type there is, check this pokemon's type against it
	
	attacking_api_datas = []
	defending_api_datas = []
	desired_modifiers_attacking = [0.5, 0]
	desired_modifiers_defending = [2]

	exported_information = []

	for poke_type in poke_types:
		#
		#	Where our pokemon is attacking
		#	A T T A C K I N G
		#
		#	Ok, but what if we have more than one type?
		#	multiplier = type_a["modifier"] * type_b["modifier"]
		for this_poke_type in poke_data["types"]:
			this_poke_type = this_poke_type.lower()
			api_data = api_matchup(this_poke_type, poke_type)
			attacking_api_datas.append(api_data)
			#
			#	Where our pokemon is defending
			#	D E F E N D I N G
			api_data = api_matchup(poke_type, this_poke_type)
			defending_api_datas.append(api_data)

	#
	#	Now analyse this information
	output_data = {
		"attacking": [],
		"defending": []
	}
	output_data_poke_types_to_use = {
		"pokemon": poke,
		"types": poke_data["types"],
		"attacking": {},
		"defending": {}
	}
	#
	#	A T T A C K I N G
	dank_attack_types = {}
	for api_data in attacking_api_datas:		
		for modifier in desired_modifiers_attacking:
			if api_data["modifier"] == modifier:
				if output_data_poke_types_to_use["attacking"].get(api_data["defending"]):
					output_data_poke_types_to_use["attacking"][api_data["defending"]] += 1
				else:
					output_data_poke_types_to_use["attacking"][api_data["defending"]] = 1
				output_data["attacking"].append(api_data)

	
	#
	#	D E F E N D I N G
	for api_data in defending_api_datas:
		for modifier in desired_modifiers_defending:
			if api_data["modifier"] == modifier:
				if output_data_poke_types_to_use["defending"].get(api_data["attacking"]):
					output_data_poke_types_to_use["defending"][api_data["attacking"]] += 1
				else:
					output_data_poke_types_to_use["defending"][api_data["attacking"]] = 1
				output_data["defending"].append(api_data)
	#print(output_data_poke_types_to_use)

	#print("A T T A C K I N G")
	#print(output_data_poke_types_to_use["attacking"])
	#print("\nD E F E N D I N G")
	#print(output_data_poke_types_to_use["defending"])
	#print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	FINAL_OUTPUT.append(output_data_poke_types_to_use)
	#
	#	Print the output
	#print(output_data)

#
#	Ok, now analyse it as a whole
total_maths = {
	
}
attacking_stats = {
	
}
defending_stats = {
	
}
for poke in FINAL_OUTPUT:
	#print(poke)
	for k,v in poke["attacking"].items():
		for poke_type in poke_types:
			if k == poke_type:
				key_str = "{}_x{}".format(
					k, v
				)
				if attacking_stats.get(key_str):
					attacking_stats[key_str] += 1
				else:
					attacking_stats[key_str] = 1
	for k,v in poke["defending"].items():
		for poke_type in poke_types:
			if k == poke_type:
				key_str = "{}_x{}".format(
					k, v
				)
				if defending_stats.get(key_str):
					defending_stats[key_str] += 1
				else:
					defending_stats[key_str] = 1


print("A T T A C K  (L O W  D A M A G E)")
print(attacking_stats)
print("\nD E F E N D  (H I G H  D A M A G E)")
print(defending_stats)
print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")