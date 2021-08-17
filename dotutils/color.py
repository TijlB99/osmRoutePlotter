from random import random

def generatePastelColor(pastel_factor=0.7, transparency=0.5):
    return (
            (random()+pastel_factor)/(1.0+pastel_factor), 
            (random()+pastel_factor)/(1.0+pastel_factor), 
            (random()+pastel_factor)/(1.0+pastel_factor), 
            transparency
        )