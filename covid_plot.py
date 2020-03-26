import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


confirmed = pd.read_csv("COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")

dead = pd.read_csv("COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")


def growthComparisonPlot(shift, frame, countries, textlabel):
   
    confirmed = frame
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for country in countries:
        countryFrame = confirmed[confirmed['Country/Region'] == country]
        dates = confirmed.columns[4:].to_numpy() 
        num_dates = np.shape(dates)[0]
        countryArray = countryFrame.to_numpy()[:, 4:]
        countryTotal = np.sum(countryArray, axis = 0)
        countryTotal = countryTotal.astype(float)
        ax1.semilogy(dates,countryTotal+1, label=country, marker = '.', linestyle = ':')

        if countryTotal[-1] <= shift:
            get_shift = countryTotal.shape[0]
        else:
            get_shift = np.argmax(countryTotal >= shift)
        

        ax2.semilogy(countryTotal[get_shift:], label = country, marker = '.', linestyle = ':')
    
    ax1.legend()
    ax1.set_xticks(ax1.get_xticks()[::10])
    ax1.set_title(textlabel)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of '+ textlabel)
    ax2.set_title(textlabel)
    ax2.set_xlabel('Days since first ' + str(shift) + ' cases')
    ax1.set_ylabel('Number of '+ textlabel)
    ax2.legend()

def newCasesComparisonPlot(frame, countries, textlabel):
   
    confirmed = frame
    fig1, ax1 = plt.subplots()

    for country in countries:
        countryFrame = confirmed[confirmed['Country/Region'] == country]
        dates = confirmed.columns[4:].to_numpy() 
        num_dates = np.shape(dates)[0]
        countryArray = countryFrame.to_numpy()[:, 4:]
        countryTotal = np.sum(countryArray, axis = 0)
        countryTotal = countryTotal.astype(float)
        newCases = np.zeros(np.shape(countryTotal))
        newCases[0] = countryTotal[0]
        for i in np.arange(1,num_dates):
            newCases[i] = countryTotal[i] - countryTotal[i-1]

        ax1.semilogy(dates,newCases + 1, label=country, marker = '.', linestyle = ':')
   
    ax1.legend()
    ax1.set_xticks(ax1.get_xticks()[::10])
    ax1.set_title(textlabel)
    ax1.set_xlabel('date')

def growthComparisonPlotByState(shift, frame, country, num_provinces, textlabel):
    confirmed = frame

    fig3, ax3 = plt.subplots()
    
    fig4, ax4 = plt.subplots()

    countryFrame = confirmed[confirmed['Country/Region'] == country]
    dates = confirmed.columns[4:].to_numpy() 
    num_dates = np.shape(dates)[0]
    print(num_dates)
    print('last updated on' + dates[-1])
    all_provinces = countryFrame['Province/State'].to_numpy()
    selected_provinces = all_provinces[0:num_provinces+2]
    selected_provinces = np.delete(selected_provinces, np.where(selected_provinces == 'Grand Princess'))
    
    selected_provinces = np.delete(selected_provinces, np.where(selected_provinces == 'Diamond Princess'))
    
    for province in selected_provinces:
        provinceFrame = confirmed[confirmed['Province/State'] == province]
        provinceArray =  provinceFrame.to_numpy()[:, 4:]
        provinceTotal = np.sum(provinceArray, axis = 0)
        provinceTotal = provinceTotal.astype(float)
        ax3.semilogy(dates,provinceTotal+1, label=province, marker = '.', linestyle = ':')

        get_shift = np.argmax(provinceTotal >= shift)
        
        if get_shift != 0:
            ax4.semilogy(provinceTotal[get_shift:], label = province, marker = '.', linestyle = ':')
    
    ax3.legend()
    ax3.set_xticks(ax3.get_xticks()[::10])
    ax3.set_title(textlabel)
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Number of '+ textlabel)
    
    ax4.set_title(textlabel)
    ax4.set_xlabel('Days since first ' + str(shift) + ' cases')
    ax4.set_ylabel('Number of '+ textlabel)
    ax4.legend()
    ax4.set_title(textlabel)

last_update = confirmed.columns[4:].to_numpy()[-1]

countries = ['US', 'Italy', 'China','France','Germany','Korea, South', 'India'] 

growthComparisonPlot(100, confirmed, countries, 'confirmed cases, updated: ' + last_update)

growthComparisonPlot(10, dead, countries, 'deaths; updated: '+ last_update)

newCasesComparisonPlot(confirmed, countries, 'new confirmed cases; updated:' + last_update)

growthComparisonPlotByState(50, confirmed, 'US', 10, 'confirmed cases; updated:' + last_update)

plt.show()
