# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 07:28:40 2024

@author: Gowtham S
"""
## Parabens
import pandas as pd
import numpy as np
import re
import string

df=pd.read_csv("allfixed_dataset.csv")

dfnew = df[['Abouts', 'Highlights', 'Ingredients']].copy()

parabens = ['methylparaben', 'ethylparaben', 'propylparaben']

# Function to extract and highlight sentences
def extract_sentences_keyword(row):
    sentences = row.split('.')
    highlighted_sentences = []
    for sentence in sentences:
        for paraben in parabens:
            if paraben in sentence.lower():
                highlighted_sentence = re.sub(paraben, lambda match: f"**{match.group(0).upper()}**", sentence, flags=re.IGNORECASE)
                highlighted_sentences.append(highlighted_sentence.strip() + '.')
    return highlighted_sentences if highlighted_sentences else np.nan


dfnew['P_Abouts'] = dfnew['Abouts'].apply(lambda x: extract_sentences_keyword(str(x)))
dfnew['P_High'] = dfnew['Highlights'].apply(lambda x: extract_sentences_keyword(str(x)))
dfnew['P_Ing'] = dfnew['Ingredients'].apply(lambda x: extract_sentences_keyword(str(x)))

dfnew.isnull().sum()

parabensType_notNull = dfnew[dfnew['P_Ing'].notnull()]
parabensType_Null = dfnew[dfnew['P_Ing'].isnull()]

parabens = ['paraben']

parabensType_Null['P_Abouts'] = parabensType_Null['Abouts'].apply(lambda x: extract_sentences_keyword(str(x)))
parabensType_Null['P_High'] = parabensType_Null['Highlights'].apply(lambda x: extract_sentences_keyword(str(x)))
parabensType_Null['P_Ing'] = parabensType_Null['Ingredients'].apply(lambda x: extract_sentences_keyword(str(x)))

parabensType_Null.isnull().sum()

# Define the paraben and negation patterns
parabens = ['formaldehydes', 'formaldehyde', 'formaldehyde-releasing', 'formaldehydes-releasing']
negation_phrases = ['free of', 'free of formaldehydes', 'does not contain', 'does not contain formaldehydes', 'no formaldehydes', 'without', 'without formaldehydes', 'formaldehydes free']

paraben_patterns = re.compile('|'.join(parabens), re.IGNORECASE)
negation_patterns = re.compile('|'.join(negation_phrases), re.IGNORECASE)

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()

# Function to highlight both paraben keywords and negation phrases
def highlight_keywords(sentence):
    highlighted_sentence = re.sub(paraben_patterns, lambda m: f'**{m.group(0).upper()}**', sentence)
    highlighted_sentence = re.sub(negation_patterns, lambda m: f'**{m.group(0).upper()}**', highlighted_sentence)
    return highlighted_sentence

# Function to extract and highlight sentences and determine binary value
def extract_and_highlight_sentences_negation(row):
    sentences = row.split('.')
    highlighted_sentences = []
    contains_parabens = np.nan
    for sentence in sentences:
        preprocessed_sentence = preprocess_text(sentence)
        if paraben_patterns.search(preprocessed_sentence):
            if negation_patterns.search(preprocessed_sentence):
                highlighted_sentence = highlight_keywords(sentence)
                highlighted_sentences.append(f'{highlighted_sentence} (No Parabens)')
                contains_parabens = 0
            else:
                highlighted_sentence = highlight_keywords(sentence)
                highlighted_sentences.append(f'{highlighted_sentence} (Contains Parabens)')
                contains_parabens = 1
    return highlighted_sentences if highlighted_sentences else np.nan, contains_parabens

#dfnew.drop(columns=['NRP_Abouts', 'NRP_High', 'NRP_Ing', 'Contains_palmitates'], inplace=True)

# Applying the function to extract and highlight sentences and determine binary value
dfnew['NP_Abouts'], abouts_parabens = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))
dfnew['NP_High'], high_parabens = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))
dfnew['NP_Ing'], ing_parabens = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))

def combine_paraben_columns(a, b, c):
    if 1 in [a, b, c]:
        return 1
    elif 0 in [a, b, c]:
        return 0
    else:
        return np.nan

# Apply the combine function to create the 'Contains_Parabens' column using numeric variables
dfnew['Contains_Parabens'] = [combine_paraben_columns(a, b, c) for a, b, c in zip(abouts_parabens, high_parabens, ing_parabens)]

dfnew[dfnew['Contains_Parabens'] == 1].count()
dfnew[dfnew['Contains_Parabens'] == 0].count()

dfnew[dfnew['Contains_Parabens'] == 'nan'].count()

dfnew.isnull().sum()

dfnew.drop(columns=['P_Abouts', 'P_High', 'P_Ing'], inplace=True)

dfnew.to_csv('Parabens_YesOrNo.csv')

dfnew[['Abouts', 'Highlights', 'Ingredients']].to_csv('webCheck.csv')

# Applying the function to extract and highlight sentences and determine binary value
dfnew['NF_Abouts'], abouts_formaldehydes = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))
dfnew['NF_High'], high_formaldehydes = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))
dfnew['NF_Ing'], ing_formaldehydes = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_sentences_negation(str(x))))

# Apply the combine function to create the 'Contains_Parabens' column using numeric variables
dfnew['Contains_Parabens'] = [combine_paraben_columns(a, b, c) for a, b, c in zip(abouts_formaldehydes, high_formaldehydes, ing_formaldehydes)]

dfnew[dfnew['Contains_Parabens'] == 1].count()
dfnew[dfnew['Contains_Parabens'] == 0].count()

dfnew[dfnew['Contains_Parabens'] == 1]

{'What it is': 'A rich, powerful, yet delicate treatment oil designed for the face and neck. Solutions for:- Dullness and uneven texture- Uneven skin toneIf you want to know more…This moisturizing oil is made with certified organic noni extract, rosehip oil, pomegranate oil and sea buckthorn oil, which combine to create a rich source of antioxidants and essential fatty acids. The formula is designed to absorb quickly into dehydrated skin to smooth, nourish, and brighten while providing a natural glow. Skin feels softer, smoother, well-hydrated, and plumper, and the visible effects of sun damage and scarring appear diminished. The oil also assists in boosting  natural radiance and creating a more even tone. What else you need to know: "This is my number one favorite product and secret travel companion. It’s a super nourishing treatment oil that is great for all skin types, and especially good for sensitive skin. I use it religiously every night and my skin is glowing in the morning. I also never travel without it and apply it throughout the flight to keep my skin hydrated."—Miranda Kerr, Brand FounderThis oil balances the pH levels in your skin and is also free of synthetic fragrance, synthetic colors, T.E.A., D.E.A., glycols, silicones, PEGs, ethoxylate, and formaldehyde. KORA Organics products are certified organic and certified natural in accordance with COSMOS strict standards. Product color and scent may vary due to the use of organic ingredients.Research results: In a consumer product test of 31 women, age 26-50 with range of normal, combination and dry skin types over 4 weeks with twice daily use after cleansing:After 1 week:- 87% Noticed that their skin looked brighter and more radiantAfter 2 weeks:- 93% Noticed their skin appears more even-toned, with enhanced clarity- 95% Noticed that any uneven or dry skin texture was visibly smootherAfter 4 weeks:- 83% Noticed any fine lines around the eye area appeared visibly softened - 93% Said noticeable improvement in the visible appearance of skin imperfections - 96% Saw visible improvement in skin looking healthier and more glowing - 100% Saw noticeable improvement in skin bounce and improved elasticity CLEAN at Sephora is our commitment to offering formulas that go beyond regulatory standards to avoid controversial ingredients without sacrificing on effectiveness.Show more', 'Skin Type': 'NA', 'Skincare Concerns': 'NA', 'Highlighted Ingredients': 'NA', 'Ingredient Callouts': 'NA', 'What Else You Need to Know': 'NA', 'Clinical Results': 'NA'}

##########################################################################################
##########################################################################################
# FORMALDEHYDES
##########################################################################################
##########################################################################################

# Updated list of formaldehyde keywords
formaldehyde_keywords = ['phthalates', 'phthalate']

# List of negation phrases
negation_phrases = ['free of', 'free of phthalates', 'does not contain', 'contains no', 'contains no phthalates', 'does not contain phthalates', 'no phthalates', 'without', 'without phthalates', 'phthalates-free']

# Compile regex patterns for formaldehyde keywords and negation phrases
formaldehyde_patterns = re.compile('|'.join(formaldehyde_keywords), re.IGNORECASE)
negation_patterns = re.compile('|'.join(negation_phrases), re.IGNORECASE)

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()

# Function to highlight both formaldehyde keywords and negation phrases
def highlight_keywords(paragraph):
    highlighted_paragraph = re.sub(formaldehyde_patterns, lambda m: f'**{m.group(0).upper()}**', paragraph)
    highlighted_paragraph = re.sub(negation_patterns, lambda m: f'**{m.group(0).upper()}**', highlighted_paragraph)
    return highlighted_paragraph

# Function to extract and highlight paragraphs and determine binary value
def extract_and_highlight_paragraphs_negation(paragraph):
    preprocessed_paragraph = preprocess_text(paragraph)
    negation_found = bool(negation_patterns.search(preprocessed_paragraph))
    formaldehyde_found = bool(formaldehyde_patterns.search(preprocessed_paragraph))
    highlighted_paragraph = highlight_keywords(paragraph)
    contains_formaldehydes = np.nan
    if formaldehyde_found:
        if negation_found:
            contains_formaldehydes = 0
            highlighted_paragraph += " (No phthalates)"
        else:
            contains_formaldehydes = 1
            highlighted_paragraph += " (Contains phthalates)"
    elif negation_found:
        highlighted_paragraph += " (No phthalates)"
    return highlighted_paragraph, contains_formaldehydes

# Sample DataFrame with formaldehyde-related data
data = {
    'Abouts': ["This product contains formaldehyde. It's great for preservation.", "No formaldehydes here."],
    'Highlights': ["Formaldehyde is included.", "Formaldehyde-releasing agents are not included."],
    'Ingredients': ["free of synthetic fragrance, synthetic colors, T.E.A., D.E.A., glycols, silicones, PEGs, ethoxylate, and formaldehyde", "Contains no harmful chemicals including formaldehyde."]
}
dfnew1 = pd.DataFrame(data)

# Applying the function to extract and highlight paragraphs and determine binary value
dfnew['NF_Abouts'], abouts_formaldehydes = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))
dfnew['NF_High'], high_formaldehydes = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))
dfnew['NF_Ing'], ing_formaldehydes = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))

# Function to combine binary values into a single column
def combine_formaldehyde_columns(a, b, c):
    if 1 in [a, b, c]:
        return 1
    elif 0 in [a, b, c]:
        return 0
    else:
        return np.nan

# Apply the combine function to create the 'Contains_Formaldehydes' column using numeric variables
dfnew['Contains_Formaldehydes'] = [combine_formaldehyde_columns(a, b, c) for a, b, c in zip(abouts_formaldehydes, high_formaldehydes, ing_formaldehydes)]


dfnew[dfnew['Contains_Formaldehydes'] == 1].count()
dfnew[dfnew['Contains_Formaldehydes'] == 0].count()

dfnew.isnull().sum()

##########################################################################################
##########################################################################################
# phthalates
##########################################################################################
##########################################################################################

# Updated list of formaldehyde keywords
phthalates_keywords = ['phthalates', 'phthalate']

# List of negation phrases
negation_phrases = ['free of', 'free of phthalates', 'does not contain', 'contains no', 'contains no phthalates', 'does not contain phthalates', 'no phthalates', 'without', 'without phthalates', 'phthalates-free', 'not included', 'not present']

# Compile regex patterns for formaldehyde keywords and negation phrases
phthalates_patterns = re.compile('|'.join(phthalates_keywords), re.IGNORECASE)
negation_patterns = re.compile('|'.join(negation_phrases), re.IGNORECASE)

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()

# Function to highlight both formaldehyde keywords and negation phrases
def highlight_keywords(paragraph):
    highlighted_paragraph = re.sub(phthalates_patterns, lambda m: f'**{m.group(0).upper()}**', paragraph)
    highlighted_paragraph = re.sub(negation_patterns, lambda m: f'**{m.group(0).upper()}**', highlighted_paragraph)
    return highlighted_paragraph

# Make it more a reusable function by taking patterns above as params - do later as i am ok with this now 
# Function to extract and highlight paragraphs and determine binary value
def extract_and_highlight_paragraphs_negation(paragraph):
    preprocessed_paragraph = preprocess_text(paragraph)
    negation_found = bool(negation_patterns.search(preprocessed_paragraph))
    phthalates_found = bool(phthalates_patterns.search(preprocessed_paragraph))
    highlighted_paragraph = highlight_keywords(paragraph)
    contains_elements = np.nan
    if phthalates_found:
        if negation_found:
            contains_elements = 0
            highlighted_paragraph += " (No phthalates)"
        else:
            contains_elements = 1
            highlighted_paragraph += " (Contains phthalates)"
    elif negation_found:
        highlighted_paragraph += " (No phthalates)"
    return highlighted_paragraph, contains_elements

"""
# Sample DataFrame with formaldehyde-related data
data = {
    'Abouts': ["This product contains phthalates. It's great for preservation.", "No phthalates here."],
    'Highlights': ["phthalates is included.", "phthalates-releasing agents are not included."],
    'Ingredients': ["free of synthetic fragrance, synthetic colors, T.E.A., D.E.A., phthalates, glycols, silicones, PEGs, ethoxylate, and formaldehyde", "Contains no harmful chemicals including phthalates."]
}
dfnew1 = pd.DataFrame(data)
"""

# Applying the function to extract and highlight paragraphs and determine binary value
dfnew['NPh_Abouts'], abouts_phthalates = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))
dfnew['NPh_High'], high_phthalates = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))
dfnew['NPh_Ing'], ing_phthalates = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_paragraphs_negation(str(x))))

# Function to combine binary values into a single column
def combine_columns(a, b, c):
    if 1 in [a, b, c]:
        return 1
    elif 0 in [a, b, c]:
        return 0
    else:
        return np.nan

# Apply the combine function to create the 'Contains_Formaldehydes' column using numeric variables
dfnew['Contains_phthalates'] = [combine_columns(a, b, c) for a, b, c in zip(abouts_phthalates, high_phthalates, ing_phthalates)]


dfnew[dfnew['Contains_phthalates'] == 1].count()
dfnew[dfnew['Contains_phthalates'] == 0].count()

dfnew.isnull().sum()

##########################################################################################
##########################################################################################
# Retinyl palmitate
##########################################################################################
##########################################################################################

# Updated list of formaldehyde keywords
palmitates_keywords = ['Retinyl palmitate']

# List of negation phrases
negation_phrases = ['free of', 'free of Retinyl palmitate', 'does not contain', 'contains no', 'contains no Retinyl palmitate', 'does not contain Retinyl palmitate', 'no Retinyl palmitate', 'without', 'without Retinyl palmitate', 'Retinyl palmitate-free', 'not included', 'not present']

# Compile regex patterns for palmitate keywords and negation phrases
palmitates_patterns = re.compile('|'.join(palmitates_keywords), re.IGNORECASE)
negation_patterns = re.compile('|'.join(negation_phrases), re.IGNORECASE)

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()

# Function to highlight both palmitate keywords and negation phrases
def highlight_keywords(sentence):
    highlighted_sentence = re.sub(palmitates_patterns, lambda m: f'**{m.group(0).upper()}**', sentence)
    highlighted_sentence = re.sub(negation_patterns, lambda m: f'**{m.group(0).upper()}**', highlighted_sentence)
    return highlighted_sentence

# Function to extract and highlight sentences and determine binary value
def extract_and_highlight_sentences(paragraph):
    sentences = paragraph.split('.')
    relevant_sentences = []
    contains_elements = np.nan
    for sentence in sentences:
        preprocessed_sentence = preprocess_text(sentence)
        palmitates_found = bool(palmitates_patterns.search(preprocessed_sentence))
        if palmitates_found:
            negation_found = bool(negation_patterns.search(preprocessed_sentence))
            highlighted_sentence = highlight_keywords(sentence.strip() + '.')
            if negation_found:
                highlighted_sentence += " (No Palmitates)"
                contains_elements = 0
            else:
                highlighted_sentence += " (Contains Palmitates)"
                contains_elements = 1
            relevant_sentences.append(highlighted_sentence)
    return relevant_sentences if relevant_sentences else [np.nan], contains_elements

"""
# Sample DataFrame with formaldehyde-related data
data = {
    'Abouts': ["This product contains phthalates. It's great for preservation.", "No phthalates here."],
    'Highlights': ["phthalates is included.", "phthalates-releasing agents are not included."],
    'Ingredients': ["free of synthetic fragrance, synthetic colors, T.E.A., D.E.A., phthalates, glycols, silicones, PEGs, ethoxylate, and formaldehyde", "Contains no harmful chemicals including phthalates."]
}
dfnew1 = pd.DataFrame(data)
"""
#dfnew.drop(columns=['NRP_Abouts', 'NRP_High', 'NRP_Ing', 'Contains_palmitates'], inplace=True)

# Applying the function to extract and highlight paragraphs and determine binary value
dfnew['NRP_Abouts'], abouts_palmitates = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_sentences(str(x))))
dfnew['NRP_High'], high_palmitates = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_sentences(str(x))))
dfnew['NRP_Ing'], ing_palmitates = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_sentences(str(x))))

# Function to combine binary values into a single column
def combine_columns(a, b, c):
    if 1 in [a, b, c]:
        return 1
    elif 0 in [a, b, c]:
        return 0
    else:
        return np.nan

# Apply the combine function to create the 'Contains_palmitatess' column using numeric variables
dfnew['Contains_palmitates'] = [combine_columns(a, b, c) for a, b, c in zip(abouts_palmitates, high_palmitates, ing_palmitates)]

# Flatten the lists in the new columns to single sentences
dfnew['NRP_Abouts'] = dfnew['NRP_Abouts'].apply(lambda x: x[0] if x else np.nan)
dfnew['NRP_High'] = dfnew['NRP_High'].apply(lambda x: x[0] if x else np.nan)
dfnew['NRP_Ing'] = dfnew['NRP_Ing'].apply(lambda x: x[0] if x else np.nan)


dfnew[dfnew['Contains_palmitates'] == 1].count()
dfnew[dfnew['Contains_palmitates'] == 0].count()

dfnew[dfnew['Contains_palmitates'] == 1].index


dfnew.isnull().sum()


##########################################################################################
##########################################################################################
# Mineral Oil
##########################################################################################
##########################################################################################

# Updated list of formaldehyde keywords
mnOil_keywords = ['Mineral Oil']

# List of negation phrases
negation_phrases = ['free of', 'free of Mineral Oil', 'does not contain', 'contains no', 'contains no Mineral Oil', 'does not contain Mineral Oil', 'no Mineral Oil', 'without', 'without Mineral Oil', 'Mineral Oil-free', 'not included', 'not present']

# Compile regex patterns for palmitate keywords and negation phrases
mnOil_patterns = re.compile('|'.join(mnOil_keywords), re.IGNORECASE)
negation_patterns = re.compile('|'.join(negation_phrases), re.IGNORECASE)

# Function to preprocess text: remove punctuation and convert to lowercase
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()

# Function to highlight both palmitate keywords and negation phrases
def highlight_keywords(sentence):
    highlighted_sentence = re.sub(mnOil_patterns, lambda m: f'**{m.group(0).upper()}**', sentence)
    highlighted_sentence = re.sub(negation_patterns, lambda m: f'**{m.group(0).upper()}**', highlighted_sentence)
    return highlighted_sentence

# Function to extract and highlight sentences and determine binary value
def extract_and_highlight_sentences(paragraph):
    sentences = paragraph.split('.')
    relevant_sentences = []
    contains_elements = np.nan
    for sentence in sentences:
        preprocessed_sentence = preprocess_text(sentence)
        mnOil_found = bool(mnOil_patterns.search(preprocessed_sentence))
        if mnOil_found:
            negation_found = bool(negation_patterns.search(preprocessed_sentence))
            highlighted_sentence = highlight_keywords(sentence.strip() + '.')
            if negation_found:
                highlighted_sentence += " (No Mineral Oil)"
                contains_elements = 0
            else:
                highlighted_sentence += " (Contains Mineral Oil)"
                contains_elements = 1
            relevant_sentences.append(highlighted_sentence)
    return relevant_sentences if relevant_sentences else [np.nan], contains_elements

"""
# Sample DataFrame with formaldehyde-related data
data = {
    'Abouts': ["This product contains phthalates. It's great for preservation.", "No phthalates here."],
    'Highlights': ["phthalates is included.", "phthalates-releasing agents are not included."],
    'Ingredients': ["free of synthetic fragrance, synthetic colors, T.E.A., D.E.A., phthalates, glycols, silicones, PEGs, ethoxylate, and formaldehyde", "Contains no harmful chemicals including phthalates."]
}
dfnew1 = pd.DataFrame(data)
"""
#dfnew.drop(columns=['NRP_Abouts', 'NRP_High', 'NRP_Ing', 'Contains_palmitates'], inplace=True)

# Applying the function to extract and highlight paragraphs and determine binary value
dfnew['NMNO_Abouts'], abouts_mnOil = zip(*dfnew['Abouts'].apply(lambda x: extract_and_highlight_sentences(str(x))))
dfnew['NMNO_High'], high_mnOil = zip(*dfnew['Highlights'].apply(lambda x: extract_and_highlight_sentences(str(x))))
dfnew['NMNO_Ing'], ing_mnOil = zip(*dfnew['Ingredients'].apply(lambda x: extract_and_highlight_sentences(str(x))))

# Function to combine binary values into a single column
def combine_columns(a, b, c):
    if 1 in [a, b, c]:
        return 1
    elif 0 in [a, b, c]:
        return 0
    else:
        return np.nan

# Apply the combine function to create the 'Contains_palmitatess' column using numeric variables
dfnew['Contains_mnOil'] = [combine_columns(a, b, c) for a, b, c in zip(abouts_mnOil, high_mnOil, ing_mnOil)]

# Flatten the lists in the new columns to single sentences
dfnew['NMNO_Abouts'] = dfnew['NMNO_Abouts'].apply(lambda x: x[0] if x else np.nan)
dfnew['NMNO_High'] = dfnew['NMNO_High'].apply(lambda x: x[0] if x else np.nan)
dfnew['NMNO_Ing'] = dfnew['NMNO_Ing'].apply(lambda x: x[0] if x else np.nan)


dfnew[dfnew['Contains_mnOil'] == 1].count()
dfnew[dfnew['Contains_mnOil'] == 0].count()

dfnew[dfnew['Contains_mnOil'] == 1].index

dfnew_clean_toCsv = dfnew[['Abouts', 'Highlights', 'Ingredients', 'Contains_Formaldehydes', 'Contains_phthalates', 'Contains_palmitates', 'Contains_mnOil']].copy()

dfnew_clean_toCsv.to_csv('allBinaryValues_exceptParabens.csv')

dfnew.to_csv('allBinaryValues_exceptParabens_unclean.csv')
