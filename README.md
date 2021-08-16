# FSIT
> Financial Statement Investing Tool

## Background
The goal of this tool is to easily assess which stocks are currently best for value-investing (long-term
holding).  Inspiration comes largely from financial math classes taken at PSU and reading a large number of
books on financial analytics, especially by/on Warren Buffet who is most notable for his value-Investing
analytics and the idea of a "durable competitive advantage".  All of the thresholds for seeing if
ratios/growth/etc are acceptable are taken right from Warren or other notable investors.  These ratios/growth
thresholds are handcrafted features that are combined with a machine learning model to best rank stocks from 
a fundamental standpoint. Then the intrinsic value of the highest ranked stocks are compared to their extrinsic
market value, and ranked according to expected return on investment.

## Pipeline
Website scraping stock data -> pre-processing -> feature extraction -> modeling -> stock fundamental ranking

