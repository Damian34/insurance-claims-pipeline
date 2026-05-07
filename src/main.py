from src.source_loader import SourceLoader
from src.claim_normalizer import ClaimNormalizer

# example usage
if __name__ == '__main__':
   loader = SourceLoader()
   normalizer = ClaimNormalizer()
   for data in loader.get_insurance_claims_data():
      normalized_data = normalizer.normalize(data)
      print(normalized_data)
