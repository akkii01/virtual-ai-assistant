"""
Module: smart_features.py
Project: Virtual AI Assistant (Mini Alexa - Web & Voice Edition)
Author: Akshit Raj
Description: 100% API-key-free advanced assistant modules using Python Standard Library:
             1. Universal Wikipedia Knowledge Engine (Exact Title Resolution + Relevance Guard + Custom Word Counts)
             2. Persistent Voice/Text Task Manager & Smart Focus Timer
             3. Offline NLP Extractive Text Summarizer & Sentiment Analyzer
"""

import os
import re
import json
import math
import urllib.request
import urllib.parse
from datetime import datetime


# ==============================================================================
# 1. UNIVERSAL WIKIPEDIA KNOWLEDGE ENGINE (Any Topic Worldwide, Zero API Key)
# ==============================================================================
class KnowledgeEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": "MiniAlexaAssistant/2.3 (Educational Python Web Project)"
        }
        self.acronym_map = {
            "rag": "Retrieval-augmented generation",
            "nlp": "Natural language processing",
            "llm": "Large language model",
            "llms": "Large language model",
            "cnn": "Convolutional neural network",
            "rnn": "Recurrent neural network",
            "gan": "Generative adversarial network",
            "api": "Application programming interface",
            "cpu": "Central processing unit",
            "gpu": "Graphics processing unit",
            "dna": "DNA",
            "rna": "RNA"
        }

    def parse_query_and_length(self, raw_query: str) -> tuple:
        """
        Cleanly isolates any world topic and desired response length even when wrapped
        in casual spoken fillers like 'ok tell me about ... in few words'.
        """
        text = raw_query.strip()
        target_words = 140
        mode_label = "Standard Overview"

        # 1. Explicit numeric word count ("in 50 words", "within 100 words", "5000 words")
        word_count_match = re.search(
            r"\b(?:in\s+|within\s+|around\s+|about\s+|under\s+)?(\d{1,5})\s+words?\b",
            text,
            flags=re.IGNORECASE
        )
        if word_count_match:
            requested = int(word_count_match.group(1))
            target_words = max(20, min(requested, 10000))
            mode_label = f"Target ~{target_words} Words"
            text = re.sub(
                r"\b(?:in\s+|within\s+|around\s+|about\s+|under\s+)?\d{1,5}\s+words?\b",
                "",
                text,
                flags=re.IGNORECASE
            )

        # 2. Qualitative length modes ("in detail", "in few words", "in short", "in medium")
        elif re.search(r"\b(in\s+detail|in\s+details|detailed|deep\s+dive|elaborate|comprehensive|full\s+explanation)\b", text, flags=re.IGNORECASE):
            target_words = 420
            mode_label = "Detailed Explanation"
            text = re.sub(
                r"\b(in\s+detail|in\s+details|detailed|deep\s+dive|elaborate|comprehensive|full\s+explanation)\b",
                "",
                text,
                flags=re.IGNORECASE
            )
        elif re.search(
            r"\b(in\s+(?:a\s+)?few\s+(?:words|lines|sentences)|in\s+short|in\s+brief|shortly|briefly|quick\s+summary|short\s+summary|concisely)\b",
            text,
            flags=re.IGNORECASE
        ):
            target_words = 60
            mode_label = "Short Summary"
            text = re.sub(
                r"\b(in\s+(?:a\s+)?few\s+(?:words|lines|sentences)|in\s+short|in\s+brief|shortly|briefly|quick\s+summary|short\s+summary|concisely)\b",
                "",
                text,
                flags=re.IGNORECASE
            )
        elif re.search(r"\b(in\s+medium|medium\s+length|moderate)\b", text, flags=re.IGNORECASE):
            target_words = 200
            mode_label = "Medium Overview"
            text = re.sub(r"\b(in\s+medium|medium\s+length|moderate)\b", "", text, flags=re.IGNORECASE)

        # 3. Remove style modifiers ("in very simple words", "in easy terms", "for beginners")
        text = re.sub(
            r"\b(?:in\s+(?:very\s+)?(?:simple|easy|plain|layman)\s+(?:words|terms|language)|for\s+beginners)\b",
            "",
            text,
            flags=re.IGNORECASE
        )

        # 4. Iteratively strip ALL conversational openers & command verbs (handles "ok tell me about...", "so what is...")
        leading_patterns = [
            r"^(?:ok|okay|alright|well|so|now|hey|hi|hello|please|kindly|can you|could you|would you|will you|alexa|mini alexa)[\s,]+",
            r"^(?:i\s+want\s+to\s+know|i\s+would\s+like\s+to\s+know|give\s+me\s+information|give\s+me\s+details|tell\s+me\s+something|tell\s+me|what\s+is|what\s+are|who\s+is|who\s+was|who\s+were|where\s+is|when\s+was|define|explain|describe|search\s+for|search|look\s+up|wiki|wikipedia)[\s:]+",
            r"^(?:about|on|regarding|the|a|an|concept\s+of|topic\s+of|meaning\s+of|medicine\s+named|drug\s+named|tablet\s+named)[\s]+",
        ]

        changed = True
        while changed:
            prev = text
            for pat in leading_patterns:
                text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()
            changed = (text != prev)

        # 5. Strip trailing filler words
        text = re.sub(
            r"\s+(?:please|right\s+now|for\s+me|about\s+it|thanks|thank\s+you)$",
            "",
            text,
            flags=re.IGNORECASE
        ).strip(" ?.!,:-")

        # 6. Expand known tech/science acronyms
        if text.lower() in self.acronym_map:
            text = self.acronym_map[text.lower()]

        return text, target_words, mode_label

    def _resolve_best_title(self, topic: str) -> str:
        """
        Resolves the exact Wikipedia article title for any topic worldwide:
        1. Checks exact title match on the full phrase first (e.g., 'Squid Game', 'Machine Learning').
        2. Strips generic descriptor suffixes ('medicine', 'tablet', 'drug', 'disease') if needed
           (e.g., 'paracetamol tablet' -> 'Paracetamol', 'baclofen medicine' -> 'Baclofen').
        3. Verifies keyword relevance so unrelated articles are never returned.
        """
        core_topic = re.sub(
            r"\s+(?:medicine|medicines|medication|drug|drugs|tablet|tablets|capsule|capsules|syrup|injection|ointment|disease|syndrome|concept|topic|subject|definition|meaning)$",
            "",
            topic,
            flags=re.IGNORECASE
        ).strip()

        candidates = []
        if core_topic and core_topic.lower() != topic.lower():
            candidates.append(core_topic)
        candidates.append(topic)

        # Pass 1: Direct Title Match via Wikipedia OpenSearch API
        for cand in candidates:
            open_url = (
                "https://en.wikipedia.org/w/api.php?action=opensearch"
                f"&search={urllib.parse.quote(cand)}&limit=5&namespace=0&format=json"
            )
            req = urllib.request.Request(open_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            titles = data[1] if len(data) > 1 else []
            non_list = [
                t for t in titles
                if not re.match(r"^(?:list of|who model list|index of|outline of)\b", t, flags=re.IGNORECASE)
            ]

            for t in non_list:
                if t.lower() == cand.lower():
                    return t
            if non_list:
                return non_list[0]

        # Pass 2: Full-Text Search with Relevance Verification
        primary_words = [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", core_topic or topic) if len(w) > 2]

        for cand in candidates:
            search_url = (
                "https://en.wikipedia.org/w/api.php?action=query&list=search"
                f"&srsearch={urllib.parse.quote(cand)}&utf8=&format=json&srlimit=5"
            )
            req = urllib.request.Request(search_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                search_data = json.loads(resp.read().decode("utf-8"))

            results = search_data.get("query", {}).get("search", [])
            for item in results:
                title = item.get("title", "")
                snippet = re.sub(r"<[^>]+>", "", item.get("snippet", "")).lower()
                if re.match(r"^(?:list of|who model list|index of|outline of)\b", title, flags=re.IGNORECASE):
                    continue
                # Ensure at least one core keyword from the user's topic actually appears in the title or snippet
                if not primary_words or any(w in title.lower() or w in snippet for w in primary_words):
                    return title

        return ""

    def _format_to_word_limit(self, raw_extract: str, target_words: int) -> tuple:
        """
        Formats full Wikipedia article text cleanly and trims to target_words
        while ending naturally at a complete sentence boundary.
        """
        cleaned = re.sub(r"\n={2,4}\s*([^=]+?)\s*={2,4}\n", r"\n\n📌 \1\n", raw_extract)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

        words = cleaned.split()
        if len(words) <= target_words:
            return cleaned, len(words)

        sliced = " ".join(words[:target_words + 25])
        sentences = re.split(r'(?<=[.!?])\s+', sliced)

        selected_sentences = []
        current_count = 0
        for sent in sentences:
            sent_words = len(sent.split())
            if current_count + sent_words <= target_words or not selected_sentences:
                selected_sentences.append(sent)
                current_count += sent_words
            else:
                break

        final_text = " ".join(selected_sentences).strip()
        final_text = re.sub(r"\s*(📌 [^\n]+)\s*", r"\n\n\1\n", final_text).strip()
        return final_text, len(final_text.split())

    def lookup(self, raw_query: str) -> dict:
        topic, target_words, mode_label = self.parse_query_and_length(raw_query)
        if not topic or len(topic) < 2:
            msg = (
                "Please specify a topic—for example:\n"
                "• 'Tell me about paracetamol in few words'\n"
                "• 'Explain black holes within 150 words'\n"
                "• 'What is machine learning in detail'"
            )
            return {"reply": msg, "speak": "Please tell me which topic you want to learn about."}

        try:
            best_title = self._resolve_best_title(topic)
            if not best_title:
                msg = f"I couldn't find an exact encyclopedia entry for '{topic}'. Try asking with just the main topic name!"
                return {"reply": msg, "speak": msg}

            extract_url = (
                "https://en.wikipedia.org/w/api.php?action=query&prop=extracts"
                f"&explaintext=1&titles={urllib.parse.quote(best_title)}&format=json"
            )
            req2 = urllib.request.Request(extract_url, headers=self.headers)
            with urllib.request.urlopen(req2, timeout=8) as resp2:
                page_data = json.loads(resp2.read().decode("utf-8"))

            pages = page_data.get("query", {}).get("pages", {})
            page_obj = next(iter(pages.values()))
            full_extract = page_obj.get("extract", "").strip()
            page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(best_title.replace(' ', '_'))}"

            if not full_extract:
                msg = f"Found topic '{best_title}', but no readable text was available."
                return {"reply": msg, "speak": msg}

            formatted_body, actual_words = self._format_to_word_limit(full_extract, target_words)

            clean_spoken = re.sub(r"📌\s*", ". Section: ", formatted_body)
            clean_spoken = re.sub(r"\s+", " ", clean_spoken).strip()

            formatted_reply = (
                f"📚 {best_title}  [{mode_label} • {actual_words} words]\n"
                f"{'-' * 52}\n"
                f"{formatted_body}\n\n"
                f"🔗 Source: {page_url}"
            )
            return {
                "reply": formatted_reply,
                "speak": f"Here is {best_title}. {clean_spoken}",
                "is_code": True
            }

        except Exception:
            msg = "Network unavailable right now for Wikipedia lookup. Please check your internet connection and try again."
            return {"reply": msg, "speak": msg}


# ==============================================================================
# 2. PERSISTENT TASK MANAGER & SMART FOCUS TIMER
# ==============================================================================
class TaskAndTimerManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file

    def _load_tasks(self) -> list:
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_tasks(self, tasks: list):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

    def add_task(self, raw_text: str) -> dict:
        task_text = re.sub(
            r"^(?:please\s+)?(?:add\s+a\s+task|add\s+task|new\s+task|create\s+task|remind\s+me\s+to|add\s+to\s+my\s+list)\s+",
            "",
            raw_text.strip(),
            flags=re.IGNORECASE
        ).strip(" .!")

        if not task_text:
            msg = "What task would you like me to add? Say: 'Add task finish Python assignment'."
            return {"reply": msg, "speak": msg}

        tasks = self._load_tasks()
        tasks.append({
            "task": task_text[0].upper() + task_text[1:],
            "done": False,
            "created": datetime.now().strftime("%d %b, %I:%M %p")
        })
        self._save_tasks(tasks)

        msg = f"✅ Task Added (#{len(tasks)}): \"{tasks[-1]['task']}\""
        return {"reply": msg, "speak": f"Added task: {task_text}"}

    def list_tasks(self) -> dict:
        tasks = self._load_tasks()
        if not tasks:
            msg = "📋 Your To-Do list is currently empty! Say 'Add task [your task]' to create one."
            return {"reply": msg, "speak": "Your to-do list is currently empty."}

        lines = ["📋 YOUR PERSONAL TASK LIST", "-" * 42]
        pending_count = 0
        for idx, item in enumerate(tasks, 1):
            status = "✔️" if item["done"] else "⏳"
            if not item["done"]:
                pending_count += 1
            lines.append(f"{idx}. [{status}] {item['task']}  ({item['created']})")

        lines.append("-" * 42)
        lines.append(f"Total: {len(tasks)} | Pending: {pending_count} | Completed: {len(tasks) - pending_count}")

        return {
            "reply": "\n".join(lines),
            "speak": f"You have {pending_count} pending tasks out of {len(tasks)} total tasks.",
            "is_code": True
        }

    def complete_task(self, raw_text: str) -> dict:
        tasks = self._load_tasks()
        if not tasks:
            msg = "Your task list is empty, so there is nothing to mark complete."
            return {"reply": msg, "speak": msg}

        num_match = re.search(r"\d+", raw_text)
        if not num_match:
            msg = "Please specify the task number—for example: 'Complete task 1'."
            return {"reply": msg, "speak": msg}

        idx = int(num_match.group()) - 1
        if idx < 0 or idx >= len(tasks):
            msg = f"Task #{idx + 1} doesn't exist. You currently have {len(tasks)} tasks."
            return {"reply": msg, "speak": msg}

        tasks[idx]["done"] = True
        self._save_tasks(tasks)
        msg = f"🎉 Marked Task #{idx + 1} as completed: \"{tasks[idx]['task']}\""
        return {"reply": msg, "speak": f"Marked task {idx + 1} as completed."}

    def delete_task(self, raw_text: str) -> dict:
        if "clear all" in raw_text.lower() or "delete all" in raw_text.lower():
            self._save_tasks([])
            msg = "🗑️ All tasks have been cleared from your list."
            return {"reply": msg, "speak": "All tasks have been cleared."}

        tasks = self._load_tasks()
        num_match = re.search(r"\d+", raw_text)
        if not num_match:
            msg = "Please specify the task number to delete—for example: 'Delete task 1' or 'Clear all tasks'."
            return {"reply": msg, "speak": msg}

        idx = int(num_match.group()) - 1
        if idx < 0 or idx >= len(tasks):
            msg = f"Task #{idx + 1} doesn't exist."
            return {"reply": msg, "speak": msg}

        removed = tasks.pop(idx)
        self._save_tasks(tasks)
        msg = f"🗑️ Deleted Task #{idx + 1}: \"{removed['task']}\""
        return {"reply": msg, "speak": f"Deleted task {idx + 1}."}

    def parse_timer_request(self, raw_text: str) -> dict:
        lower = raw_text.lower()
        if any(w in lower for w in ["stop timer", "cancel timer", "reset timer"]):
            return {
                "reply": "⏹️ Focus timer stopped.",
                "speak": "Focus timer stopped.",
                "timer_seconds": 0
            }

        word_nums = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "ten": 10, "fifteen": 15, "twenty": 20, "twenty five": 25, "thirty": 30, "forty five": 45
        }

        amount = None
        digit_match = re.search(r"\d+", lower)
        if digit_match:
            amount = int(digit_match.group())
        else:
            for word, val in word_nums.items():
                if re.search(rf"\b{word}\b", lower):
                    amount = val
                    break

        if amount is None:
            amount = 25
            unit = "minute"
        else:
            unit = "second" if any(u in lower for u in ["second", "seconds", "sec"]) else "minute"

        total_seconds = amount if unit == "second" else amount * 60
        label = f"{amount} {unit}{'s' if amount > 1 else ''}"

        return {
            "reply": f"⏱️ Focus Timer Started for {label}! Stay focused—I'll alert you out loud when time is up.",
            "speak": f"Starting a {label} focus timer now.",
            "timer_seconds": total_seconds,
            "timer_label": label
        }


# ==============================================================================
# 3. OFFLINE NLP TEXT SUMMARIZER & SENTIMENT ANALYZER (Zero API Key)
# ==============================================================================
class OfflineNLPEngine:
    def __init__(self):
        self.stopwords = {
            "the", "is", "in", "at", "of", "on", "and", "a", "an", "to", "for", "with",
            "that", "this", "it", "as", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "but", "if", "or", "because",
            "from", "by", "about", "into", "through", "during", "before", "after",
            "above", "below", "up", "down", "out", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how",
            "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
            "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can",
            "will", "just", "should", "now", "we", "you", "they", "he", "she", "i", "my", "our"
        }

        self.positive_words = {
            "good", "great", "awesome", "amazing", "excellent", "happy", "love", "loved",
            "best", "wonderful", "fantastic", "helpful", "positive", "success", "successful",
            "easy", "fast", "clean", "smart", "impressed", "impressive", "enjoy", "enjoyed",
            "brilliant", "perfect", "super", "nice", "excited", "exciting", "productive", "win"
        }

        self.negative_words = {
            "bad", "worst", "terrible", "awful", "horrible", "sad", "hate", "hated",
            "poor", "slow", "hard", "difficult", "broken", "error", "bug", "bugs", "fail",
            "failed", "failure", "boring", "confusing", "useless", "waste", "problem",
            "issue", "stress", "angry", "disappointed", "disappointing", "weak", "wrong"
        }

    def _extract_payload(self, raw_text: str) -> str:
        cleaned = re.sub(
            r"^(?:please\s+)?(?:summarize\s+this\s+text|summarize\s+this|summarize|summary\s+of|analyze\s+sentiment\s+of|analyze\s+sentiment|sentiment\s+of|analyze\s+this|analyze|nlp\s+analyze)\s*[:\-]?\s*",
            "",
            raw_text.strip(),
            flags=re.IGNORECASE
        ).strip()
        return cleaned

    def analyze_and_summarize(self, raw_text: str) -> dict:
        text = self._extract_payload(raw_text)
        if not text or len(text.split()) < 4:
            guide = (
                "🧠 Offline NLP Summarizer & Sentiment Analyzer Ready!\n"
                "How to use:\n"
                "• Type or paste:  summarize: [paste any long article or paragraph]\n"
                "• Or check tone:   analyze: [paste any review, feedback, or message]"
            )
            return {"reply": guide, "speak": "Paste or type summarize followed by your paragraph to get an instant summary and sentiment analysis."}

        words = re.findall(r"[a-zA-Z']+", text.lower())
        content_words = [w for w in words if w not in self.stopwords and len(w) > 2]

        freq = {}
        for w in content_words:
            freq[w] = freq.get(w, 0) + 1

        top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keyword_str = ", ".join([k[0].title() for k in top_keywords]) if top_keywords else "General"

        pos_score = 0
        neg_score = 0
        for idx, w in enumerate(words):
            prev_word = words[idx - 1] if idx > 0 else ""
            negated = prev_word in {"not", "no", "never", "isn't", "wasn't", "don't", "didn't", "can't"}
            if w in self.positive_words:
                if negated:
                    neg_score += 1
                else:
                    pos_score += 1
            elif w in self.negative_words:
                if negated:
                    pos_score += 1
                else:
                    neg_score += 1

        net_score = pos_score - neg_score
        if net_score > 0:
            sentiment_label = f"😊 Positive (Score: +{net_score})"
        elif net_score < 0:
            sentiment_label = f"😟 Negative (Score: {net_score})"
        else:
            sentiment_label = "😐 Neutral / Balanced (Score: 0)"

        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        if len(sentences) <= 2:
            summary = text
        else:
            max_freq = max(freq.values()) if freq else 1
            norm_freq = {k: v / max_freq for k, v in freq.items()}
            scored_sentences = []
            for idx, sent in enumerate(sentences):
                sent_words = re.findall(r"[a-zA-Z']+", sent.lower())
                score = sum(norm_freq.get(w, 0) for w in sent_words) / (math.log(len(sent_words) + 2))
                scored_sentences.append((score, idx, sent))

            top_two = sorted(scored_sentences, key=lambda x: x[0], reverse=True)[:2]
            top_two_ordered = sorted(top_two, key=lambda x: x[1])
            summary = " ".join([s[2] for s in top_two_ordered])

        read_sec = max(5, round((len(words) / 200) * 60))

        report = (
            "🧠 OFFLINE NLP ANALYSIS & SUMMARY REPORT\n"
            f"{'-' * 48}\n"
            f"📌 Extractive Summary:\n{summary}\n\n"
            f"🎭 Detected Tone:  {sentiment_label}\n"
            f"🔑 Top Keywords:   {keyword_str}\n"
            f"📊 Text Stats:     {len(words)} words | {len(sentences)} sentences | ~{read_sec}s read"
        )

        return {
            "reply": report,
            "speak": f"Analysis complete. The overall tone is {sentiment_label.split()[1]}. Here is your summary: {summary}",
            "is_code": True
        }