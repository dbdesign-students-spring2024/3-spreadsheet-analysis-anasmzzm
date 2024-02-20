# Spreadsheet Analysis
### By Anas Moazzam

## Source of Data
This dataset was sourced by wesbscraping [basketball-reference.com](https://www.basketball-reference.com/leagues/). This website compiles comprehensive data on every single NBA game since 1946. To webscrape this data, I used BeautifulSoup and Playwright to parse through the HTML tags within the seasons tab, access the games within each season, scrape the box score, and ultimately turned this into a CSV file. At first, I wanted to be ambitious and scrape data from seasons 2014 through 2023. However, since this took over 3 days to complete, I decided to limit the scope of my analysis and focused on the 2022-2023 season for my analysis.

### Raw Data
|    |    mp |    mp |    fg |    fga |   fg% |    team   |
|----|-------|-------|-------|--------|-------|-----------|
|  0 | 240.0 | 240.0 |  38.0 |   72.0 | 0.528 | POR       |
|  1 | 240.0 | 240.0 |  40.0 |   84.0 | 0.476 | MIA       |
|  2 | 240.0 | 240.0 |  41.0 |   78.0 | 0.526 | CLE       |
|  3 | 240.0 | 240.0 |  29.0 |   74.0 | 0.392 | DAL       |
|  4 | 240.0 | 240.0 |  39.0 |   81.0 | 0.481 | ATL       |
|  5 | 240.0 | 240.0 |  36.0 |  100.0 |  0.36 | DAL       |
|  6 | 240.0 | 240.0 |  37.0 |   87.0 | 0.425 | LAL       |
|  7 | 240.0 | 240.0 |  47.0 |  106.0 | 0.443 | TOR       |
|  8 | 240.0 | 240.0 |  37.0 |   85.0 | 0.435 | MIN       |
|  9 | 240.0 | 240.0 |  41.0 |   89.0 | 0.461 | SAS       |
| 10 | 240.0 | 240.0 |  27.0 |   86.0 | 0.314 | ORL       |
| 11 | 240.0 | 240.0 |  34.0 |   99.0 | 0.343 | MEM       |

I only included a lines as there were over 100 columns and over 20,000 games total.

## Webscraping and Cleaning Data
To access the historical data, I decided to webscrape through each season, access each game, then add it into a file. I decided to create a function that gets the html link for each season, and saves it to disk.

```python
async def scrape_season(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = await get_html(url, "#content .filter")
    
    soup = BeautifulSoup(html)
    #get all links with anchor tags from html "a"
    links = soup.find_all("a")
    #getting all links with href within it
    href = [l["href"] for l in links]
    #creating full links for standing pages
    standing_pages = [f"https://basketball-reference.com{l}" for l in href]
    
    #saving to disk so we dont process while scraping
    for url in standing_pages:
        save_path = os.path.join(STANDINGS_DIR, url.split('/')[-1])
        #if we already scraped, don't scrape again
        if os.path.exists(save_path):
            continue
        
        html = await get_html(url, '#all_schedule')
        with open(save_path, 'w+') as f:
            f.write(html)
```
I still needed to access the boxscores of each game so I created another function that gets the html content for each boxscore and adds it to disk. 
```python
async def scrape_game(standings_file):
    with open(standings_file, 'r') as f:
        html = f.read()

    #cleaning links
    soup = BeautifulSoup(html)
    links = soup.find_all('a')
    hrefs = [l.get('href') for l in links]
    boxscores = [l for l in hrefs if l and 'boxscore' in l and '.html' in l]
    boxscores = [f"https://basketball-reference.com{l}" for l in boxscores]

    for url in boxscores:
        save_path = os.path.join(SCORES_DIR, url.split('/')[-1])
        if os.path.exists(save_path):
            continue

        html = await get_html(url, '#content')
        if not html:
            continue
        with open(save_path, 'w+') as f:
            f.write(html)
```
After navigating through all the HTML, I continued to get only the basic box scores of each game, formatting it (such as getting rid of quarterly stats), and adding each boxscore to my dataset. Luckily, this method resulted in pretty clean data, however, also resulted in over 20,000 pieces of data. To consolodate my analysis, I chose to clean my data to only focus on the 2022-2023 season. As there were games from 2014 and over a 100 columns, I used Pandas in python to get my dataset to only games within my desired season and columns.
```python
impt_cols = ['team', 'team_opp', 'fga', 'fg%', '3p', '3p%', 'ft', 
             'fta', 'ft%', 'trb', 'ast', 'stl', 'blk', 'tov', 
             'pf', 'pts', 'ortg', 'drtg', 'season', 'won']

df_2023 = df[df['season'] == 2023]
cleaned_df = df_2023[impt_cols].copy().reset_index(drop=True)
```
### Links to data
- [Raw Data](https://github.com/dbdesign-students-spring2024/3-spreadsheet-analysis-anasmzzm/blob/main/data/nba_games.csv)
- [Cleaned Data](https://github.com/dbdesign-students-spring2024/3-spreadsheet-analysis-anasmzzm/blob/main/data/cleaned_csv)
- [Spreadsheet](https://github.com/dbdesign-students-spring2024/3-spreadsheet-analysis-anasmzzm/blob/main/data/nba_spreadsheet.xlsx) 

## Analysis
I decided to split my analysis into two manners. One was a general outlook on the 2022-2023 NBA season and looking specifcally at my hometown team, the New York Knicks. Here are some fun facts I calculated about the 2022-2023 NBA season, which I used MAX(), MIN(), and AVERAGE() to calculate.

#### 2022-2023 Overall Analysis
- The maximum points scored in a game this season was 176 scored by the Sacramento Kings. For context, the NBA record is 186!
- The minimum points scored was 79 points which was scored by the Cleveland Cavaliers. The average points scored in the 2023 season was 114 points.
- The average personal fouls per game was about 20 fouls per game.
- The maximum offensive rating scored by a team in a game was 151.3 which was earned by Los Angeles Clippers.