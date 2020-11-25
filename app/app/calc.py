from django.test import TestCase

from app.calc import add, subtracted


class CalcTests(TestCase):
    def add(x, y):
    """Add two numbers together"""
    return x + y

    def subtract(x, y):
    """Subtract two numbers"""
    return y - x
