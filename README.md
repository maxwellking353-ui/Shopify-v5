import time
import re
import random
import re
import csv
import os
import asyncio
import json
import phonenumbers
import time
import ssl
from faker import Faker
from datetime import datetime
import aiohttp
import urllib.parse
import uuid
import re
from datetime import datetime
from typing import List, Dict
from fastapi import FastAPI, Query
import aiohttp
from contextlib import asynccontextmanager

    
def find_between(text, start_str, end_str):
    start_idx = text.find(start_str)
    if start_idx == -1:
        return None
    start_idx += len(start_str)
    end_idx = text.find(end_str, start_idx)
    if end_idx == -1:
        return None
    return text[start_idx:end_idx]



def build_delivery_terms(
    is_shippable,
    address,
    stable_id,
    variant_price,
    currency_code,
    handle="927e65bd4bc6307e397981607cd07c2e-2d5b7643c5a9b084c778d283352aeeef",
):
    if is_shippable:
        return {
            "deliveryLines": [
                {
                    "destination": {
                        "partialStreetAddress": {
                            "address1": address["street"],
                            "address2": address["street"],
                            "city": address["city"],
                            "countryCode": address["country"],
                            "postalCode": address["postal_code"],
                            "firstName": address["first_name"],
                            "lastName": address["last_name"],
                            "zoneCode": address["zoneCode"],
                            "phone": address["phone"],
                            "oneTimeUse": False,
                        },
                    },
                    "selectedDeliveryStrategy": {
                        "deliveryStrategyByHandle": {
                            "handle": handle,
                            "customDeliveryRate": False,
                        },
                        "options": {},
                    },
                    "targetMerchandiseLines": {
                        "lines": [
                            {
                                "stableId": stable_id,
                            },
                        ],
                    },
                    "deliveryMethodTypes": [
                        "SHIPPING",
                    ],
                    "expectedTotalPrice": {
                        "value": {
                            "amount": variant_price,
                            "currencyCode": currency_code,
                        },
                    },
                    "destinationChanged": False,
                },
            ],
            "noDeliveryRequired": [],
            "useProgressiveRates": False,
            "prefetchShippingRatesStrategy": None,
            "supportsSplitShipping": True,
        }
    else:
        return {
            "deliveryLines": 
                {
                    "selectedDeliveryStrategy": {
                        "deliveryStrategyMatchingConditions": {
                            "estimatedTimeInTransit": {
                                "any": True,
                            },
                            "shipments": {
                                "any": True,
                            },
                        },
                        "options": {},
                    },
                    "targetMerchandiseLines": {
                        "lines": [
                            {
                                "stableId": stable_id,
                            },
                        ],
                    },
                    "deliveryMethodTypes": [
                        "NONE",
                    ],
                    "expectedTotalPrice": {
                        "any": True,
                    },
                    "destinationChanged": True,
                },
            ],
            "noDeliveryRequired": [],
            "useProgressiveRates": False,
            "prefetchShippingRatesStrategy": None,
            "supportsSplitShipping": True,
        }


def build_submit_delivery_terms(
    is_shippable, address, stable_id, shipping_amount, currency_code, seller_handle
):
    if is_shippable:
        return {
            "deliveryLines": [
                {
                    "destination": {
                        "streetAddress": {
                            "address1": address["street"],
                            "address2": address["street"],
                            "city": address["city"],
                            "countryCode": address["country"],
                            "postalCode": address["postal_code"],
                            "firstName": address["first_name"],
                            "lastName": address["last_name"],
                            "zoneCode": address["zoneCode"],
                            "phone": address["phone"],
                            "oneTimeUse": False,
                        },
                    },
                    "selectedDeliveryStrategy": {
                        "deliveryStrategyByHandle": {
                            "handle": seller_handle,
                            "customDeliveryRate": False,
                        },
                        "options": {
                            "phone": address["phone"],
                        },
                    },
                    "targetMerchandiseLines": {
                        "lines": [
                            {
                                "stableId": stable_id,
                            },
                        ],
                    },
                    "deliveryMethodTypes": [
                        "SHIPPING",
                    ],
                    "expectedTotalPrice": {
                        "value": {
                            "amount": shipping_amount,
                            "currencyCode": currency_code,
                        },
                    },
                    "destinationChanged": False,
                },
            ],
            "noDeliveryRequired": [],
            "useProgressiveRates": False,
            "prefetchShippingRatesStrategy": None,
            "supportsSplitShipping": True,
        }
    else:
        return {
            "deliveryLines": [
                {
                    "selectedDeliveryStrategy": {
                        "deliveryStrategyMatchingConditions": {
                            "estimatedTimeInTransit": {
                                "any": True,
                            },
                            "shipments": {
                                "any": True,
                            },
                        },
                        "options": {},
                    },
                    "targetMerchandiseLines": {
                        "lines": [
                            {
                                "stableId": stable_id,
                            },
                        ],
                    },
                    "deliveryMethodTypes": [
                        "NONE",
                    ],
                    "expectedTotalPrice": {
                        "any": True,
                    },
                    "destinationChanged": True,
                },
            ],
            "noDeliveryRequired": [],
            "useProgressiveRates": False,
            "prefetchShippingRatesStrategy": None,
            "supportsSplitShipping": True,
        }
        


def parse_card_input(card_input: str):
    text = card_input or ""
    
    def luhn_check(num):
        digits = list(map(int, num))
        odd = sum(digits[-1::-2])
        even = sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
        return (odd + even) % 10 == 0
    
    def month_to_number(month_name):
        month_map = {
            'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
            'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
            'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
            'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
            'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
            'dec': 12, 'december': 12
        }
        return month_map.get(month_name[:3].lower(), 1)
    
    def parse_cc_line(line: str):
        line = line.strip()
        if not line or line.startswith("#"):
            return Mone 
        
        MONTH_PATTERNS = [
            r'(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)',
            r'(?:0?[1-9]|1[0-2])'
        ]
        
        YEAR_PATTERNS = [
            r'\'?\d{2}',
            r'\d{4}'    
        ]
        
        SEPARATORS = r'[\s\|\/\-\.,\;:_]'
        
        PATTERNS = [
            re.compile(r"\b(\d{13,19})" + SEPARATORS + r"(" + MONTH_PATTERNS[1] + r")" + SEPARATORS + r"(" + YEAR_PATTERNS[1] + r")" + SEPARATORS + r"(\d{3,4})\b", re.IGNORECASE),
            re.compile(r"\b(\d{13,19})" + SEPARATORS + r"(" + MONTH_PATTERNS[1] + r")" + SEPARATORS + r"(" + YEAR_PATTERNS[0] + r")" + SEPARATORS + r"(\d{3,4})\b", re.IGNORECASE),
            re.compile(r"\b(\d{13,19})" + SEPARATORS + r"(" + MONTH_PATTERNS[0] + r")" + SEPARATORS + r"(" + "|".join(YEAR_PATTERNS) + r")" + SEPARATORS + r"(\d{3,4})\b", re.IGNORECASE),
            re.compile(r"\b(\d{13,19})" + SEPARATORS + r"(" + MONTH_PATTERNS[1] + r")[\/\-](" + "|".join(YEAR_PATTERNS) + r")" + SEPARATORS + r"(\d{3,4})\b", re.IGNORECASE),
            re.compile(r"\b(\d{3,4})" + SEPARATORS + r"(\d{13,19})" + SEPARATORS + r"(" + MONTH_PATTERNS[1] + r")" + SEPARATORS + r"(" + "|".join(YEAR_PATTERNS) + r")\b", re.IGNORECASE),
            re.compile(r"(?:card|cc|ccnum|cc num|card num|card number|cardnumber|number|pan)\s*[:=\-]?\s*(\d{13,19}).*?(?:exp|expiry|expires|expiration|exp date|expiry date|date)\s*[:=\-]?\s*(" + MONTH_PATTERNS[1] + r")[\/\-](" + "|".join(YEAR_PATTERNS) + r").*?(?:cvv|cvc|cv2|code|security code|security|pin)\s*[:=\-]?\s*(\d{3,4})", re.IGNORECASE | re.DOTALL),
            re.compile(r"(?:card|cc|ccnum|cc num|card num|card number|cardnumber|number|pan)\s*[:=\-]?\s*(\d{13,19}).*?(?:exp|expiry|expires|expiration|exp date|expiry date|date)\s*[:=\-]?\s*(" + MONTH_PATTERNS[0] + r")\s*" + SEPARATORS + r"?\s*(" + "|".join(YEAR_PATTERNS) + r").*?(?:cvv|cvc|cv2|code|security code|security|pin)\s*[:=\-]?\s*(\d{3,4})", re.IGNORECASE | re.DOTALL),
            re.compile(r"(?:card|cc|ccnum|cc num|card num|card number|cardnumber|number|pan)\s*[:=\-]?\s*(\d{13,19}).*?(?:exp|expiry|expires|expiration|exp date|expiry date|date)\s*[:=\-]?\s*(" + MONTH_PATTERNS[1] + r")(" + YEAR_PATTERNS[1] + r").*?(?:cvv|cvc|cv2|code|security code|security|pin)\s*[:=\-]?\s*(\d{3,4})", re.IGNORECASE | re.DOTALL),
            re.compile(r"\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{3,4})" + SEPARATORS + r"(" + MONTH_PATTERNS[1] + r")" + SEPARATORS + r"(" + "|".join(YEAR_PATTERNS) + r")" + SEPARATORS + r"(\d{3,4})\b", re.IGNORECASE),
            re.compile(r"\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{3,4})\s+(" + MONTH_PATTERNS[1] + r")[\/\-](" + "|".join(YEAR_PATTERNS) + r")\s+(\d{3,4})\b", re.IGNORECASE),
        ]
        
        for pattern in PATTERNS:
            match = pattern.search(line)
            if match:
                try:
                    groups = match.groups()
                    
                    if len(groups[0]) in [3, 4] and len(groups) == 4:
                        if len(groups[1]) >= 13:
                            cvv, card, month, year = groups
                        else:
                            card, month, year, cvv = groups
                    else:
                        card, month, year, cvv = groups
                    
                    card = re.sub(r'[\s\-]', '', card)
                    
                    if not re.fullmatch(r"\d{13,19}", card):
                        continue
                    
                    if month.isalpha():
                        month = month_to_number(month.lower())
                    else:
                        try:
                            month = int(month)
                        except:
                            continue
                    
                    try:
                        year = str(year).lstrip("'")
                        year_int = int(year)
                        if year_int < 100:
                            year_int += 2000
                        elif year_int < 2000:
                            year_int += 2000
                    except:
                        continue
                    
                    if not (1 <= month <= 12):
                        continue
                    
                    return {
                        "number": card,
                        "month": month,
                        "year": year_int,
                        "verification_value": cvv,
                        "name": "Test Card"
                    }
                except Exception:
                    continue
        
        parts = re.split(r"[,\|;:\s]+", line)
        parts = [p for p in parts if p]
        if len(parts) < 4:
            return None
        number = re.sub(r'[\s\-]', '', parts[0])
        if not re.fullmatch(r"\d{13,19}", number or ""):
            return None
        try:
            month = int(parts[1])
            year = int(parts[2])
            if year < 100:
                year += 2000
        except Exception:
            return None
        cvv = parts[3]
        return {
            "number": number,
            "month": month,
            "year": year,
            "verification_value": cvv,
            "name": "Test Card"
        }
    
    def _extract_multiline_cards(text: str) -> List[Dict]:
        cards = []
        
        card_patterns = [
            r'(?:ccnum|cc num|card num|card number|card|cc|number|pan|cardnumber)\s*[:=\-]?\s*(\d{13,19})',
            r'\b(\d{13,19})\b',
            r'(\d{13,19})',
        ]
        
        exp_patterns = [
            r'(?:exp|expiry|expires|expiration|date|exp date|expiry date)\s*[:=\-]?\s*(\d{1,2})\s*[\/\-]\s*(\d{2,4})',
            r'(?:exp|expiry|expires|expiration|date|exp date|expiry date)\s*[:=\-]?\s*(\d{2})(\d{2,4})',
            r'\b(\d{1,2})\s*[\/\-]\s*(\d{2,4})\b',
            r'\b(\d{2})[^\d]*(\d{2,4})\b',
        ]
        
        cvv_patterns = [
            r'(?:cvv|cvc|cv2|code|security code|security|pin)\s*[:=\-]?\s*(\d{3,4})',
            r'\b(\d{3,4})\b',
        ]
        
        card_numbers = []
        seen_card_nums = {}
        for pattern in card_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                card_num = match.group(1)
                if 13 <= len(card_num) <= 19:
                    if card_num not in seen_card_nums:
                        seen_card_nums[card_num] = (match.start(), match.end())
                        card_numbers.append((card_num, match.start(), match.end()))
        
        for card_num, card_start, card_end in card_numbers:
            window_start = max(0, card_start - 200)
            window_end = min(len(text), card_end + 300)
            window_text = text[window_start:window_end]
            
            card_offset_in_window = card_start - window_start
            card_in_window_start = card_offset_in_window
            card_in_window_end = card_offset_in_window + len(card_num)
            
            exp_month = None
            exp_year = None
            year_match_pos = None
            for pattern in exp_patterns:
                match = re.search(pattern, window_text, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:
                        exp_month = int(match.group(1))
                        year_str = match.group(2)
                        exp_year = int(year_str)
                        if exp_year < 100:
                            exp_year += 2000
                        if 1 <= exp_month <= 12:
                            break
                        else:
                            exp_month = None
                            exp_year = None
            
            if not exp_month or not exp_year:
                two_digit_matches = list(re.finditer(r'(\d{2})', window_text))
                year_matches = list(re.finditer(r'(\d{2,4})', window_text))
                
                for month_match in two_digit_matches:
                    if (month_match.start() >= card_in_window_start and 
                        month_match.start() < card_in_window_end):
                        continue
                        
                    potential_month = int(month_match.group(1))
                    if 1 <= potential_month <= 12:
                        for year_match in year_matches:
                            if (year_match.start() >= card_in_window_start and 
                                year_match.start() < card_in_window_end):
                                continue
                                
                            if year_match.start() > month_match.end():
                                potential_year = int(year_match.group(1))
                                if potential_year >= 20 and potential_year <= 99:
                                    potential_year += 2000
                                elif potential_year >= 2020 and potential_year <= 2099:
                                    pass
                                else:
                                    continue
                                
                                if year_match.start() - month_match.end() <= 100:
                                    exp_month = potential_month
                                    exp_year = potential_year
                                    year_match_pos = (year_match.start(), year_match.end())
                                    break
                    if exp_month and exp_year:
                        break
            
            cvv = None
            all_3digit = list(re.finditer(r'(\d{3})', window_text))
            valid_3digit = []
            for match in all_3digit:
                if (match.start() >= card_in_window_start and 
                    match.start() < card_in_window_end):
                    continue
                
                if year_match_pos:
                    year_start, year_end = year_match_pos
                    if (match.start() >= year_start and match.start() < year_end):
                        continue
                    
                potential = match.group(1)
                is_valid = Truen
                if exp_month and potential == str(exp_month).zfill(2):
                    is_valid = False
                if exp_year and potential == str(exp_year)[-3:]:
                    is_valid = False
                if is_valid:
                    valid_3digit.append((match, potential))
            
            if len(valid_3digit) == 1:
                cvv = valid_3digit[0][1]
            else:
                for i, pattern in enumerate(cvv_patterns):
                    matches = list(re.finditer(pattern, window_text, re.IGNORECASE))
                    matches_after = [m for m in matches if m.start() > card_offset_in_window]
                    matches_before = [m for m in matches if m.start() <= card_offset_in_window]
                    sorted_matches = matches_after + matches_before
                    
                    for match in sorted_matches:
                        potential_cvv = match.group(1)
                        is_valid_cvv = (potential_cvv != card_num[-4:] and potential_cvv not in card_num)
                        if exp_year:
                            is_valid_cvv = is_valid_cvv and (potential_cvv != str(exp_year)[-4:] and potential_cvv not in str(exp_year))
                        if exp_month:
      
