import model
import os

model_service = model.init()

def lambda_handle(event, context):
    return model_service.lam
