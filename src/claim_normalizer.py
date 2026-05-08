from typing import Any
from src.logger_cfg import logg

class ClaimNormalizer:
    def normalize(self, record: dict[str, str]) -> dict[str, Any] | None:
        """I wouldn't like to end pipeline on incorrect data"""
        try:
            return self.__normalize(record)
        except (ValueError, TypeError) as e:
            logg.error(f"Claim Normalizer error: {e}", exc_info=True)
            return None

    def __normalize(self, record: dict[str, str]) -> dict[str, Any]:
        return {
            "months_as_customer": self.__to_int(record["months_as_customer"]),
            "age": self.__to_int(record["age"]),
            "policy_number": self.__to_int(record["policy_number"]),
            "policy_bind_date": record["policy_bind_date"],
            "policy_state": self.__normalize_str(record["policy_state"]),
            "policy_csl": self.__normalize_str(record["policy_csl"]),
            "policy_deductable": self.__to_int(record["policy_deductable"]),
            "policy_annual_premium": self.__to_float(record["policy_annual_premium"]),
            "insured_sex": self.__normalize_str(record["insured_sex"]),
            "insured_education_level": self.__normalize_str(record["insured_education_level"]),
            "insured_occupation": self.__normalize_str(record["insured_occupation"]),
            "incident_date": record["incident_date"],
            "incident_type": self.__normalize_str(record["incident_type"]),
            "collision_type": self.__normalize_str(record["collision_type"]),
            "incident_severity": self.__normalize_str(record["incident_severity"]),
            "authorities_contacted": self.__normalize_str(record["authorities_contacted"]),
            "incident_state": self.__normalize_str(record["incident_state"]),
            "incident_city": self.__normalize_str(record["incident_city"]),
            "incident_location": self.__normalize_str(record["incident_location"]),
            "incident_hour_of_the_day": self.__to_int(record["incident_hour_of_the_day"]),
            "number_of_vehicles_involved": self.__to_int(record["number_of_vehicles_involved"]),
            "property_damage": self.__to_bool_yes_no(record["property_damage"]),
            "bodily_injuries": self.__to_int(record["bodily_injuries"]),
            "witnesses": self.__to_int(record["witnesses"]),
            "police_report_available": self.__to_bool_yes_no(record["police_report_available"]),
            "total_claim_amount": self.__to_int(record["total_claim_amount"]),
            "injury_claim": self.__to_int(record["injury_claim"]),
            "property_claim": self.__to_int(record["property_claim"]),
            "vehicle_claim": self.__to_int(record["vehicle_claim"]),
            "auto_make": self.__normalize_str(record["auto_make"]),
            "auto_model": self.__normalize_str(record["auto_model"]),
            "auto_year": self.__to_int(record["auto_year"]),
            "fraud_reported": self.__to_bool_y_n(record["fraud_reported"]),
        }

    def __normalize_str(self, value: str) -> str:
        return None if value.strip() in ["?", "None", ""] else value

    def __to_int(self, value: str) -> int:
        return int(value)

    def __to_float(self, value: str) -> float:
        return float(value)

    def __to_bool_yes_no(self, value: str) -> bool | None:
        if value.upper() == "YES":
            return True
        elif value.upper() == "NO":
            return False
        else:
            return None

    def __to_bool_y_n(self, value: str) -> bool | None:
        if value.upper() == "Y":
            return True
        elif value.upper() == "N":
            return False
        else:
            return None
