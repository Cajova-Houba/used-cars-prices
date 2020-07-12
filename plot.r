library("ggplot2")

carData = read.csv(file='data.csv')
names(carData)
years <- carData[["year"]]
kms <- carData[["kilometers"]]
prices <- carData[["price"]]

plot(x=prices, y=kms,
     pch=18, 
     cex=2, 
     col="#69b3a2",
     xlab="Price [Kè]", ylab="Kilometers",
     main="Price x kilometers"
)

plot(x=prices, y=years,
     pch=18, 
     cex=2, 
     col="#69b3a2",
     xlab="Price [Kè]", ylab="Year",
     main="Price x years"
)

plot(x=years, y=kms,
     pch=18, 
     cex=2, 
     col="#69b3a2",
     xlab="Year", ylab="Kilometers",
     main="Year x kilometers"
)
