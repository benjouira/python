import select_from_elk_with_sql as sfews
import re

df= sfews.x()

# df['Banque'] = df['Banque'].str.replace('\d+', '')
# df['Banque'] = df['Banque'].str.replace('€', '')
# df['Banque'] = df['Banque'].str.replace('$', '')
# df['Banque'] = df['Banque'].str.replace('STBTEC', 'STB')

# df['Banque'] = df['Banque'].str.replace('BIAT', 'BIA')
# df['Banque'] = df['Banque'].str.replace('BIA', 'BIAT')
# df['Banque'] = df['Banque'].str.replace('BW', 'WB')

# # df.groupby(['Banque'])
# df = df.groupby(by=["Banque","Valider"], as_index=False).sum()

# # df['Name'] = df['Name'].str.replace('\d+', '')re.sub(r'[^a-zA-Z]', '', s)
# print (df.sort_values(by=['Valider'], ascending=False))
print(df)

