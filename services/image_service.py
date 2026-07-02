from typing import Optional, List
from pathlib import Path
import shutil
import uuid
from PIL import Image

from models.hero import Hero, HeroImage
from database.database import Database
from config import load_config


class ImageService:
    def __init__(self, database: Database):
        self.db = database
        self.config = load_config()
        self.images_dir = Path(self.config.data_dir) / self.config.images_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.max_size = (512, 512)
        self.thumbnail_size = (128, 128)

    def add_image_to_hero(self, hero: Hero, source_path: Path,
                          is_primary: bool = False, caption: str = "") -> Optional[HeroImage]:
        if not source_path.exists():
            return None

        hero_dir = self.images_dir / hero.id
        hero_dir.mkdir(parents=True, exist_ok=True)

        ext = source_path.suffix.lower()
        if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']:
            ext = '.png'

        new_filename = f"{uuid.uuid4().hex}{ext}"
        dest_path = hero_dir / new_filename

        try:
            with Image.open(source_path) as img:
                img = img.convert('RGBA')
                img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                img.save(dest_path, 'PNG')
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

        if is_primary:
            for img in hero.images:
                img.is_primary = False

        new_image = HeroImage(
            hero_id=hero.id,
            image_path=str(dest_path.relative_to(self.images_dir)),
            is_primary=is_primary,
            caption=caption,
            order=len(hero.images)
        )

        hero.images.append(new_image)
        return new_image

    def remove_image(self, hero: Hero, image_id: str) -> bool:
        image = None
        for img in hero.images:
            if img.id == image_id:
                image = img
                break

        if not image:
            return False

        image_path = self.images_dir / image.image_path
        if image_path.exists():
            image_path.unlink()

        hero.images = [img for img in hero.images if img.id != image_id]

        if image.is_primary and hero.images:
            hero.images[0].is_primary = True

        return True

    def set_primary_image(self, hero: Hero, image_id: str) -> bool:
        for img in hero.images:
            img.is_primary = (img.id == image_id)
        return True

    def get_image_path(self, hero: Hero, image_id: Optional[str] = None) -> Optional[Path]:
        if image_id:
            for img in hero.images:
                if img.id == image_id:
                    return self.images_dir / img.image_path

        primary = hero.get_primary_image()
        if primary:
            return self.images_dir / primary.image_path

        if hero.images:
            return self.images_dir / hero.images[0].image_path

        return None

    def get_thumbnail(self, hero: Hero, image_id: Optional[str] = None,
                      size: tuple = None) -> Optional[Image.Image]:
        size = size or self.thumbnail_size
        image_path = self.get_image_path(hero, image_id)

        if not image_path or not image_path.exists():
            return None

        try:
            with Image.open(image_path) as img:
                img = img.convert('RGBA')
                img.thumbnail(size, Image.Resampling.LANCZOS)
                return img.copy()
        except Exception:
            return None

    def copy_image(self, source_hero: Hero, target_hero: Hero,
                   image_id: str, is_primary: bool = False) -> Optional[HeroImage]:
        for img in source_hero.images:
            if img.id == image_id:
                source_path = self.images_dir / img.image_path
                if source_path.exists():
                    target_dir = self.images_dir / target_hero.id
                    target_dir.mkdir(parents=True, exist_ok=True)

                    new_filename = f"{uuid.uuid4().hex}{source_path.suffix}"
                    dest_path = target_dir / new_filename
                    shutil.copy2(source_path, dest_path)

                    new_image = HeroImage(
                        hero_id=target_hero.id,
                        image_path=str(dest_path.relative_to(self.images_dir)),
                        is_primary=is_primary,
                        caption=img.caption,
                        order=len(target_hero.images)
                    )

                    if is_primary:
                        for ti in target_hero.images:
                            ti.is_primary = False

                    target_hero.images.append(new_image)
                    return new_image

        return None

    def get_all_hero_images(self, hero: Hero) -> List[HeroImage]:
        return hero.images

    def cleanup_orphaned_images(self) -> int:
        used_paths = set()
        for hero in self.db.heroes:
            for img in hero.images:
                used_paths.add(img.image_path)

        count = 0
        for hero_dir in self.images_dir.iterdir():
            if hero_dir.is_dir():
                for img_file in hero_dir.iterdir():
                    rel_path = img_file.relative_to(self.images_dir)
                    if str(rel_path) not in used_paths:
                        img_file.unlink()
                        count += 1

                try:
                    hero_dir.rmdir()
                except OSError:
                    pass

        return count