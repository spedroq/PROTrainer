import requests
import json
#
#   A P I
api_base_url = "http://kerbin.xyz/pokes/"
api_type_matchup_argument_string = "?mode=matchup&attacking={}&defending={}"
api_poke_lookup_argument_string = "?mode=lookup&poke={}"

#
#   A P I    
#
def json_request(url):
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



poke_list = ["pikachu", "machop"]
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
dank_types_defending = {}
dank_types_attacking = {}

for poke in kanto_elite_four_pokes:
	poke_data = api_poke_lookup(poke)
	#print(poke_data)
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("P O K E M O N  :  {}".format(poke))
	this_poke_type = poke_data["types"][0].lower()
	#for t in this_poke_types:
	#	t = t.lower()
	print("T Y P E  :  {}".format(this_poke_type))
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("A T T A C K")
	two_times_count = 0
	one_times_count = 0
	half_times_count = 0
	zero_times_count = 0
	for poke_type in poke_types:
		#
		#	A T T A C K
		#
		
		#	Check this poketype as the attacking one against the poke in the list
		modifiers = [1]
		for p_type in this_poke_types:
			api_data = api_matchup(p_type, poke_type)
			modifiers.append(api_data["modifier"])
			if api_data["modifier"] == 2:
				two_times_count += 1
				
			if api_data["modifier"] == 1:
				one_times_count += 1
			if api_data["modifier"] == 0.5:
				half_times_count += 1
				if dank_types_defending.get(p_type):
					dank_types_defending[p_type] += 1
				else:
					dank_types_defending[p_type] = 1
				print("{} vs. {} = {}".format(p_type, poke_type, api_data["modifier"]))
			if api_data["modifier"] == 0:
				if dank_types_defending.get(p_type):
					dank_types_defending[p_type] += 1
				else:
					dank_types_defending[p_type] = 1
				zero_times_count += 1
				print("{} vs. {} = {}".format(p_type, poke_type, api_data["modifier"]))
		calculated_modifier = 1
		for modifier in modifiers:
			calculated_modifier = calculated_modifier * modifier

	


		
			#print("{} vs. {} = {}".format(this_poke_type, poke_type, api_data["modifier"]))
			#print(api_data)
	print("2x\t{}\n1x\t{}\n0.5x\t{}\n0x\t{}".format(
		two_times_count, one_times_count, half_times_count, zero_times_count
	))
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("D E F E N D")
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")

	two_times_count = 0
	one_times_count = 0
	half_times_count = 0
	zero_times_count = 0
	for poke_type in poke_types:
		#
		#	A T T A C K
		#
		
		#	Check this poketype as the attacking one against the poke in the list
		modifiers = [1]
		for p_type in this_poke_types:
			api_data = api_matchup(poke_type, p_type)
			modifiers.append(api_data["modifier"])
			if api_data["modifier"] == 2:
				print("{} vs. {} = {}".format(poke_type, p_type, api_data["modifier"]))
				if dank_types_attacking.get(p_type):
					dank_types_attacking[p_type] += 1
				else:
					dank_types_attacking[p_type] = 1
				two_times_count += 1
				
			if api_data["modifier"] == 1:
				one_times_count += 1
			if api_data["modifier"] == 0.5:
				half_times_count += 1
				#print("{} vs. {} = {}".format(p_type, poke_type, api_data["modifier"]))
			if api_data["modifier"] == 0:
				zero_times_count += 1
				#print("{} vs. {} = {}".format(p_type, poke_type, api_data["modifier"]))
		calculated_modifier = 1
		for modifier in modifiers:
			calculated_modifier = calculated_modifier * modifier

	
				

	print("2x\t{}\n1x\t{}\n0.5x\t{}\n0x\t{}".format(
		two_times_count, one_times_count, half_times_count, zero_times_count
	))
	#print("\nA N A L Y S I S")
	#print(dank_types)
	print("\n\nD E F E N D I N G  :  \n".format(dank_types_defending))
	print("\n\nA T T A C K I N G  :  \n".format(dank_types_attacking))

#
#	

print(overall_dank_types)