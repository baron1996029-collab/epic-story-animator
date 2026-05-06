#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Processor Module
Handles text parsing and scene generation using Ollama
"""

import json
import requests
from config import OLLAMA_HOST, OLLAMA_MODEL, MAX_SCENES


class OllamaProcessor:
    """Process stories with Ollama to generate scene structure"""
    
    def __init__(self):
        self.host = OLLAMA_HOST
        self.model = OLLAMA_MODEL
        self.api_url = f"{self.host}/api/generate"
    
    def parse_story(self, story_text):
        """
        Parse story text and generate scenes with metadata
        Returns list of scene dictionaries with:
        - title: Scene title
        - description: What happens in this scene
        - animation_type: Type of animation (historical_map, timeline, graph, etc)
        - keywords: Search terms for images
        - duration: Scene duration in seconds
        """
        
        prompt = f"""أنت مساعد متخصص في تحويل القصص التاريخية إلى مشاهد بصرية احترافية.

القصة:
{story_text}

قم بتحليل القصة وتقسيمها إلى {MAX_SCENES} مشاهد كحد أقصى. لكل مشهد، أعطني:
1. العنوان (title)
2. الوصف التفصيلي (description)
3. نوع الأنيميشن المناسب (animation_type): اختر من: historical_map, timeline, graph, text_reveal, image_zoom, transition
4. كلمات مفتاحية للبحث عن الصور (keywords)
5. مدة المشهد بالثواني (duration)

أرجع الإجابة بصيغة JSON صارمة:
{{
  "scenes": [
    {{
      "title": "عنوان المشهد",
      "description": "وصف ماذا يحدث",
      "animation_type": "historical_map",
      "keywords": ["كلمة1", "كلمة2"],
      "duration": 15
    }}
  ]
}}

تأكد أن المجموع الكلي للمشاهد لا يتجاوز {MAX_SCENES} مشاهد."""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ Ollama error: {response.status_code}")
                return None
            
            result = response.json()
            response_text = result.get("response", "")
            
            # Extract JSON from response
            scenes_data = self._extract_json(response_text)
            
            if scenes_data and "scenes" in scenes_data:
                return scenes_data["scenes"]
            else:
                print("❌ Failed to parse Ollama response")
                return None
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {self.host}")
            print("💡 Make sure Ollama is running: ollama serve")
            return None
        except Exception as e:
            print(f"❌ Error processing story: {e}")
            return None
    
    def _extract_json(self, text):
        """Extract JSON from response text"""
        try:
            # Try to find JSON block in text
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            
            return None
        except json.JSONDecodeError:
            return None
