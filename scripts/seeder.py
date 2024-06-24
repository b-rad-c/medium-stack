#!/usr/bin/env python3
import os
import random

from typing import List
from pathlib import Path
from glob import glob

from mcore.db import MongoDB
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
            self.db = MongoDB.from_cache()

            self.users:List[User] = []
            self.artists:List[Artist] = []

            self.image_paths:List[Path] = []
            self.still_images:List[StillImage] = []
            self._load_image_samples()

        #
        # util methods
        #

        def _load_image_samples(self):
            pattern = (IMAGE_SAMPLE_SOURCES / '*').absolute()
            for path in glob(str(pattern)):
                self.image_paths.append(Path(path))
            
            random.shuffle(self.image_paths)

        def _next_image_path(self) -> Path:
            path = self.image_paths.pop(0)
            self.image_paths.append(path)
            return path
        
        #
        # seeder methods
        #
    
        def seed(self):
            for _ in range(5):
                user = self.seed_user()

        def seed_user(self) -> User:
            user_creator = UserCreator.generate()
            user = self.mstack.user_create(user_creator)
            self.users.append(user)

            self.mstack.login(user.email, user_creator.password1)

            # populate FileUploaders
            for _ in range(random.randint(1, 3)):
                self.mstack.upload_file(self._next_image_path(), FileUploadTypes.image)

            self.seed_artist(user)

            return user
    
        def seed_artist(self, user:User):
            artist_creator = ArtistCreator.generate(user)
            artist = self.mstack.create_artist(artist_creator)
            self.artists.append(artist)

            self.seed_still_images(artist)
    

        def seed_still_images(self, artist:Artist):
            for _ in range(random.randint(3, 10)):

                image_release_creator = self.seed_image_release(artist)
                image_release = self.mstack.create_image_release(image_release_creator)

                still_image_creator = StillImageCreator(
                    creator_id=artist.cid,
                    release=image_release.cid,
                    title=TitleData.generate(),
                    credits=[Credit.generate() for _ in range(random.randint(1, 5))],
                    genres=random_genres(genres=art_genres),
                    tags=random_tags(),
                    alt_text=lorem.sentence(),
                )

                still_image = self.mstack.create_still_image(still_image_creator)
                self.still_images.append(still_image)


        def seed_image_release(self, artist:Artist) -> ImageRelease:
            master_path = self._next_image_path()

            pattern = str(master_path.parent.parent / 'thumbs' / f'{master_path.stem}*')
            alt_paths = glob(pattern)
            assert len(alt_paths) > 0

            master = ImageFile.ingest(master_path, user_cid=artist.user_cid, leave_original=True)
            self.db.create(master)

            alts = []
            for alt_path in alt_paths:
                alt = ImageFile.ingest(alt_path, user_cid=artist.user_cid, leave_original=True)
                self.db.create(alt)
                alts.append(alt)

            return ImageReleaseCreator(
                master=master.cid,
                alt_formats=[alt.cid for alt in alts]
            )

if __name__ == '__main__':
    seeder = DataSeeder()
    seeder.seed()
