#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Composer Module
Combines all scenes, images, and transitions into final video
"""

import os
from pathlib import Path
from moviepy.editor import (
    VideoFileClip, ImageClip, CompositeVideoClip,
    concatenate_videoclips, TransitionVideoClip
)
from datetime import datetime
from config import OUTPUT_DIR, TEMP_DIR, VIDEO_FPS, MAX_VIDEO_DURATION


class VideoComposer:
    """Compose final video from scene clips and images"""
    
    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path(TEMP_DIR)
    
    def compose(self, scene_videos, image_data, scenes_metadata):
        """
        Compose final video from all components
        
        Args:
            scene_videos: List of paths to scene video files
            image_data: Dict of scene index -> image paths
            scenes_metadata: List of scene metadata dicts
        
        Returns:
            Path to final output video or None
        """
        
        if not scene_videos:
            print("❌ No scene videos to compose")
            return None
        
        try:
            # Load and prepare clips
            clips = []
            
            for i, video_path in enumerate(scene_videos):
                try:
                    # Load scene video
                    scene_clip = VideoFileClip(video_path)
                    
                    # Get duration from metadata if available
                    if scenes_metadata and i < len(scenes_metadata):
                        target_duration = scenes_metadata[i].get("duration", 15)
                        if scene_clip.duration > target_duration:
                            scene_clip = scene_clip.subclipped(0, target_duration)
                    
                    # Add image overlay if available
                    if i in image_data and image_data[i]:
                        scene_clip = self._overlay_images(scene_clip, image_data[i])
                    
                    clips.append(scene_clip)
                
                except Exception as e:
                    print(f"⚠️  Error loading scene {i}: {e}")
                    continue
            
            if not clips:
                print("❌ Failed to load any scene clips")
                return None
            
            # Add cinematic transitions between clips
            print("🎬 Adding cinematic transitions...")
            clips_with_transitions = self._add_transitions(clips)
            
            # Concatenate all clips
            print("🎬 Concatenating clips...")
            final_video = concatenate_videoclips(clips_with_transitions, method="chain")
            
            # Limit total duration
            if final_video.duration > MAX_VIDEO_DURATION:
                print(f"⏱️  Trimming video to {MAX_VIDEO_DURATION}s...")
                final_video = final_video.subclipped(0, MAX_VIDEO_DURATION)
            
            # Set output properties
            final_video = final_video.set_fps(VIDEO_FPS)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"epic_story_{timestamp}.mp4"
            
            # Write to file
            print(f"📝 Writing video to {output_path}...")
            final_video.write_videofile(
                str(output_path),
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Cleanup
            final_video.close()
            for clip in clips:
                clip.close()
            
            print(f"✅ Video created: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"❌ Error composing video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _overlay_images(self, video_clip, image_paths):
        """
        Overlay images on video clip with cinematic effects
        
        Args:
            video_clip: VideoFileClip
            image_paths: List of image paths
        
        Returns:
            Composite video clip with images
        """
        
        try:
            duration = video_clip.duration
            
            # Calculate image display duration
            img_duration = duration / len(image_paths)
            
            # Create image clips
            image_clips = []
            for idx, img_path in enumerate(image_paths):
                try:
                    img_clip = ImageClip(img_path)
                    
                    # Resize to match video
                    img_clip = img_clip.resize(height=int(video_clip.h * 0.6))
                    
                    # Position on right side
                    img_clip = img_clip.set_position(
                        (video_clip.w - img_clip.w - 30, 30)
                    )
                    
                    # Set duration and start time
                    start_time = idx * img_duration
                    img_clip = img_clip.set_duration(img_duration)
                    img_clip = img_clip.set_start(start_time)
                    
                    image_clips.append(img_clip)
                
                except Exception as e:
                    print(f"⚠️  Error processing image {img_path}: {e}")
                    continue
            
            # Compose video with images
            if image_clips:
                composite = CompositeVideoClip(
                    [video_clip] + image_clips,
                    size=(video_clip.w, video_clip.h)
                )
                return composite
            else:
                return video_clip
        
        except Exception as e:
            print(f"⚠️  Error overlaying images: {e}")
            return video_clip
    
    def _add_transitions(self, clips, transition_type="fade"):
        """
        Add cinematic transitions between clips
        
        Args:
            clips: List of video clips
            transition_type: Type of transition
        
        Returns:
            List of clips with transitions applied
        """
        
        if len(clips) <= 1:
            return clips
        
        try:
            transition_duration = 1.0  # 1 second transitions
            result_clips = [clips[0]]
            
            for i in range(1, len(clips)):
                prev_clip = clips[i-1]
                curr_clip = clips[i]
                
                # Create transition using fade effect
                # Simple approach: overlap last frames with fade
                transition = TransitionVideoClip(
                    [prev_clip, curr_clip],
                    transition_duration,
                    transition_type
                )
                
                result_clips.append(transition)
                result_clips.append(curr_clip)
            
            return result_clips
        
        except Exception as e:
            print(f"⚠️  Error adding transitions: {e}")
            # Return original clips without transitions
            return clips
