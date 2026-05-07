from typing import Any

"""
https://rezerwacja.cargogroup.pl/resources/data/forms/artykuly/9/OWU_PZU.pdf
I'm aware that source data contains USD prices and PZU OWU contains PLN prices but
in order to make it less complicated, USD values will have constant value
"""
class ClaimAnalyzer:
    __usd_value = 4.0

    def calculate_and_enrich(self, record: dict[str, str]) -> dict[str, Any]:
        is_approved, rejection_reasons = self.__calculate_is_approved(record)
        payout_amount = self.__calculate_payout_amount(record, is_approved)
        return {
            **record,
            "is_approved": is_approved,
            "rejection_reasons": rejection_reasons,
            "payout_amount": payout_amount,
        }

    def __calculate_is_approved(self, record: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Verifies if the claim is approved for payout based on OWU PZU Auto rules.
        Source: Ogólne Warunki Ubezpieczeń Komunikacyjnych PZU Auto (UZ/59/2024)

        Rejection rules (OWU §12 - Wyłączenia odpowiedzialności):
        1. FRAUD - claim marked as fraudulent (fraud_reported == 1)
           -> mapped from: fraud_reported
        2. NO_POLICE_REPORT - vehicle theft without police report
           -> mapped from: incident_type == 'Vehicle Theft' AND police_report_available != 'YES'
        3. BELOW_MINIMUM_THRESHOLD - claim amount below franszyza integralna (300 PLN / ~75 USD)
           -> mapped from: total_claim_amount < 300 PLN

        :param record: auto claim record
        :return: tuple[is_approved, rejection_reasons]
        """
        rejection_reasons = []

        # 1
        if record["fraud_reported"]:
            rejection_reasons.append("FRAUD")

        # 2
        if record["incident_type"].lower() == "vehicle theft" and record["police_report_available"] is not True:
            rejection_reasons.append("NO_POLICE_REPORT")

        # 3
        if record["total_claim_amount"] / self.__usd_value < 300:
            rejection_reasons.append("BELOW_MINIMUM_THRESHOLD")

        is_approved = not rejection_reasons

        return is_approved, rejection_reasons

    def __calculate_payout_amount(self, record: dict[str, Any], is_approved: bool) -> float:
        """
        Calculates the final payout amount based on OWU PZU Auto rules.
        Source: Ogólne Warunki Ubezpieczeń Komunikacyjnych PZU Auto (UZ/59/2024)

        Calculation steps (OWU §15-§20 - Ustalenie wysokości odszkodowania):
        1. Sum claim components: injury_claim + property_claim + vehicle_claim
        2. Subtract deductible (franszyza): policy_deductable
        3. Apply CSL limit - using per person limit (first value)
        because each claim is individual per policyholder, not per incident
        policy_csl format: "250/500" -> 250k per person, 500k per incident
        4. If claim is not approved (is_approved == False) -> return 0.0
        5. Return final payout, minimum 0.0 (never negative)

        :param record: auto claim record
        :param is_approved: is approved for payout
        :return: payout_amount as float, 0.0 if not approved
        """
        if not is_approved:
            return 0.0

        total = record["total_claim_amount"] - record["policy_deductable"]

        csl_per_person = record["policy_csl"].split("/")[1]
        csl_limit = int(csl_per_person) * 1000
        total = min(total, csl_limit)

        return max(0.0, float(total))
