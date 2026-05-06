#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Epic Story Animator
Generates cinematic historical story animations from text
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

from config import *
from modules.ollama_processor import OllamaProcessor
from modules.scene_generator import SceneGenerator
from modules.image_processor import ImageProcessor
from modules.video_composer import VideoComposer


class EpicStoryAnimator:
    """Main orchestrator for the animation pipeline"""
    
    def __init__(self):
        self.ollama = OllamaProcessor()
        self.scene_gen = SceneGenerator()
        self.img_processor = ImageProcessor()
        self.video_composer = VideoComposer()
        
        # Setup directories
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        Path(TEMP_DIR).mkdir(exist_ok=True)
        
        print("✅ Epic Story Animator initialized")
    
    def process(self, story_text):
        """Main pipeline to convert story text to animated video"""
        print("\n🎬 Starting animation pipeline...\n")
        
        # Step 1: Parse story with Ollama
        print("📖 Step 1: Parsing story with Ollama...")
        scenes_data = self.ollama.parse_story(story_text)
        
        if not scenes_data:
            print("❌ Failed to parse story")
            return None
        
        print(f"✅ Generated {len(scenes_data)} scenes\n")
        
        # Step 2: Generate scenes with Manim
        print("🎨 Step 2: Generating Manim animations...")
        scene_videos = []
        for i, scene in enumerate(scenes_data):
            print(f"   Rendering scene {i+1}/{len(scenes_data)}: {scene['title']}")
            video_path = self.scene_gen.create_scene(scene, i)
            if video_path:
                scene_videos.append(video_path)
        
        print(f"✅ Generated {len(scene_videos)} animation videos\n")
        
        # Step 3: Fetch and process historical images
        print("🖼️  Step 3: Fetching and processing images...")
        image_data = self.img_processor.fetch_images(scenes_data)
        processed_images = self.img_processor.enhance_images(image_data)
        print(f"✅ Processed {len(processed_images)} images\n")
        
        # Step 4: Compose final video
        print("🎬 Step 4: Composing final video...")
        output_video = self.video_composer.compose(
            scene_videos, 
            processed_images, 
            scenes_data
        )
        
        if output_video:
            print(f"✅ Final video saved: {output_video}\n")
            return output_video
        else:
            print("❌ Failed to compose video")
            return None
    
    def cleanup(self):
        """Clean temporary files"""
        import shutil
        if Path(TEMP_DIR).exists():
            shutil.rmtree(TEMP_DIR)
            print("🧹 Cleaned temporary files")


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           🎬 EPIC STORY ANIMATOR 🎬                         ║
    ║     Convert Historical Stories to Cinematic Animations      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Get story input
    if len(sys.argv) > 1:
        story_text = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your historical story (press Enter twice to finish):\n")
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    if lines and lines[-1] == "":
                        break
                lines.append(line)
            except EOFError:
                break
        story_text = "\n".join(lines).strip()
    
    if not story_text:
        print("❌ No story provided!")
        sys.exit(1)
    
    print(f"\n📖 Story received ({len(story_text)} characters)\n")
    
    # Process
    animator = EpicStoryAnimator()
    try:
        result = animator.process(story_text)
        if result:
            print("\n✨ Animation complete! ✨")
            print(f"📹 Video: {result}")
        else:
            print("\n❌ Animation failed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        animator.cleanup()


if __name__ == "__main__":
    main()
