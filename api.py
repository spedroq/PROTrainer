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

for poke in kanto_elite_four_pokes:
	poke_data = api_poke_lookup(poke)
	#print(poke_data)
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("P O K E M O N  :  {}".format(poke))
	this_poke_type = poke_data["types"][0].lower()
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
		api_data = api_matchup(this_poke_type, poke_type)
		if api_data["modifier"] == 2:
			two_times_count += 1
			print("{} vs. {} = {}".format(this_poke_type, poke_type, api_data["modifier"]))
		if api_data["modifier"] == 1:
			one_times_count += 1
		if api_data["modifier"] == 0.5:
			half_times_count += 1
		if api_data["modifier"] == 0:
			zero_times_count += 1
		#print("{} vs. {} = {}".format(this_poke_type, poke_type, api_data["modifier"]))
		#print(api_data)
	print("2x\t{}\n1x\t{}\n0.5x\t{}\n0x\t{}".format(
		two_times_count, one_times_count, half_times_count, zero_times_count
	))
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	print("D E F E N D")
	print("\n-	=	-	=	-	=	-	=	-	=	-	=	-	=	\n")
	dank_types = {}
	two_times_count = 0
	one_times_count = 0
	half_times_count = 0
	zero_times_count = 0
	for poke_type in poke_types:
		#
		#	A T T A C K
		#
		
		#	Check this poketype as the attacking one against the poke in the list
		api_data = api_matchup(poke_type, this_poke_type)
		if api_data["modifier"] == 2:
			print("{} vs. {} = {}".format(poke_type, this_poke_type, api_data["modifier"]))
			#
			#	dank type
			if dank_types.get(poke_type):
				dank_types[poke_type] += 1
			else:
				dank_types[poke_type] = 1
				
			if overall_dank_types.get(poke_type):
				overall_dank_types[poke_type] += 1
			else:
				overall_dank_types[poke_type] = 1

			two_times_count += 1
		if api_data["modifier"] == 1:
			one_times_count += 1
		if api_data["modifier"] == 0.5:
			print("{} vs. {} = {}".format(poke_type, this_poke_type, api_data["modifier"]))
			half_times_count += 1
		if api_data["modifier"] == 0:
			zero_times_count += 1
		#print("{} vs. {} = {}".format(this_poke_type, poke_type, api_data["modifier"]))
		#print(api_data)
	print("2x\t{}\n1x\t{}\n0.5x\t{}\n0x\t{}".format(
		two_times_count, one_times_count, half_times_count, zero_times_count
	))
	print("\nA N A L Y S I S")
	print(dank_types)

#
#	

print(overall_dank_types)