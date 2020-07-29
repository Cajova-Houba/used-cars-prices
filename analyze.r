library("ggplot2")
library("scatterplot3d")
library("magrittr")
library("dplyr")

# load data
carData = read.csv(file='data.csv')

# print header and first couple of lines
names(carData)
head(carData)

# get data components as num vectors
years <- as.numeric(carData[["year"]])
kms <- as.numeric(carData[["kilometers"]])
prices <- as.numeric(carData[["price"]])

# do stuff

mean(kms)
median(kms)
sd(kms)
quantile(kms)

mean(prices)
mean(years)

median(prices)
median(years)

lmres <- lm(price ~ year, data= carData)
plot(carData$year, carData$price, xlab="Year", ylab="Price [K�]")
summary(lmres)
abline(lmres)

# plot(x=prices, y=kms,
#      pch=18, 
#      cex=2, 
#      col="#69b3a2",
#      xlab="Price [K�]", ylab="Kilometers",
#      main="Price x kilometers"
# )
# 
# plot(x=prices, y=years,
#      pch=18, 
#      cex=2, 
#      col="#69b3a2",
#      xlab="Price [K�]", ylab="Year",
#      main="Price x years"
# )
# 
# plot(x=years, y=kms,
#      pch=18, 
#      cex=2, 
#      col="#69b3a2",
#      xlab="Year", ylab="Kilometers",
#      main="Year x kilometers"
# )
hist(kms)
hist(prices)
hist(years)
hist(carData$brand)

meanBrandPrices <- tapply(carData$price, carData$brand, mean)
meanBrandYears <- tapply(carData$year, carData$brand, mean)
meanBrandKilometers <- tapply(carData$kilometers, carData$brand, mean)
brandCounts <-(tapply(carData$price, carData$brand, length))
barplot(sort(meanBrandPrices))
barplot(meanBrandKilometers)
brandCountsFiltered = which(brandCounts < 200)
names(brandCountsFiltered)
barplot(brandCountsFiltered)
carDataByBrand <- split(carData, carData$brand)
names(carDataByBrand)
skodaMeanPrice <- mean(carDataByBrand$�koda$price)
skodaMeanYeras <- mean(carDataByBrand$�koda$year)

plot(x=carDataByBrand$�koda$kilometers, y=carDataByBrand$�koda$price,
      pch=18, 
      cex=2, 
      col="#69b3a2",
      xlab="Kilometers", ylab="Price [K�]",
      main="Price x kilometers (�koda)"
 )

plot(x=carDataByBrand$�koda$year, y=carDataByBrand$�koda$price,
     pch=18, 
     cex=2, 
     col="#69b3a2",
     xlab="Kilometers", ylab="Price [K�]",
     main="Price x year (�koda)"
)

boxplot(price ~ year, 
        data=carDataByBrand$�koda, 
        range=0, 
        xlab="Manufactured", 
        ylab="Price [K�]",
        main="Price by year (�koda)")

boxplot(price ~ year, 
        data=carDataByBrand$Volkswagen, 
        range=0, 
        xlab="Manufactured", 
        ylab="Price [K�]",
        main="Price by year (VW)")

boxplot(price ~ year, 
        data=carDataByBrand$Ford, 
        range=0, 
        xlab="Manufactured", 
        ylab="Price [K�]",
        main="Price by year (Ford)")

boxplot(kilometers ~ year, 
        data=carDataByBrand$�koda, 
        range=0, 
        xlab="Manufactured", 
        ylab="Kilometers",
        main="Kilometers by year (�koda)")

boxplot(price ~ year,
        data=carData,
        range=0,
        xlab="Manufactured",
        ylab="Price [K�]",
        main="Price by year")

year2000Data <- carData[which(carData$year == 2000),]

mean(year2000Data$price)
mean(year2000Data$kilometers)

boxplot(kilometers ~ year, 
        data=carData, 
        range=0, 
        xlab="Manufactured", 
        ylab="Kilometers",
        main="Kilometers by year")
