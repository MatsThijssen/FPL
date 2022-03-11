---
layout: default
title: Home
---



# Fixture Difficulty Rating
Fixture Difficulty Rating (FDR) is one of the most useful tools to plan player transfers in FPL. The idea is to quantify the toughness of competition a team will face in their upcoming games which will give an estimate of how easy it will be for a team to score or keep a clean sheet. FPL provides an "official" FDR [here](https://fantasy.premierleague.com/fixtures/fdr), however it has a few shortcomings:
1. It does not separate between offense and defense.
2. Values are not updated very often
3. Some of the values appear to be off

Issues nr. 1 and 2 are fairly easy to fix. Regarding nr.2 there is even a valid argument to be made against updating so as to not confuse users with frequently changing values.
Number 3 however, is one of the biggest issues. At the time of writing (March 2022), MUN (A) is given the same difficulty as e.g. LIV (H) or CHE (H). Given Manchester Uniteds lackluster form, I believe this to be an overstatement. Similarly, grouping teams like WAT and LEE with BRE or NEW fails to highlight the vast difference in performance between these teams, particularly in recent times.

## My Approach
My FDR is based purely on xG/xGA (expected goals for/against). The algorithm computes a weighted average of a team's xG and xGA over the past seven games and uses that to assign each team an offensive and defensive strength. For details, see FPL.ipynb in my GitHub repo (though it is a bit of a mess right now). Below you can see the "Offensive FDR" for all Premier League teams. The scale goes from dark green (low defensive strength) to dark red (high defensive strength), in essence telling you how easy or hard it is to score against that opponent. On the y-axis, teams are sorted by offensive form, Manchester City having the best offensive form and Burnley the worst.

Although there is no direct mapping from FDR values to expected goals, I use this as a more or less accurate guide:
- Red: Hard to score 1 goal.
- Orange: Maybe 1 goal.
- Beige: Probably 1 goal, maybe 2.
- Green: Probably 2 goals.
- Dark green: 3+ goals likely.

Again, this is merely a guide. Some teams are so strong (e.g. Liverpool/Man City) they can score 2 or 3 goals even against the strongest opposition. Furthermore, things change quickly and the return/injury of a key player or a tactical change can cause results in complete disagreement with the FDR values. I think tools like this are best used in conjunction with watching actual games and having a decent understanding of football.
 


<img src="OffFDR.png" width=1000/>

Note that for double gameweeks (DGW), teams are not necessarily in the right order. It would be slightly tedious to fix, so I have avoided to do so as I don't believe it to be that important.

Below is the corresponding "Defensive FDR", telling you how easy/hard it will be to avoid conceding against a certain team. Like the Offensive FDR, teams on the y-axis are sorted by defensive form, and the colors go from dark green (low offensive strength) to red (high offensive strength). Against a dark green team, there is a good chance to keep a clean sheet, while against a red team it will be a great challenge.

<img src"DefFDR.png" width=1000/>

For both these charts it is important to consider a teams inheret strength as well as the FDR values. As mentioned, teams like Liverpool and Manchester City are likely to score (and keep clean sheets) against almost any competition. On the other side of the spectrum, a team like Norwich will struggle to both score and keep balls out of their own net, even if they are facing a "dark green" team.

Go [here](./GvxG.html) to see some fun stuff.

