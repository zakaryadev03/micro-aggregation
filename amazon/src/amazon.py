# amazon.py
from __future__ import annotations
import os
import re
import logging
from typing import List, Dict, Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AmazonAPI:
    def __init__(self, api_key: Optional[str] = None, host: Optional[str] = None):
        self.base_url = "https://real-time-amazon-data.p.rapidapi.com/search"
        self.api_key = api_key or os.getenv("AMAZON_API_KEY")
        self.host = host or "real-time-amazon-data.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host,
        }

    def search_products(self, query: str, timeout: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Query the RapidAPI Amazon endpoint and return a normalized list of products
        or None on failure (keeps parity with the JS version).
        """
        params = {"query": query}
        try:
            resp = requests.get(self.base_url, headers=self.headers, params=params, timeout=timeout)
            resp.raise_for_status()
            body = resp.json()
            return self._normalize(body)
        except Exception as exc:
            logger.error("Amazon API error: %s", exc)
            return None

    def _parse_price(self, raw: Optional[str]) -> Optional[float]:
        if not raw:
            return None
        # Keep digits and dot (remove currency symbols, commas, etc.)
        cleaned = re.sub(r"[^0-9.]", "", raw)
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None

    def _normalize(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = (raw or {}).get("data", {}).get("products", []) or []
        out = []
        for item in items:
            price = self._parse_price(item.get("product_price")) or 0
            original = self._parse_price(item.get("product_original_price"))
            discount = None
            if original and original > 0:
                # same rounding behavior as JS: Math.round(...)
                discount_pct = round(((original - price) / original) * 100)
                discount = f"{discount_pct}%"
            out.append({
                "product_id": item.get("asin"),
                "title": item.get("product_title"),
                "price": price,
                "original_price": original,
                "currency": item.get("currency") or "USD",
                "discount": discount,
                "image_url": item.get("product_photo"),
                "platform": "Amazon",
            })
        return out
