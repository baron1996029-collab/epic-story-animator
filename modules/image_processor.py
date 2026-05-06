#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processor Module
Fetches and processes historical images from Wikimedia
"""

import os
import requests
from pathlib import Path
from PIL import Image, ImageEnhance
from io import BytesIO
from config import TEMP_DIR


class ImageProcessor:
    """Fetch and enhance historical images"""
    
    def __init__(self):
        self.temp_dir = Path(TEMP_DIR) / "images"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Epic-Story-Animator/1.0'
        })
    
    def fetch_images(self, scenes_data):
        """
        Fetch images from Wikimedia Commons for each scene
        
        Args:
            scenes_data: List of scene dictionaries
        
        Returns:
            Dict mapping scene index to list of image paths
        """
        
        images_by_scene = {}
        
        for scene_idx, scene in enumerate(scenes_data):
            keywords = scene.get("keywords", [])
            images = []
            
            for keyword in keywords[:2]:  # Limit to 2 keywords per scene
                image_path = self._fetch_from_wikimedia(keyword, scene_idx)
                if image_path:
                    images.append(image_path)
            
            if images:
                images_by_scene[scene_idx] = images
        
        return images_by_scene
    
    def _fetch_from_wikimedia(self, query, scene_idx):
        """
        Fetch image from Wikimedia Commons
        
        Args:
            query: Search query (in Arabic)
            scene_idx: Scene index
        
        Returns:
            Path to downloaded image or None
        """
        
        try:
            # Wikimedia API endpoint
            url = "https://commons.wikimedia.org/w/api.php"
            
            params = {
                "action": "query",
                "list": "allimages",
                "aisort": "timestamp",
                "aidir": "descending",
                "ailimit": 5,
                "aifrom": query,
                "format": "json"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            images = data.get("query", {}).get("allimages", [])
            
            if not images:
                return None
            
            # Get first image
            image_title = images[0]["name"]
            image_url = self._get_image_url(image_title)
            
            if image_url:
                return self._download_image(image_url, scene_idx, query)
            
            return None
        
        except Exception as e:
            print(f"⚠️  Error fetching image for '{query}': {e}")
            return None
    
    def _get_image_url(self, image_title):
        """Get direct image URL from Wikimedia title"""
        
        try:
            url = "https://commons.wikimedia.org/w/api.php"
            
            params = {
                "action": "query",
                "titles": f"File:{image_title}",
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            
            for page in pages.values():
                imageinfo = page.get("imageinfo", [])
                if imageinfo:
                    return imageinfo[0].get("url")
            
            return None
        
        except Exception as e:
            print(f"⚠️  Error getting image URL: {e}")
            return None
    
    def _download_image(self, image_url, scene_idx, query):
        """
        Download and save image
        
        Args:
            image_url: URL to image
            scene_idx: Scene index
            query: Original search query
        
        Returns:
            Path to saved image
        """
        
        try:
            response = self.session.get(image_url, timeout=15)
            
            if response.status_code != 200:
                return None
            
            # Save image
            img_name = f"scene_{scene_idx}_{query.replace(' ', '_')}.jpg"
            img_path = self.temp_dir / img_name
            
            with open(img_path, "wb") as f:
                f.write(response.content)
            
            return str(img_path)
        
        except Exception as e:
            print(f"⚠️  Error downloading image: {e}")
            return None
    
    def enhance_images(self, images_by_scene):
        """
        Enhance downloaded images for better cinematic quality
        
        Args:
            images_by_scene: Dict of scene index -> image paths
        
        Returns:
            Dict of enhanced image paths
        """
        
        enhanced = {}
        
        for scene_idx, image_paths in images_by_scene.items():
            enhanced_paths = []
            
            for img_path in image_paths:
                try:
                    enhanced_path = self._enhance_single_image(img_path, scene_idx)
                    if enhanced_path:
                        enhanced_paths.append(enhanced_path)
                
                except Exception as e:
                    print(f"⚠️  Error enhancing {img_path}: {e}")
            
            if enhanced_paths:
                enhanced[scene_idx] = enhanced_paths
        
        return enhanced
    
    def _enhance_single_image(self, img_path, scene_idx):
        """
        Enhance a single image
        
        Args:
            img_path: Path to original image
            scene_idx: Scene index
        
        Returns:
            Path to enhanced image
        """
        
        try:
            # Open image
            img = Image.open(img_path)
            
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (0, 0, 0))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            
            # Enhance color
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.15)
            
            # Resize to fit video (16:9 ratio)
            target_width = 1920
            target_height = 1080
            
            img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Create new image with proper dimensions
            final_img = Image.new('RGB', (target_width, target_height), (11, 0, 20))
            
            # Paste enhanced image centered
            x = (target_width - img.width) // 2
            y = (target_height - img.height) // 2
            final_img.paste(img, (x, y))
            
            # Save enhanced image
            enhanced_name = f"enhanced_scene_{scene_idx}_{Path(img_path).stem}.jpg"
            enhanced_path = self.temp_dir / enhanced_name
            
            final_img.save(enhanced_path, quality=95)
            
            return str(enhanced_path)
        
        except Exception as e:
            print(f"⚠️  Enhancement error for {img_path}: {e}")
            return None
