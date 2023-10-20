import openai

openai.api_key = "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"

# def chat_with_chatgpt(prompt, model="gpt-4"):
#     response = openai.Completion.create(
#         engine=model,
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = response.choices[0].text.strip()
#     return message

import csv

columns_to_keep = ['Filière de formation', 'Établissement', 'Commune de l’établissement']

with open('formations.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=";")
    rows = list(reader)

# Filter only the required columns
columns = list(rows[0].keys())

print("The list of columns is {columns}".format(columns = columns))

    
filtered_rows = [{column: row[column] for column in columns_to_keep} for row in rows]

from random import shuffle

shuffle(filtered_rows)

filtered_rows = filtered_rows[:50]

formations = '\n'.join(str(d) for d in filtered_rows)


print(formations)

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Vous êtes un conseiller d'orientation qui à partir d'une lettre de motivation, d'une liste de formation disponible et d'un test de personalité sur un candidat va proposer une liste de formation intéressante pour le candidat"},
            {"role": "system", "content": formations},

            {"role": "user", "content": prompt},
        ],
    )

    message = response.choices[0]['message'].content
    return message


# for row in filtered_rows:
#     for key in row:
#         print("Row name: {name} <{text}>\n".format(name = key, text = row[key]))

# for row in filtered_rows:
#     print(row)

import sys

motivation_file = sys.argv[1]
personnality_file = sys.argv[2]


motivation_letter = "Not read"


with open(motivation_file,"r") as file:
    motivation_letter = file.read()

with open(personnality_file,"r") as file:
    personnality = file.read()

with open("formations.csv","r") as file:
    formations_list = file.readline()


print ("------ Lettre de motivation du candidat --------\n{motivation_letter}\n--------- Fin de la lettre ----------".format(motivation_letter = motivation_letter))
    
interests_prompt = "Extrait de cette lettre de motivation les centres d'interets du candidat, en une simple liste succincte, separe par des virgules, sans aucun autre texte additionnel, sans entête: "

interests = chat_with_chatgpt(interests_prompt + motivation_letter)

print("Le candidat a les interets suivant: {interests}".format(interests = interests))

skills_prompt = "Extrait de cette lettre de motivation les competences du candidat, en une simple liste succincte, separe par des virgules, sans aucun autre texte additionnel, sans entête: "
skills = chat_with_chatgpt(skills_prompt + motivation_letter)

print("Le candidat a les competences suivantes: {skills}".format(skills = skills))

personnality_prompt = "Voici les résults au test de personnalité du Big Five du candidat: {personnality}. Décrire la personnalité du candidat en un petit paragraphe".format(personnality = personnality)

personnality_synthesis = chat_with_chatgpt(personnality_prompt)

print("---- Description de la personnalité du candidat ------\n{personnality_synthesis}\n------ Fin de la personnalité -------".format(personnality_synthesis = personnality_synthesis))


formations_prompt = "A partir de la liste des centres d'interets du candidat: {interests} et la liste des competences du candidat: {skills}, la liste des formations disponibles ainsi que sa personnalité selon ses résultats au test de personnalité du Big Five: {personnality}. Faire une liste succincte, separe par des virgules de formations qui correspondent au profil du candidat, en précisant le nom des etablissements, ainsi que la commune des etablissements, préciser une probabilité d'acception de la candidature en fonction du profil du candidat ainsi qu'une très petite description de la formation, en précisant là où sa personnalité peut être un atout".format(skills = skills, interests = interests, personnality = personnality)
formations = chat_with_chatgpt(formations_prompt)

print("Les formations pour le candidat: {formations}".format(formations = formations))




