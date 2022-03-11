---
layout: default
title: Home
---



# Fixture Difficulty Rating
Fixture Difficulty Rating (FDR) is one of the most useful tools to plan player transfers in FPL. The idea is to quantify the toughness of competition a team will face in their upcoming games. This will give an estimate of how easy it will be for a team to score or keep a clean sheet. FPL provides an "official" FDR [here](https://fantasy.premierleague.com/fixtures/fdr), however it has a number of issues:
#### It does not separate between offense and defense.
Some teams are notable stronger offensively than defensively (e.g. Leeds) or vice versa (e.g. Wolves). If you are looking at bringing in an attacker, you ideally want them from playing teams that are weak at the back. On the other hand, when thinking about defenders, clean sheets are important, and thus you would like them to face teams that might have lesser attacking output.
#### Values are static and appear not realistic
FPL states that "The FDR is based on a complex algorithm developed by FPL experts". However, followers of football will likely disagree with many of the values assigned in the official FDR. For example, it has been clear that Manchester United (away) have not provided the same challenge as Liverpoolor Chelsea (at home), at least not in the beginning of the season. This ties in with another concept, namely that team-strength changes throughout the season, due to many reasons: Managerial changes, player transfers, injuries, fixture congestion, or simply "form". FPL claims that the FDR is "reviewed on a weekly basis and updated as the season progresses", but I have found these updates to be rather seldom and not in line with how the teams are actually performing.

## My Approach
Due to these issues, I decided to make my own fixture difficulty rating, based purely on xG/xGA (expected goals for/against). The algorithm computes a weighted average of a team's xG and xGA over the past seven games and uses that to assign each team an offensive and defensive strength. Below you can see the "Offensive FDR" for all Premier League teams. The scale goes from dark green (low defensive strength) to dark red (high defensive strength). On the y-axis, teams are sorted by offensive form, Manchester City having the best offensive form and Burnley the worst.

Although there is not a direct mapping from the values to expected goals, use this to guide your interpretation:
- Red: Hard to score even 1 goal.
- Orange: Maybe 1 goal.
- Beige: Probably 1 goal, maybe 2.
- Green: Probably 2 goals
- Dark green: 3+ goals likely.

Again this is merely a guide. Some teams are so strong (Liverpool/Man City) they can make 2 or 3 goals even against the strongest opposition. Furthermore, thigns change quickly and the return/injury of a key player or a tactical change can mean a de facto adjustment of several steps up or down the scale. I think tools like this is best used in conjunction with your own intuition and knowledge and that a combined decision is always the best.
 


<img src="OffFDR.png" width=500/>

Go [here](./GvxG.html) to see some fun stuff.

