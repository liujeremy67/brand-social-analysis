Problem Statement
Adidas aims to improve its online marketing strategy by reallocating content
creation resources toward specific video topics and social media platforms
(e.g. YouTube, Instagram, TikTok) that drive the highest audience engagement.
This analysis compares Adidas’ video and social media performance against Nike’s
to identify content themes and platforms where Adidas can improve or capitalize.
In doing so, Adidas will ensure more effective use of existing marketing budgets
and strengthen its brand presence within the sportswear content landscape.

Context
Sportswear brands invest heavily in digital marketing across multiple video and
social media platforms. To optimize its content strategy, Adidas needs to identify
which video categories and platforms generate the highest engagement metrics,
such as likes, shares, and comments, relative to competitors like Nike.

Analysis Outline
1. Data Collection
 - Scrape a selection of YouTube videos from the Adidas and Nike channels
   - Up to 100 per channel
 - Gather a sample of social media data from Instagram and TikTok
   - Up to 20 per account (limited by Apify)

2. Data Cleaning
 - JSON structures must be normalized for dataframe output
 - Standardize any time formatting inconsistencies across platforms
 - Extract relevant features from post data
 - Handle missing values

3. Video Categorization
 - Define key content categories for the content space
   - Product
   - Athlete
   - Fitness
   - Lifestyle
 - Use NLP models to classify videos based on video titles, descriptions
   - Supervised with HuggingFace
 - Self validate video classifications on a separately sampled test set

4. Feature Engineering
 - Define and calculate engagement rates (likes/views, comments/views)
 - Group engagement metrics by platform
 - Consider both time-based features and content features

5. EDA
 - Summarize statistics for each brand by category, platform, and post time
 - Visualize distributions

6. Brand Contrast
 - Compare category engagement rates within each brand and between brands
 - Assess significance of differences in engagement (via ANOVA, t-test)
 - Check key assumptions before tests!
   - Independence, normality, equal variances, sample size
 - Apply significance test corrections for multiple hypothesis tests

7. Insights
 - Examine categories Adidas lags in competitively
 - Recommend reallocating to higher performing categories and platforms both
   within the brand and in the industry (in this case only adding Nike)
 - Posting strategies based on time
