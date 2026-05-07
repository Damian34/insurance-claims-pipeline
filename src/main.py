from src.source_loader import SourceLoader

# example usage
if __name__ == '__main__':
   loader = SourceLoader()
   for data in loader.get_insurance_claims_data():
      print(data)
