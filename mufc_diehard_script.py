import numpy as np
import pandas as pd
import requests
from StringIO import StringIO 

def net_df(link):
	r1 = requests.get(link)
	data1 = r1.content
	return pd.read_csv(StringIO(data1))


###Downloading data from google spreadsheet using the google_sheet_id (which we cannot provide here for obvious reasons!)
reponse_link = 'https://docs.google.com/spreadsheets/d/'+google_sheet_id+'/export?format=csv&id'

#data_in = pd.read_csv('mufc_week1.csv')
data_in = net_df(reponse_link)
#data_in = data_in.ix[23:]#selecting data if needed
data_in = data_in.reset_index()
loop_length = len(data_in['List your starting 11'])

opponents = 'West Ham United'
home = 'yes'
week = '1'

### Case 1 - 90min game
col = ['Name','Selection','Selection pts','MOTM','MOTM pts','W_D_L','W_D_L pts','HT Score','HT pts','90 min Score','90 min pts','Red Cards','Rd card pts', 'Total Points']
########################################################################################################
### Case 2 - 120min game
#col = ['Name','Selection','Selection pts','MOTM','MOTM pts','W_D_L','W_D_L pts','Red Cards','Rd card pts','HT Score','HT pts','90 min Score','90 min pts','120 min score','120 min pts','Penalties','Penalties pts','Total Points']
########################################################################################################

#initialising a new dataframe
new_data = pd.DataFrame(index=data_in.index, columns = col)


#function to split names of the 11 players given from users. Google spreadsheet usually gives all the names combined
def split_names(inlist):
	outlist = []
	for ik in range(len(inlist)):
		if inlist[ik][0] == ' ':
			outlist.append(inlist[ik][1:])
		else:
			outlist.append(inlist[ik][:])
	return outlist


#initialising some list to store results of users 
res_lineup = [] ; res_motm = [] ; res_wdl = [] ; res_ht = [] ; res_ft = [] ; res_redc = []
user_sel = [] ; sel_motm = [] ; disp_ht_score = [] ; disp_ft_score = []

########################################################################################################
res_penalties = [] ; res_120 = [] ; disp_120_score = []
########################################################################################################


## looping over the all participants except last input which is the admin input - which contains all right answers
for i in range(loop_length):
	#line up scoring part
	print i
	user_choice = set(split_names(data_in['List your starting 11'][i].split(',')))
	real_lineup = set(split_names(data_in['List your starting 11'][loop_length-1].split(','))) # taking last row as correct value to calculate from
	#calculating number of names that the user got right compared to admin answers
	score = len(user_choice & real_lineup)
	if score < 11:
		res_lineup.append(score)
	else:
		res_lineup.append(13)
	usrls = []
	#looping over the each's user's choice of results 
	length_usr_choice = len(list(user_choice))
	for j in range(length_usr_choice):
#		try:
#			usrls.append(list(user_choice)[j].split('\t')[0]+' '+list(user_choice)[j].split('\t')[2])
#		except:
		if list(user_choice)[j].split(' ')[0] == '1':
			usrls.append(list(user_choice)[j].split(' ')[0]+' '+list(user_choice)[j].split(' ')[2]+' '+list(user_choice)[j].split(' ')[3])
		else:
			usrls.append(list(user_choice)[j].split(' ')[0]+' '+list(user_choice)[j].split(' ')[-1])
	user_sel.append(usrls)

	#Man of the match
	user_motm = data_in['Select your Manchester United Man of the Match'][i]
	sel_motm.append(user_motm.split('\t')[-1])
	real_motm = data_in['Select your Manchester United Man of the Match'][loop_length-1]
	if user_motm == real_motm:
		res_motm.append(3)
	else:
		res_motm.append(0)

	#win draw lose
	user_wdl = data_in['Will the match be a win, draw or lose for Manchester United?'][i]
	real_wdl = data_in['Will the match be a win, draw or lose for Manchester United?'][loop_length-1]
	if user_wdl == real_wdl:
		if user_wdl == 'Win':
			res_wdl.append(2)
		if user_wdl == 'Draw':
			res_wdl.append(3)
		if user_wdl == 'Lose':
			res_wdl.append(5)
	else:
		res_wdl.append(0)

	#half time score
	user_ht_utd_goals = data_in['How many goals will Manchester United Score at Half Time?'][i]
	user_ht_op_goals = data_in['How many goals will '+opponents+' Score at Half Time?'][i]
	if home == 'yes':
		disp_ht_score.append(str(int(user_ht_utd_goals))+'-'+str(int(user_ht_op_goals)))
	else:
		disp_ht_score.append(str(int(user_ht_op_goals))+'-'+str(int(user_ht_utd_goals)))
	real_ht_utd_goals = data_in['How many goals will Manchester United Score at Half Time?'][loop_length-1]
	real_ht_op_goals = data_in['How many goals will '+opponents+' Score at Half Time?'][loop_length-1]
	if user_ht_utd_goals == real_ht_utd_goals and user_ht_op_goals == real_ht_op_goals:
		res_ht.append(3)
	else:
		res_ht.append(0)

	#full time score
	user_ft_utd_goals = data_in['How many goals will Manchester United Score at end of 90min?'][i]
	user_ft_op_goals = data_in['How many goals will '+opponents+' Score at end of 90min?'][i]
	if home == 'yes':
		disp_ft_score.append(str(int(user_ft_utd_goals))+'-'+str(int(user_ft_op_goals)))
	else:
		disp_ft_score.append(str(int(user_ft_op_goals))+'-'+str(int(user_ft_utd_goals)))
	real_ft_utd_goals = data_in['How many goals will Manchester United Score at end of 90min?'][loop_length-1]
	real_ft_op_goals = data_in['How many goals will '+opponents+' Score at end of 90min?'][loop_length-1]
	if user_ft_utd_goals == real_ft_utd_goals and user_ft_op_goals == real_ft_op_goals:
		score_test = user_ft_utd_goals - user_ft_op_goals
		if user_wdl == 'Win' and score_test > 0:
			res_ft.append(6)
		elif user_wdl == 'Draw' and score_test == 0:
			res_ft.append(6)
		elif user_wdl == 'Lose' and score_test < 0:
			res_ft.append(6)
		else:
			res_ft.append(0)
	else:
		res_ft.append(0)

	#red cards
	user_redcard = data_in['How many red cards will there be during this game?'][i]
	real_redcard = data_in['How many red cards will there be during this game?'][loop_length-1]
	if user_redcard == real_redcard and real_redcard == 0:
		res_redc.append(1)
	if user_redcard == real_redcard and real_redcard == 1:
		res_redc.append(3)
	if user_redcard == real_redcard and real_redcard == 2:
		res_redc.append(6)
	if user_redcard == real_redcard and real_redcard > 2:
		res_redc.append(10)
	else:
		res_redc.append(0)

	#case 2 for 120min games possibility
	########################################################################################################
	'''
	#penalties
	user_penalties = data_in['Will there be penalties ?'][i]
	real_penalties = data_in['Will there be penalties ?'][loop_length-1]
	if user_penalties == real_penalties:
		res_penalties.append(1)
	else:
		res_penalties.append(0)

	#120 min scores
	user_120_utd_goals = data_in['How many goals will Manchester United Score after 120min?'][i]
	user_120_op_goals = data_in['How many goals will '+opponents+' Score after 120min?'][i]
	if home == 'yes':
		disp_120_score.append(str(int(user_120_utd_goals))+'-'+str(int(user_120_op_goals)))
	else:
		disp_120_score.append(str(int(user_120_op_goals))+'-'+str(int(user_120_utd_goals)))

	real_120_utd_goals = data_in['How many goals will Manchester United Score after 120min?'][loop_length-1]
	real_120_op_goals = data_in['How many goals will '+opponents+' Score after 120min?'][loop_length-1]
	if user_120_utd_goals == real_120_utd_goals and user_120_op_goals == real_120_op_goals:
		res_120.append(1)
	else:
		res_120.append(0)
	'''
	########################################################################################################


#sending all the results to the main data frame 

#new_data['Name'] = data_in['Name (Your name for the game) ']
new_data['Name'] = data_in['Name ']
#new_data['Selection'] = data_in['List your starting 11']
new_data['Selection'] = user_sel
new_data['Selection pts'] = res_lineup
new_data['MOTM'] = sel_motm
new_data['MOTM pts'] = res_motm
new_data['W_D_L'] = data_in['Will the match be a win, draw or lose for Manchester United?']
new_data['W_D_L pts'] = res_wdl
new_data['HT Score'] = disp_ht_score
new_data['HT pts'] = res_ht
new_data['90 min Score'] = disp_ft_score
new_data['90 min pts'] = res_ft
new_data['Red Cards'] = data_in['How many red cards will there be during this game?']
new_data['Rd card pts'] = res_redc
########################################################################################################
'''
#case 2 120min game
new_data['120 min score'] = disp_120_score
new_data['120 min pts'] = res_120
new_data['Penalties'] = data_in['Will there be penalties ?']
new_data['Penalties pts'] = res_penalties
'''
########################################################################################################

#calculating the total points of every user
new_data['Total Points'] = new_data['Selection pts']+new_data['MOTM pts']+new_data['W_D_L pts']+new_data['HT pts']+new_data['90 min pts']+new_data['Rd card pts']
#new_data['Total Points'] = new_data['Selection pts']+new_data['MOTM pts']+new_data['W_D_L pts']+new_data['HT pts']+new_data['90 min pts']+new_data['Rd card pts']+new_data['120 min pts']+new_data['Penalties pts']


final_data = new_data.ix[:loop_length-2]
sorted_final = final_data.sort(columns=['Total Points'],ascending=False)

sorted_final.to_csv('mufc_res_game'+week+'.csv')
