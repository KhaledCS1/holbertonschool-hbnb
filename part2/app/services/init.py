"""Services package - Singleton facade instance"""
from app.services.facade import HBnBFacade

# Create a singleton instance of the facade
facade = HBnBFacade()

__all__ = ['facade']
