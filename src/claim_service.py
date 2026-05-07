from typing import Generator, Any

from src.source_loader import SourceLoader
from src.claim_normalizer import ClaimNormalizer
from src.claim_analyzer import ClaimAnalyzer

class ClaimService:
    def __init__(self):
        self.__source_loader = SourceLoader()
        self.__normalizer = ClaimNormalizer()
        self.__analyzer = ClaimAnalyzer()

    def get_insurance_claims(self) -> Generator[dict[str, Any], None, None]:
        for raw_data in self.__source_loader.get_insurance_claims_data():
            normalized = self.__normalizer.normalize(raw_data)
            if normalized is not None:
                yield self.__analyzer.calculate_and_enrich(normalized)
