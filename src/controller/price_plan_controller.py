from flask import abort

from service.price_plan_service import PricePlanService
from .electricity_reading_controller import repository as readings_repository

def get_all():
    price_plan_service = PricePlanService(readings_repository)
    plans = price_plan_service.get_all()
    print (plans)
    return plans