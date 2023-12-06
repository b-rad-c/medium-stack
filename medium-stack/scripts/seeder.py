#!/usr/bin/env python3
import os
import random

from typing import List
from pathlib import Path
from glob import glob

from mcore.client import MStackClient
from mcore.models import *
from mart.models import *
from mcore.util import art_genres, random_tags, random_genres

from lorem_text import lorem


_MCORE_SAMPLE_DATA_DIR = '/app/samples'
MCORE_SAMPLE_DATA_DIR = Path(os.environ.get('MCORE_SAMPLE_DATA_DIR', _MCORE_SAMPLE_DATA_DIR))

IMAGE_SAMPLE_SOURCES = MCORE_SAMPLE_DATA_DIR / 'files' / 'images' / 'src'
IMAGE_SAMPLE_THUMBS = MCORE_SAMPLE_DATA_DIR / 'files' / 'images' / 'thumbs'


class DataSeeder:
    
        def __init__(self):
            self.mstack = MStackClient()

            self.users:List[User] = []
            self.artists:List[Artist] = []

            self.image_paths:List[Path] = []
            self.still_images:List[StillImage] = []
            self._load_image_samples()
    
        def seed(self):
            self.seed_users()
            self.seed_artists()
            self.seed_still_images()
    
        def seed_users(self):
            for _ in range(10):
                user_creator = UserCreator.generate()
                user = self.mstack.create_user(user_creator)
                self.users.append(user)
            
            random.shuffle(self.users)
    
        def seed_artists(self):
            count = int(len(self.users) * (2/3))
            for user in self.users[:count]:
                artist_creator = ArtistCreator.generate(user)
                artist = self.mstack.create_artist(artist_creator)
                self.artists.append(artist)
    

        def seed_still_images(self):
            for artist in self.artists:
                for _ in range(random.randint(3, 25)):
                    still_image_creator = StillImageCreator(
                        creator_id=artist.cid,
                        release=self._get_image_release(artist).cid,
                        title=TitleData.generate(),
                        credits=[Credit.generate() for _ in range(random.randint(1, 5))],
                        genres=random_genres(genres=art_genres),
                        tags=random_tags(),
                        alt_text=lorem.sentence(),
                    )
                    still_image = self.mstack.create_still_image(still_image_creator)
                    self.still_images.append(still_image)

        def _load_image_samples(self):
            pattern = (IMAGE_SAMPLE_SOURCES / '*').absolute()
            for path in glob(str(pattern)):
                self.image_paths.append(Path(path))
            
            random.shuffle(self.image_paths)

        def _get_image_release(self, artist:Artist) -> ImageRelease:
            master_path = self.image_paths.pop()
            pattern = str(master_path.parent.parent / 'thumbs' / f'{master_path.stem}*')
            alt_paths = glob(pattern)
            assert len(alt_paths) > 0

            master = ImageFile.ingest(master_path, user_cid=artist.user_cid)
            alts = [ImageFile.ingest(path, user_cid=artist.user_cid) for path in alt_paths]

            return ImageRelease(
                master=master.cid,
                alts=[alt.cid for alt in alts]
            )

if __name__ == '__main__':
    seeder = DataSeeder()
    seeder.seed()
    breakpoint()

