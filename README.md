# hut8_calc

# Install Dependencies
pip install -r ./requirements.txt

# How to run the BE
uvicorn main:app --reload

# Assumptions
1. 30 days in a month. This affects calculations for monthly cost and revenue as not all months have 30 days, but it should be a reasonable average.
2. Using 24 hour weighted BTC price. Used as it was easy to find.