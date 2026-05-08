from src.processing.claim_analyzer import ClaimAnalyzer
from src.processing.claim_normalizer import ClaimNormalizer
from src.processing.source_loader import SourceLoader

# example usage
if __name__ == '__main__':
   loader = SourceLoader()
   normalizer = ClaimNormalizer()
   analyzer = ClaimAnalyzer()
   for raw_data in loader.get_insurance_claims_data():
      normalized = normalizer.normalize(raw_data)
      if normalized is not None:
         print(analyzer.calculate_and_enrich(normalized))
