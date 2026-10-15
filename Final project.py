#Final Project: Percentage of female ministers in governments over time
#Share of women in ministerial positions per country, 2005-2024

import numpy as np
import matplotlib.pyplot as plt

#Reading the data from the csv file

countries = []  # name of the country for each row
years = []      # year for each row
shares = []     # percentage of women ministers for each row

import os  # needed to find the folder where this script is saved
folder = os.path.dirname(os.path.abspath(__file__))  # the folder this script is in
file = open(os.path.join(folder, "share-of-women-in-ministerial-positions.csv"))  # open the csv file from that folder
lines = file.readlines()  # read all lines of the file into a list
file.close()  # close the file again

#These rows are not countries but groups of countries, so they are skipped
aggregates = ["(WB)", "European Union", "income countries", "World"]

for line in lines[1:]:  # start at 1 to skip the header line
    parts = line.strip().split(",")  # split the line at the commas: name, code, year, share
    name = parts[0]
    is_aggregate = False  # assume the row is a country until proven otherwise
    for a in aggregates:  # check the name against each aggregate label
        if a in name:
            is_aggregate = True
    if is_aggregate == False:  # only keep real countries
        countries.append(name)
        years.append(int(parts[2]))
        shares.append(float(parts[3]))

countries = np.array(countries)  # convert lists to numpy arrays for easy math
years = np.array(years)
shares = np.array(shares)

print("Number of rows (countries only):", len(shares))

#Average share per year with statistical uncertainty

unique_years = np.unique(years)  # all the different years in the data, sorted
yearly_means = []          # average share of women ministers for each year
yearly_uncertainties = []  # statistical uncertainty of that average for each year
parity_counts = []         # number of countries with 50% or more women ministers
outliers_removed = []      # number of outliers removed in each year

for y in unique_years:  # loop once for each year
    shares_this_year = shares[years == y]  # pick only the rows of this year
    parity_counts.append(np.sum(shares_this_year >= 50))  # count countries at or above 50% (all countries, before outlier removal)
    q1 = np.percentile(shares_this_year, 25)  # lower quartile of this year
    q3 = np.percentile(shares_this_year, 75)  # upper quartile of this year
    iqr = q3 - q1  # interquartile range = spread of the middle half of the countries
    low_limit = q1 - 1.5 * iqr  # values below this are outliers
    high_limit = q3 + 1.5 * iqr  # values above this are outliers
    n_before = len(shares_this_year)  # number of countries before removing outliers
    shares_this_year = shares_this_year[(shares_this_year >= low_limit) & (shares_this_year <= high_limit)]  # keep only non-outliers
    outliers_removed.append(n_before - len(shares_this_year))  # remember how many were removed
    yearly_means.append(np.mean(shares_this_year))  # average over all countries
    yearly_uncertainties.append(np.std(shares_this_year) / np.sqrt(len(shares_this_year)))  # standard error = std / sqrt(N)

yearly_means = np.array(yearly_means)
yearly_uncertainties = np.array(yearly_uncertainties)

print("Outliers removed per year:", outliers_removed, "Total:", sum(outliers_removed))
print("\nYear, average share (%), uncertainty, countries with >= 50% (all countries):")
for i in range(len(unique_years)):  # print one line per year
    print(f"{unique_years[i]}: Mean = {yearly_means[i]:.2f}, Uncertainty = {yearly_uncertainties[i]:.2f}, Parity countries = {parity_counts[i]}")

#Linear fit to the yearly averages

fit, cov = np.polyfit(unique_years, yearly_means, 1, cov=True)  # straight line fit, cov gives the uncertainties
slope = fit[0]  # percentage points gained per year
intercept = fit[1]
slope_uncertainty = np.sqrt(cov[0][0])  # uncertainty of the slope
r = np.corrcoef(unique_years, yearly_means)[0][1]  # correlation coefficient

print(f"\nTrend = {slope:.2f} +- {slope_uncertainty:.2f} percentage points per year, R^2 = {r**2:.2f}")

#Extrapolation: how many years until the average reaches 50%
years_to_parity = (50 - yearly_means[-1]) / slope
print(f"Years until 50% at this rate (from {unique_years[-1]}): {years_to_parity:.0f}")

#Plot 1: Average share of women ministers over time

plt.figure()  # start a new figure
plt.errorbar(unique_years, yearly_means, yerr=yearly_uncertainties, fmt='o')  # yearly average with error bars
plt.ylim(15, 30)  # y-axis runs from 15% to 30%
plt.xlabel("Year")  # label the x-axis
plt.ylabel("Average share of women ministers (%)")  # label the y-axis
plt.xticks([2005, 2010, 2015, 2020, 2024])  # whole years on the x-axis
plt.title("Percentage of Female Ministers in Governments Over Time")  # add a title
plt.text(2005, 33, f"Trend = {slope:.2f} +- {slope_uncertainty:.2f} % per year")  # write the result on the plot
plt.savefig("plot1_average_over_time.png")  # save this figure as an image file
plt.show()  # display the plot on screen

#Plot 2: Regions in the year with the highest world average, compared to the world average

#The csv also has rows for world regions (World Bank regions) and for the world, so we read those separately
region_names = []   # name of the region for each row
region_years = []   # year for each row
region_shares = []  # percentage of women ministers for each row
world_years = []    # years of the world rows
world_shares = []   # world average (percentage of women ministers) for each year

for line in lines[1:]:  # go through the file again
    parts = line.strip().split(",")  # split the line at the commas
    if "(WB)" in parts[0]:  # rows of the World Bank regions
        region_names.append(parts[0].replace(" (WB)", ""))  # remove " (WB)" from the name
        region_years.append(int(parts[2]))
        region_shares.append(float(parts[3]))
    if parts[0] == "World":  # the row with the world average
        world_years.append(int(parts[2]))
        world_shares.append(float(parts[3]))

region_names = np.array(region_names)
region_years = np.array(region_years)
region_shares = np.array(region_shares)
world_years = np.array(world_years)
world_shares = np.array(world_shares)

best_year = world_years[np.argmax(world_shares)]  # the year with the highest world average
world_average = world_shares[world_years == best_year][0]  # world average in that year
print(f"\nYear with the highest world average: {best_year} ({world_average:.2f}%)")

names_best = region_names[region_years == best_year]  # regions in that year
shares_best = region_shares[region_years == best_year]  # their shares in that year
order = np.argsort(shares_best)[::-1]  # order from the biggest share to the smallest
names_best = names_best[order]
shares_best = shares_best[order]

print("Regions in", best_year, "(biggest share first):")
for i in range(len(names_best)):  # print one line per region
    print(f"{names_best[i]}: {shares_best[i]:.2f}% ({shares_best[i] - world_average:+.2f} points compared to the world)")

plt.figure(figsize=(10, 6))  # start a second, new (larger) figure
plt.bar(names_best, shares_best)  # one bar per region
plt.axhline(world_average, color='red', linestyle='--', label=f"World average = {world_average:.1f}%")  # red dashed line at the world average
plt.xlabel("Region")  # label the x-axis
plt.ylabel("Share of women ministers (%)")  # label the y-axis
plt.title(f"Women Ministers by Region in {best_year} Compared to the World")  # add a title
plt.xticks(rotation=20, ha="right")  # tilt the region names so they fit
plt.legend()  # show the label of the red line
plt.tight_layout()  # make sure nothing is cut off
plt.savefig("plot2_regions.png")  # save this figure as an image file
plt.show()  # display the plot on screen

worst_year = world_years[np.argmin(world_shares)]  # the year with the highest world average
world_average = world_shares[world_years == worst_year][0]  # world average in that year
print(f"\nYear with the lowest world average: {worst_year} ({world_average:.2f}%)")