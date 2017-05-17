library("RTextTools")
library("tm")
library("ggplot2")

#https://www.r-bloggers.com/clustering-search-keywords-using-k-means-clustering/

#Get Business Description, not including NA
descriptions <- na.omit(output[['Business Description']])

dtm <- create_matrix(descriptions, 
                     stemWords=TRUE, 
                     removeStopwords=TRUE, 
                     minWordLength=1,
                     removePunctuation= TRUE)

#Requires tm
findFreqTerms(dtm, lowfreq=1000)

# #I think there are 5 main topics: Data Science, Web Analytics, R, Julia, Wordpress
# kmeans5<- kmeans(dtm, 5)
# 
# #Merge cluster assignment back to keywords
# kw_with_cluster <- as.data.frame(cbind(descriptions, kmeans5$cluster))
# names(kw_with_cluster) <- c("keyword", "kmeans5")
# 
# #Make df for each cluster result, quickly "eyeball" results
# cluster1 <- subset(kw_with_cluster, subset=kmeans5 == 1)
# cluster2 <- subset(kw_with_cluster, subset=kmeans5 == 2)
# cluster3 <- subset(kw_with_cluster, subset=kmeans5 == 3)
# cluster4 <- subset(kw_with_cluster, subset=kmeans5 == 4)
# cluster5 <- subset(kw_with_cluster, subset=kmeans5 == 5)

dtm <- dtm[sample(nrow(dtm), 7600), ]

#accumulator for cost results
cost_df <- data.frame()

#run kmeans for all clusters up to 100
for(i in 1:100){
  print(paste0("Running calculations for K = ", i))
  #Run kmeans for each level of i, allowing up to 100 iterations for convergence
  kmeans<- kmeans(x=dtm, centers=i, iter.max=100)
  
  #Combine cluster number and cost together, write to df
  cost_df<- rbind(cost_df, cbind(i, kmeans$tot.withinss))
  
}
names(cost_df) <- c("cluster", "cost")

#Calculate lm's for emphasis
lm(cost_df$cost[1:10] ~ cost_df$cluster[1:10])
lm(cost_df$cost[10:19] ~ cost_df$cluster[10:19])
lm(cost_df$cost[20:100] ~ cost_df$cluster[20:100])

cost_df$fitted <- ifelse(cost_df$cluster <10, (19019.9 - 550.9*cost_df$cluster), 
                         ifelse(cost_df$cluster <20, (15251.5 - 116.5*cost_df$cluster),
                                (13246.1 - 35.9*cost_df$cluster)))

#Cost plot
ggplot(data=cost_df, aes(x=cluster, y=cost, group=1)) + 
  theme_bw(base_family="Arial") + 
  geom_line(colour = "darkgreen") +
  theme(text = element_text(size=20)) +
  ggtitle("Reduction In Cost For Values of 'k'\n") +
  xlab("\nClusters") + 
  ylab("Within-Cluster Sum of Squares\n") +
  scale_x_continuous(breaks=seq(from=0, to=100, by= 10)) +
  geom_line(aes(y= fitted), linetype=2)
