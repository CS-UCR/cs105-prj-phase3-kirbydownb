# Yelp Ratings Project Phases 1 and 2 :rewind:

In phases 1 and 2, we collected two sets of data: the median income of California zip codes and Yelp reviews about restaurants in those zip codes. We stored that data in a MongoDB Atlas Cluster in phase 1 and cleaned up the data in phase 2.


# Yelp Rating Project Phase 3 :fast_forward:

In phase 3, we will take this cleaned data and insert it into a model in order ro perform predictions on the data. 

We used XGB, which is a decision tree classifier in order to predict the rating of a restaurant. We chopped up the continuous rating data into discrete buckets, and then used the other features we had collected and allowed to the decision tree
