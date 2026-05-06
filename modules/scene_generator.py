#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scene Generator Module
Creates cinematic animations using Manim
"""

import os
import subprocess
from pathlib import Path
from manim import *
from config import *


class CustomScene(Scene):
    """Base custom scene with cinematic styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera.background_color = BACKGROUND_COLOR
    
    def setup(self):
        """Setup scene styling"""
        self.set_background()
    
    def set_background(self):
        """Set cinematic background"""
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BACKGROUND_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        self.add(bg)


class HistoricalMapScene(CustomScene):
    """Scene showing historical map with markers and highlights"""
    
    def __init__(self, title, description, *args, **kwargs):
        self.title = title
        self.description = description
        super().__init__(*args, **kwargs)
    
    def construct(self):
        """Construct the map animation"""
        # Title
        title_text = Text(self.title, font_size=60, color=PRIMARY_COLOR)
        title_text.to_edge(UP, buff=0.5)
        
        # Description
        desc_text = Text(self.description, font_size=28, color=WHITE, t2c={"": WHITE})
        desc_text.next_to(title_text, DOWN, buff=0.8)
        desc_text.width = config.frame_width - 1
        
        # Animate in
        self.play(Write(title_text), run_time=1.5)
        self.play(FadeIn(desc_text), run_time=1)
        
        # Hold
        self.wait(2)
        
        # Animate out
        self.play(FadeOut(title_text), FadeOut(desc_text), run_time=1)


class TimelineScene(CustomScene):
    """Scene showing a historical timeline"""
    
    def __init__(self, title, events, *args, **kwargs):
        self.title = title
        self.events = events  # List of (year, event) tuples
        super().__init__(*args, **kwargs)
    
    def construct(self):
        """Construct the timeline animation"""
        # Title
        title = Text(self.title, font_size=50, color=PRIMARY_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        
        # Timeline line
        timeline = Line(
            start=LEFT * 4 + DOWN * 2,
            end=RIGHT * 4 + DOWN * 2,
            stroke_color=SECONDARY_COLOR,
            stroke_width=3
        )
        self.play(Create(timeline), run_time=1.5)
        
        # Events
        num_events = min(len(self.events), 3)  # Limit to 3 events
        for i, (year, event) in enumerate(self.events[:num_events]):
            x_pos = -3 + (i * 3)
            
            # Dot
            dot = Dot(point=[x_pos, -2, 0], radius=0.2, color=ACCENT_COLOR)
            
            # Year label
            year_text = Text(str(year), font_size=24, color=PRIMARY_COLOR)
            year_text.next_to(dot, DOWN, buff=0.3)
            
            # Event text
            event_text = Text(event[:30], font_size=16, color=WHITE)
            event_text.next_to(year_text, DOWN, buff=0.2)
            
            self.play(Create(dot), run_time=0.5)
            self.play(Write(year_text), Write(event_text), run_time=0.8)
            self.wait(0.5)
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(timeline), run_time=1)


class GraphScene(CustomScene):
    """Scene showing data visualization"""
    
    def __init__(self, title, data_points, *args, **kwargs):
        self.title = title
        self.data_points = data_points
        super().__init__(*args, **kwargs)
    
    def construct(self):
        """Construct the graph animation"""
        # Title
        title = Text(self.title, font_size=50, color=PRIMARY_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"color": SECONDARY_COLOR, "stroke_width": 2},
            tips=False,
        )
        axes.scale(0.5)
        axes.to_edge(DOWN)
        
        self.play(Create(axes), run_time=1)
        
        # Plot points with animation
        for i, point in enumerate(self.data_points[:5]):  # Limit to 5 points
            dot = Dot(
                point=axes.coords_to_point(point[0], point[1]),
                radius=0.15,
                color=ACCENT_COLOR
            )
            self.play(Create(dot), run_time=0.5)
            self.wait(0.3)
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(axes), run_time=1)


class TextRevealScene(CustomScene):
    """Scene with text reveal animation"""
    
    def __init__(self, title, text_content, *args, **kwargs):
        self.title = title
        self.text_content = text_content
        super().__init__(*args, **kwargs)
    
    def construct(self):
        """Construct the text reveal animation"""
        # Title
        title = Text(self.title, font_size=50, color=PRIMARY_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        
        # Main text
        content = Text(self.text_content, font_size=28, color=WHITE)
        content.width = config.frame_width - 1
        content.next_to(title, DOWN, buff=1)
        
        self.play(Write(content), run_time=3)
        self.wait(1.5)
        
        self.play(FadeOut(title), FadeOut(content), run_time=1)


class SceneGenerator:
    """Generate Manim scenes for story"""
    
    def __init__(self):
        self.temp_dir = Path(TEMP_DIR) / "scenes"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def create_scene(self, scene_data, scene_index):
        """
        Create a single scene animation
        
        Args:
            scene_data: Dict with scene metadata
            scene_index: Index of scene
        
        Returns:
            Path to rendered video file
        """
        
        title = scene_data.get("title", f"Scene {scene_index + 1}")
        description = scene_data.get("description", "")
        animation_type = scene_data.get("animation_type", "text_reveal")
        
        # Create scene file
        scene_class_name = f"Scene_{scene_index}"
        py_file = self.temp_dir / f"scene_{scene_index}.py"
        
        # Generate scene code based on animation type
        scene_code = self._generate_scene_code(
            scene_class_name,
            animation_type,
            title,
            description
        )
        
        # Write scene file
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(scene_code)
        
        # Render with manim
        output_file = self.temp_dir / f"scene_{scene_index}.mp4"
        
        try:
            cmd = [
                "manim",
                "-q", "h",  # High quality, no preview
                "-o", f"scene_{scene_index}.mp4",
                str(py_file),
                scene_class_name
            ]
            
            result = subprocess.run(
                cmd,
                cwd=str(self.temp_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # Find the rendered video
                render_dir = self.temp_dir / "videos"
                if render_dir.exists():
                    for video in render_dir.rglob("*.mp4"):
                        return str(video)
            else:
                print(f"⚠️  Manim render warning: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            print(f"⚠️  Scene {scene_index} render timeout")
        except Exception as e:
            print(f"⚠️  Error rendering scene {scene_index}: {e}")
        
        return None
    
    def _generate_scene_code(self, class_name, anim_type, title, description):
        """Generate Python code for Manim scene"""
        
        code = f'''
from manim import *

class {class_name}(Scene):
    def construct(self):
        self.camera.background_color = "{BACKGROUND_COLOR}"
        
        # Title
        title = Text("{title}", font_size=50, color="{PRIMARY_COLOR}")
        title.to_edge(UP, buff=0.5)
        
        # Description
        desc = Text("{description[:80]}", font_size=28, color=WHITE)
        desc.next_to(title, DOWN, buff=0.5)
        desc.width = config.frame_width - 1
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(desc), run_time=1)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(desc), run_time=1)
'''
        
        return code
