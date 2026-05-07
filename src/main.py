from src.claim_analyzer import ClaimAnalyzer
from src.source_loader import SourceLoader
from src.claim_normalizer import ClaimNormalizer

# example usage
if __name__ == '__main__':
   loader = SourceLoader()
   normalizer = ClaimNormalizer()
   analyzer = ClaimAnalyzer()
   for data in loader.get_insurance_claims_data():
      normalized_data = normalizer.normalize(data)
      enriched_data = analyzer.calculate_and_enrich(normalized_data)
      print(enriched_data)
