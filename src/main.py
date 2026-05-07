from src.claim_service import ClaimService

# example usage
if __name__ == '__main__':
   service = ClaimService()
   for data in service.get_insurance_claims():
      print(data)
