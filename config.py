import pandas as pd
# GDELT 2.0 base URL
GDELT_BASE = "http://data.gdeltproject.org/gdeltv2/"


# Where to store downloaded files
DATA_DIR = "data/gdelt_raw/" #stores unparsed datasets
PARSED_DIR = "data/gdelt_parsed/" #stores the parsed datasets
OUTPUT_DIR = "data/combined_datasets/" #stores the final combined dataset
CACHE_DIR = "data/cache/"
CACHE_FILTERED = "data/cache/filtered"
CACHE_ZIP_DIR = "data/cache/zips/"
CACHE_PARSED_DIR = "data/cache/parsed/"
# Themes relevant to crime/policing
CRIME_THEMES = ["CRIME", "VIOLENCE", "POLICE", "LAW_ENFORCEMENT", "SECURITY",
    "ASSAULT", "MURDER", "HOMICIDE", "SHOOTING", "STABBING",
    "KIDNAPPING", "ROBBERY", "BURGLARY", "ARSON",
    "ARREST", "RAID", "INVESTIGATION", "SECURITY_FORCES",
    "TERROR", "TERRORISM", "EXTREMISM", "BOMBING", "EXPLOSION",
    "COURT", "TRIAL", "SENTENCING", "PROSECUTION", "JUDICIARY",
    "PUBLIC_SAFETY", "EMERGENCY_SERVICES", "FIRE_DEPARTMENT"
]

GKG_COLS = [
    "GKGRECORDID","V2.1DATE","V2SOURCECOLLECTIONIDENTIFIER","V2SOURCECOMMONNAME",
    "V2DOCUMENTIDENTIFIER","V1COUNTS","V2.1COUNTS","V1THEMES","V2ENHANCEDTHEMES",
    "V1LOCATIONS","V2ENHANCEDLOCATIONS","V1PERSONS","V2ENHANCEDPERSONS",
    "V1ORGANIZATIONS","V2ENHANCEDORGANIZATIONS","V1.5TONE","V2.1ENHANCEDDATES",
    "V2GCAM","V2.1SHARINGIMAGE","V2.1RELATEDIMAGES","V2.1SOCIALIMAGEEMBEDS",
    "V2.1SOCIALVIDEOEMBEDS","V2.1QUOTATIONS","V2.1ALLNAMES","V2.1AMOUNTS",
    "V2.1TRANSLATIONINFO","V2EXTRASXML"
]

#list of the 50 most popular websites for British readers.
UK_SITES = [
    "BBC.CO.UK",
    "THEGUARDIAN.COM",
    "THESUN.CO.UK",
    "MIRROR.CO.UK",
    "INDEPENDENT.CO.UK",
    "DAILYMAIL.CO.UK",
    "NEWS.SKY.COM",
    "TELEGRAPH.CO.UK",
    "EXPRESS.CO.UK",
    "UK.NEWS.YAHOO.COM",
    "ITV.COM/NEWS",
    "MONEYSAVINGEXPERT.COM",
    "BBCGOODFOOD.COM",
    "METRO.CO.UK",
    "THETIMES.CO.UK",
    "MANCHESTEREVENINGNEWS.CO.UK",
    "STANDARD.CO.UK",
    "DAILYSTAR.CO.UK",
    "NYTIMES.COM",
    "BIRMINGHAMMAIL.CO.UK",
    "INEWS.CO.UK",
    "CHANNEL4.COM/NEWS",
    "RADIOTIMES.COM",
    "DAILYRECORD.CO.UK",
    "FORBES.COM",
    "MYLONDON.NEWS",
    "OK.CO.UK",
    "PEOPLE.COM",
    "REUTERS.COM",
    "SCREENRANT.COM",
    "SUBSTACK.COM",
    "TECHRADAR.COM",
    "TIMEOUT.COM",
    "WALESONLINE.CO.UK",
    "WHICH.CO.UK"
]
GREATER_LONDON_LOC = [
    "LONDON",
    "CITY OF LONDON",
    "WESTMINSTER",
    "CAMDEN",
    "ISLINGTON",
    "HACKNEY",
    "TOWER HAMLETS",
    "GREENWICH",
    "LEWISHAM",
    "SOUTHWARK",
    "LAMBETH",
    "WANDSWORTH",
    "HAMMERSMITH",
    "FULHAM",
    "KENSINGTON",
    "CHELSEA",
    "BRENT",
    "EALING",
    "HOUNSLOW",
    "RICHMOND",
    "KINGSTON",
    "MERTON",
    "SUTTON",
    "CROYDON",
    "BROMLEY",
    "BARNET",
    "HARROW",
    "HILLINGDON",
    "ENFIELD",
    "WALTHAM FOREST",
    "REDBRIDGE",
    "NEWHAM",
    "BARKING",
    "DAGENHAM",
    "HAVERING",

    # Surrounding areas
    "WATFORD",
    "BASILDON",
    "SLOUGH",
    "WINDSOR",
    "MAIDENHEAD",
    "ST ALBANS",
    "HERTFORD",
    "BROXBOURNE",
    "EPPING",
    "EPPING FOREST",
    "DARTFORD",
    "SEVENOAKS",
    "EPSOM",
    "EWELL",
    "REIGATE",
    "BANSTEAD",
    "WOKING",
    "GUILDFORD",
    "HIGH WYCOMBE",
    "AMERSHAM",
    "CHESHAM",
]
