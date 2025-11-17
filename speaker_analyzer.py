import os
import torch
import numpy as np
from typing import List, Dict, Tuple
import librosa
import soundfile as sf
from transformers import pipeline
import re

class SpeakerAnalyzer:
    """Advanced speaker diarization and conversation analysis"""
    
    def __init__(self):
        print("🎙️ Initializing Speaker Analyzer...")
        
        # Initialize sentiment and emotion models
        self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                         model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.emotion_analyzer = pipeline("text-classification", 
                                       model="j-hartmann/emotion-english-distilroberta-base")
        
        # Conversation patterns for meaningful moments
        self.question_patterns = [
            r'\b(what|how|why|when|where|who|which|can|could|would|should|do|does|did|is|are|was|were)\b.*\?',
            r'\b(tell me|explain|describe|share|what do you think|how do you feel)\b',
            r'\b(really|seriously|actually|honestly|truly)\b.*\?'
        ]
        
        self.insight_patterns = [
            r'\b(the key is|the secret is|the most important|crucial|essential|critical)\b',
            r'\b(I realized|I discovered|I found|I learned|I understand)\b',
            r'\b(the truth is|in reality|actually|fundamentally)\b',
            r'\b(because|since|due to|as a result|consequently)\b'
        ]
        
        self.humor_patterns = [
            r'\b(haha|lol|funny|hilarious|ridiculous|absurd)\b',
            r'\b(joking|kidding|just kidding|obviously)\b',
            r'\b(can you believe|imagine|picture this)\b'
        ]
        
        self.controversy_patterns = [
            r'\b(disagree|wrong|incorrect|false|bullshit)\b',
            r'\b(controversial|debate|argument|dispute)\b',
            r'\b(I disagree|that\'s not true|actually it\'s)\b'
        ]
    
    def analyze_speakers(self, audio_path: str, segments: List[Dict]) -> List[Dict]:
        """Analyze speakers and enhance segments with speaker information"""
        print("👥 Analyzing speakers and conversation patterns...")
        
        enhanced_segments = []
        
        for i, segment in enumerate(segments):
            text = segment["text"]
            start_time = segment["start"]
            end_time = segment["end"]
            
            # Analyze text content
            sentiment = self.sentiment_analyzer(text)[0]
            emotion = self.emotion_analyzer(text)[0]
            
            # Detect conversation patterns
            is_question = self._detect_pattern(text, self.question_patterns)
            is_insight = self._detect_pattern(text, self.insight_patterns)
            is_humor = self._detect_pattern(text, self.humor_patterns)
            is_controversy = self._detect_pattern(text, self.controversy_patterns)
            
            # Estimate speaker (basic heuristic - can be enhanced with real diarization)
            speaker = self._estimate_speaker(segments, i)
            
            # Calculate engagement score
            engagement_score = self._calculate_engagement(
                text, sentiment, emotion, is_question, is_insight, is_humor, is_controversy
            )
            
            enhanced_segment = {
                "text": text,
                "start": start_time,
                "end": end_time,
                "speaker": speaker,
                "sentiment": sentiment,
                "emotion": emotion,
                "is_question": is_question,
                "is_insight": is_insight,
                "is_humor": is_humor,
                "is_controversy": is_controversy,
                "engagement_score": engagement_score,
                "word_count": len(text.split())
            }
            
            enhanced_segments.append(enhanced_segment)
        
        return enhanced_segments
    
    def _detect_pattern(self, text: str, patterns: List[str]) -> bool:
        """Detect if text matches any of the given patterns"""
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def _estimate_speaker(self, segments: List[Dict], current_index: int) -> str:
        """Estimate speaker based on conversation flow"""
        # Simple heuristic: alternate speakers, can be enhanced with real diarization
        if current_index == 0:
            return "Speaker_A"
        
        # Look for response patterns
        current_text = segments[current_index]["text"].lower()
        prev_text = segments[current_index - 1]["text"].lower()
        
        # Response indicators
        response_words = ["yes", "no", "well", "actually", "i think", "i believe", "that's true"]
        if any(word in current_text for word in response_words):
            # Likely different speaker from previous
            prev_speaker = segments[current_index - 1].get("speaker", "Speaker_A")
            return "Speaker_B" if prev_speaker == "Speaker_A" else "Speaker_A"
        
        # Continuation indicators
        continuation_words = ["and", "so", "then", "also", "furthermore", "additionally"]
        if any(word in current_text for word in continuation_words):
            # Likely same speaker as previous
            return segments[current_index - 1].get("speaker", "Speaker_A")
        
        # Default alternation
        prev_speaker = segments[current_index - 1].get("speaker", "Speaker_A")
        return "Speaker_B" if prev_speaker == "Speaker_A" else "Speaker_A"
    
    def _calculate_engagement(self, text: str, sentiment: Dict, emotion: Dict, 
                             is_question: bool, is_insight: bool, is_humor: bool, 
                             is_controversy: bool) -> float:
        """Calculate engagement score for a segment"""
        score = 0.0
        
        # Sentiment impact
        if sentiment["label"] == "POSITIVE":
            score += sentiment["score"] * 2
        elif sentiment["label"] == "NEGATIVE":
            score += sentiment["score"] * 1.5
        
        # Emotion impact
        high_impact_emotions = ["joy", "surprise", "anger", "fear", "sadness"]
        if emotion["label"] in high_impact_emotions:
            score += emotion["score"] * 1.5
        
        # Content pattern impact
        if is_question:
            score += 1.0  # Questions engage audience
        if is_insight:
            score += 1.5  # Insights provide value
        if is_humor:
            score += 1.2  # Humor increases shareability
        if is_controversy:
            score += 1.3  # Controversy drives engagement
        
        # Length optimization
        word_count = len(text.split())
        if 8 <= word_count <= 25:  # Optimal length for shorts
            score += 0.5
        elif word_count > 40:  # Too long
            score -= 0.3
        
        # Viral keywords
        viral_keywords = [
            "amazing", "incredible", "unbelievable", "shocking", "mind-blowing",
            "game-changer", "revolutionary", "breakthrough", "secret", "reveal"
        ]
        keyword_count = sum(1 for keyword in viral_keywords if keyword.lower() in text.lower())
        score += keyword_count * 0.3
        
        return score
    
    def identify_meaningful_moments(self, enhanced_segments: List[Dict]) -> List[Dict]:
        """Identify the most meaningful moments for shorts"""
        print("🎯 Identifying meaningful moments for viral shorts...")
        
        # Filter and score segments
        meaningful_moments = []
        
        for segment in enhanced_segments:
            # Base score from engagement
            viral_score = segment["engagement_score"]
            
            # Context bonuses
            if segment["is_question"] and segment["word_count"] < 15:
                viral_score += 0.8  # Short questions are great hooks
            
            if segment["is_insight"] and segment["sentiment"]["label"] == "POSITIVE":
                viral_score += 1.2  # Positive insights are highly shareable
            
            if segment["is_humor"] and segment["emotion"]["label"] == "joy":
                viral_score += 1.0  # Funny content performs well
            
            # Speaker transition bonus
            if self._is_speaker_transition(enhanced_segments, segment):
                viral_score += 0.5  # Speaker changes create dynamic content
            
            # Create moment data
            moment = {
                "text": segment["text"],
                "start": segment["start"],
                "end": segment["end"],
                "speaker": segment["speaker"],
                "viral_score": viral_score,
                "sentiment": segment["sentiment"],
                "emotion": segment["emotion"],
                "is_question": segment["is_question"],
                "is_insight": segment["is_insight"],
                "is_humor": segment["is_humor"],
                "is_controversy": segment["is_controversy"],
                "engagement_score": segment["engagement_score"]
            }
            
            meaningful_moments.append(moment)
        
        # Sort by viral score and return top moments
        meaningful_moments.sort(key=lambda x: x["viral_score"], reverse=True)
        
        # Filter out very short or very long segments
        filtered_moments = []
        for moment in meaningful_moments:
            duration = moment["end"] - moment["start"]
            if 5 <= duration <= 60:  # 5 seconds to 1 minute
                filtered_moments.append(moment)
        
        return filtered_moments[:15]  # Return top 15 moments
    
    def _is_speaker_transition(self, segments: List[Dict], current_segment: Dict) -> bool:
        """Check if this segment represents a speaker transition"""
        current_index = segments.index(current_segment)
        if current_index == 0:
            return False
        
        prev_speaker = segments[current_index - 1]["speaker"]
        current_speaker = current_segment["speaker"]
        
        return prev_speaker != current_speaker
    
    def group_conversation_threads(self, meaningful_moments: List[Dict]) -> List[Dict]:
        """Group related segments into conversation threads for better shorts"""
        print("🧵 Grouping conversation threads...")
        
        threads = []
        current_thread = []
        
        for i, moment in enumerate(meaningful_moments):
            if not current_thread:
                current_thread.append(moment)
                continue
            
            last_moment = current_thread[-1]
            
            # Check if this moment continues the conversation
            time_gap = moment["start"] - last_moment["end"]
            same_topic = self._is_same_topic(last_moment["text"], moment["text"])
            
            if time_gap < 10 and same_topic:  # Less than 10 seconds gap and same topic
                current_thread.append(moment)
            else:
                # End current thread and start new one
                if len(current_thread) >= 1:
                    threads.append(self._merge_thread(current_thread))
                current_thread = [moment]
        
        # Add the last thread
        if current_thread:
            threads.append(self._merge_thread(current_thread))
        
        return threads
    
    def _is_same_topic(self, text1: str, text2: str) -> bool:
        """Check if two texts are about the same topic"""
        # Simple keyword overlap check
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "i", "you", "he", "she", "it", "we", "they"}
        words1 -= common_words
        words2 -= common_words
        
        if not words1 or not words2:
            return False
        
        overlap = len(words1.intersection(words2))
        similarity = overlap / min(len(words1), len(words2))
        
        return similarity > 0.3  # 30% word overlap threshold
    
    def _merge_thread(self, thread: List[Dict]) -> Dict:
        """Merge a thread of segments into a single moment"""
        if len(thread) == 1:
            return thread[0]
        
        # Combine text, timing, and scores
        combined_text = " ".join([moment["text"] for moment in thread])
        start_time = thread[0]["start"]
        end_time = thread[-1]["end"]
        
        # Calculate combined scores
        total_viral_score = sum(moment["viral_score"] for moment in thread)
        avg_engagement = sum(moment["engagement_score"] for moment in thread) / len(thread)
        
        # Get speakers involved
        speakers = list(set(moment["speaker"] for moment in thread))
        
        return {
            "text": combined_text,
            "start": start_time,
            "end": end_time,
            "speakers": speakers,
            "viral_score": total_viral_score,
            "engagement_score": avg_engagement,
            "is_multi_speaker": len(speakers) > 1,
            "segment_count": len(thread)
        }
