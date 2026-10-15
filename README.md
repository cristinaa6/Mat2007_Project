# Mat2007_Project
This is the project for my Intro to Programming class. Hi Panos! :))

PERCENTAGE OF FEMALE MINISTERS IN GOVERNMENTS OVER TIME

This project analyses the share of women among ministers in 193 countries between 2005 and 2024. It produces two plots: the worldwide average over time, and a comparison of World Bank regions in the year with the highest world average.


FILES IN THIS REPOSITORY

README.md                                      this file
final_project.py                               the code (analysis and both plots)
report.pdf                                     the short report (2 pages)
share-of-women-in-ministerial-positions.csv    the dataset, unmodified


HOW TO RUN THE CODE

1. Requirements
   - Python 3.8 or newer (tested with Python 3.12)
   - numpy and matplotlib (tested with numpy 2.4 and matplotlib 3.10)
   No other libraries are needed. No internet connection is needed once the csv file is in the folder.

2. Installation
   Open a terminal in the project folder and type:
       pip install numpy matplotlib
   On macOS or Linux you may need to type pip3 and python3 instead of pip and python.

4. Execution
   - Make sure final_project.py and share-of-women-in-ministerial-positions.csv are in the SAME folder, and that the csv file keeps its exact name.
   - In Visual Studio Code: File > Open Folder, choose the project folder, open final_project.py and press the Run button (the triangle at the top right).
   - Or in a terminal inside the project folder, type:
       python final_project.py
   The code finds the csv file next to itself, so it works from any terminal location.

5. Conditions and things to know
   - Two plot windows open one after the other. Close the first window to see the second.
   - The plots are also saved as plot1_average_over_time.png and plot2_regions.png in the folder from which the code is run.
   - On a computer without a display, run with: MPLBACKEND=Agg python final_project.py (the plots are then only saved, not shown).
   - The code runs in a few seconds.

6. Expected output (last lines of the printout)
       Trend = 0.59 +- 0.05 percentage points per year, R^2 = 0.93
       Years until 50% at this rate (from 2024): 45

       Year with the highest world average: 2023 (23.26%)
   Other key results: yearly average 13.1 +- 0.7 % (2005) and 23.6 +- 1.0 % (2024); 43 of 2438 values removed as outliers (1.5 x IQR rule, applied per year); in 2023 North America 40.8 % and South Asia 10.2 % versus a world average of 23.3 %.


DATASET

Name: Share of women in ministerial positions
Where to find it: Our World in Data
    Page:   https://ourworldindata.org/grapher/share-of-women-in-ministerial-positions
    Direct csv download:
            https://ourworldindata.org/grapher/share-of-women-in-ministerial-positions.csv?v=1&csvType=full&useColumnShortNames=false
Original sources: Inter-Parliamentary Union (IPU) and UN Women, via the World Bank Gender Statistics, processed by Our World in Data (open access, CC BY).
Columns: Entity (country or region), Code, Year, and the percentage of ministers who are women.

Does the dataset need to be cleaned to reproduce the results? No. Use the csv file exactly as downloaded, without manual editing. The code does the cleaning itself: it skips the header row and removes the 12 aggregate rows (World, income groups, European Union, World Bank regions) from the country analysis. The region and world rows are read separately for the second plot. The file has no missing values.

Note on reproducibility: Our World in Data updates this dataset. A file downloaded later may contain newer years or revised values, so the numbers could differ from the report. The csv file included in this repository gives the results listed above.


METHOD IN BRIEF

1. Read the csv file and remove the aggregate rows.
2. For each year: remove outliers (1.5 x IQR rule), compute the mean over countries and its standard error (standard deviation divided by the square root of the number of countries).
3. Fit a straight line to the yearly means (numpy polyfit) and extrapolate to 50 %.
4. Find the year with the highest world average and compare the six World Bank regions with the world value (bar plot).


LIMITATIONS

The share of women among ministers is a proxy for political power; it does not measure heads of state or which portfolios women hold. The regions are World Bank regions, not continents.
