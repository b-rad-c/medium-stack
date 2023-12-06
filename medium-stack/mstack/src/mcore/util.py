import datetime
import signal
import time
import random

from collections import namedtuple

from mcore.types import ContentId

from pydantic import BaseModel
from lorem_text import lorem

__all__ = [
    'utc_now',
    'DaemonController',

    'example_model',
    'example_cid',

    'first_names_male',
    'first_names_female',
    'first_names',
    'last_names',
    'adjectives',
    'nouns',
    'words',
    'domains',
    'art_genres',
    'music_genres',
    'Name',
    'random_name',
    'random_email',
    'random_phone_number',
    'random_tags',
    'random_genres'
]

def utc_now():
    """mongodb returns timezone unaware objects with less precision that datetime,
    this hack creates utc timestamps that will be the same before and after mongo
    ensure that pydantic models can be compared for equality
    """
    date = datetime.datetime.now(datetime.timezone.utc)
    micro = str(date.microsecond)
    return date.replace(microsecond=int(micro[0:3] + '000'), tzinfo=None)

class DaemonController:

    def __init__(self):
        self.run_daemon = True
        signal.signal(signal.SIGTERM, self.handle_sigterm)

    def handle_sigterm(self, signum, frame):
        print(f"Caught signal {signum}...")
        self.run_daemon = False

    def sleep(self, duration:float, sleep_interval:float = 0.1):
        end_time = time.time() + duration
        while time.time() < end_time and self.run_daemon:
            time.sleep(sleep_interval)

#
# examples
#


def example_model(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    return model_type(**example)

def example_cid(model_type:BaseModel, index=0):
    try:
        example = model_type.model_json_schema()['examples'][index]
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not have examples defined')
    except IndexError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define example at index: {index}')
    
    try:
        cid = example['cid']
    except KeyError:
        raise AssertionError(f'model {model_type.__class__.__name__} does not define a cid in the example at index: {index}')
    
    return ContentId.parse(cid)


#
# randomization for generators
#

first_names_male = [
    'John',
    'James',
    'Robert',
    'Michael',
    'William',
    'Christopher',
    'Daniel',
    'Joshua',
    'David',
    'Andrew',
    'Richard',
    'Matthew',
    'Joseph',
    'Thomas',
    'José',
    'Charles',
    'Oscar',
    'Manuel',
    'Jorge',
    'Salmon',
    'Kevin',
    'Brian',
    'Jason',
    'Jeffrey'
]

first_names_female = [
    'Mary',
    'Patricia',
    'Jennifer',
    'Elizabeth',
    'Linda',
    'Barbara',
    'Susan',
    'Jessica',
    'Sarah',
    'Karen',
    'Nancy',
    'Lisa',
    'Betty',
    'Margaret',
    'Sandra',
    'Ashley',
    'Dorothy',
    'Kimberly',
    'Emily',
    'Donna',
    'Michelle',
    'Carol',
    'Amanda',
    'Melissa',
    'Deborah'
]

first_names = first_names_male + first_names_female

last_names = [
    'Smith',
    'Johnson',
    'Williams',
    'Brown',
    'Jones',
    'García',
    'Miller',
    'Davis',
    'Rodríguez',
    'Martínez',
    'Hernández',
    'López',
    'González',
    'Wilson',
    'Anderson',
    'Thomas',
    'Taylor',
    'Moore',
    'Jackson',
    'Martin',
    'Lee',
    'Pérez',
    'Thompson',
    'White',
    'Harris',
    'Sánchez'
]

nouns = [
    'apple',
    'cheese',
    'banana',
    'cherry',
    'soccer',
    'kite',
    'dog',
    'hill',
    'mountain',
    'river',
    'slime'
]

adjectives = [
    'big',
    'small',
    'fast',
    'slow',
    'red',
    'blue',
    'slimey'
]

words = nouns + adjectives

domains = [
    'bigemailcorp.com',
    'example.com',
    'bigtech.com',
    'bigbank.com',
    'biginsurance.com',
    'snailmail.com'
]

art_genres = [
    'surrealism',
    'impressionism',
    'expressionism',
    'cubism',
    'abstract',
    'pop art',
    'minimalism',
    'fauvism',
    'realism',
    'post-impressionism',
    'art nouveau'
]

music_genres = [
    'rock',
    'pop',
    'rap',
    'country',
    'jazz',
    'blues',
    'classical',
    'metal',
    'electronic',
    'folk'
]

Name = namedtuple('Person', ['first', 'middle', 'last'])

def random_name() -> Name:
    # get male or female names
    if random.randint(0, 1) == 0:
        names = first_names_male
    else:
        names = first_names_female 

    # middle
    seed = random.randint(0, 8)
    if seed in [0, 1, 2]:
        middle = random.choice(names)
    elif seed in [3, 4, 5]:
        middle = random.choice(names)[0]
    elif seed == 6:
        middle = f'{random.choice(names)} {random.choice(names)}'
    elif seed == 7:
        middle = f'{random.choice(names)[0]}. {random.choice(names)[0]}.'
    else:
       middle = f'{random.choice(names)[0]}.'
    
    return Name(first=random.choice(names), middle=middle, last=random.choice(last_names))

def random_email(name:Name = None) -> str:
    if name is None:
        name = random_name()

    seed = random.randint(0, 5)
    if seed == 0:
        return f'{name.first}.{name.last}@{random.choice(domains)}'
    elif seed == 2:
        return f'{name.first[0]}{name.last}@{random.choice(domains)}'
    elif seed == 3:
        return f'{name.first[0]}_{name.last}{random.randint(0, 999)}@{random.choice(domains)}'
    elif seed == 4:
        return f'{random.choice(words)}_{name.last}{random.randint(0, 999)}@{random.choice(domains)}'
    else:
        return f'{random.choice(words)}_{random.choice(words)}@{random.choice(domains)}'

def random_phone_number() -> str:
    area_codes = ['513', '616', '213', '312', '404', '502', '614', '317']
    return f'tel:+1-{random.choice(area_codes)}-555-{random.randint(1000, 9999)}'

def random_tags(number:int=None):
    if number is None:
        number = random.randint(1, 5)
    tags = []
    for _ in range(number):
        while True:
            tag = lorem.words(1)
            if tag not in tags:
                tags.append(tag)
                break
    return tags

def random_genres(number:int=None, genres=None):
    if number is None:
        number = random.randint(1, 5)
        
    if genres is None:
        genres = art_genres + music_genres
    
    if number > len(genres):
        raise ValueError(f'number of genres requested ({number}) is greater than the number of genres available ({len(genres)})')

    genres = []
    for _ in range(number):
        while True:
            genre = lorem.words(1)
            if genre not in genres:
                genres.append(genre)
                break

    return genres